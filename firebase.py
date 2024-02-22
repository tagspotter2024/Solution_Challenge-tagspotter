import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

from datetime import datetime


cred = credentials.Certificate('tagspotter-372a2-firebase-adminsdk-afop7-b3b61ba449.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tagspotter-372a2-default-rtdb.firebaseio.com/'
})




def firebase_store(nospace_text, current_datetime,gmailid):
    ref = db.reference('/numberplates')
    current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
    data = {
        'number': nospace_text,
        'date_time': current_datetime_str,
        'gmail':gmailid
    }
    new_record_ref = ref.push(data)
    print(f"Stored with ID: {new_record_ref.key}")


def firebase_find(nospace_text):
    ref = db.reference('/details')
    query = ref.order_by_child("number").equal_to(nospace_text)
    result = query.get()


    gmail_address = ""

    for key, value in result.items():
        
        date_time_value = value.get("email", "")  
        username, domain = date_time_value.split("@") if "@" in date_time_value else ("", "")

        gmail_address = f'{username}@{domain}'
    
    print(gmail_address)
    return gmail_address