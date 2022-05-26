from pymongo import MongoClient
import hashlib
import gridfs
import os
import Server_GUI
import Server
import Configuration

cluster = MongoClient("mongodb+srv://ItayKlainer:klainer2104@teachatooldb.nazai.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
teachatooldb = cluster["TeachaTool"]
teachers_collection = teachatooldb["Teachers"]
students_collection = teachatooldb["Students"]
files_collection = teachatooldb["fs.files"]
chunk_files_collection = teachatooldb["fs.chunks"]
gridfs_connection_to_db = gridfs.GridFS(teachatooldb)

def add_teacher(username, password):
    hash_password = hashlib.sha256(bytes(password, 'UTF-8'))
    teachers_collection.insert_one({"_id": teachers_collection.count_documents({}), "Username": username, "Password": hash_password.hexdigest()})

def check_teacher_log_in(username, password):
    hash_password = hashlib.sha256(bytes(password, 'UTF-8'))
    if teachers_collection.count_documents({"Username": username, "Password": hash_password.hexdigest()}) > 0:
        return True
    else:
        return False


def check_teacher_register(username, password1, password2):
    if not username or not password1 or not password2:
        return 0
    elif password1 != password2:
        return 1
    elif len(password1) < 8:
        return 2
    elif teachers_collection.count_documents({"Username": username}) > 0:
        return 3
    else:
        add_teacher(username, password1)
        return 4


def add_student(username, password):
    hash_password = hashlib.sha256(bytes(password, 'UTF-8'))
    students_collection.insert_one({"_id": students_collection.count_documents({}), "Username": username, "Password": hash_password.hexdigest()})


def check_student_log_in(username, password):
    hash_password = hashlib.sha256(bytes(password, 'UTF-8'))
    if students_collection.count_documents({"Username": username, "Password": hash_password.hexdigest()}) > 0:
        return True
    else:
        return False


def check_student_register(username, password1, password2):
    if not username or not password1 or not password2:
        return 0
    elif password1 != password2:
        return 1
    elif len(password1) < 8:
        return 2
    elif students_collection.count_documents({"Username": username}) > 0:
        return 3
    else:
        add_student(username, password1)
        return 4


def upload_file(path, username, browse_files_combobox, server, chat, student_list, chat_combobox, screen_share_combobox):
    try:
        file = open(path, "rb")
        file_name = os.path.basename(path)
        file_data = file.read()
        file_hash = hashlib.md5(file_data)
        gridfs_connection_to_db.put(file_data, file_name=file_name, teacher_name=username, file_hash= file_hash.hexdigest())
    except:
        Server_GUI.print_message("Error, file hasn't been uploaded", chat, "red")
    else:
        Server_GUI.update_files_combobox(browse_files_combobox)
        Server_GUI.print_message("The file " + file_name + " has been uploaded", chat, "blue")
        Server.Server.send_files(server, file_name, chat, student_list, chat_combobox, screen_share_combobox, True)


def delete_file(file_name, server, chat, student_list, chat_combobox, screen_share_combobox, browse_files_combobox):
    if file_name:
        try:
            file_document = teachatooldb.fs.files.find_one({"file_name": file_name})
            file_id = file_document["_id"]
            gridfs_connection_to_db.delete(file_id)
        except:
                Server_GUI.print_message("Error, couldn't delete file", chat, "red")
        else:
            Server_GUI.update_files_combobox(browse_files_combobox)
            Server_GUI.print_message("The file " + file_name + " has been deleted", chat, "blue")
            Server.Server.send_files(server, file_name, chat, student_list, chat_combobox, screen_share_combobox, False)
    else:
        Server_GUI.print_message("Please select a file from the list above", chat, "green")


def download_file(file_name, chat):
    if file_name:
        try:
            file_document = teachatooldb.fs.files.find_one({"file_name": file_name})
            file_id = file_document["_id"]
            file_data = gridfs_connection_to_db.get(file_id).read()
            new_file = open(Configuration.folder_to_download_files + file_name, "wb")
            new_file.write(file_data)
            new_file.close()
        except:
                Server_GUI.print_message("Error, couldn't download file", chat, "red")
        else:
            Server_GUI.print_message("File has been downloaded at " + Configuration.folder_to_download_files, chat, "blue")
            original_file_hash = file_document["file_hash"]
            new_file_hash = hashlib.md5(file_data)
            if original_file_hash != new_file_hash.hexdigest():
                Server_GUI.print_message("ERROR, the file has been changed, please download it again  " + Configuration.folder_to_download_files, chat, "red")
    else:
        Server_GUI.print_message("Please select a file from the list above", chat, "green")


def get_file_names_list():
    file_names_lst = []
    files_lst = list(files_collection.find())
    for file in files_lst:
        file_names_lst.append(file["file_name"])
    return file_names_lst
