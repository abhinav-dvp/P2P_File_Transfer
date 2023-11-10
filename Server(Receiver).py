import socket

def receive_file(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(1)

    print(f"Server listening on port {port}...")

    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    file_name = input("Enter the name for the received file: ")

    with open(file_name, 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)

    print(f"File received successfully: {file_name}")

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    port = int(input("Enter the port to listen on: "))
    receive_file(port)



