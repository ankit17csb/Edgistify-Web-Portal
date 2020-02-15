from typing import Optional,Callable, Any,List
import datetime
import mongoengine
import bson


class Owner(mongoengine.Document):
    registered_date = mongoengine.DateTimeField(default=datetime.datetime.now)
    name = mongoengine.StringField(required=True)
    email = mongoengine.StringField(required=True)
    password = mongoengine.StringField(required=True)
    post = mongoengine.ListField()
 

    meta = {
        'db_alias': 'chor',
        'collection': 'owners'
    }





def create_account(name, email, posts) -> Owner:
    owner = Owner()
    owner.name = name
    owner.email = email
    owner.post = posts
    owner.save()
    return owner

def create_account_by_flask(email, name, password) -> Owner:  
       
    owner = Owner()
    owner.name = name
    owner.email = email
    owner.password = password
   

    owner.save()
    return owner


def deletePost(e_id, pub):
    Owner.objects(email = e_id).update_one(pull__post=pub)


    

def addPost(e_id, pub):
    Owner.objects(email = e_id).update_one(push__post=pub)




def find_account_by_fid_and_password(facultyid: str, password: str) -> Owner:
    owner = Owner.objects(email=facultyid, password = password).first()
    return owner


def find_account_by_fid(email: str) -> Owner:
    owner = Owner.objects(email=email).first()
    return owner







