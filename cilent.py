import socket
import threading
import sqlite3

# Set up the database
conn = sqlite3.connect('chat.db', check_same_thread=False)
conn.execute('''
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    message TEXT NOT NULL
)
''')

# Broadcast function to send messages to all clients
clients = []

def broadcast(message, _client):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                username, text = message.split(":", 1)  # Username: message format
                print(f"[{username}] {text}")
                # Save to database
                conn.execute('INSERT INTO messages (username, message) VALUES (?, ?)', (username, text))
                conn.commit()
                # Broadcast the message to all clients
                broadcast(message.encode('utf-8'), client_socket)
            else:
                connected = False
        except:
            connected = False

    # Remove client if disconnected
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 5555))
    server.listen()

    print("[STARTING] Server is starting...")

    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

# Start the server
if __name__ == "__main__":
    start_server()
