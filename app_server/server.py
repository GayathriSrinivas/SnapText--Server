
from flask import *
import requests
import db_util
import json
import urllib2
app = Flask(__name__)
API_KEY = 'key=AIzaSyAj-OXTDcDJhJBLbc7XNVfkHqQYNMnIn0w'


@app.route('/contactList',methods = ['POST'])
def contact_list():
	return db_util.check_contact(request.json)

@app.route('/registration')
def registration():
	regid = request.args.get('regid',None)
	phone_number = request.args.get('phoneNo',None)
	db_util.register_device(regid,phone_number)
	return "Hello"

@app.route('/send_message')
def send_msg_to_server():
	message = urllib2.unquote(request.args.get('message',None))
	sender_number = request.args.get('sender_number',None) 
	receiver_number = request.args.get('receiver_number',None) 
	print "sender ::",sender_number,"receiver ::",receiver_number,"message :",message, API_KEY
	regid = db_util.fetch_registration_id(receiver_number)
	url = 'https://android.googleapis.com/gcm/send'
	payload = {'registration_ids' : [ regid ] , 'data' : { 'message' : message, 'sender' : sender_number } }
	headers = {'Content-Type': 'application/json' , 'Authorization' : API_KEY}
	print "-----------------------------------------------------------"
	r = requests.post(url, data = json.dumps(payload), headers = headers)
	print r.text , r.status_code
	print "-----------------------------------------------------------"
	return "MSG RECEIVED BY SERVER"

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
