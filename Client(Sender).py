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

def discover_server(port, timeout=5):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    client_socket.bind(('0.0.0.0', 0))

    message = b"DISCOVER_SERVER"

    start_time = time.time()

    while time.time() - start_time < timeout:
        client_socket.sendto(message, ('<broadcast>', port))
        try:
            data, server_address = client_socket.recvfrom(1024)
            if data.decode() == "SERVER_FOUND":
                return server_address[0]
        except socket.error:
            pass

    return None

if __name__ == "__main__":
    server_port = int(input("Enter the server port: "))
    file_to_send = input("Enter the path of the file to send: ")

    # Discover the server IP address
    server_ip = discover_server(server_port)

    if server_ip:
        print(f"Server found at {server_ip}")
        send_file(server_ip, server_port, file_to_send)
    else:
        print("Server not found.")
