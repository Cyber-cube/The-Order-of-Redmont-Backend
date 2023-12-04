from flask import Flask, render_template, request, redirect, url_for, flash, session
from cors import CORS
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
    users["users"][id] = {username: username,
              "is_accepted": False,
              "is_headmaster": False}
    pending_users["users"].append = f"{id} ({username})"
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
  elif users[id]["is_accepted"] == False:
    return "Your account has not been accepted yet"
  elif users[id]["is_accepted"]:
    return "Your account had been accepted"



if __name__ == "__main__":
  app.debug == True
  app.run(host='0.0.0.0', port=81)