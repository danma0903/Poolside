from flask import Flask, request, jsonify, Blueprint, render_template, Response
import cv2
import base64
import threading
import time

app = Flask(__name__, template_folder='website/templates', static_folder='website/static')
# Register API blueprint (adds routes under /api/*)
from routes import bp as api_bp
app.register_blueprint(api_bp)
#app.register_blueprint(, url_prefix='/')
veiws  = Blueprint('veiws',__name__)
app.register_blueprint(veiws)

# Global variable to control video streaming
video_capture = None
streaming_active = False

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

@app.route("/get-user/<user_id>") #endpoint to get user information by user_id
def get_user(user_id):
    user_data = {# mock user data
        "user_id": user_id,
        "name": "John Doe",
        "email": "jdoe@example.com"
    }

    extra = request.args.get("extra")
    if extra:
        user_data["extra"] = extra
    return jsonify(user_data)


@app.route("/create-user", methods=["POST"]) #endpoint to create a new user
def create_user():
    user_info = request.get_json()
    response = { # mock response for user creation
        "message": "User created successfully",
        "user": user_info
    }
    return jsonify(response), 201

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
    app.run(debug=True)