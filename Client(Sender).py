import socket
from zeroconf import Zeroconf, ServiceBrowser

class ServiceListener:
    def remove_service(self, zeroconf, type, name):
        pass

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            self.connect_to_server(socket.inet_ntoa(info.address), info.port)

    def connect_to_server(self, server_ip, server_port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        file_to_send = input("Enter the path of the file to send: ")

        with open(file_to_send, 'rb') as file:
            while True:
                data = file.read(1024)
                if not data:
                    break
                client_socket.sendall(data)

        print(f"File sent successfully: {file_to_send}")

        client_socket.close()

if __name__ == "__main__":
    zeroconf = Zeroconf()
    listener = ServiceListener()
    browser = ServiceBrowser(zeroconf, "_filetransfer._tcp.local.", listener)

    try:
        while True:
            pass
    except KeyboardInterrupt:
        zeroconf.close()
