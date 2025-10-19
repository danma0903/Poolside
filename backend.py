from flask import Flask, request, jsonify, Blueprint, render_template, Response
import cv2
import base64
import threading
import time
import torch
from ultralytics import YOLO
from collections import deque

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')

# Register blueprints
from routes import bp as api_bp
app.register_blueprint(api_bp)
veiws = Blueprint('veiws', __name__)
app.register_blueprint(veiws)

# Global variables
video_capture = None
streaming_active = False
model = YOLO("video_streaming_backend/yolov8n.pt")

# Detection configuration
DETECTION_CONFIG = {
    'history_length': 5,  # Number of frames to track
    'alert_threshold': 1,  # Alert if threshold met in this many frames
    'objects_to_track': {
        'person': {'class_id': 0, 'min_count': 2, 'name': 'People'},
        'chair': {'class_id': 56, 'min_count': 0, 'name': 'Chairs'},  # COCO class 56
        'cell phone': {'class_id': 67, 'min_count': 1, 'name': 'Cell Phones'}  # COCO class 67
    }
}

# Detection tracking
detection_history = deque(maxlen=DETECTION_CONFIG['history_length'])
alert_active = False  


def process_frame(frame):
    """Run YOLO inference on a frame and return the annotated frame with object detection tracking"""
    global detection_history, alert_active
    
    results = model(frame)
    annotated = results[0].plot()
    
    # Count objects in the frame
    frame_counts = {}
    for obj_name, obj_config in DETECTION_CONFIG['objects_to_track'].items():
        frame_counts[obj_name] = 0
    
    if len(results) > 0 and results[0].boxes is not None:
        for box in results[0].boxes:
            class_id = int(box.cls)
            for obj_name, obj_config in DETECTION_CONFIG['objects_to_track'].items():
                if class_id == obj_config['class_id']:
                    frame_counts[obj_name] += 1
    
    # Track detection history
    detection_history.append(frame_counts)
    
    # Check for consistent detection based on thresholds
    if len(detection_history) >= 2:  # the history length is 2 so we need to check if the alert threshold is met in 2 frames
        alert_triggered = True
        alert_message_parts = []
        
        for obj_name, obj_config in DETECTION_CONFIG['objects_to_track'].items():
            min_count = obj_config['min_count']
            frames_with_min_count = sum(1 for counts in detection_history 
                                      if counts[obj_name] >= min_count)
            
            if frames_with_min_count < DETECTION_CONFIG['alert_threshold']:
                alert_triggered = False
            else:
                alert_message_parts.append(f"{obj_config['name']}: {min_count}+")
        
        if alert_triggered and not alert_active:
            alert_active = True
            alert_msg = f"ALERT: {' + '.join(alert_message_parts)} consistently detected!"
            print(alert_msg)
        elif not alert_triggered and alert_active:
            alert_active = False
            print("Alert cleared: Detection thresholds no longer met")
    
    # Add object count text to frame
    y_offset = 10
    for obj_name, obj_config in DETECTION_CONFIG['objects_to_track'].items():
        count = frame_counts[obj_name]
        min_count = obj_config['min_count']
        color = (0, 255, 0) if count >= min_count else (0, 255, 255)
        
        cv2.putText(annotated, f"{obj_config['name']}: {count}", (10, y_offset), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        y_offset += 25
    
    if alert_active:
        cv2.putText(annotated, "ALERT: THRESHOLDS MET!!!", (10, y_offset + 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    return annotated


def get_video_frames():
    """Generator function to yield YOLO-processed frames as JPEG bytes"""
    global video_capture, streaming_active
    
    video_capture = cv2.VideoCapture(0) # the camera or video file ###########################################################
    streaming_active = True

    try:
        while streaming_active and video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                # Restart video when it ends
                video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            # ✅ Apply YOLO model
            annotated_frame = process_frame(frame)

            # Encode as JPEG
            _, buffer = cv2.imencode('.jpg', annotated_frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            frame_bytes = buffer.tobytes()

            # Stream the annotated frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(1/60)  # the video is 120 fps so we need to sleep for 1/120 seconds to maintain the fps

    finally:
        if video_capture:
            video_capture.release()
        streaming_active = False


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/video_stream')
def video_stream():
    """Stream YOLO-processed video frames as MJPEG"""
    return Response(get_video_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_info')
def video_info():
    """Get information about the video stream"""
    global video_capture, streaming_active
    
    if video_capture and video_capture.isOpened():
        fps = video_capture.get(cv2.CAP_PROP_FPS)
        frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        return jsonify({
            "status": "active" if streaming_active else "inactive",
            "fps": fps,
            "frame_count": frame_count,
            "width": width,
            "height": height,
            "duration": frame_count / fps if fps > 0 else 0
        })
    else:
        return jsonify({
            "status": "inactive",
            "message": "Video stream not initialized"
        })


@app.route('/stop_video')
def stop_video():
    """Stop the video stream"""
    global streaming_active, video_capture
    
    streaming_active = False
    if video_capture:
        video_capture.release()
        video_capture = None
    
    return jsonify({"message": "Video stream stopped"})


@app.route('/detection_status')
def detection_status():
    """Get current object detection status and alert information"""
    global detection_history, alert_active
    
    if len(detection_history) == 0:
        return jsonify({
            "current_counts": {},
            "alert_active": False,
            "history_length": 0,
            "frames_meeting_thresholds": {},
            "alert_threshold": DETECTION_CONFIG['alert_threshold'],
            "detection_config": DETECTION_CONFIG
        })
    
    current_counts = detection_history[-1] if detection_history else {}
    
    # Calculate frames meeting thresholds for each object
    frames_meeting_thresholds = {}
    for obj_name, obj_config in DETECTION_CONFIG['objects_to_track'].items():
        min_count = obj_config['min_count']
        frames_meeting_thresholds[obj_name] = sum(1 for counts in detection_history if counts[obj_name] >= min_count)
    
    # Get recent detection history
    recent_counts = []
    for counts in list(detection_history)[-10:]:  # if the last 10 frames are not met, then the alert is not active
        recent_counts.append(counts)
    
    return jsonify({
        "current_counts": current_counts,
        "alert_active": alert_active,
        "history_length": len(detection_history),
        "frames_meeting_thresholds": frames_meeting_thresholds,
        "alert_threshold": DETECTION_CONFIG['alert_threshold'],
        "detection_config": DETECTION_CONFIG,
        "recent_counts": recent_counts
    })


@app.route('/update_detection_config', methods=['POST'])
def update_detection_config():
    """Update detection configuration"""
    global DETECTION_CONFIG, detection_history
    
    try:
        data = request.get_json()
        
        # Update history length if provided
        if 'history_length' in data:
            new_length = int(data['history_length'])
            if new_length > 0:
                DETECTION_CONFIG['history_length'] = new_length
                # Resize the deque
                old_history = list(detection_history)
                detection_history = deque(old_history, maxlen=new_length)
        
        # Update alert threshold if provided
        if 'alert_threshold' in data:
            new_threshold = int(data['alert_threshold'])
            if new_threshold > 0:
                DETECTION_CONFIG['alert_threshold'] = new_threshold
        
        # Update object configurations if provided
        if 'objects_to_track' in data:
            for obj_name, obj_config in data['objects_to_track'].items():
                if obj_name in DETECTION_CONFIG['objects_to_track']:
                    if 'min_count' in obj_config:
                        DETECTION_CONFIG['objects_to_track'][obj_name]['min_count'] = int(obj_config['min_count'])
                    if 'name' in obj_config:
                        DETECTION_CONFIG['objects_to_track'][obj_name]['name'] = str(obj_config['name'])
        
        return jsonify({
            "message": "Detection configuration updated successfully",
            "new_config": DETECTION_CONFIG
        })
        
    except Exception as e:
        return jsonify({
            "error": f"Failed to update configuration: {str(e)}"
        }), 400


if __name__ == "__main__":
    app.run(debug=True)
