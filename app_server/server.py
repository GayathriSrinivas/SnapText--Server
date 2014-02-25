
from flask import *
import requests
import db_util
import json
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

@app.route('/send_msg_to_server')
def send_msg_to_server():
	message = request.args.get('message',None)
	phone_number = request.args.get('phone_number',None) 
	print phone_number, message, API_KEXY
	regid = db_util.fetch_registration_id(phone_number)
	url = 'https://android.googleapis.com/gcm/send'
	payload = {'registration_ids' : [ regid ] , 'data' : { 'message' : message } }
	headers = {'Content-Type': 'application/json' , 'Authorization' : API_KEY}
	print "-----------------------------------------------------------"
	r = requests.post(url, data = json.dumps(payload), headers = headers)
	print r.text , r.status_code
	print "-----------------------------------------------------------"
	return "MSG RECEIVED BY SERVER"

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
