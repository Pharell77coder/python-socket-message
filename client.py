import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(message)
        except Exception as e:
            print(f"Erreur de réception : {e}")
            break

def start_client():
    host, port = 'localhost', 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        username = input("Entrez votre nom d'utilisateur : ")
        client_socket.sendall(username.encode('utf-8'))

        receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
        receive_thread.start()

        while True:
            message = input()
            if message.lower() == 'exit':
                client_socket.sendall(message.encode('utf-8'))
                break
            client_socket.sendall(message.encode('utf-8'))

    except Exception as e:
        print(f"Échec de la connexion : {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()

