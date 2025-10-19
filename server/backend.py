from flask import Flask, request, jsonify, Blueprint, render_template, Response
import cv2
import base64
import threading
from flask_cors import CORS
from flask_sse import sse

import time

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')
CORS(app,supports_credentials=True)
app.config["REDIS_URL"] = "redis://localhost:6379"
app.register_blueprint(sse, url_prefix='/alert-stream')

# Register API blueprint (adds routes under /api/*)
# from routes import bp as api_bp
# app.register_blueprint(api_bp)
#app.register_blueprint(, url_prefix='/')
# veiws  = Blueprint('veiws',__name__)
# app.register_blueprint(veiws)

# Global variable to control video streaming

video_capture = None
streaming_active = False
@app.route('/test-alert')
def test_alert():
    sse.publish({'message':"good"},type='alert')
    # sse.publish({},type='relieve-alert')
    return "test-complete"

@app.route('/test-alert-relief')
def test_alert_relief():
    sse.publish({'message':"good"},type='relieve-alert')
    # sse.publish({},type='relieve-alert')
    return "test-complete"

@app.route('/get-stream-url',methods=['POST','OPTIONS'])
def get_stream_url():
    return ("hello")
def get_video_frames():
    """Generator function to yield video frames as JPEG bytes"""
    global video_capture, streaming_active
    
    # Initialize video capture
    video_capture = cv2.VideoCapture("video_streaming_backend/data/trimmed_video.mp4")
    streaming_active = True
    
    try:
        while streaming_active and video_capture.isOpened():
            ret, frame = video_capture.read()
            if not ret:
                # Loop the video when it ends
                video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            frame_bytes = buffer.tobytes()
            
            # Yield frame in MJPEG format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Control frame rate (30 FPS)
            time.sleep(1/30)
    finally:
        if video_capture:
            video_capture.release()
        streaming_active = False

@app.route('/')
def home():
    return render_template("index.html")



#@app.route('/alert-stream')


@app.route('/video_stream')
def video_stream():
    """Stream video frames as MJPEG"""
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







if __name__ == "__main__": #if this file is run directly, start the Flask app
    app.run(host='0.0.0.0',debug=False)