from flask import Flask, redirect ,url_for, request ,render_template, session
import psycopg2
import fun 
import psycopg2
from flask import Flask, redirect, url_for, request,Flask, render_template, request, flash
from adminForms import adminWorks,hodTable,crossCuttingTable,facultyTable,leaveHTable
import psycopg2
from config import config
import helper as st
import mongoengine
from flask_pymongo import PyMongo

fun.initialize()

app = Flask(__name__)
app.secret_key = 'super secret key'

def global_init():
    mongoengine.register_connection(alias='chor',name='portal')

@app.route('/')
def welcome():
        return render_template('welcome.html')

@app.route('/direct_to_register_f')
def direct_to_register_f():
    return render_template('register_f.html')

@app.route('/direct_to_login_f')
def direct_to_login_f():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('welcome'))

@app.route('/reCommentCheck')
def reCommentCheck():
    user = session.get('user')
    if(leaves.can_apply(user)==0):
        l_id=leaves.reCommentCheck(user)
        if(l_id != -1):
            return redirect(url_for('reCommentFinal',l_id=l_id))

        else:
            return redirect(url_for('profile'))
            #no such  leave where to recomment
    else:
        return redirect(url_for('profile'))
        #no pending leaves



@app.route('/reCommentFinal/<l_id>', methods = [ 'GET' , 'POST' ])
def reCommentFinal(l_id):
    user = session.get('user')
    if request.method == 'POST':
        commnt = request.form["reCmnt"]
        leaves.reComment(user,l_id,commnt)
        return redirect(url_for('profile')) #add msg
    return render_template('reComment.html',lid=l_id)

@app.route('/profile/comment_on_leaves',methods=['GET','POST'])
def comment_on_leaves():
    if request.method == 'POST':
        user=session.get('user')
        lid=request.form['lid']
        ct=request.form['ctext']
        resp=request.form['response']
        flag=leaves.can_comment(user,lid)
        if flag ==0:
            return  redirect(url_for('profile'))
        else:
            leaves.add_comment(user,lid,ct,resp)
            return redirect(url_for('profile'))
    return render_template('comment_on_leaves.html')

@app.route('/profile/apply_for_leaves',methods = [ 'GET' , 'POST' ])
def apply_for_leaves():
    if request.method == 'POST' :
        user=session.get('user')
        flag=leaves.can_apply(user)
        if flag == 1:
            sd=request.form['sdate']
            ed=request.form['edate']
            ct=request.form['comment']
            leaves.apply(user,sd,ed,ct)
        return redirect(url_for('profile'))
        
    return render_template('apply_for_leaves.html')

@app.route('/profile')
def profile():
    user = session.get('user')
    #print(user+"\\\\\\\\\\\\\\\\\\\\\\\\")
    if user:
        emp = fun.fetch_employee(user)
        return render_template('profile.html', emp1 =emp )
    return redirect(url_for('login'))



@app.route('/update_profile')
def update_profile():
    return render_template('update_profile.html' )

@app.route('/view_profile')
def view_profile():
    eid = session.get('user')
    
    #users = mongo.db.users
    login_user = st.find_account_by_fid(eid)
   
    name = login_user.name
    pubs = login_user.post
    pub_size = len(pubs)
  
    #info = st.getInfo(id)
    return render_template('view_profile.html' , eid = eid ,name=name , pubs=pubs , pub_size=pub_size)

@app.route('/show_comment' , methods = ['GET', 'POST'])
def show_comment():
    user = session.get('user')
    login_user = st.find_account_by_fid(user)
    
    if request.method == 'POST':
        post_no = request.form['post_no']
        if post_no != "":
            post_id = post_no
            
            All_comments = fun.fetch_comments(post_id)
            
            return render_template('show_comment.html' ,All_comments=All_comments)
    return redirect('all_post') 

@app.route('/all_post')
def all_post():
    record = fun.get_employee_list()
    record_size = len(record)
    All_post = []
    record1 = ["dddd@gmail.com", "eeee@gmail.com"] 
    record_size1 = len(record1)
    record2 = fun.get_post_list()
    record2_size = len(record2)
    return render_template('all_post.html' ,All_post=record2 , post_size=record2_size)

    '''for i in range(record_size1):
        e_id = record1[i]
        login_user = st.find_account_by_fid(e_id)
        pubs = login_user.post
        pub_size = len(pubs)
        All_post.append(pubs)

    
    post_size = len(All_post)
    return render_template('all_post.html' ,All_post=All_post , post_size=post_size)
     '''
    
@app.route('/edit_publication', methods = ['GET', 'POST'])
def edit_publication():
    user = session.get('user')
    login_user = st.find_account_by_fid(user)

    if request.method == 'POST':
        pub = request.form['post']
        if pub != "":
            st.addPost(user, str(pub))
            n = fun.total_post()
            r = int(n)+1
            e_id = login_user.email
            fun.insert_post(r,pub,e_id)
            return redirect(url_for('update_profile'))
        else:
            return redirect(url_for('update_profile'))


    else:
        return 'please give the imformation' 


@app.route('/edit_comment', methods = ['GET', 'POST'])
def edit_comment():
    user = session.get('user')
    login_user = st.find_account_by_fid(user)

    if request.method == 'POST':
        post_no = request.form['post_no']
        comment = request.form['comment']
        if comment != "":
            n = fun.total_comment()
            post_id = int(post_no)
            r = int(n)+1
            e_id = login_user.email
            fun.insert_Edgistify_comment(r,comment,e_id,post_id)
            return redirect(url_for('all_post'))
    return redirect(url_for('all_post'))

@app.route('/delete_publication', methods = ['GET', 'POST'])
def delete_publication():
    user = session.get('user')
    login_user = st.find_account_by_fid(user)
    if request.method == 'POST':
        pub_no = request.form['publication']
        pub_no = int(pub_no)
        pub1 = login_user.publication
        if pub_no-1 < len(pub1):
            pub = pub1[pub_no-1]
            st.deletePublication(user, str(pub))
            return redirect(url_for('update_profile'))
        else:
            return redirect(url_for('update_profile'))



    else:
        return 'please give the imformation'




@app.route('/profile/leaves_to_comment')
def leaves_to_comment():
    user=session.get('user')
    l=leaves.get_leaves_to_comment(user)
    return render_template('leaves_to_comment.html',l=l)


@app.route('/login', methods = [ 'GET' , 'POST' ])
def login():
    error=""
    if request.method == 'POST':
        fid = request.form["fid"]
        password = request.form["password"]
        l = fun.verify_credentials(fid,password)
        if l == 0 :
            error="invalid username or password"
        else:
            session['user'] = fid
            return redirect(url_for('profile'))
    return render_template('login.html', error=error)

@app.route('/register', methods = [ 'GET' , 'POST' ])
def register_f():
    if request.method == 'POST':
        email = request.form["email"]
        name = request.form["name"]
        password = request.form["password"]
        st.create_account_by_flask(email,name, password)
        fun.insert_faculty(email,password,name)
        return redirect(url_for('welcome'))        
    return redirect(url_for('welcome'))


@app.route('/checkLeaveH',methods = ['GET', 'POST'])
def checkLeaveH():
    form1 = leaveHTable()
    if request.method == 'POST':
        if form1.validate() == False:
            flash('All fields are required.')
            return render_template('leaveH.html', form = form1)
                    
        else:
            strName = request.form["child"]
            strCount = request.form["parent"]
            strfr = request.form["forWhom"]
            global var
            conn = None
            try:
                params = config()
                print('Connecting to the PostgreSQL database...')
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                if(var==1):
                    sql = "INSERT INTO leave_hierarchy(child,parent,for_whom) VALUES(%s,%s,%s)"
                    cur.execute(sql,(strName,strCount,strfr))
                elif(var==2):
                    sql = "update leave_hierarchy set for_whom = %s where child = %s and parent = %s"
                    cur.execute(sql,(strfr,strName,strCount))
                elif(var==3):
                    cur.execute("DELETE FROM leave_hierarchy WHERE for_whom = %s", (strfr,))
                    

                else:
                    return "render_template('failed.html')  "
                rows_changed = cur.rowcount
                conn.commit()
                cur.close()
                var=0
                if(rows_changed != 0):
                    return render_template('success.html')
                else:
                    return ("No row changed/inserted/deleted, please reload admin page")

            except (Exception, psycopg2.DatabaseError) as error:
                #return "render_template('failed.html') d"
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
            return "render_template('failed.html') d"
            

    elif request.method == 'GET':
        return render_template('leaveH.html', form = form1)



@app.route('/checkFaculty',methods = ['GET', 'POST'])
def checkFaculty():
    form1 = facultyTable()
    if request.method == 'POST':
        if form1.validate() == False:
            flash('All fields are required.')
            return render_template('facultyTable.html', form = form1)
                    
        else:
            strName = request.form["username"]
            strCount = request.form["dept"]
            global var
            conn = None
            try:
                params = config()
                print('Connecting to the PostgreSQL database...')
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                if(var==1):
                    sql = "INSERT INTO faculty(eid,department) VALUES(%s,%s)"
                    cur.execute(sql,(strName,strCount))
                elif(var==2):
                    sql = "update faculty set department = %s where eid = %s"
                    cur.execute(sql,(strCount,strName))
                elif(var==3):
                    cur.execute("DELETE FROM faculty WHERE eid = %s", (strName,))
                    

                else:
                    return "render_template('failed.html')  "
                rows_changed = cur.rowcount
                conn.commit()
                cur.close()
                var=0
                if(rows_changed != 0):
                    return render_template('success.html')
                else:
                    return ("No row changed/inserted/deleted, please reload admin page")

            except (Exception, psycopg2.DatabaseError) as error:
                #return "render_template('failed.html') d"
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
            return "render_template('failed.html') d"
            

    elif request.method == 'GET':
        return render_template('facultyTable.html', form = form1)



@app.route('/checkCC',methods = ['GET', 'POST'])
def checkCC():
    form1 = crossCuttingTable()
    if request.method == 'POST':
        if form1.validate() == False:
            flash('All fields are required.')
            return render_template('crossCuttingTable.html', form = form1)
                    
        else:
            strName = request.form["username"]
            strCount = request.form["desgn"]
            global var
            conn = None
            try:
                params = config()
                print('Connecting to the PostgreSQL database...')
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                if(var==1):
                    sql = "INSERT INTO cross_cutting(eid,designation) VALUES(%s,%s)"
                    cur.execute(sql,(strName,strCount))
                elif(var==2):
                    sql = "update cross_cutting set eid = %s where designation = %s"
                    cur.execute(sql,(strName,strCount))
                elif(var==3):
                    cur.execute("DELETE FROM cross_cutting WHERE eid = %s", (strName,))
                    

                else:
                    return "render_template('failed.html')  "
                rows_changed = cur.rowcount
                conn.commit()
                cur.close()
                var=0
                if(rows_changed != 0):
                    return render_template('success.html')
                else:
                    return ("No row changed/inserted/deleted, please reload admin page")

            except (Exception, psycopg2.DatabaseError) as error:
                #return "render_template('failed.html') d"
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
            return "render_template('failed.html') d"
            

    elif request.method == 'GET':
        return render_template('crossCuttingTable.html', form = form1)


@app.route('/checkHod',methods = ['GET', 'POST'])
def checkHod():
    form1 = hodTable()
    if request.method == 'POST':
        if form1.validate() == False:
            flash('All fields are required.')
            return render_template('hodTable.html', form = form1)
                    
        else:
            strName = request.form["username"]
            strCount = request.form["dept"]
            global var
            conn = None
            try:
                params = config()
                print('Connecting to the PostgreSQL database...')
                conn = psycopg2.connect(**params)
                cur = conn.cursor()
                if(var==1):
                    sql = "INSERT INTO hod(eid,department) VALUES(%s,%s)"
                    cur.execute(sql,(strName,strCount))
                elif(var==2):
                    sql = "update hod set eid = %s where department = %s"
                    cur.execute(sql,(strName,strCount))
                elif(var==3):
                    cur.execute("DELETE FROM hod WHERE eid = %s", (strName,))
                    

                else:
                    return "render_template('failed.html')  "
                rows_changed = cur.rowcount
                conn.commit()
                cur.close()
                var=0
                if(rows_changed != 0):
                    return render_template('success.html')
                else:
                    return ("No row changed/inserted/deleted, please reload admin page")

            except (Exception, psycopg2.DatabaseError) as error:
                #return "render_template('failed.html') d"
                print(error)
            finally:
                if conn is not None:
                    conn.close()
                    print('Database connection closed.')
            return "render_template('failed.html') d"
            

    elif request.method == 'GET':
        return render_template('hodTable.html', form = form1)




@app.route('/admin',methods = ['GET', 'POST'])
def admin():
    form = adminWorks()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('adminHome.html', form = form)
        
        else:
            str1 = request.form["Opt"]
            str2 = request.form["Table"]
            global var
            
            if(str2=='fac' ):
                if(str1=='I'):
                    var=1
                elif(str1=='U'):
                    var=2
                elif(str1=='D'):
                    var=3
                return redirect(url_for('checkFaculty'))

            elif(str2=='hod' ):
                if(str1=='I'):
                    var=1
                elif(str1=='U'):
                    var=2
                elif(str1=='D'):
                    var=3
                return redirect(url_for('checkHod'))
                
            elif(str2=='crossC' ):
                if(str1=='I'):
                    var=1
                elif(str1=='U'):
                    var=2
                elif(str1=='D'):
                    var=3
                return redirect(url_for('checkCC'))

            elif(str2=='leaveH' ):
                if(str1=='I'):
                    var=1
                elif(str1=='U'):
                    var=2
                elif(str1=='D'):
                    var=3
                return redirect(url_for('checkLeaveH'))

            else:
                return "render_template('failed.html') dsa"
            

         
    elif request.method == 'GET':
         return render_template('adminHome.html', form = form)

if __name__ == '__main__':
    global_init()




    
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug = True )

    var= -1