import asyncio
import websockets
import cv2
import numpy as np
import base64
from ultralytics import YOLO

model = YOLO("yolov8n.pt")

async def video_client():
    uri = "ws://localhost:8888"  # same as the server
    async with websockets.connect(uri) as websocket:
        print("Connected to WebSocket video stream on :", uri)
        
        try:
            while True:
                # Receive base64-encoded JPEG
                frame_b64 = await websocket.recv()
                
                # Decode base64 → bytes
                frame_bytes = base64.b64decode(frame_b64)
                
                # Convert bytes → NumPy array
                np_arr = np.frombuffer(frame_bytes, np.uint8)
                
                # Decode JPEG → OpenCV frame
                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                
                # Apply YOLO model inference
                results = model(frame)
                annotated_frame = results[0].plot()
                
                # Display frame
                cv2.imshow("YOLO Stream", annotated_frame)
                if cv2.waitKey(1) & 0xFF == 13:  # Enter key to quit
                    break
        except websockets.ConnectionClosed:
            print("❌ WebSocket connection closed")
        finally:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(video_client())