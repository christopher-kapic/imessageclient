# For Writing and Testing Functions and Scripts
# Ian Cramer
# 2020-08-25


import sqlite3
from subprocess import *
from datetime import *
import sqlite3
import re
import os
import sys
import json

# start_time = datetime.now() # For Timing Purposes

######################################################################
################################ Constants ###########################


NUM_CONVERSATIONS = 20
NUM_MESSAGES = 50


######################################################################


######################################################################
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


######################################################################
############################### Script ###############################


# Connect to chat.db database
conn = connectToDatabase()
c = conn.cursor()


# Collect messages from the database (This is used to find the people most recently texted with.)
today = str(datetime.today()).split()[0].split("-")
lastMonth = f"{today[0]}-0{str(int(today[1])-1)}-{today[2]}"
c.execute(
    f"SELECT handle_id,is_from_me FROM message WHERE datetime(message.date/1000000000 + strftime('%s', '2001-01-01') ,'unixepoch','localtime') > '{lastMonth}';"
)
data = c.fetchall()
data.reverse()


# Get Handle IDs from the data extracted from the "Messages" table above. The Handle ID of a person in your "Messages" table is the number person you sent a text to. i.e. A person with Handle ID 78 is the 78th person you sent a text to. Your phone uses this to recognize which contact you are sending a message to or receiving a message from.
handleIds = []
for m in data:
    if len(handleIds) == NUM_CONVERSATIONS:
        break
    elif m[0] in handleIds or m[0] == 0:
        pass
    else:
        handleIds.append(m[0])


# Get Phone Numbers. The ID of a person in the "Handle" table is the phone number of the person you are sending a text to or receiving a text from. The Row ID of a person in the "Handle" table is the same as the Handle ID of a message in the "Messages" table
phoneNumbers = []
for hId in handleIds:
    c.execute(f"SELECT id FROM handle WHERE ROWID={hId};")
    phoneNumbers.append(c.fetchall()[0][0])


# This block of code runs an applescript process that recovers the contact names of the phone numbers extracted from the "Handle" table, then uses those contact names to create Conversation objects that store the names of contacts and the recent messages exchanged with them.
# TIME CONSUMER
# convoStart_time = datetime.now() # For Timing Purposes

conversations = []
for i in range(len(handleIds)):
    convo = Conversation(getName(phoneNumbers[i]), handleIds[i], phoneNumbers[i])
    conversations.append(convo)

# convo_time = datetime.now()-convoStart_time # For Timing Purposes


# Collecting Messages Again. This time we are collecting the text of each messages sent and received as well as who sent the text message ("is_from_me" field) to store them in the Conversation objects.
for convo in conversations:
    c.execute(
        f"SELECT is_from_me, text FROM message WHERE handle_id={convo.handleId} and datetime(message.date/1000000000 + strftime('%s', '2001-01-01') ,'unixepoch','localtime') > '{lastMonth}';"
    )
    data = c.fetchall()
    convo.addMessages(data[-NUM_MESSAGES:])


# To see JSON in Terminal
# for convo in conversations:
#     print()
#     print(convo.json())
#     print()


######################################################################

# tRunTime = datetime.now() - start_time # For Timing Purposes
# print('Total Run Time:', tRunTime) # For Timing Purposes
# print('Conversations Time:', convo_time) # For Timing Purposes
# print(timeToFloat(tRunTime)-timeToFloat(convo_time)) # For Timing Purposes

