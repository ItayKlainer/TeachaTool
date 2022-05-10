from pymongo import MongoClient
import hashlib
cluster = MongoClient("mongodb+srv://ItayKlainer:klainer2104@teachatooldb.nazai.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
teachatooldb = cluster["TeachaTool"]
teachers_collection = teachatooldb["Teachers"]
students_collection = teachatooldb["Students"]
files_collection = teachatooldb["Files"]

def add_teacher(username, password):
    hash_password = hashlib.sha256(bytes(password, 'UTF-8'))
    teachers_collection.insert_one({"_id": teachers_collection.count_documents({}), "Username": username, "Password": hash_password.hexdigest()})

def add_student(username, password):
    hash_password = hashlib.sha256(bytes(password, 'UTF-8'))
    students_collection.insert_one({"_id": students_collection.count_documents({}), "Username": username, "Password": hash_password.hexdigest()})


def check_teacher_log_in(username, password):
    hash_password = hashlib.sha256(bytes(password, 'UTF-8'))
    if teachers_collection.count_documents({"Username": username, "Password": hash_password.hexdigest()}) > 0:
        return True
    else:
        print(username, password)
        return False


def check_teacher_register(username, password1, password2):
    if not username or not password1 or not password2:
        return 0;
    elif password1 != password2:
        return 1
    elif len(password1) < 8:
        return 2
    elif teachers_collection.count_documents({"Username": username}) > 0:
        return 3
    else:
        add_teacher(username, password1)
        return 4


