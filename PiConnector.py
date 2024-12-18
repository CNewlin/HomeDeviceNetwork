```
import bluetooth
import socket
import threading

# Define the Bluetooth service and characteristics UUIDs
SERVICE_UUID = "0000180f-0000-1000-8000-00805f9b34fb"  # Battery Service
CHARACTERISTIC_UUID = "00002a19-0000-1000-8000-00805f9b34fb"  # Battery Level

# TCP server details
TCP_SERVER_IP = 'host ip'
TCP_SERVER_PORT = 4020  # Change to your TCP server port

def handle_bluetooth_client(client_sock, tcp_client):
    print("Accepted connection from Bluetooth", client_sock.getpeername())

    while True:
        try:
            # Check for data from Bluetooth client
            data = client_sock.recv(1024)
            if not data:
                break

            print("Received data from Bluetooth:", data.decode())

            # Send received data to the TCP server
            tcp_client.sendall(data)

        except OSError:
            break

    print("Disconnected from Bluetooth.")
    client_sock.close()

def handle_tcp_server(tcp_client, client_sock):
    while True:
        try:
            # Check for data from TCP server
            tcp_data = tcp_client.recv(1024)
            if not tcp_data:
                break

            print("Received data from TCP server:", tcp_data.decode())

            # Send received data from TCP server to Bluetooth client
            client_sock.sendall(tcp_data)

        except OSError:
            break

    print("Disconnected from TCP server.")
    tcp_client.close()

def main():
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]
    uuid = SERVICE_UUID

    bluetooth.advertise_service(server_sock, "MyBLEServer", service_id=uuid, service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS], profiles=[bluetooth.SERIAL_PORT_PROFILE])

    print(f"Waiting for a connection on RFCOMM channel {port}...")
    client_sock, client_info = server_sock.accept()

    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((TCP_SERVER_IP, TCP_SERVER_PORT))

    print(f"Connected to TCP server {TCP_SERVER_IP}:{TCP_SERVER_PORT}")

    # Create threads for handling Bluetooth client and TCP server communication
    bt_thread = threading.Thread(target=handle_bluetooth_client, args=(client_sock, tcp_client))
    tcp_thread = threading.Thread(target=handle_tcp_server, args=(tcp_client, client_sock))

    bt_thread.start()
    tcp_thread.start()

    bt_thread.join()
    tcp_thread.join()

    client_sock.close()
    server_sock.close()

if __name__ == "__main__":
    main()
```