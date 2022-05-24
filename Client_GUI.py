from tkinter import *
from tkinter import messagebox
import Client
import DataBase

def start_front_page():
    front_page_client = Tk()
    front_page_client.title("TeachaTool - Student")
    front_page_client.geometry("1280x720")
    front_page_client.iconbitmap("Logo.ico")
    front_page_client.resizable()

    welcome_lbl = Label(front_page_client, text="Welcome to TeachaTool", font=("Arial", 54, "bold"))
    welcome_lbl.place(relx=0.5, y=50, anchor=CENTER)

    login_lbl = Label(front_page_client, text="Log in:", font=("Arial", 32, "underline"))
    login_lbl.place(x=350, y=150)

    username_lbl = Label(front_page_client, text="Username:", font=("Arial", 20, "underline"))
    username_lbl.place(x=350, y=250)

    username = StringVar()

    username_entry = Entry(front_page_client, textvariable=username, font=("Arial", 14))
    username_entry.place(x=500, y=255, height=30, width=200)

    password_lbl = Label(front_page_client, text="Password:", font=("Arial", 20, "underline"))
    password_lbl.place(x=350, y=300)

    password = StringVar()

    password_entry = Entry(front_page_client, textvariable=password, show='*', font=("Arial", 16))
    password_entry.place(x=500, y=305, height=30, width=200)

    login_btn = Button(front_page_client, text="Log in", command=lambda: [log_in(username.get(), password.get(), front_page_client)], font=("Arial", 18, "bold"))
    login_btn.place(x=350, y=375)

    register_btn = Button(front_page_client, text="Register", command=lambda: [start_register_page(front_page_client)], font=("Arial", 18, "bold"))
    register_btn.place(x=1000, y=375)

    register_lbl = Label(front_page_client, text="Don't have an account?\nregister here", font=("Arial", 10, "underline"))
    register_lbl.place(x=990, y=425)

    mainloop()


def start_register_page(front_page_client):
    front_page_client.withdraw()
    register_page_client = Toplevel()
    register_page_client.title("TeachaTool - Teacher")
    register_page_client.geometry("1280x720")
    register_page_client.iconbitmap("Logo.ico")
    register_page_client.resizable()

    welcome_lbl = Label(register_page_client, text="Welcome to TeachaTool", font=("Arial", 54, "bold"))
    welcome_lbl.place(relx=0.5, y=50, anchor=CENTER)

    register_lbl = Label(register_page_client, text="Register:", font=("Arial", 32, "underline"))
    register_lbl.place(x=350, y=150)

    username_lbl = Label(register_page_client, text="Username:", font=("Arial", 20, "underline"))
    username_lbl.place(x=350, y=250)

    new_username = StringVar()

    username_entry = Entry(register_page_client, textvariable=new_username, font=("Arial", 14))
    username_entry.place(x=500, y=255, height=30, width=200)

    password_lbl = Label(register_page_client, text="Password:", font=("Arial", 20, "underline"))
    password_lbl.place(x=355, y=300)

    password1 = StringVar()

    password_entry = Entry(register_page_client, textvariable=password1, show='*', font=("Arial", 16))
    password_entry.place(x=500, y=305, height=30, width=200)

    re_enter_password_lbl = Label(register_page_client, text="Re enter your password:", font=("Arial", 20, "underline"))
    re_enter_password_lbl.place(x=185, y=350)

    password2 = StringVar()

    re_enter_password_entry = Entry(register_page_client, textvariable=password2, show='*', font=("Arial", 16))
    re_enter_password_entry.place(x=500, y=355, height=30, width=200)

    register_btn = Button(register_page_client, text="Register", command=lambda: [register(new_username.get(), password1.get(), password2.get(), register_page_client, front_page_client)], font=("Arial", 18, "bold"))
    register_btn.place(x=365, y=425)

    login_btn = Button(register_page_client, text="Log in", command=lambda: [register_page_client.withdraw(), front_page_client.deiconify()], font=("Arial", 18, "bold"))
    login_btn.place(x=1000, y=425)

    register_lbl = Label(register_page_client, text="Already have an account?\nlog in here", font=("Arial", 10, "underline"))
    register_lbl.place(x=975, y=475)

    mainloop()


def register(username, password1, password2, register_page_client, front_page_client):
    num = DataBase.check_student_register(username, password1, password2)
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
        register_page_client.withdraw()
        front_page_client.deiconify()


def log_in(username, password, front_page_client):
    can_connect = False
    if DataBase.check_student_log_in(username, password):
       if Client.check_server():
           start_main_page(front_page_client, username)
       else:
         messagebox.showerror("ERROR", "Couldn't connect to the teacher")
    else:
        messagebox.showwarning("Invalid Credentials", "Incorrect username or password,\nplease try again")


def start_main_page(front_page_client, username):
    front_page_client.withdraw()
    main_page_client = Toplevel()
    main_page_client.title("TeachaTool - Client")
    main_page_client.geometry("1280x720")
    main_page_client.iconbitmap("Logo.ico")
    main_page_client.resizable()

    message = StringVar()

    student_message = Entry(main_page_client, textvariable=message, font=("Arial", 10))
    student_message.place(x=805, y=600, height=25, width=420)

    chat = Text(main_page_client)
    chat.place(x=775, y=20, height=575, width=450)
    chat.config(state=DISABLED)

    chat_scrollbar = Scrollbar(main_page_client)
    chat_scrollbar.place(x=1225, y=20, height=575)
    chat_scrollbar.config(command=chat.yview)

    client = Client.client_create(username)
    Client.client_start(client, chat, front_page_client, main_page_client)

    public_message_icon = PhotoImage(file='Send_message.png')
    send_public_message_btn = Button(main_page_client, image=public_message_icon, command=lambda: [Client.Client.write(client, message.get(), chat, True, front_page_client, main_page_client), student_message.delete(0, 'end')], font=("Arial", 14, "bold"))
    send_public_message_btn.place(x=775, y=600, height=25, width=25)

    private_message_icon = PhotoImage(file='Send_private_message.png')
    send_private_message_btn = Button(main_page_client, image=private_message_icon, command=lambda: [Client.Client.write(client, message.get(), chat, False, front_page_client, main_page_client), student_message.delete(0, 'end')], font=("Arial", 14, "bold"))
    send_private_message_btn.place(x=775, y=630, height=25, width=25)

    browse_files_btn = Button(main_page_client, text="Browse\nFiles", font=("Arial", 18,))
    browse_files_btn.place(x=500, y=250, height=150, width=150)



    mainloop()


def print_message(message, chat):
    chat.insert('end', message + '\n')

def active_chat(chat):
    chat.config(state=NORMAL)


def disable_chat(chat):
    chat.config(state=DISABLED)


if __name__ == "__main__":
    start_front_page()
