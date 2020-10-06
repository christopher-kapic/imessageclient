from app import app
from flask import render_template
from flask import request


import sqlite3
from subprocess import Popen, PIPE
from datetime import datetime
import json


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/init")
def load_init():
    NUM_CONVERSATIONS = 20
    NUM_MESSAGES = 50

    conn = connectToDatabase()
    c = conn.cursor()

    today = str(datetime.today()).split()[0].split("-")
    lastMonth = f"{today[0]}-0{str(int(today[1])-1)}-{today[2]}"
    c.execute(
        f"SELECT handle_id,is_from_me FROM message WHERE datetime(message.date/1000000000 + strftime('%s', '2001-01-01') ,'unixepoch','localtime') > '{lastMonth}';"
    )
    data = c.fetchall()
    data.reverse()

    handleIds = []
    for m in data:
        if len(handleIds) == NUM_CONVERSATIONS:
            break
        elif m[0] in handleIds or m[0] == 0:
            pass
        else:
            handleIds.append(m[0])

    phoneNumbers = []
    for hId in handleIds:
        c.execute(f"SELECT id FROM handle WHERE ROWID={hId};")
        phoneNumbers.append(c.fetchall()[0][0])

    conversations = []
    for i in range(len(handleIds)):
        convo = Conversation(getName(phoneNumbers[i]), handleIds[i], phoneNumbers[i])
        conversations.append(convo)

    for convo in conversations:
        c.execute(
            f"SELECT is_from_me, text FROM message WHERE handle_id={convo.handleId} and datetime(message.date/1000000000 + strftime('%s', '2001-01-01') ,'unixepoch','localtime') > '{lastMonth}';"
        )
        data = c.fetchall()
        convo.addMessages(data[-NUM_MESSAGES:])

    json_string = json.dumps([convo.__dict__ for convo in conversations])

    return json_string


@app.route("/api/message", methods=["POST"])
def send_message():
    # message = json.loads(json)
    message = json.dumps(request.get_json(force=True))
    message = json.loads(message)
    print(message)
    # r = message.get("recipient")
    # t = message.get("text")
    r = message["recipient"]
    t = message["text"]
    # r = request.form["recipient"]
    # t = request.form["text"]

    # r = request.form.get("recipient")
    # t = request.form.get("text")

    # r = request.get_json().get("recipient")
    # t = request.get_json().get("text")

    tell = f'tell application "Messages"\n'
    myTry = f"try\n"
    sendText = f'send "{t}" to buddy "{r}"\n'
    onError = f"on error\n"
    delay = f"delay 5\n"
    endTry = f"end try\n"
    endTell = f"end tell"
    appleScript = f"{tell}{myTry}{sendText}{onError}{delay}{sendText}{endTry}{endTell}"

    output = Popen(f"osascript -e '{appleScript}'", shell=True, stdout=PIPE).stdout
    oStr = output.read().decode("utf-8").strip()

    if oStr == "":
        # This means it worked properly no error
        return 0
    elif "error" in oStr.lower():
        # This means there was an error. We can work on distinguishing errors and returning distinct error values/messages later if you want.
        return 1
    else:
        # This means something happend and I'm not sure if its an error or if the text managed to send and there's just something else going on that being reported. We can investigate this later if you want too.
        return 2


############################## Objects ###############################
class Conversation(object):
    def __init__(self, contact, handleId, phoneNumber):
        self.contact = contact
        self.handleId = handleId
        self.phoneNumber = phoneNumber
        self.messages = []

    def __repr__(self):
        return self.contact

    def __str__(self):
        printStr = f"{self.contact}"
        for m in self.messages:
            if m[0] == 1:
                person = "Me:   "
            else:
                person = f"{self.contact}:   "
            printStr = printStr + f"\n\t{person}{m[1]}"

        return printStr

    def addMessages(self, messages):
        # messages.reverse()
        self.messages = messages

    def json(self):
        return json.dumps(self.__dict__)


######################################################################
############################# Functions ##############################


def connectToDatabase():
    output = Popen(f"whoami", shell=True, stdout=PIPE).stdout
    IAm = output.read().decode("utf-8").strip()

    # Relevant tables are "handle", "message", "chat"
    conn = sqlite3.connect(f"/Users/{IAm}/Library/Messages/chat.db")
    return conn


def getName(id):
    tell = f'tell application "Messages"'
    myTry = f"try"
    get = f'get full name of every buddy where handle is "{id}"'
    onErr = f"on error errStr"
    ifErr = f"errStr"
    endTry = f"end try"
    endTell = f"end tell"

    appleScript = f"{tell}\n{myTry}\n{get}\n{onErr}\n{ifErr}\n{endTry}\n{endTell}"

    output = Popen(f"osascript -e '{appleScript}'", shell=True, stdout=PIPE).stdout
    buddy = output.read().decode("utf-8").strip().split(",")[0]

    return buddy


def timeToFloat(time):
    return float(str(time).split(":")[-1])


######################################################################

