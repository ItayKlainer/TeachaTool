from tkinter import *
from tkinter import ttk
import Server

def server_GUI():
    main_server = Tk()
    main_server.title("TeachaTool - Teacher")
    main_server.geometry("1280x720")
    main_server.iconbitmap("Logo.ico")
    main_server.resizable()
    welcome_lbl = Label(main_server, text="Welcome to TeachaTool", font=("Arial", 40, "bold"))
    welcome_lbl.place(relx=0.5, y=50, anchor=CENTER)

    username_lbl = Label(main_server, text="Username:", font=("Arial", 20, "underline"))
    username_lbl.place(x=500, y=250)

    username = StringVar()

    username_entry = Entry(main_server, textvariable=username, font=("Arial", 16))
    username_entry.place(x=650, y=255, height=30, width=150)

    password_lbl = Label(main_server, text="Password:", font=("Arial", 20, "underline"))
    password_lbl.place(x=500, y=300)

    password = StringVar()

    password_entry = Entry(main_server, textvariable=password, show='*', font=("Arial", 16))
    password_entry.place(x=650, y=305, height=30, width=150)

    log_in_btn = Button(main_server, text="Log in", command=lambda: [main_server.destroy(), server_log_in()], font=("Arial", 14, "bold"))
    log_in_btn.place(x=525, y=450)

    register_btn = Button(main_server, text="Register", command=server_register, font=("Arial", 14, "bold"))
    register_btn.place(x=675, y=450)


    register_lbl = Label(main_server, text="Don't have an account?\nregister here", font=("Arial", 10, "underline"))
    register_lbl.place(x=655, y=490)

    mainloop()


def server_log_in():
    #checking with database
    #if username & password true:
    options_server = Toplevel()
    options_server.title("TeachaTool - Teacher")
    options_server.geometry("1280x720")
    options_server.iconbitmap("Logo.ico")
    options_server.resizable()

    message = StringVar()
    teacher_message = Entry(options_server, textvariable=message, font=("Arial", 10))
    teacher_message.place(x=805, y=600, height=25, width=420)

    chat = Text(options_server)
    chat.place(x=775, y=20, height=575, width=450)
    chat.config(state=DISABLED)

    chat_scrollbar = Scrollbar(options_server)
    chat_scrollbar.place(x=1225, y=20, height=575)
    chat_scrollbar.config(command=chat.yview)

    student_list = Listbox(options_server)
    student_list.place(x=20, y=50, height=500, width=250)

    chat_combobox = ttk.Combobox(options_server, value="Everyone")
    chat_combobox.place(x=775, y=630)
    chat_combobox.current(0)

    student_list_lbl = Label(options_server, text="Currently online:", font=("Arial", 14, "underline"))
    student_list_lbl.place(x=20, y=10)

    server = Server.server_create()
    Server.server_start(server, chat, student_list, chat_combobox)

    photo = PhotoImage(file='Send_message.png')
    send_message_btn = Button(options_server, image=photo, command=lambda: [Server.Server.write(server,message.get(), chat, student_list, chat_combobox), teacher_message.delete(0, 'end')], font=("Arial", 14, "bold"))
    send_message_btn.place(x=775, y=600, height=25, width=25)

    mainloop()

def print_message(message, chat):
    chat.insert('end', message + '\n')


def server_register():
    print("4")


def add_to_list(student_list, name):
    student_list.insert(END, name)


def remove_from_list(student_list, index):
    student_list.delete(index)


def update_combobox(chat_combobox, client_lst):
    chat_combobox['values'] = client_lst


def check_receiver(chat_combobox):
    return chat_combobox.get()


def active_chat(chat):
    chat.config(state=NORMAL)


def disable_chat(chat):
    chat.config(state=DISABLED)

if __name__ == "__main__":
    server_GUI()