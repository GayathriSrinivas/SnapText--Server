
from flask import *
import requests
import db_util
import json
import urllib2
import os
import tempfile

app = Flask(__name__)
API_KEY = 'key=AIzaSyAj-OXTDcDJhJBLbc7XNVfkHqQYNMnIn0w'
API_KEY = 'key=AIzaSyB1-K_bzAWP2jvdWhhR63OM6Zbn5k303ns'

@app.route('/contactList',methods = ['POST'])
def contact_list():
	#print "##########",request.data
	temp = json.loads(request.data.decode('cp437'))
	print "????????????",temp
	return db_util.check_contact(temp)

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
	message_type = request.args.get('message_type',None)
	print "sender ::",sender_number,"receiver ::",receiver_number,"message :",message, "type :",message_type
	regid = db_util.fetch_registration_id(receiver_number)
	url = 'https://android.googleapis.com/gcm/send'
	payload = {'registration_ids' : [ regid ] , 'data' : { 'message' : message, 'sender' : sender_number , 'type' : message_type  } }
	headers = {'Content-Type': 'application/json' , 'Authorization' : API_KEY}
	print "-----------------------------------------------------------"
	r = requests.post(url, data = json.dumps(payload), headers = headers)
	print r.text , r.status_code
	print "-----------------------------------------------------------"
	return "MSG RECEIVED BY SERVER"

@app.route('/image',methods = ['POST'])
def image():
	tup = tempfile.mkstemp(suffix=".jpg",prefix="image_",dir="/var/www/snaptext_images")
	f = os.fdopen(tup[0], "w")
	print "Asoulte filname :: ",tup[1]
	link = "http://snaptext.foamsnet.com/snaptext_images/%s" % os.path.basename(tup[1])
	print link
	f.write(request.data)
	f.close()
	os.system("chmod a+r %s" % tup[1])
	return json.dumps({"fileName" : link })

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0')
