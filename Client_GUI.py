from tkinter import *


def client_log_in():
    print("3")

def client_register():
    print("4")


def client_GUI():
    main_client = Tk()
    main_client.title("TeachaTool - Student")
    main_client.geometry("1280x720")
    main_client.iconbitmap("Logo.ico")
    main_client.resizable()

    welcome_lbl = Label(main_client, text="Welcome to TeachaTool", font=("Arial", 40, "bold")).place(relx=0.5, y=50,anchor=CENTER)

    username_lbl = Label(main_client, text="Username:", font=("Arial", 20, "underline")).place(x=500, y=250)
    username = StringVar()
    username_entry = Entry(main_client, textvariable=username, font=("Arial", 16)).place(x=650, y=255, height=30, width=150)

    password_lbl = Label(main_client, text="Password:", font=("Arial", 20, "underline")).place(x=500, y=300)
    password = StringVar()
    password_entry = Entry(main_client, textvariable=password, show='*',font=("Arial", 16)).place(x=650, y=305, height=30, width=150)

    log_in_btn = Button(main_client, text="Log in", command=client_log_in, font=("Arial", 14, "bold")).place(x=525, y=450)

    register_btn = Button(main_client, text="Register", command=client_register, font=("Arial", 14, "bold")).place(x=675, y=450)
    register_lbl = Label(main_client, text="Don't have an account?\nregister here", font=("Arial", 10, "underline")).place(x=655, y=490)
    mainloop()

if __name__ == "__main__":
    client_GUI()