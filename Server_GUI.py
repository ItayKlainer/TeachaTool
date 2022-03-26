from tkinter import *
import Server

def server_GUI():
    main_server = Tk()
    main_server.title("TeachaTool - Teacher")
    main_server.geometry("1280x720")
    main_server.iconbitmap("Logo.ico")
    main_server.resizable()

    welcome_lbl = Label(main_server, text="Welcome to TeachaTool", font=("Arial", 40, "bold")).place(relx=0.5, y=50, anchor=CENTER)

    username_lbl = Label(main_server, text="Username:", font=("Arial", 20, "underline")).place(x=500, y=250)
    username = StringVar()
    username_entry = Entry(main_server, textvariable=username, font=("Arial", 16)).place(x=650, y=255, height=30, width=150)

    password_lbl = Label(main_server, text="Password:", font=("Arial", 20, "underline")).place(x=500, y=300)
    password = StringVar()
    password_entry = Entry(main_server, textvariable=password, show='*', font=("Arial", 16)).place(x=650, y=305, height=30, width=150)

    log_in_btn = Button(main_server, text="Log in", command=lambda: [main_server.destroy(), server_log_in()], font=("Arial", 14, "bold")).place(x=525, y=450)

    register_btn = Button(main_server, text="Register", command=server_register, font=("Arial", 14, "bold")).place(x=675, y=450)
    register_lbl = Label(main_server, text="Don't have an account?\nregister here", font=("Arial", 10, "underline")).place(x=655, y=490)
    mainloop()

def server_log_in():

    def delete_entry():
        #teacher_message.delete(0, 'end')
        print ("basbosa")

    #checking with database
    #if username & password true:
    options_server = Toplevel()
    options_server.title("TeachaTool - Teacher")
    options_server.geometry("1280x720")
    options_server.iconbitmap("Logo.ico")
    options_server.resizable()

    server = Server.server_create()
    Server.server_start(server)
    message = StringVar()
    teacher_message = Entry(options_server, textvariable=message, font=("Arial", 16)).place(x=650, y=255, height=30, width=150)
    write_btn = Button(options_server, text="Send\nmessage", command=lambda: [Server.Server.write(server,message.get()), delete_entry()], font=("Arial", 14, "bold")).place(x=675, y=450)
    #delete_btn = Button(options_server, text="delete", command= delete_entry, font=("Arial", 14, "bold")).place(x=600, y=450)
    mainloop()


def server_register():
    print("4")



if __name__ == "__main__":
    server_GUI()




