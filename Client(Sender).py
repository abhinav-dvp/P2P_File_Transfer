import socket

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

if __name__ == "__main__":
    server_ip = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port: "))
    file_to_send = input("Enter the path of the file to send: ")

    send_file(server_ip, server_port, file_to_send)
