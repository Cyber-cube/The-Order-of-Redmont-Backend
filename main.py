from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_cors import CORS
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/register', methods=["POST"])
def register():
  id = str(request.form["id"])
  username = str(request.form["username"])
  with open(".data/users.json") as f:
    users = json.load(f)
  with open("./data/pendingusers.json") as file:
    pending_users = json.load(file)
  if id in users:
    return "You already have an account"
  elif username in users:
    return "Username already taken"
  else:
    users[id] = {
      "username": username,
      "is_accepted": False,
      "is_headmaster": False}
    pending_users["users"][id] = {
      "username": username
    }
    with open(".data/users.json", "w") as f:
      json.dump(users, f, indent=2)
    with open(".data/pendingusers.json", "w") as file:
      json.dump(pending_users, file, indent=2)
    return "User registered successfully, now please wait until you are accepted by the headmaster"

@app.route('/checkaccstatus', methods=["POST"])
def checkstatus():
  id = str(request.form["id"])
  with open(".data/users.json") as f:
    users = json.load(f)
  if id not in users:
    return "You haven't registered an account yet"
  elif users[id]["is_accepted"] is False:
    return "Your account has not been accepted yet"
  elif users[id]["is_accepted"] is True:
    return "Your account has been accepted"

@app.route('/acceptpage', methods=["POST"])
def acceptpage():
  id = str(request.form["id"])
  with open(".data/users.json") as f:
    users = json.load(f)
  if users[id]["is_headmaster"] is False:
    return "You are not the headmaster"
  else:
    with open(".data/pendingusers.json") as f:
      pending_users = json.load(f)
    return render_template("acceptingpage.html", data=pending_users["users"])

@app.route('/accept', methods=["POST"])
def accept():
  id = str(request.form["id"])
  with open("./data/users.json") as f:
    users = json.load(f)
  if not id in users: 
    return "Invalid ID, please enter the correct ID"
  elif users[id]["is_accepted"] == True:
    return "This user is already accepted"
  elif users[id]["is_accepted"] is False:
    users[id]["is_accepted"] = True
    with open("./data/users.json", "w") as f:
      json.dump(users, f, indent=2)
    with open(".data/pendingusers.json") as file:
      pending_users = json.load(file)
    pending_users["users"].pop(id)
    with open("./data/pendingusers.json", "w") as file:
      json.dump(pending_users, file, indent=2)
    return "User accepted !"
     
@app.route('/checkaccstatus', methods=["POST"])
def checkaccstatus():
  device_id = str(request.form["device_id"])

  with open("data.json") as f:
    data = json.load(f)
  if data[str(device_id)]["account_accepted"] == False:
    return "Your account is not accepted yet\n(apka account abhi tak accept nahi hua hai)"
  else:
    return "Your account has been accepted, you can login now\n(Apka account accept ho gaya hai, aab aap login kar sakte hai)"
    
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=8080)