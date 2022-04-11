import socket
import threading
import Client_GUI


class Client:
    def __init__(self, address):
        self.client_name = "student"  # name will come from connection
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(address)
        self.client.send(self.client_name.encode())
        print("Connected to server")

    def write(self, client_message, chat, ispublic):
        if client_message.strip():
            if ispublic:
                client_message = "1" + self.client_name + ": " + client_message
                #Client_GUI.print_message(client_message[1:], chat)
                self.client.send(client_message.encode())
            else:
                client_message = "0" + self.client_name + "(Private): " + client_message
                Client_GUI.print_message(client_message[1:], chat)
                self.client.send(client_message.encode())

    def receive(self, chat):
        while True:
            server_message = self.client.recv(1024).decode('utf-8')
            if server_message[0] == '1':
                Client_GUI.print_message(server_message[1:], chat)
            else:
                Client_GUI.print_message(server_message[1:] + "(private)", chat)




def client_create():
    address = ("192.168.1.35", 6565)
    client = Client(address)
    return client

def client_start(client, chat):
    receiving = threading.Thread(target=client.receive, args=(chat,))
    receiving.start()



'''
if message_type == "file":  # buffer overflow - add try
    file_name = self.client.recv(1024).decode()
    buffer = self.client.recv(1024)
    new_file = open(file_name, "wb")
    new_file.write(buffer)
    print("The file: " + file_name + " has been received from your teacher")
    new_file.close()
'''