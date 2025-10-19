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
    async with websockets.serve(video_stream, "10.0.0.119", 8888):
        print("WebSocket server started on ws://10.113.114.118:8888")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())