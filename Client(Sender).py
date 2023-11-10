import socket
from zeroconf import Zeroconf, ServiceBrowser, ServiceStateChange

def on_service_state_change(zeroconf, service_type, name, state_change):
    if state_change is ServiceStateChange.Added:
        info = zeroconf.get_service_info(service_type, name)
        if info:
            print(f"Discovered service: {info.server} at {socket.inet_ntoa(info.address)}:{info.port}")
            send_file(socket.inet_ntoa(info.address), info.port)

def send_file(ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, port))

    file_to_send = input("Enter the path of the file to send: ")

    with open(file_to_send, 'rb') as file:
        while True:
            data = file.read(1024)
            if not data:
                break
            client_socket.sendall(data)

    print(f"File sent successfully: {file_to_send}")

    client_socket.close()

service_type = "_transfer._tcp.local."

# mDNS Service Discovery
zeroconf = Zeroconf()
browser = ServiceBrowser(zeroconf, service_type, handlers=[on_service_state_change])

try:
    input("Press Enter to exit...\n")
finally:
    zeroconf.close()
