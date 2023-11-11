from mongoengine import *


connect(db="hw", host="mongodb://localhost:27017")


class Contact(Document):
    name = StringField(required=True)
    email = StringField(required=True)
    send_email = BooleanField(default=False)