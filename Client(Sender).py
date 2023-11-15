import socket
import time

def send_file(ip, port, file_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    with open(file_path, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.sendall(data)

    print(f"File sent successfully: {file_path}")

    client_socket.close()

def broadcast_message(message, port):
    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Enable broadcasting on the socket
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Set up the client address
    client_address = ('255.255.255.255', port)

    while True:
        # Send the broadcast message
        print("Broadcasting")
        client_socket.sendto(message.encode(), client_address)
        # Set a timeout for receiving the server IP address
        client_socket.settimeout(1)
        try:
            # Receive the server IP address
            data, address = client_socket.recvfrom(1024)
            return data.decode()
        except socket.timeout:
            # No response received within the timeout, continue broadcasting
            pass
        finally:
            # Reset the timeout to None
            client_socket.settimeout(None)

if __name__ == "__main__":
    file_to_send = input("Enter the path of the file to send: ")

    # Discover the server IP address
    server_ip = broadcast_message("FIND_SERVER", 6000)

    if server_ip:
        print(f"Server found at {server_ip}")
        send_file(server_ip, 6000, file_to_send)
    else:
        print("Server not found.")
