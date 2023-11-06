import threading
import socket
import time

# Server-side function to handle each client connection
def handle_client(client_socket):
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')

            # Check for incoming data and respond accordingly
            if not data:
                break
            if data == "ping":
                # If the received data is 'ping', respond with 'pong'
                client_socket.send("pong".encode('utf-8'))
    except Exception as e:
        # Print any server errors that occur during client communication
        print(f"Server error: {e}")
    finally:
        # Close the client socket
        client_socket.close()

# Function to start the server
def start_server():
    # Create a socket for the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8888))  # Bind to port 8888 and accept incoming connections
    server.listen(5)  # Listen for incoming connections with a queue of 5

    print("Server listening on port 8888")

    # Continuously accept incoming connections
    while True:
        client_socket, addr = server.accept()  # Accept a client connection
        # Create a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Function to start the client
def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('0.0.0.0', 8888))  # Connect to the server

    try:
        while True:
            # Send 'ping' to the server
            client.send("ping".encode('utf-8'))
            # Receive the server response
            response = client.recv(1024).decode('utf-8')
            if response == "pong":
                print("Received 'pong'")
            time.sleep(1)  # Wait for 1 second before sending the next 'ping'
    except Exception as e:
        # Print any client errors that occur during communication
        print(f"Client error: {e}")
    finally:
        # Close the client socket
        client.close()

if __name__ == '__main__':
    # Create a thread for the server and start it
    server = threading.Thread(target=start_server, args=())
    server.start()

    # Create a thread for the client and start it
    client = threading.Thread(target=start_client, args=())
    client.start()
