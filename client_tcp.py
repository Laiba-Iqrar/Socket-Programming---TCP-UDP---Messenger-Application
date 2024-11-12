import socket
import threading

def receive_messages(client_socket):
    """Handle receiving messages from the server"""
    while True:
        try:
            # Receive and print message from server
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            # Close connection if receiving fails
            print("Disconnected from the server.")
            client_socket.close()
            break

def send_messages(client_socket):
    """Handle sending messages to the server"""
    while True:
        # Get message from user without the "you:" prompt
        message = input("")
        client_socket.send(message.encode())

def connect_to_chat_room():
    host = '127.0.0.1'  # Server IP
    port = 12345        # Server port

    # Set up the client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Enter the client’s name once
    name = input("Enter your name: ")
    client_socket.send(name.encode())  # Send name to the server

    # Start threads for sending and receiving messages
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    receive_thread.start()
    send_thread.start()

# Connect to the chat room
connect_to_chat_room()
