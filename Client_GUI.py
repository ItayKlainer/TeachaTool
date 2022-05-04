from tkinter import *
import Client


def client_GUI():
    main_client = Tk()
    main_client.title("TeachaTool - Student")
    main_client.geometry("1280x720")
    main_client.iconbitmap("Logo.ico")
    main_client.resizable()

    welcome_lbl = Label(main_client, text="Welcome to TeachaTool", font=("Arial", 40, "bold"))
    welcome_lbl.place(relx=0.5, y=50, anchor=CENTER)

    username_lbl = Label(main_client, text="Username:", font=("Arial", 20, "underline"))
    username_lbl.place(x=500, y=250)

    username = StringVar()

    username_entry = Entry(main_client, textvariable=username, font=("Arial", 16))
    username_entry.place(x=650, y=255, height=30, width=150)

    password_lbl = Label(main_client, text="Password:", font=("Arial", 20, "underline"))
    password_lbl.place(x=500, y=300)

    password = StringVar()

    password_entry = Entry(main_client, textvariable=password, show='*', font=("Arial", 16))
    password_entry.place(x=650, y=305, height=30, width=150)

    log_in_btn = Button(main_client, text="Log in", command=lambda: [client_log_in(main_client)], font=("Arial", 14, "bold"))
    log_in_btn.place(x=525, y=450)

    register_btn = Button(main_client, text="Register", command=client_register, font=("Arial", 14, "bold"))
    register_btn.place(x=675, y=450)

    register_lbl = Label(main_client, text="Don't have an account?\nregister here", font=("Arial", 10, "underline"))
    register_lbl.place(x=655, y=490)

    mainloop()


def client_log_in(main_client):  #checking with database, if username & password true:
    main_client.destroy()
    options_server = Tk()
    options_server.title("TeachaTool - Client")
    options_server.geometry("1280x720")
    options_server.iconbitmap("Logo.ico")
    options_server.resizable()

    message = StringVar()
    student_message = Entry(options_server, textvariable=message, font=("Arial", 10))
    student_message.place(x=805, y=600, height=25, width=420)

    chat = Text(options_server)
    chat.place(x=775, y=20, height=575, width=450)
    chat.config(state=DISABLED)

    chat_scrollbar = Scrollbar(options_server)
    chat_scrollbar.place(x=1225, y=20, height=575)
    chat_scrollbar.config(command=chat.yview)

    client = Client.client_create()
    Client.client_start(client, chat)

    public_message_icon = PhotoImage(file='Send_message.png')
    send_public_message_btn = Button(options_server, image=public_message_icon, command=lambda: [Client.Client.write(client, message.get(), chat, True), student_message.delete(0, 'end')], font=("Arial", 14, "bold"))
    send_public_message_btn.place(x=775, y=600, height=25, width=25)

    private_message_icon = PhotoImage(file='Send_private_message.png')
    send_private_message_btn = Button(options_server, image=private_message_icon, command=lambda: [Client.Client.write(client, message.get(), chat, False), student_message.delete(0, 'end')], font=("Arial", 14, "bold"))
    send_private_message_btn.place(x=775, y=630, height=25, width=25)

    mainloop()


def print_message(message, chat):
    chat.insert('end', message + '\n')


def client_register():
    print("4")


def active_chat(chat):
    chat.config(state=NORMAL)


def disable_chat(chat):
    chat.config(state=DISABLED)


if __name__ == "__main__":
    client_GUI()
