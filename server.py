
from flask import *
import requests
import db_util
app = Flask(__name__)


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
	print phone_number, message
	regid = db_util.fetch_registration_id(phone_number)
	url = "https://android.googleapis.com/gcm/send"

	return "MSG RECEIVED BY SERVER", regid



if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
