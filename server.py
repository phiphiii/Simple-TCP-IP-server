import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
clients = []

class User:
    def __init__(self, conn, addr, username):
        self.conn = conn
        self.addr = addr
        self.username = username
        self.defaultUsername = True
    def __repr__(self):
        return f"{self.addr[0]}:{self.addr[1]}, {self.username}"

def handle_client(user):
    print(f"Nowy użytkownik {user.addr[0]}:{user.addr[1]} dołączył do czatu.")
    while True:
        try:
            msg = user.conn.recv(1024)
            if not msg:
                break
            if user.defaultUsername:
                user.username = msg.decode('utf-8')
                print(f"{user.addr[0]}:{user.addr[1]} zmienił nazwę na {user.username}")
                user.defaultUsername = False
            else:
                recived_msg = msg.decode('utf-8')
                full_msg = (f"[{user.username}]: {recived_msg}")
                msg = full_msg.encode('utf-8')
                for client in clients:
                    if client != user:
                        try:
                            client.conn.send(msg)
                        except:
                            clients.remove(client)
        except ConnectionResetError:
            break

    print(f"Użytkownik {user.username} opuścił czat.")
    if user in clients:
        clients.remove(user)
    user.conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Serwer nasłuchuje na {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        #clients.append((conn,f"User {threading.active_count() - 1}"))
        new_client = User(conn, addr,f"User_{threading.active_count() - 1}")
        clients.append(new_client)
        thread = threading.Thread(target=handle_client, args=(new_client,))
        thread.start()
        print(f"Aktywna ilość połączeń: {threading.active_count() - 1}")
        print("Połączeni użytkownicy: ")
        print(clients)


if __name__ == "__main__":
    start_server()