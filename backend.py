from flask import Flask, request, jsonify, Blueprint, render_template, Response
import cv2
import base64
import threading
import time
from ultralytics import YOLO

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


def process_frame(frame):
    """Run YOLO inference on a frame and return the annotated frame"""
    results = model(frame)
    annotated = results[0].plot()
    return annotated


def get_video_frames():
    """Generator function to yield YOLO-processed frames as JPEG bytes"""
    global video_capture, streaming_active
    
    video_capture = cv2.VideoCapture("video_streaming_backend/data/trimmed_video.mp4")
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

            time.sleep(1/30)  # Maintain ~30 FPS

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


if __name__ == "__main__":
    app.run(debug=True)
