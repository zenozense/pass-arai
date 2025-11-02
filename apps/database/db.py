import os
import pytz
import bcrypt
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

# ----------------connect section----------------

mongo_string = os.getenv("url")
client = MongoClient(mongo_string)
database_1 = client["database1"]
collection_log = database_1["log"]
collection_users = database_1["users"]

# ----------------CRUD operation----------------

def create_register_user(username, password):
    query = {"username": username}

    if collection_users.find_one(query):
        return False

    password_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes,salt)
    username_information = {
        "username" : username,
        "password" : hashed_password,
        "created_at": datetime.now(pytz.timezone("Asia/Bangkok"))
    }

    result = collection_users.insert_one(username_information)
    return True,result.inserted_id


def is_exists_user(username,password):
    """login username and password"""
    query = {"username" : username}
    user_docment = collection_users.find_one(query)

    if not user_docment :
        return False
    password_bytes = password.encode("utf-8")
    hashed_password_from_DB = user_docment["password"]

    if bcrypt.checkpw(password_bytes,hashed_password_from_DB):
        return True
    else :
        return False


def save_new_generated_password(users, password, note=""):
    new_password_and_note = {
        "username": users,
        "generated_password": password,
        "note": note,
        "created at": datetime.now(pytz.timezone("Asia/Bangkok"))
    }
    result = collection_log.insert_one(new_password_and_note)
    return result.inserted_id


def get_all_logs_for_user(username):
    query = {"username": username}
    logs_cursor = collection_log.find(query).sort("created at", -1)
    return tuple(logs_cursor)


def update_note(log_id, new_note):
    query = {"_id": ObjectId(log_id)}
    new_values = {"$set": {"note": new_note}}
    result = collection_log.update_one(query, new_values)
    if result.modified_count > 0:
        return result.modified_count


def delete_specific_generated_password(log_id):
    try:
        query = {"_id": ObjectId(log_id)}
        result = collection_log.delete_one(query)
        if result.deleted_count > 0:
            return True
        else:
            return False

    except Exception as e:
        return False
