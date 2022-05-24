import socket
import threading
import Client_GUI
import Configuration
from tkinter import messagebox
from vidstream import ScreenShareClient
import Registry

class Client:
    def __init__(self, address, username):
        self.client_name = username
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(address)
        self.client.send(self.client_name.encode())
        self.stream_client = ScreenShareClient(Configuration.server_ip, Configuration.stream_port)

    def write(self, client_message, chat, ispublic, front_page_client, main_page_client):
        try:
            if client_message.strip():
                if ispublic:
                    client_message = "1" + self.client_name + ": " + client_message
                    self.client.send(client_message.encode())
                else:
                    client_message = "0" + self.client_name + "(Private): " + client_message
                    Client_GUI.active_chat(chat)
                    Client_GUI.print_message(client_message[1:], chat)
                    Client_GUI.disable_chat(chat)
                    self.client.send(client_message.encode())
        except:
            self.disconnect(front_page_client, main_page_client)

    def receive(self, chat, front_page_client, main_page_client):
        while True:
            try:
                server_message = self.client.recv(1024).decode('utf-8')
                if server_message[0] == '0':
                    Client_GUI.active_chat(chat)
                    Client_GUI.print_message(server_message[1:], chat)
                    Client_GUI.disable_chat(chat)
                elif server_message[0] == '1':
                    print("file")
                elif server_message[0] == '2':
                    self.stream_client = ScreenShareClient(Configuration.server_ip, Configuration.stream_port)
                    self.stream_client.start_stream()
                elif server_message[0] == '3':
                    server_message = server_message[1:]
                    for i in range(len(server_message)):
                        Registry.apply_permission(i, int(server_message[i]))

            except:
                self.disconnect(front_page_client, main_page_client)
                break

    def disconnect(self, front_page_client, main_page_client):
        messagebox.showerror("ERROR", "Teacher has disconnected, sending you to the front page")
        main_page_client.withdraw()
        front_page_client.deiconify()
        self.client.close()


def check_server():
    address = (Configuration.server_ip, Configuration.port)
    try:
        client_check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_check.connect(address)
    except:
        return False
    else:
        client_check.close()
        return True


def client_create(username):
    address = (Configuration.server_ip, Configuration.port)
    client = Client(address, username)
    return client


def client_start(client, chat, front_page_client, main_page_client):
    receiving = threading.Thread(target=client.receive, args=(chat, front_page_client, main_page_client))
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

