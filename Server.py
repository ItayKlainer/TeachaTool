import socket
import threading
import time
import Server_GUI
import Configuration


class Server:
    # Creates a server on the given address
    def __init__(self, address):
        #self.server_name = input("Enter server name: ")  # will come from log in db
        self.server_name = "teacher"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.name_socket_address_list = []
        self.name_list = ["Everyone"]

    # Binds the server
    def bind(self):
        self.server.bind(self.address)

    # Listens for clients
    def listen(self, chat, student_list, chat_combobox):
        self.server.listen()
        while True:
            connection, address = self.server.accept()
            name = connection.recv(1024).decode('utf-8')
            self.name_socket_address_list.append([name, connection, address])
            self.name_list.append(name)
            print("Connected to client")
            Server_GUI.add_to_list(student_list, name)
            Server_GUI.update_combobox(chat_combobox, self.name_list)
            receiving = threading.Thread(target=self.receive, args=(connection, chat, student_list, chat_combobox,))
            receiving.start()

    def write(self, server_message, chat, student_list, chat_combobox):
        if server_message.strip():
            receiver = Server_GUI.check_receiver(chat_combobox)
            if receiver == "Everyone":
                Server_GUI.active_chat(chat)
                Server_GUI.print_message(self.server_name + ":" + server_message, chat)
                Server_GUI.disable_chat(chat)
                server_message = "1" + self.server_name + ": " + server_message
                for i in range(len(self.name_socket_address_list)):
                    try:
                        self.name_socket_address_list[i][1].send(server_message.encode())
                    except:
                        print("Student " + self.name_socket_address_list[i][0] + " has been disconnected")
                        self.name_socket_address_list.pop(i)
                        self.name_list.pop(i+1)
                        Server_GUI.remove_from_list(student_list, i)
                        Server_GUI.update_combobox(chat_combobox,self.name_list)
            else:
                receiver_index = self.name_list.index(receiver)
                try:
                    Server_GUI.active_chat(chat)
                    Server_GUI.print_message(self.server_name + "(Private to " + receiver + "):" + server_message, chat)
                    Server_GUI.disable_chat(chat)
                    server_message = "1" + self.server_name + "(Private): " + server_message
                    self.name_socket_address_list[receiver_index - 1][1].send(server_message.encode())
                except:
                    print("Student " + self.name_socket_address_list[receiver_index - 1][0] + " has been disconnected")
                    self.name_socket_address_list.pop(receiver_index - 1)
                    self.name_list.pop(receiver_index)
                    Server_GUI.remove_from_list(student_list, receiver_index - 1)
                    Server_GUI.update_combobox(chat_combobox, self.name_list)

    def receive(self, connection, chat, student_list, chat_combobox):
        while True:
            try:
                client_message = connection.recv(1024).decode('utf-8')
                if client_message[0] == '0':
                    Server_GUI.active_chat(chat)
                    Server_GUI.print_message(client_message[1:], chat)
                    Server_GUI.disable_chat(chat)
                if client_message[0] == '1':
                    Server_GUI.active_chat(chat)
                    Server_GUI.print_message(client_message[1:], chat)
                    Server_GUI.disable_chat(chat)
                    for i in range(len(self.name_socket_address_list)):
                        try:
                            self.name_socket_address_list[i][1].send(client_message.encode())
                        except:
                            print("The student " + self.name_socket_address_list[i][0] + " has disconnected")
                            self.name_socket_address_list.pop(i)
                            self.name_list.pop(i + 1)
                            Server_GUI.remove_from_list(student_list, i)
                            Server_GUI.update_combobox(chat_combobox, self.name_list)
            except:
                for i in self.name_socket_address_list:
                    if i.count(connection) > 0:
                        print("The student " + i[0] + " has disconnected")
                        Server_GUI.remove_from_list(student_list, self.name_socket_address_list.index(i))
                        self.name_list.pop(self.name_socket_address_list.index(i) + 1)
                        self.name_socket_address_list.pop(self.name_socket_address_list.index(i))
                        Server_GUI.update_combobox(chat_combobox, self.name_list)

    def check_connection(self, student_list, chat_combobox):
        while True:
            for i in range(len(self.name_socket_address_list)):
                try:
                    self.name_socket_address_list[i][1].send("check".encode())
                except:
                    print("Student " + self.name_socket_address_list[i][0] + " has been disconnected")
                    self.name_socket_address_list.pop(i)
                    self.name_list.pop(i + 1)
                    Server_GUI.remove_from_list(student_list, i)
                    Server_GUI.update_combobox(chat_combobox, self.name_list)
            time.sleep(0.5)


def server_create():
    address = (Configuration.server_ip, Configuration.port)
    server = Server(address)
    server.bind()
    return server


def server_start(server, chat, student_list, chat_combobox):
    listening = threading.Thread(target=server.listen, args=(chat, student_list,chat_combobox,))
    listening.start()
    #checking_connection = threading.Thread(target=server.check_connection, args=(student_list, chat_combobox,))
    #checking_connection.start()

