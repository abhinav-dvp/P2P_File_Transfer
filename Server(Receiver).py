import socket
from zeroconf import ServiceInfo, Zeroconf

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

port = int(input("Enter the port to listen on: "))

# mDNS Service Registration
desc = {'path': '/transfer'}
info = ServiceInfo("_transfer._tcp.local.",
                    f"Transfer-{socket.gethostname()}._transfer._tcp.local.",
                    socket.inet_aton(socket.gethostbyname(socket.gethostname())),
                    port, 0, 0, desc)

zeroconf = Zeroconf()
zeroconf.register_service(info)

try:
    receive_file(port)
finally:
    zeroconf.unregister_service(info)
    zeroconf.close()
