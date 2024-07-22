import socket
import threading

clients = {}

class ClientThread(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.username = None

    def run(self):
        try:
            self.username = self.conn.recv(1024).decode('utf-8')
            clients[self.username] = self.conn
            print(f"{self.username} s'est connecté depuis {self.addr}")

            while True:
                message = self.conn.recv(1024).decode('utf-8')
                if message.lower() == 'exit':
                    break
                print(f"{self.username} : {message}")
                self.broadcast_message(f"{self.username} : {message}")

        except Exception as e:
            print(f"Erreur avec {self.addr} : {e}")
        finally:
            self.conn.close()
            del clients[self.username]
            print(f"{self.username} s'est déconnecté")

    def broadcast_message(self, message):
        for username, client_conn in clients.items():
            if client_conn != self.conn:
                try:
                    client_conn.sendall(message.encode('utf-8'))
                except Exception as e:
                    print(f"Erreur en envoyant le message à {username} : {e}")

def start_server():
    host, port = 'localhost', 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Serveur écoute sur {host}: {port}")

    try:
        while True:
            conn, addr = server_socket.accept()
            new_thread = ClientThread(conn, addr)
            new_thread.start()
    except KeyboardInterrupt:
        print("Serveur arrêté par l'utilisateur")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()

