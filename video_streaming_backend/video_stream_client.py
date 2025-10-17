import cv2
import socket
import pickle
import struct


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 8888))  # Replace 'server_ip_address' with the actual server IP
data = b""
payload_size = struct.calcsize("Q")
printed = False

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
        ''' The data might contain partial information outside of the frame, but
        we know that each data will start with a serialized version of  the size 
        of the frame data then the actual frame. data will first save 
        everything after "Q".'''

        msg_size = struct.unpack("Q", packed_msg_size)[0] # Size of the data frame
        while len(data) < msg_size:
            # There is a chance we might not have enough data streamed in to read a complete frame
            data += client_socket.recv(4 * 1024)  # 4K buffer size
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame = pickle.loads(frame_data)
        # At this point, we might want to process the frame using the model.
        #cv2.imshow('Client', frame) # Shows the video on a cs2 frame.
        if not printed:
            print("frame example: \n", frame, "\n", frame.shape)
            printed = True
        if cv2.waitKey(1) == 13:
            break
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    cv2.destroyAllWindows()