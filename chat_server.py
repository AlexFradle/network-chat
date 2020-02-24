import socket
import threading


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.clients = []

    def listen(self) -> None:
        """
        Listens for client connections
        :return: None
        """
        self.sock.listen(5)
        while True:
            # Accepts client connection
            clnt, addr = self.sock.accept()
            # Adds client to list of clients
            self.clients.append(clnt)
            print(f"Connected -> [{addr[0]}:{addr[1]}]")
            # Loops through clients to send connected message
            for client in self.clients:
                client.send(f"Connected -> [{addr[0]}:{addr[1]}]".encode())
            # Constantly listens for messages
            threading.Thread(target=self.listen_to_client, args=(clnt, addr), daemon=True).start()

    def listen_to_client(self, clnt: socket.socket, addr: tuple) -> bool:
        """
        Constantly running to listen for messages
        :param clnt: Client to listen for
        :param addr: Address of the client
        :return: ??
        """
        bytes_num = 1024
        while True:
            try:
                # Message sent by client
                data = clnt.recv(bytes_num)
                if data:
                    for client in self.clients:
                        client.send(f"[{addr[0]}:{addr[1]}] - {data.decode()}".encode())
            except:
                # Client disconnected
                print(f"Disconnected -> [{addr[0]}:{addr[1]}]")
                # Removes client from clients list
                self.clients.remove(clnt)
                clnt.close()
                # Sends disconnected message to all clients
                for client in self.clients:
                    client.send(f"Disconnected -> [{addr[0]}:{addr[1]}]".encode())
                return False


if __name__ == '__main__':
    s = Server("192.168.1.16", 51123)
    s.listen()
