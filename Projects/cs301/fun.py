import psycopg2
from psycopg2 import Error
from datetime import datetime


con = psycopg2.connect(
        user = "postgres",
        password = "postgres",
        host = "127.0.0.1",
        database ="db"
        )

cur = con.cursor()

def initialize():

    cur.execute(''' CREATE TABLE IF NOT EXISTS employee
    (eid text not null ,
     password text not null ,
     name text not null
     );''')

    cur.execute(''' CREATE TABLE IF NOT EXISTS Edgistify_comment
    (comment_id INT not null ,
     comment text not null ,
     written_id text not null,
     post_id text not null
     );''')

    cur.execute(''' CREATE TABLE IF NOT EXISTS Post
    (post_id INT not null ,
     post text not null ,
     owner_id text not null
     );''')



    cur.execute(''' CREATE TABLE IF NOT EXISTS cross_cutting
    (eid text not null ,
     designation text not null 
     );''')

    print('Tables created..........................................')

    con.commit()

def insert_faculty(eid,password,name):
    cur.execute('''insert into employee (eid,password,name) values (%s,%s,%s)''',(eid,password,name))
    #cur.execute('''insert into faculty (eid,department) values (%s,%s)''',(eid,department))
    con.commit()
    return None

def insert_Edgistify_comment(comment_id,comment, written_id, post_id):
    cur.execute('''insert into Edgistify_comment (comment_id,comment, written_id, post_id) values (%s,%s,%s,%s)''',(comment_id,comment, written_id,post_id))
    #cur.execute('''insert into faculty (eid,department) values (%s,%s)''',(eid,department))
    con.commit()
    return None

def insert_post(post_id,post, owner_id):
    cur.execute('''insert into Post (post_id,post, owner_id) values (%s,%s,%s)''',(post_id,post, owner_id))
    #cur.execute('''insert into faculty (eid,department) values (%s,%s)''',(eid,department))
    con.commit()
    return None

def verify_credentials(id,passw):
    cur.execute('''select count(*) from employee where eid = %s and password = %s  ;  ''',(id,passw))
    
    n = cur.fetchone()
    if n[0] == 1 :
        return 1
    else:
        return 0

def fetch_employee(id):
    cur.execute('''select * from employee where eid= %s ;''',(id,))
    n = cur.fetchone()
    d =dict()
    d['Employee id'] =n[0]
    d['Name']=n[2]
    return d

def fetch_comments(post_id):
    cur.execute('''select comment from Edgistify_comment where post_id= %s ;''',(post_id))
    n = cur.fetchall()
    return n

def get_employee_list():
    cur.execute('''select eid from employee ;''')
    n = cur.fetchall()
    return n[0]

def get_post_list():
    cur.execute('''select post from Post ;''')
    n = cur.fetchall()
    return n

def total_comment():
    cur.execute('''select count(*) from Edgistify_comment;''')
    n = cur.fetchone()
    return n[0]


def total_post():
    cur.execute('''select count(*) from Post;''')
    n = cur.fetchone()
    return n[0]

#def insert_hod(eid,password,name,department,doj,):
    #cur.execute('''insert into hod (fid,password,name,department) values(%s,%s,%s,%s)''' ,(fid,password,name,department))
   # con.commit()

#def insert_cross_cutting(eid,name,passw ord,):
     #cur.execute('''insert into cross_cutting(fid,password,name,designation) values(%s,%s,%s,%s)''' ,(fid,password,name,designation))
     #con.commit()

