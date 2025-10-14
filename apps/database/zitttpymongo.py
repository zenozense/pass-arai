import os
import pytz
import bcrypt
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

#-----connection section

mongo_string = os.getenv("url")
client = MongoClient(mongo_string)
database_1 = client["database1"]
collection_log = database_1["log"]  
collection_users = database_1["users"]

#-----CRUD operation

def create_register_user(username, password,dateofbirth):
    ''' 
    save new register username with hashed password to MongoDB 
    '''
    query = {"_id": username}

    # check whether already registered or not 
    if collection_users.find_one(query):
        print(f"❌ Username {username} already exists.")
        return False

    password_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes,salt)
    username_information = {
        "_id" : username,
        "password" : hashed_password,
        "date of birth" : dateofbirth,
        "created at": datetime.now(pytz.timezone("Asia/Bangkok"))
    }

    result = collection_users.insert_one(username_information)
    print(f"✅ User '{username}' registered successfully.")
    return True,result.inserted_id


def is_exists_user(username,password):
    ''' Verify user's login credentials against the database '''
    query = {"_id" : username}
    user_docment = collection_users.find_one(query)

    #check wether username exists in the Database
    if not user_docment :
        return False

    #check wether the password is same as hashed password in DB
    password_bytes = password.encode("utf-8")
    hashed_password_from_DB = user_docment["password"]

    if bcrypt.checkpw(password_bytes,hashed_password_from_DB):
        return True
    else :
        return False

def save_new_generated_password(users, password, note="."):
    ''' save a new generated password to MongoDB '''
    new_password_and_note = {
        "username": users,
        "generated password": password,
        "note": note,
        "created at": datetime.now(pytz.timezone("Asia/Bangkok"))
    }
    result = collection_log.insert_one(new_password_and_note)
    print(f"🔑 Password = '{password}' saved with ID: {result.inserted_id}")
    return result.inserted_id

def get_all_logs_for_user(username):
    """
    pull logs's user then
    return list of dictionary that contain user's log informataion
    """
    query = {"username": username}
    
    # find and sorted the information by lasted date
    logs_cursor = collection_log.find(query).sort("created at", -1)
    
    print(f"✅ get all logs in formation for {username}")
    return list(logs_cursor)

def get_all_generated_passwords_for_user(username):
    '''
    Finds all generated password logs for a specific user and returns a list of their
    generated passwords only.
    '''
    query = {"username": username}
    projection = {"generated password": 1, "_id": 0}
    password_docs_cursor = collection_log.find(query, projection)
    password_list = [doc.get("generated password") for doc in password_docs_cursor]
    
    if password_list:
        print(f"✅ Found {len(password_list)} generated password(s) for '{username}'.")
    else:
        print(f"❌ No generated passwords found for '{username}'.")
        
    return password_list

def update_note(log_id, new_note):
    ''' update some note '''
    query = {"_id": ObjectId(log_id)}
    new_values = {"$set": {"note": new_note}}  # ใช้ $set เพื่ออัพเดตค่า
    result = collection_log.update_one(query, new_values)
    if result.modified_count > 0:
        print(f"✅ Note for {log_id} updated.")
    else:
        print(f"❌ No update made for {log_id}.")
    return result.modified_count

def delete_specific_generated_password(log_id):
    ''' Delete a single generated password entry from the log collection using its ID. '''
    try:
        # convert string_id to object_id
        query = {"_id": ObjectId(log_id)}
        
        result = collection_log.delete_one(query)
        
        if result.deleted_count > 0:
            print(f"✅ Generated password with log ID '{log_id}' has been deleted.")
            return True
        else:
            print(f"❌ No generated password found with log ID '{log_id}'.")
            return False
            
    except Exception as e:
        # if the form of log_id is incorrect
        print(f"An error occurred (invalid ID format likely): {e}")
        return False

