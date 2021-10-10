from flask import Flask,request,jsonify
import firebase_admin
from firebase_admin import db
from flask_cors import CORS
import string
import random
from datetime import datetime
import pytz

IST = pytz.timezone('Asia/Kolkata')
app= Flask(__name__)
CORS(app)
cred_object = firebase_admin.credentials.Certificate('/home/universalclass/universalclass-182de-firebase-adminsdk-3anjr-3cd620da5e.json')
default_app = firebase_admin.initialize_app(cred_object, {
        'databaseURL': 'https://universalclass-182de-default-rtdb.firebaseio.com/'
        })

@app.route('/add_data',methods=['POST'])
def add_data():
    data=request.get_json()
    id=data['id']
    university=data['university']
    occ = data['account_type']
    pref = data['interest']
    name= data['name']

    ref = db.reference("/USER")
    data={
        'id':id,
        'name':name,
        'university':university,
        'account_type':occ,
        'interest':pref,

    }
    ref.push().set(data)
    print(data)
    return jsonify('Done')

@app.route('/add_meet',methods=['POST'])
def add_meet():
    data=request.get_json()

    user_data =db.reference('USER').order_by_child('id').equal_to(data['id']).get()
    user_data=dict(user_data)
    user_data=user_data[list(user_data.keys())[0]]

    N=5
    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k = N))
    if user_data['account_type']=='teacher':
        data_to_push={
            'id':data['id'],
            'class_name':data['class_name'],
            'label':data['label'],
            'university':user_data['university'],
            'link':data['link'],
            'start_time':data['start_time'],
            'end_time':data['end_time'],
            'date':data['date'],
            'teacher_name':user_data['name'],
            'meeting_id': res,
        }
        ref = db.reference("/MEETIINGS")
        ref.push().set(data_to_push)
        return {'status':'200 success','data':data_to_push}

    else:
        return {'error':'Not a Teacher Exception'}

@app.route('/get_data',methods=['POST'])
def get_data():
    data= request.get_json()
    if data['id']!=None:
        user_data =db.reference('USER').order_by_child('id').equal_to(data['id']).get()
        user_data=dict(user_data)
        user_data=user_data[list(user_data.keys())[0]]
        to_be_sent=[]
        for interest in user_data['interest']:
            meetings_data=db.reference('MEETIINGS').order_by_child('label').equal_to(interest).get()
            meetings_data=dict(meetings_data)
            for key in meetings_data.keys():
                d= meetings_data[key]
                fin_time = datetime.strptime(d['date']+' '+d['end_time'], "%Y-%m-%d %H:%M" )
                cur_time=datetime.strptime(datetime.now(IST).strftime('%Y-%m-%d %H:%M'),"%Y-%m-%d %H:%M")
                if fin_time > cur_time :
                    to_be_sent.append(d)
                else:
                    refer=db.reference('MEETIINGS')
                    refer.child(key).set({})
        return jsonify(to_be_sent)
    else:
        to_be_sent=[]
        meetings_data=db.reference('MEETIINGS').order_by_child('label').get()
        meetings_data=dict(meetings_data)
        for key in meetings_data.keys():
                d= meetings_data[key]

                fin_time = datetime.strptime(f"{d['date']} {d['end_time']}", "%Y-%m-%d %H:%M" )

                if fin_time > datetime.now():
                    to_be_sent.append(d)
                else:
                    refer=db.reference('MEETIINGS')
                    refer.child(key).set({})
        return jsonify(to_be_sent)


if __name__=='__main__':
    app.run(debug=True)