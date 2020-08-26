# For Writing and Testing Functions


import sqlite3
from subprocess import *
from datetime import *
import sqlite3
import re
import os
import sys





def connectToDatabase():
	output = Popen(f"whoami", shell=True, stdout=PIPE).stdout
	IAm = output.read().decode("utf-8").strip()

	# Relevant tables are "handle" and "message"
	conn = sqlite3.connect(f'/Users/{IAm}/Library/Messages/chat.db')
	return conn

def getName(id):
	tell = f'tell application "Messages"'
	myTry = f'try'
	get = f'get full name of every buddy where handle is "{id}"'
	onErr = f'on error errStr'
	ifErr = f'errStr'
	endTry = f'end try'
	endTell = f'end tell'

	appleScript = f'{tell}\n{myTry}\n{get}\n{onErr}\n{ifErr}\n{endTry}\n{endTell}'

	output = Popen(f"osascript -e '{appleScript}'", shell=True, stdout=PIPE).stdout
	buddy = output.read().decode("utf-8").strip().split(',')[0]

	return buddy







today = str(datetime.today()).split()[0].split('-')
lastMonth = f'{today[0]}-0{str(int(today[1])-1)}-{today[2]}'

conn = connectToDatabase()
c = conn.cursor()


today = str(datetime.today()).split()[0].split('-')
lastMonth = f'{today[0]}-0{str(int(today[1])-1)}-{today[2]}'
c.execute(f"SELECT handle_id, is_from_me FROM message WHERE datetime(message.date/1000000000 + strftime('%s', '2001-01-01') ,'unixepoch','localtime') > {lastMonth};")
data = c.fetchall()


data.reverse()
handleIds = []
for m in data:
	if m[0] in handleIds:
		pass
	else:
		handleIds.append(m[0])


rowIds = []
for hId in handleIds[0:3]:
	c.execute(f"SELECT id FROM handle WHERE ROWID={hId};")
	rowIds.append(c.fetchall()[0][0])



contacts = []
for rId in rowIds:
	contacts.append(getName(rId))


print(contacts)