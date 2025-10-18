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

'''import cv2
import socket
import pickle
import struct
from ultralytics import YOLO


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8888))  # Replace 'server_ip_address' with the actual server IP
data = b""
payload_size = struct.calcsize("Q")
printed = False

model = YOLO("yolov8n.pt")

try:
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4 * 1024)  # 4K buffer size
            if not packet:
                break
            data += packet
        if not data:
            break
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        The data might contain partial information outside of the frame, but
        we know that each data will start with a serialized version of  the size 
        of the frame data then the actual frame. data will first save 
        everything after "Q".

        msg_size = struct.unpack("Q", packed_msg_size)[0] # Size of the data frame
        while len(data) < msg_size:
            # There is a chance we might not have enough data streamed in to read a complete frame
            data += client_socket.recv(4 * 1024)  # 4K buffer size
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        annotated_frame = model(frame)[0].plot()
        # At this point, we might want to process the frame using the model.
        cv2.imshow('Client', annotated_frame) # Shows the video on a cs2 frame.
        if not printed:
            print("frame example: \n", frame, "\n", frame.shape)
            printed = True
        if cv2.waitKey(1) == 13:
            break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cv2.destroyAllWindows()'''
