from src.database.config import supabase
import bcrypt

def hash_pass(pwd):
  return bcrypt.hashpw(pwd.encode(),bcrypt.gensalt()).decode()

def check_pass(pwd,hashed):
  return bcrypt.checkpw(pwd.encode(),hashed.encode())

def check_teacher_exists(username):
  #checks for unique username, returns false if username is already taken
  responce = supabase.table("teachers").select("user_name").eq("user_name", username).execute()
  return len(responce.data) > 0

def create_teacher(username,password,name):
  data={"user_name":username,"password":hash_pass(password),"name":name}
  response = supabase.table("teachers").insert(data).execute()
  return response.data

def teacher_login(username,password):
  response = supabase.table("teachers").select("*").eq("user_name",username).execute()
  if response.data :
    teacher= response.data[0]
    if check_pass(password,teacher["password"]):
      return teacher
  return None


def get_all_students():
  response = supabase.table("students").select("*").execute()
  return response.data