import socket
import threading


class Client:
    def __init__(self, address):
        self.client_name = input("Enter your name: ")  # name will come from connection
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(address)
        self.client.send(self.client_name.encode())
        print("Connected to server")
        print("Enter 0 to send a private message to your teacher, enter 1 to send it to the whole class")

    def write(self):
        while True:
            public_private = input()  # will put a button in the GUI - public or private / 0 for private 1 for public
            if public_private == '0' or public_private == '1':
                client_message = input()
                client_message = public_private + self.client_name + ": " + client_message
                self.client.send(client_message.encode())
            else:
                print("wrong type, please enter 0 for private and 1 for public")

    def receive(self):
        while True:
            message_type = self.client.recv(1024).decode('utf-8')
            if message_type == "file":  # buffer overflow - add try
                file_name = self.client.recv(1024).decode()
                buffer = self.client.recv(1024)
                new_file = open(file_name, "wb")
                new_file.write(buffer)
                print("The file: " + file_name + " has been received from your teacher")
                new_file.close()

            else:
                server_message = self.client.recv(1024).decode('utf-8')
                print(server_message)


def main():
    address = ("172.20.133.99", 6565)
    client = Client(address)
    writing = threading.Thread(target=client.write)
    receiving = threading.Thread(target=client.receive)
    writing.start()
    receiving.start()


if __name__ == '__main__':
    main()
