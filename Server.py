import socket
import threading
import Server_GUI


class Server:
    # Creates a server on the given address
    def __init__(self, address):
        #self.server_name = input("Enter server name: ")  # will come from log in db
        self.server_name = "teacher"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.name_socket_address_list = []
        print("type file in order to send a file to the class, type -1 to send a message to the whole class, and type and index to send a private message")

    # Binds the server
    def bind(self):
        self.server.bind(self.address)

    # Listens for clients
    def listen(self, chat):
        self.server.listen()
        while True:
            connection, address = self.server.accept()
            name = connection.recv(1024).decode('utf-8')
            self.name_socket_address_list.append([name, connection, address])
            print("Connected to client")
            receiving = threading.Thread(target=self.receive, args=(connection, chat,))
            receiving.start()

    def write(self, server_message, chat):
        if server_message.strip():
            server_message = "1" + self.server_name + ": " + server_message
            Server_GUI.print_message(server_message[1:], chat)
            for i in range(len(self.name_socket_address_list)):
                try:
                    self.name_socket_address_list[i][1].send(server_message.encode())
                except:
                    print("Student " + self.name_socket_address_list[i][0] + " has been disconnected")
                    self.name_socket_address_list.pop(i)

    def receive(self, connection, chat):
        while True:
            #try:
            client_message = connection.recv(1024).decode('utf-8')
            if client_message[0] == '0':
                Server_GUI.print_message(client_message[1:], chat)
            if client_message[0] == '1':
                Server_GUI.print_message(client_message[1:], chat)
                for i in range(len(self.name_socket_address_list)):
                    try:
                        self.name_socket_address_list[i][1].send(client_message.encode())
                    except:
                        print("The student " + self.name_socket_address_list[i][0] + " has disconnected")
                        self.name_socket_address_list.pop(i)
            #except:
                #for i in self.name_socket_address_list:
                    #if i.count(connection)>0:
                        #print("The student " + i[0] + " has disconnected")
                        #self.name_socket_address_list.pop(self.name_socket_address_list.index(i))


def server_create():
    address = ("192.168.1.35", 6565)
    server = Server(address)
    server.bind()
    return server

def server_start(server, chat):
    listening = threading.Thread(target=server.listen, args=(chat,))
    listening.start()

