import socket
import threading
import sys
from ascii_magic import AsciiArt

HOST = '127.0.0.1'
PORT = 12345

def receive_messages(sock):
    while True:
        try:
            msg = sock.recv(1024).decode('utf-8')
            if msg:
                if msg.startswith("ART:"):
                    img_name = msg.split(":")[1]
                    msg = AsciiArt.from_image(img_name).to_ascii()
                print(f"\r{msg}\nTy: ", end="", flush=True)
        except Exception as e:
            print("\n[BŁĄD] Rozłączono z serwerem.")
            sock.close()
            break


def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
    except ConnectionRefusedError:
        print("Błąd połączenia z serverem")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()
    print("Połączono z czatem.")
    username = input("Podaj nazwę użytkownika: ")
    client.send(username.encode('utf-8'))

    while True:
        try:
            msg = input("Ty: ")
            if msg.lower() == 'exit':
                client.close()
                sys.exit(0)

            if msg:
                client.send(msg.encode('utf-8'))
        except KeyboardInterrupt:
            client.close()
            sys.exit(0)


if __name__ == "__main__":
    start_client()