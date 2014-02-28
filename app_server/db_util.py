
#!/usr/bin/python

# A python script connecting to a MongoDB given a MongoDB Connection URI.

import sys
import pymongo
import hashlib
import json
import os
import boto.ses

### Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname
client = None

def fetch_api_key():
	file_handler = open('api_key.txt','r')
	return file_handler.readline()
	file_handler.close()

def db_open():
	global client
	MONGODB_URI = 'mongodb://snaptext:gayathri@ds033709.mongolab.com:33709/snaptext'
	client = pymongo.MongoClient(MONGODB_URI)
	db = client.get_default_database()
	return db['users']	

def db_close():
	global client
	client.close()

def check_contact(contacts):
	users = db_open()
	contact_indices = []
	for index , contact  in enumerate(contacts["ContactList"]):
		query = users.find_one({'phone_number' : contact["phoneNumber"]})
		if( query != None):
			print contact['name'], ":" ,query["phone_number"] 
			contact_indices.append(index)
	db_close()
	print "Done Processing all the contact List.. Sending them back to Client.. !!"
	return json.dumps(contact_indices)

def register_device(regid,phone_number):
    users = db_open()
    users.insert({ "regid" : regid , "phone_number" : phone_number })
    db_close()

def fetch_registration_id(phone_number):
	users = db_open()
	isPresent = False
	query = users.find_one({'phone_number' : phone_number })
	if( query != None ):
		isPresent = True
	db_close()

	if(isPresent):
		return query['regid']
	else:
		return None

if __name__ == '__main__':
  contacts = {"ContactList":[{"phoneNumber":"16508617024","name":"gayathri Usa"},{"phoneNumber":"14086674169","name":"Madhu Sjsu"},{"phoneNumber":"14088966069","name":"Madhumati Ef"},{"phoneNumber":"14089871682","name":"Chaithanya Sjsu"},{"phoneNumber":"14083069340","name":"Preethika Pachaiyappa"},{"phoneNumber":"14806190550","name":"Deeps Usa"},{"phoneNumber":"16507455912","name":"Suganya Sivakumar"},{"phoneNumber":"14089871681","name":"Rk Sjsu"},{"phoneNumber":"18018755555","name":"Praveen Kumar Shanmugam"},{"phoneNumber":"12138808918","name":"Divya"},{"phoneNumber":"13122732472","name":"Vivek Kopparthi"},{"phoneNumber":"16508611330","name":"viki usa"}]}
  check_contact(contacts)
  print fetch_registration_id("16508611330")