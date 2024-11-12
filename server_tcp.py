import socket
import threading

# List to keep track of all connected clients and their names
clients = []
client_names = {}

def broadcast(message, current_client=None):
    """Send a message to all clients, optionally excluding the sender"""
    for client in clients:
        if client != current_client:
            client.send(message)

def handle_client(client):
    """Handle each client connection"""
    # Ask the client for their name
    client.send("Enter your name: ".encode())
    name = client.recv(1024).decode().strip()
    client_names[client] = name  # Store the client's name
    clients.append(client)

    # Welcome the new client and announce their joining
    welcome_message = f"Welcome to the group, {name}!"
    client.send(welcome_message.encode())
    broadcast(f"{name} has joined the chat!".encode(), client)
    print(f"{name} has connected.")

    while True:
        try:
            # Receive message from client
            message = client.recv(1024)
            if message:
                # Format message to include client's name
                full_message = f"{name}: {message.decode()}"
                print(full_message)  # Print to server console
                broadcast(full_message.encode(), client)
        
        except:
            # Remove client on disconnect
            clients.remove(client)
            broadcast(f"{name} has left the chat.".encode(), client)
            print(f"{name} has disconnected.")
            client.close()
            break

def start_chat_room():
    host = '127.0.0.1'  # Localhost IP
    port = 12345        # Server port

    # Set up the server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Chat room server started on {host}:{port}")

    while True:
        # Accept new client connections
        client, address = server_socket.accept()
        print(f"New connection from {address}")
        
        # Start a new thread for the connected client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

# Run the chat room server
start_chat_room()
