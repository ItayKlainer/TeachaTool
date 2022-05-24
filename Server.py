import socket
import threading
import time
import Server_GUI
import Configuration
from vidstream import StreamingServer

class Server:
    # Creates a server on the given address
    def __init__(self, address, username):
        self.server_name = username
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.name_socket_address_list = []
        self.name_list = ["Everyone"]
        self.stream_server = StreamingServer(Configuration.server_ip, Configuration.stream_port, slots=1, quit_key=chr(27))

    # Binds the server
    def bind(self):
        self.server.bind(self.address)

    # Listens for clients
    def listen(self, chat, student_list, chat_combobox, screen_share_combobox):
        self.server.listen()
        while True:
            connection, address = self.server.accept()
            name = connection.recv(1024).decode('utf-8')
            if name.strip():
                self.name_socket_address_list.append([name, connection, address])
                self.name_list.append(name)
                Server_GUI.print_message(name + " has connected", chat, "blue")
                Server_GUI.add_to_list(student_list, name)
                Server_GUI.update_combobox(chat_combobox, screen_share_combobox, self.name_list)
                receiving = threading.Thread(target=self.receive, args=(connection, chat, student_list, chat_combobox, screen_share_combobox,))
                receiving.start()

    def write(self, server_message, chat, student_list, chat_combobox, screen_share_combobox):
        if server_message.strip():
            receiver = Server_GUI.check_chat_receiver(chat_combobox)
            if receiver == "Everyone":
                Server_GUI.print_message(self.server_name + ":" + server_message, chat, "")
                server_message = "0" + self.server_name + ": " + server_message
                for i in range(len(self.name_socket_address_list)):
                    try:
                        self.name_socket_address_list[i][1].send(server_message.encode())
                    except:
                        self.disconnect_client(i, chat, student_list, chat_combobox, screen_share_combobox)
            else:
                try:
                    receiver_index = self.name_list.index(receiver)
                except:
                    Server_GUI.print_message("Unknown student", chat, "red")

                else:
                    try:
                        self.name_socket_address_list[receiver_index - 1][1].send(("0" + self.server_name + "(Private): " + server_message).encode())
                        Server_GUI.print_message(self.server_name + "(Private to " + receiver + "):" + server_message, chat, "")
                    except:
                        self.disconnect_client(receiver_index-1, chat, student_list, chat_combobox, screen_share_combobox)

    def receive(self, connection, chat, student_list, chat_combobox, screen_share_combobox):
        while True:
            try:
                client_message = connection.recv(1024).decode('utf-8')
                if client_message[0] == '0':
                    Server_GUI.print_message(client_message[1:], chat, "")
                if client_message[0] == '1':
                    Server_GUI.print_message(client_message[1:], chat, "")
                    for i in range(len(self.name_socket_address_list)):
                        try:
                            self.name_socket_address_list[i][1].send(('0' + client_message[1:]).encode())
                        except:
                            self.disconnect_client(i, chat, student_list, chat_combobox, screen_share_combobox)
            except:
                for i in self.name_socket_address_list:
                    if i.count(connection) > 0:
                        self.disconnect_client(self.name_socket_address_list.index(i), chat, student_list, chat_combobox, screen_share_combobox)

    def ask_for_stream(self, name, chat):
        if name in self.name_list:
            self.stream_server.start_server()
            self.name_socket_address_list[self.name_list.index(name) - 1][1].send("2".encode())
        else:
            if name.strip():
                Server_GUI.print_message("Unknown student", chat, "red")
            else:
                Server_GUI.print_message("Please choose a student from the list", chat, "green")

    def send_permissions(self, permissions, chat, student_list, chat_combobox, screen_share_combobox):
        for i in range(len(self.name_socket_address_list)):
            try:
                self.name_socket_address_list[i][1].send(('3' + permissions).encode())
            except:
                self.disconnect_client(i, chat, student_list, chat_combobox, screen_share_combobox)
        else:
            Server_GUI.print_message("Permissions have been applied", chat, "green")



    def check_connection(self, chat, student_list, chat_combobox, screen_share_combobox):
        while True:
            for i in range(len(self.name_socket_address_list)):
                try:
                    self.name_socket_address_list[i][1].send("check".encode())
                except:
                    self.disconnect_client(i, chat, student_list, chat_combobox, screen_share_combobox)
            time.sleep(1)

    def disconnect_client(self, i, chat, student_list, chat_combobox, screen_share_combobox):
        Server_GUI.print_message(self.name_socket_address_list[i][0] + " has disconnected", chat, "blue")
        self.name_socket_address_list[i][1].close()
        self.name_socket_address_list.pop(i)
        self.name_list.pop(i + 1)
        Server_GUI.remove_from_list(student_list, i)
        Server_GUI.update_combobox(chat_combobox, screen_share_combobox, self.name_list)




def server_create(username):
    address = (Configuration.server_ip, Configuration.port)
    server = Server(address, username)
    server.bind()
    return server


def server_start(server, chat, student_list, chat_combobox, screen_share_combobox):
    listening = threading.Thread(target=server.listen, args=(chat, student_list, chat_combobox, screen_share_combobox,))
    listening.start()
    checking_connection = threading.Thread(target=server.check_connection, args=(chat, student_list, chat_combobox, screen_share_combobox,))
    checking_connection.start()

