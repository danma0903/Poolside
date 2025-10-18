import asyncio
import websockets
import cv2
import base64

async def video_stream(websocket):
    cap = cv2.VideoCapture("data/trimmed_video.mp4")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer).decode('utf-8')

        # Send frame as base64 string
        await websocket.send(jpg_as_text)

        # Control frame rate (e.g., ~30 FPS)
        await asyncio.sleep(1/30)

    cap.release()

async def main():
    async with websockets.serve(video_stream, "localhost", 8888):
        print("WebSocket server started on ws://localhost:8888")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())

'''import cv2
import socket
import pickle
import struct
import time



if __name__ == "__main__":

    printed = False
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 8888))
        server_socket.listen(5)
        print("Server is listening...")
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address} accepted")
        cap = cv2.VideoCapture("data/trimmed_video.mp4") 
        while True:
            ret, frame = cap.read()
            frame_data = pickle.dumps(frame)
            client_socket.sendall(struct.pack("Q", len(frame_data))) # "Q" is a formatter while frame data is the actual size of messages to read
            client_socket.sendall(frame_data)
            if cv2.waitKey(1) == 13:
                break
            if ret == False:
                print("End of video stream")
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        server_socket.close()
        cap.release()
        cv2.destroyAllWindows()'''