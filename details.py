import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


cred = credentials.Certificate('tagspotter-372a2-firebase-adminsdk-afop7-b3b61ba449.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tagspotter-372a2-default-rtdb.firebaseio.com/'
})

ref = db.reference('/details')

for x in range(1):
    name = input("Enter name: ")
    phone = input("Enter phone number: ")
    nospace_text = input("Enter car number plate: ")
    gmail = input("Enter gmail: ")

    data = {
        'name': name,
        'phone_no': phone,
        'number': nospace_text,
        'email': gmail
    }

    new_record_ref = ref.push(data)
    print(f"Stored with ID: {new_record_ref.key}")
