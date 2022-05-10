from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import Server
import DataBase


def start_front_page():
    front_page_server = Tk()
    front_page_server.title("TeachaTool - Teacher")
    front_page_server.geometry("1280x720")
    front_page_server.iconbitmap("Logo.ico")
    front_page_server.resizable()

    welcome_lbl = Label(front_page_server, text="Welcome to TeachaTool", font=("Arial", 54, "bold"))
    welcome_lbl.place(relx=0.5, y=50, anchor=CENTER)

    login_lbl = Label(front_page_server, text="Log in:", font=("Arial", 32, "underline"))
    login_lbl.place(x=350, y=150)

    username_lbl = Label(front_page_server, text="Username:", font=("Arial", 20, "underline"))
    username_lbl.place(x=350, y=250)

    username = StringVar()

    username_entry = Entry(front_page_server, textvariable=username, font=("Arial", 14))
    username_entry.place(x=500, y=255, height=30, width=200)

    password_lbl = Label(front_page_server, text="Password:", font=("Arial", 20, "underline"))
    password_lbl.place(x=350, y=300)

    password = StringVar()

    password_entry = Entry(front_page_server, textvariable=password, show='*', font=("Arial", 16))
    password_entry.place(x=500, y=305, height=30, width=200)

    login_btn = Button(front_page_server, text="Log in", command=lambda: [log_in(username.get(), password.get(), front_page_server)], font=("Arial", 18, "bold"))
    login_btn.place(x=350, y=375)

    register_btn = Button(front_page_server, text="Register", command=lambda: [start_register_page(front_page_server)], font=("Arial", 18, "bold"))
    register_btn.place(x=1000, y=375)

    register_lbl = Label(front_page_server, text="Don't have an account?\nregister here", font=("Arial", 10, "underline"))
    register_lbl.place(x=990, y=425)

    mainloop()


def start_register_page(front_page_server):
    front_page_server.withdraw()
    register_page_server = Toplevel()
    register_page_server.title("TeachaTool - Teacher")
    register_page_server.geometry("1280x720")
    register_page_server.iconbitmap("Logo.ico")
    register_page_server.resizable()

    welcome_lbl = Label(register_page_server, text="Welcome to TeachaTool", font=("Arial", 54, "bold"))
    welcome_lbl.place(relx=0.5, y=50, anchor=CENTER)

    register_lbl = Label(register_page_server, text="Register:", font=("Arial", 32, "underline"))
    register_lbl.place(x=350, y=150)

    username_lbl = Label(register_page_server, text="Username:", font=("Arial", 20, "underline"))
    username_lbl.place(x=350, y=250)

    new_username = StringVar()

    username_entry = Entry(register_page_server, textvariable=new_username, font=("Arial", 14))
    username_entry.place(x=500, y=255, height=30, width=200)

    password_lbl = Label(register_page_server, text="Password:", font=("Arial", 20, "underline"))
    password_lbl.place(x=355, y=300)

    password1 = StringVar()

    password_entry = Entry(register_page_server, textvariable=password1, show='*', font=("Arial", 16))
    password_entry.place(x=500, y=305, height=30, width=200)

    re_enter_password_lbl = Label(register_page_server, text="Re enter your password:", font=("Arial", 20, "underline"))
    re_enter_password_lbl.place(x=185, y=350)

    password2 = StringVar()

    re_enter_password_entry = Entry(register_page_server, textvariable=password2, show='*', font=("Arial", 16))
    re_enter_password_entry.place(x=500, y=355, height=30, width=200)

    register_btn = Button(register_page_server, text="Register", command=lambda: [register(new_username.get(), password1.get(), password2.get(), register_page_server, front_page_server)], font=("Arial", 18, "bold"))
    register_btn.place(x=365, y=425)

    login_btn = Button(register_page_server, text="Log in", command=lambda: [register_page_server.withdraw(), front_page_server.deiconify()], font=("Arial", 18, "bold"))
    login_btn.place(x=1000, y=425)

    register_lbl = Label(register_page_server, text="Already have an account?\nlog in here", font=("Arial", 10, "underline"))
    register_lbl.place(x=975, y=475)

    mainloop()


def register(username, password1, password2, register_page_server, front_page_server):
    num = DataBase.check_teacher_register(username, password1, password2)
    if num == 0:
        messagebox.showwarning("Error", "Please fill up all the entries")
    elif num == 1:
        messagebox.showwarning("Error", "You must enter the same password twice")
    elif num == 2:
        messagebox.showwarning("Error", "Password must be atleast 8 characters long")
    elif num == 3:
        messagebox.showwarning("Error", "Username already exists")
    else:
        messagebox.showinfo("Account has been created", "The account has been created,\nplease log in now")
        register_page_server.withdraw()
        front_page_server.deiconify()


def log_in(username, password, front_page_server):
    if DataBase.check_teacher_log_in(username, password):
        start_main_page(front_page_server, username)
    else:
        messagebox.showwarning("Invalid Credentials", "Incorrect username or password,\nplease try again")


def start_main_page(front_page_server, username):
    front_page_server.withdraw()
    main_page_server = Toplevel()
    main_page_server.title("TeachaTool - Teacher")
    main_page_server.geometry("1280x720")
    main_page_server.iconbitmap("Logo.ico")
    main_page_server.resizable()

    message = StringVar()

    teacher_message = Entry(main_page_server, textvariable=message, font=("Arial", 10))
    teacher_message.place(x=805, y=600, height=25, width=420)

    chat = Text(main_page_server)
    chat.place(x=775, y=20, height=575, width=450)
    chat.config(state=DISABLED)

    chat_scrollbar = Scrollbar(main_page_server)
    chat_scrollbar.place(x=1225, y=20, height=575)
    chat_scrollbar.config(command=chat.yview)

    student_list = Listbox(main_page_server)
    student_list.place(x=20, y=50, height=500, width=250)

    chat_combobox = ttk.Combobox(main_page_server, value="Everyone")
    chat_combobox.place(x=775, y=630)
    chat_combobox.current(0)

    screen_share_combobox = ttk.Combobox(main_page_server)
    screen_share_combobox.place(x=475, y=50)

    student_list_lbl = Label(main_page_server, text="Currently online:", font=("Arial", 14, "underline"))
    student_list_lbl.place(x=20, y=10)

    server = Server.server_create(username)
    Server.server_start(server, chat, student_list, chat_combobox, screen_share_combobox)

    photo = PhotoImage(file='Send_message.png')
    send_message_btn = Button(main_page_server, image=photo, command=lambda: [Server.Server.write(server,message.get(), chat, student_list, chat_combobox, screen_share_combobox), teacher_message.delete(0, 'end')], font=("Arial", 14, "bold"))
    send_message_btn.place(x=775, y=600, height=25, width=25)

    screen_share_btn = Button(main_page_server, text="Watch the screen of", command=lambda: [Server.Server.ask_for_stream(server, check_screen_share_receiver(screen_share_combobox))], font=("Arial", 12, "bold"))
    screen_share_btn.place(x=300, y=50)

    stop_screen_share_lbl = Label(main_page_server, text="To close a screen,\npress the window and then press ESC", justify=LEFT, font=("Arial", 12,))
    stop_screen_share_lbl.place(x=300, y=90)
    #stop_screen_share_btn = Button(main_page_server, text="Stop all screen shares", command=lambda: [Server.Server.stop_all_streams(server)], font=("Arial", 11, "bold"))
    #stop_screen_share_btn.place(x=300, y=100)

    mainloop()


def print_message(message, chat):
    chat.insert('end', message + '\n')


def add_to_list(student_list, name):
    student_list.insert(END, name)


def remove_from_list(student_list, index):
    student_list.delete(index)


def update_combobox(chat_combobox, screen_share_combobox, client_lst):
    chat_combobox['values'] = client_lst
    screen_share_combobox['values'] = client_lst[1:]


def check_chat_receiver(chat_combobox):
    return chat_combobox.get()


def check_screen_share_receiver(screen_share_combobox):
    return screen_share_combobox.get()


def active_chat(chat):
    chat.config(state=NORMAL)


def disable_chat(chat):
    chat.config(state=DISABLED)

if __name__ == "__main__":
    start_front_page()