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


######################################################################
################################ Constants ###########################



NUM_CONVERSATIONS = 3
NUM_MESSAGES = 5



######################################################################







######################################################################
############################## Objects ###############################
class Conversation():
	def __init__(self, contact, handleId):
		self.contact = contact
		self.handleId = handleId
		self.messages = []

	def __repr__(self):
		return self.contact

	def __str__(self):
		printStr = f'{self.contact}'
		for m in self.messages:
			if m[0] == 1:
				person = 'Me:   '
			else:
				person = f'{self.contact}:   '
			printStr = printStr + f'\n\t{person}{m[1]}'

		return printStr


	def addMessages(self, messages):
		messages.reverse()
		self.messages = messages




######################################################################
############################# Functions ##############################



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



######################################################################



######################################################################
############################### Script ###############################



conn = connectToDatabase()
c = conn.cursor()


today = str(datetime.today()).split()[0].split('-')
lastMonth = f'{today[0]}-0{str(int(today[1])-1)}-{today[2]}'
c.execute(f"SELECT handle_id, is_from_me FROM message WHERE datetime(message.date/1000000000 + strftime('%s', '2001-01-01') ,'unixepoch','localtime') > {lastMonth};")
data = c.fetchall()
data.reverse()



handleIds = []
for m in data:
	if len(handleIds) == NUM_CONVERSATIONS:
		break
	if m[0] in handleIds:
		pass
	else:
		handleIds.append(m[0])



rowIds = []
for hId in handleIds:
	c.execute(f"SELECT id FROM handle WHERE ROWID={hId};")
	rowIds.append(c.fetchall()[0][0])



conversations = []
for i in range(len(handleIds)):
	convo = Conversation(getName(rowIds[i]), handleIds[i])
	conversations.append(convo)



for convo in conversations:
	c.execute(f"SELECT is_from_me, text FROM message WHERE handle_id={convo.handleId};")
	data = c.fetchall()
	data.reverse()
	convo.addMessages(data[0:NUM_MESSAGES])



for convo in conversations:
	print(convo)
	print('\n\n')



######################################################################





















