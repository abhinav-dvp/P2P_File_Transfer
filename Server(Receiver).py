import socket

def receive_broadcast(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    server_address = ('', port)

    server_socket.bind(server_address)

    print(f"Listening for broadcasts on port {port}...")

    x = True
    while x == True:
        # Receive the broadcast message
        print ("Condition X = ", x)
        data, address = server_socket.recvfrom(1024)
        print(f"Received Broadcast from : {address}")

        # Send the server IP address to the client
        if data.decode() == "FIND_SERVER":
            server_socket.sendto(socket.gethostbyname(socket.gethostname()).encode(), address)
            server_socket.close()
            x = False

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
    receive_broadcast(6000)
    receive_file(6000)


