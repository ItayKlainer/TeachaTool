from pymongo import MongoClient
import hashlib
import gridfs


cluster = MongoClient("mongodb+srv://ItayKlainer:klainer2104@teachatooldb.nazai.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
teachatooldb = cluster["TeachaTool"]
teachers_collection = teachatooldb["Teachers"]
students_collection = teachatooldb["Students"]
files_collection = teachatooldb["Files"]

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

'''
def upload_file():
    name = "Image"
    filelocation = path
    filedata = open(filelocation, "rb")
    data = filedata.read()
    fs = gridfs.GridFS(mongodb)
    finish = filelocation.split(".")
    finish = finish[1]
    fs.put(data, filename=name, ending=finish)
    print("upload complete")




#Download
name=input("Enter a name of file: ")
data=mongodb.fs.files.find_one({"filename":name})
my_id = data["_id"]
outputdata= fs.get(my_id).read()
siyomet=collection.find_one({"_id":my_id})
finalsiyomet=siyomet["ending"]
download_location= str("D:\PythonDownloads")
output = open(download_location+ f"\{name}.{finalsiyomet}", "wb")
output.write(outputdata)
output.close()
print("download complete")
'''
