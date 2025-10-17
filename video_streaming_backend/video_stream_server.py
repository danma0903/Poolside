import cv2
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
            # time.sleep(1)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client_socket.close()
        server_socket.close()
        cap.release()
        cv2.destroyAllWindows()