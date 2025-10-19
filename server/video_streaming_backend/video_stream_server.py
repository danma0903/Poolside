import asyncio
import websockets
import cv2
import base64
from ultralytics import YOLO
import requests

model = YOLO("best1.pt")

async def video_stream(websocket):
    cap = cv2.VideoCapture("data/trimmed_video.mp4")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply YOLO model inference
        results = model(frame)
        annotated_frame = results[0].plot()

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        target_detected = False
        for box in results[0].boxes:
            cls_index = int(box.cls[0])
            class_name = model.names[cls_index]
            # Replace person with intended target class.
            if (class_name == "toddler"):
                target_detected = True
                break

                
        if target_detected:
            requests.get("http://10.113.114.118:5000/test-alert")
        else:
            requests.get("http://10.113.114.118:5000/test-alert-relief")

        
        # Display frame
        #cv2.imshow("YOLO Stream", annotated_frame)
        if cv2.waitKey(1) & 0xFF == 13:  # Enter key to quit
            break

        # Send frame as base64 string
        await websocket.send(jpg_as_text)

        # Control frame rate (e.g., ~30 FPS)
        await asyncio.sleep(1/30)

    cap.release()

async def main():
    async with websockets.serve(video_stream, "10.0.0.119", 8888):
        print("WebSocket server started on ws://10.113.114.118:8888")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
