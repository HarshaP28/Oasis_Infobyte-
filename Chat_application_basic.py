import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 55555

# ─────────────────────────────────────────────────────────────
#  SERVER
# ─────────────────────────────────────────────────────────────
clients   = []
usernames = []

def broadcast(message, sender=None):
    for client in clients:
        if client != sender:
            try:
                client.send(message)
            except:
                remove_client(client)

def remove_client(client):
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        username = usernames[index]
        usernames.remove(username)
        broadcast(f"📢 {username} left the chat!\n".encode("utf-8"))
        client.close()
        print(f"  ❌ {username} disconnected.")

def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message:
                index    = clients.index(client)
                username = usernames[index]
                print(f"  [{username}]: {message}")
                broadcast(f"[{username}]: {message}\n".encode("utf-8"), sender=client)
            else:
                remove_client(client)
                break
        except:
            remove_client(client)
            break

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()

    print("=" * 45)
    print("  💬 Chat Server Started!")
    print(f"  Listening on {HOST}:{PORT}")
    print("  Waiting for users to connect...")
    print("  Press Ctrl+C to stop server")
    print("=" * 45)

    while True:
        try:
            client, address = server.accept()
            print(f"\n  ✅ New connection from {address}")
            client.send("USERNAME".encode("utf-8"))
            username = client.recv(1024).decode("utf-8")
            usernames.append(username)
            clients.append(client)
            print(f"  👤 {username} joined!")
            broadcast(f"📢 {username} joined the chat!\n".encode("utf-8"))
            client.send("✅ Connected! Start chatting!\n".encode("utf-8"))
            t = threading.Thread(target=handle_client, args=(client,))
            t.daemon = True
            t.start()
        except KeyboardInterrupt:
            print("\n  Server stopped.")
            break

# ─────────────────────────────────────────────────────────────
#  CLIENT
# ─────────────────────────────────────────────────────────────
def receive_messages(client, username):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "USERNAME":
                client.send(username.encode("utf-8"))
            else:
                print(f"  {message}", end="")
                print(f"  You: ", end="", flush=True)
        except:
            print("\n  ❌ Disconnected from server!")
            client.close()
            break

def start_client():
    print("=" * 45)
    print("  💬 Basic Chat App — Client")
    print("=" * 45)

    username = input("  Enter your username: ").strip()
    if not username:
        username = "User"

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("\n  ❌ Cannot connect to server!")
        print("  Run this file in another terminal and choose option 1 first!")
        return

    t = threading.Thread(target=receive_messages, args=(client, username))
    t.daemon = True
    t.start()

    print(f"\n  ✅ Connected! Type your message and press Enter.")
    print(f"  Type 'quit' to exit.\n")

    while True:
        try:
            message = input(f"  You: ").strip()
            if message.lower() == "quit":
                client.close()
                print("  👋 Goodbye!")
                break
            if message:
                client.send(message.encode("utf-8"))
        except KeyboardInterrupt:
            client.close()
            break

# ─────────────────────────────────────────────────────────────
#  MAIN MENU
# ─────────────────────────────────────────────────────────────
def main():
    print("\n" + "=" * 45)
    print("  💬 BASIC CHAT APPLICATION")
    print("=" * 45)
    print("  1. Start Server (run this first!)")
    print("  2. Join as Client (connect to chat)")
    print("  3. Exit")
    print("=" * 45)

    choice = input("  Enter choice (1/2/3): ").strip()

    if choice == "1":
        start_server()
    elif choice == "2":
        start_client()
    elif choice == "3":
        print("  Goodbye!")
        sys.exit(0)
    else:
        print("  Invalid choice!")
        main()

if __name__ == "__main__":
    main()