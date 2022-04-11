from scapy.all import *
from scapy.layers.inet import Ether, IP, TCP, UDP
import threading
from collections import defaultdict
import socket
import time
from project_settings import *
import select
import pickle
from tkinter import *
from tkinter import ttk
import tkinter as tk

running = True


class Filter:
    #  filter all the trafic

    @staticmethod
    def filter_by_specific_ip(packets, ip_to_detect=[]):
        #  filter by ip
        d = defaultdict(lambda: [])
        for packet in packets:
            for i in packet:
                if IP in i and i[IP].src in ip_to_detect:
                    d[i[IP].src].append(i)
        return d

    @staticmethod
    def filter_by_protocols(packets, protocols_to_detect=[]):
        d = defaultdict(lambda: [])
        for packet in packets:
            for i in packet:
                if IP in i:
                    if TCP in i:
                        if str(i[TCP].dport) in protocols_to_detect:
                            d[i[TCP].dport].append(i)
                    elif UDP in i:
                        if str(i[UDP].dport) in protocols_to_detect:
                            d[i[UDP].dport].append(i)
        return d

    @staticmethod
    def filter_by_src_ip(packets):
        #  accept if there is ip
        d = defaultdict(lambda: 0)
        for packet in packets:
            if IP in packet:
                d[packet[IP].src] += 1
        return d

    @staticmethod
    def filter_by_mac_src(packets):
        #  accept if there is mac
        d = defaultdict(lambda: 0)
        for packet in packets:
            if Ether in packet:
                d[packet[Ether].src] += 1
        return d


class Client:
    def __init__(self):

        self.privileges = -1
        self.root = Tk()
        self.root['background'] = '#DADEEA'
        self.root.geometry("1200x800")
        self.frm = tk.Frame(self.root)
        self.frm['background'] = '#DADEEA'

        self.frm.grid()
        tk.Text()
        self.start_button = tk.Button(self.frm, text="Click here to start", command=self.start, height = 2,width = 15, background  = "#82C5C4",  activebackground='#82C5C4')
        self.start_button.grid(column=0, row=1,padx=550,pady=150)
        tk.Label(self.frm, bg = '#DADEEA', text="Welcome the app",font=('Helvetica bold', 40)).grid(row=0, pady = 50)
        self.new_rules = defaultdict(lambda : [])

        self.root.mainloop()

    def start(self):
        self.client = socket.socket()
        self.client.connect(
            ("127.0.0.1", SERVER_PORT))  # should connect to server IP but for now it connectes to the same computer

        self.rules = {}

        self.__admin_opcodes = {CHANGE_CLIENT_RULES: self.change_clients_rules,
                                CHECK_FOR_ANOMALIES: self.check_for_anomalies}

        self.__client_opcodes = {NEW_RULES: self.process_new_rules}

        self.login_to_server()

    def open_new_window(self,window_name, size):

        new_window = Toplevel(self.root)
        new_window['background'] = '#DADEEA'

        new_window.title(window_name)

        new_window.geometry(size)
        return new_window


    def recv_from_server(self):
        while True:
            server_data = self.client.recv(1024).decode()
            opcode, data = server_data.split('!')
            self.__client_opcodes[int(opcode)](data)

    def clear_screen(self):
        for widgets in self.frm.winfo_children():
            widgets.destroy()

    def send_login_info_to_server(self):
        self.client.send(
            f"{LOGIN}!{self.username_input.get()}!{self.password_input.get()}".encode())
        #  check if connected successfully
        login_result = self.client.recv(1024).decode()
        if int(login_result) == COULD_NOT_LOGIN_CLIENT:
            choice = input("Do you want to try again or quit? (y for try again) ")
            if choice == 'y':
                self.login_to_server()
                return
            else:
                #  if user don't want to try again end the program
                global running
                running = False

        elif int(login_result) == CLIENT:
            self.privileges = CLIENT
            threading.Thread(target=self.recv_from_server).start()
            self.clear_screen()
            Label(self.frm, text="Monitoring...", font=('Helvetica bold', 16), bg='#DADEEA').grid(column=2, row=3)

        elif int(login_result) == ADMIN:
            self.privileges = ADMIN
            self.clear_screen()
            tk.Button(self.frm, text="Change rules", command=self.change_clients_rules, height=2, width=15, font=('Helvetica bold', 16),
                                        background="#82C5C4", activebackground='#82C5C4').grid(column=0, row=1, padx=500,pady=200)
            tk.Button(self.frm, text="Check anomalies", command=self.check_for_anomalies, height=2, width=15,  font=('Helvetica bold', 16),
                                          background="#82C5C4", activebackground='#82C5C4').grid(column=0, row=2,pady = 20)
        else:
            print("ERROR")

    def login_to_server(self):
        #  login to server with username and password
        self.clear_screen()
        self.username_input = tk.Entry(self.frm,
                                           width=40,
                                           font=('Helvetica bold', 16),
                                        justify='center',
                                        bg="#CFDFE4"
                                        )
      #  self.username_input.tag_configure("center", justify='center')

        self.password_input = tk.Entry(self.frm,
                                           width=40,
                                           font=('Helvetica bold', 16),
                                        justify='center',
                                        show='*',
                                        bg = "#CFDFE4"
                                        )
        #self.username_input.tag_configure("center", justify='center')

        self.username_input.grid(column=3, row=2, pady = 200)
        Label(self.frm, text="Enter your username",font=('Helvetica bold', 16), bg = '#DADEEA').grid(column=2, row=2)

        self.password_input.grid(column=3, row=3, padx = 100, pady = 0)
        Label(self.frm, text="Enter your password",font=('Helvetica bold', 16), bg = '#DADEEA').grid(column=2, row=3)

        tk.Button(self.frm, text="Connect to server",bg = '#DADEEA', command=self.send_login_info_to_server,font=('Helvetica bold', 16)).place(rely = 0.05, relx = 0.5, bordermode=OUTSIDE, height=20, width=200)

    def process_new_rules(self, new_rules):
        last_rule = None
        for i, new_rule_object in enumerate(new_rules.split(RULES_SEPERATOR)[:-1]):
            if i % 2 == 0:
                last_rule = new_rule_object
                self.rules[new_rule_object] = []
            else:
                for filter in new_rule_object.split(FILTERS_SEPERATORS)[:-1]:
                    self.rules[last_rule].append(filter)


    def change_clients_rules(self):
        new_window = self.open_new_window("Rules","800x600")
        self.ip_input_text = tk.Entry(new_window,
                                           width=40,
                                           font=('Helvetica bold', 16),
                                        justify='center',
                                      bg = "#CFDFE4")

        self.protocol_input_text = tk.Entry(new_window,
                                           width=40,
                                           font=('Helvetica bold', 16),
                                        justify='center',
                                            bg = "#CFDFE4")

        self.new_rules = defaultdict(lambda : [])
        tk.Label(new_window, text="Enter ip to filter", bg = "#DADEEA",font=('Helvetica bold', 16)).grid(pady=100,row=0,column = 0)
        tk.Label(new_window, text="Enter port to filter", bg = "#DADEEA", font=('Helvetica bold', 16)).grid(pady = 100,row=1, column=0)
        self.ip_input_text.grid(column=2, row=0)
        self.protocol_input_text.grid(column=2, row=1)

        tk.Button(new_window, bg = "#82C5C4",font=('Helvetica bold', 12), text="Add ip", command=self.add_ip_filter).grid(column=0, row=2)
        tk.Button(new_window,  bg = "#82C5C4",font=('Helvetica bold', 12), text="Add port", command=self.add_protocol_filter).grid(column=1, row=2)
        tk.Button(new_window, bg = "#82C5C4",font=('Helvetica bold', 12), text="Save", command=self.save_new_rules).grid(column=2, row=2)

    def add_ip_filter(self):
        ips=""
        ip_filter = self.ip_input_text.get()
        try:
            socket.inet_aton(ip_filter)
            ips += ip_filter + FILTERS_SEPERATORS
        except:
            print("Invalid ip")

        self.new_rules[FILTER_BY_IP] += str(ip_filter) + FILTERS_SEPERATORS

    def add_protocol_filter(self):
        protocols=""
        protocol_filter = self.protocol_input_text.get()
        if protocol_filter.isnumeric() and int(protocol_filter) > 0:
            protocols += protocol_filter + FILTERS_SEPERATORS

        self.new_rules[FILTER_BY_PROTOCOL] += str(protocol_filter) + FILTERS_SEPERATORS

    def save_new_rules(self):
        string_new_rules = ""
        for filter in self.new_rules:
            string_new_rules+= str(filter) + RULES_SEPERATOR + "".join(self.new_rules[filter])+RULES_SEPERATOR
        self.client.send(f"{CHANGE_CLIENT_RULES}!{string_new_rules}".encode())


    def check_for_anomalies(self):
        self.client.send(f"{CHECK_FOR_ANOMALIES}".encode())
        ttk.Label(self.frm, text=self.client.recv(2048).decode()).grid(column=0, row=3)

    def add_new_admin(self):
        # In order to add another admin - will be used in later versions. for now you can add new admin by creating one in mongodb
        username = input("Pls enter new admin username ")
        password = input("Pls enter new admin password ")
        self.client.send(f"{ADD_NEW_ADMIN}!{username}!{password}".encode())


class Sniffer:
    # Only one object from this class
    def __init__(self):
        self.__packets = []
        self.client = Client()

    def __summary_to_text(self, summary):
        text = ""
        d = defaultdict(lambda: 0)
        for i in summary:
            for packet in i:
                if str(FILTER_BY_IP) in self.client.rules:
                    ip = str(packet[IP].src)
                if str(FILTER_BY_PROTOCOL) in self.client.rules:
                    if TCP in packet:
                        port = str(packet[TCP].dport)
                    else:
                        port = str(packet[UDP].dport)
                d[(ip, port)] += 1

        for i in d:
            text += str(i).replace(' ', "") + ":" + str(d[i]) + " "
        return text

    def __summary_packets(self):
        #  create a summary of all the network traffic

        # TODO - add the ability to filter multiple stuff (protocols and ips and ect)
        while running:
            summary = None
            time.sleep(1)

            if str(FILTER_BY_PROTOCOL) in self.client.rules:
                if summary is None:
                    summary = Filter().filter_by_protocols(self.__packets, self.client.rules[str(FILTER_BY_PROTOCOL)])
                elif summary is not None and len(summary) > 0:
                    summary = Filter().filter_by_protocols(list(summary.values()),
                                                           self.client.rules[str(FILTER_BY_PROTOCOL)])

            if str(FILTER_BY_IP) in self.client.rules:
                if summary is None:
                    summary = Filter().filter_by_specific_ip(self.__packets, self.client.rules[str(FILTER_BY_IP)])
                elif summary is not None and len(summary) > 0:
                    summary = Filter().filter_by_specific_ip(list(summary.values()),
                                                             self.client.rules[str(FILTER_BY_IP)])

            if summary is not None and len(summary) > 0:
                self.client.client.send(f"{PACKET_INFO}!{self.__summary_to_text((list(summary.values())))}".encode())

    def __add_packet(self, packet_to_add):
        self.__packets.append(packet_to_add)

    def run(self):
        threading.Thread(target=self.__summary_packets).start()
        sniff(prn=lambda packet: self.__add_packet(packet))


if __name__ == "__main__":
    s = Sniffer()
    if s.client.privileges == CLIENT:
        threading.Thread(target=s.run).start()