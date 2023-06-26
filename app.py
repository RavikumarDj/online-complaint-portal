from flask import Flask,redirect,url_for,render_template,request,flash,abort,session,send_from_directory
from flask_session import Session
from key import secret_key,salt1,salt2
from stoken import token
from cmail import sendmail
from itsdangerous import URLSafeTimedSerializer
import mysql.connector
from otp import genotp
from io import BytesIO
import os
app=Flask(__name__)
app.secret_key=secret_key
app.config['SESSION_TYPE']='filesystem'
Session(app)
mydb=mysql.connector.connect(host='localhost',user='root',password='Sanvi',db='online')
'''app.config['SESSION_TYPE'] = 'filesystem'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Sanvi'
app.config['MYSQL_DB'] = 'online'
Session(app)
mysql = MySQL(app)
@app.route('/',methods=['GET','POST'])
def home():
     if request.method=="POST":
        name=request.form['name']
        emailid=request.form['emailid']
        message=request.form['message']
        cursor=mysql.connection.cursor()
        cursor.execute('insert into contactus(name,emailid,message) values(%s,%s,%s)',[name,emailid,message])
        mysql.connection.commit()
     return render_template('home.html')
#----------------------------admin login---------------------------------------
@app.route('/adminsignin', methods = ['GET','POST'])
def aregister():
    if session.get('admin'):
        return redirect(url_for('admindashboard'))
    if request.method == 'POST':
        adminid= request.form['adminid']
        phonenumber= request.form['phonenumber']
        email = request.form['email']
        password= request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute ('select adminid from admin')
        data = cursor.fetchall()
        cursor.execute ('select email from admin')
        edata = cursor.fetchall()
        if (adminid,)in data:
            flash('user already exits')
            return render_template('admin.html')
        if (email,)in edata:
            flash('email already exits')                                                                                                                                                                                                                                                                                                                                                                                                                                                         
            return render_template('admin.html')
        cursor.close()
        subject='Email Confirmation'
        confirm_link=url_for('confirm',token=token(email,salt1),_external=True)
        body=f"Thanks for signing up.Follow this link-\n\n{confirm_link}"
        sendmail(to=email,body=body,subject=subject)
        flash('Confirmation link sent check your email')
    return render_template('admin.html')
@app.route('/alogin',methods=['GET','POST'])#after register login with rollno and password route
def alogin():
    if session.get('admin'):
        return redirect(url_for('admindashboard'))
    if request.method=='POST':
        adminid=request.form['adminid']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from admin where adminid=%s and password=%s',[adminid,password])#if the count is 0 then either username or password is wrong or if it is 1 then it is login successfully
        count=cursor.fetchall()[0]
        if count==0:
            flash('Invalid username or password')
            return render_template('alogin.html')
        else:
            session['admin']=adminid
            return redirect(url_for('admindashboard'))
    return render_template('alogin.html')

@app.route('/alogout')
def alogout():
    if session.get('admin'):
        session.pop('admin')
        return redirect(url_for('alogin'))
    else:
        flash('u are already logged out!')
        return redirect(url_for('alogin'))
        #return redirect(url_for('loginp'))

@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        email=serializer.loads(token,salt=salt1,max_age=120)
    except Exception as e:
        #print(e)
        flash('Link expired')
        return render_template('sorry.html')
    else:
        cursor=mysql.connection.cursor()
        cursor.execute('select emailstatus from user where email=%s',[email])
        status=cursor.fetchone()[0]
        print(status)
        cursor.close()
        if status=='confirmed':
            flash('Email already confirmed')
            return redirect(url_for('alogin'))
        else:
            cursor=mysql.connection.cursor()
            cursor.execute("update user set emailstatus='confirmed' where email=%s",[email])
            mysql.connection.commit()
            flash('Email confirmation success')
            return redirect(url_for('alogin'))

@app.route('/aotp/<otp>/<adminid>/<email>/<phonenumber>/<password>',methods = ['GET','POST'])
def aotp(otp,adminid,email,phonenumber,password):
    if request.method == 'POST':
        uotp=request.form['otp']
        if otp == uotp:
            cursor = mysql.connection.cursor()
            cursor.execute('insert into admin values(%s,%s,%s,%s)',(adminid,email,phonenumber,password))
            mysql.connection.commit()
            cursor.close()
            flash('Details Registered')#send mail to the user as successful registration
            return redirect(url_for('alogin'))
        else:
            flash('wrong otp')
            return render_template('otp.html',otp = otp,adminid=adminid,email=email,password= password,phonenumber=phonenumber)'''
#------------------------------------user login---------------------------
'''@app.route('/signin', methods = ['GET','POST'])
def register():
    if session.get('user'):
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password= request.form['password']
        phno= request.form['phno']
        state=request.form['state']
        address=request.form['address']
        pincode=request.form['pincode']
        cursor=mysql.connection.cursor()
        cursor.execute ('select username from user')
        data = cursor.fetchall()
        cursor.execute ('select email from user')
        edata = cursor.fetchall()
        if (username,)in data:
            flash('user already exits')
            return render_template('usersignin.html')
        if (email,)in edata:
            flash('email already exits')                                                                                                                                                                                                                                                                                                                                                                                                                                                         
            return render_template('usersignin.html')
        cursor.close()
        subject = 'Email Confirmation'
        confirm_link = url_for('confirm', token=token(email, salt1), _external=True)
        body = f"Thanks for signing up. Follow this link-\n\n{confirm_link}"
        sendmail(to=email, body=body, subject=subject)

        flash('Confirmation link sent. Check your email')

    return render_template('usersignin.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('home'))
    if request.method=='POST':
        username=request.form['name']
        password=request.form['password']
        cursor=mysql.connection.cursor()
        cursor.execute('select count(*) from user where username=%s and password=%s',[username,password])
        count=cursor.fetchone()[0]
        if count==0:
            flash('invalid user name or password')
            return render_template('userlogin.html')
        else:
            session['user']=username
            return redirect(url_for('home'))
    return render_template('userlogin.html')

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('login'))
    else:
        flash('u are already logged out!')
        return redirect(url_for('login'))
        #return redirect(url_for('loginp'))
        
@app.route('/otp/<otp>/<username>/<email>/<password>/<phno>/<state>/<address>/<pincode>',methods = ['GET','POST'])
def otp(otp,username,email,password,phno,state,address,pincode):
    if request.method == 'POST':
        uotp=request.form['otp']
        if otp == uotp:
            cursor = mysql.connection.cursor()
            cursor.execute('insert into user values(%s,%s,%s,%s,%s,%s,%s)',(username,email,password,phno,state,address,pincode))
            mysql.connection.commit()
            cursor.close()
            flash('Details Registered')#send mail to the user as successful registration
           
            return redirect(url_for('login'))
        else:
            flash('wrong otp')
            return render_template('otp1.html',otp = otp,name = name,email=email,password= password,phno=phno,state=state,address=address,pincode=pincode)
@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        email=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mysql.connection.cursor(buffered=True)
                cursor.execute('update users set password=%s where email=%s',[newpassword,email])
                mysql.connection.commit()
                flash('Reset Successful')
                return redirect(url_for('login'))
            else:
                flash('Passwords mismatched')'''

@app.route('/',methods=['GET','POST'])
def home():
     if request.method=="POST":
        name=request.form['name']
        emailid=request.form['emailid']
        message=request.form['message']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into contactus(name,emailid,message) values(%s,%s,%s)',[name,emailid,message])
        mydb.commit()
     return render_template('home.html')

@app.route('/adminsignin', methods = ['GET','POST'])
def aregister():
    if session.get('admin'):
        return redirect(url_for('admindashboard'))
    if request.method == 'POST':
        adminid= request.form['adminid']
        email = request.form['email']
        phonenumber= request.form['phonenumber']
        password= request.form['password']
        cursor=mydb.cursor(buffered=True)
        '''try:
            cursor.execute('insert into admin (adminid,phonenumber,email,password) values(%s,%s,%s,%s)',(adminid,phonenumber,email,password))
        except mysql.connector.IntegrityError:
            flash('Username or email is already in use')
            return render_template('admin.html')
        else:
            mydb.commit()
            cursor.close()
            subject='Email Confirmation'
            confirm_link=url_for('adconfirm',token=token(email,salt1),_external=True)
            body=f"Thanks for signing up.Follow this link-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Confirmation link sent check your email')
            return render_template('admin.html')'''
        cursor.execute('select count(*) from admin where adminid=%s',[adminid])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from admin where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('username already in use')
            return render_template('admin.html')
        elif count1==1:
            flash('Email already in use')
            return render_template('admin.html')
        data={'adminid':adminid,'email':email,'phonenumber':phonenumber ,'password':password,}
        subject='Email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('adconfirm',token=token(data,salt1),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return render_template('alogin.html')
    return render_template('admin.html')


'''@app.route('/alogin',methods=['GET','POST'])
def alogin():
   if session.get('admin'):
        return redirect(url_for('admindashboard'))
   if request.method == 'POST':
        adminid=request.form['adminid']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from admin where adminid=%s',[adminid])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.execute('select count(*) from admin where adminid%s and password=%s',[adminid,password])
            p_count=cursor.fetchone()[0]
            if p_count==1:
                session['admin']=adminid
                cursor.execute('select emailstatus from admin where adminid=%s',[adminid])
                status=cursor.fetchone()[0]
                cursor.close()
                if status!='confirmed':
                    return redirect(url_for('admindashboard'))
                else:
                    return redirect(url_for('admininactive.html'))
            else:
                cursor.close()
                flash('invalid password')
                return render_template('alogin.html')
        else:
            cursor.close()
            flash('invalid adminid')
            return render_template('alogin.html')'''
        
@app.route('/alogin',methods=['GET','POST'])#after register login with rollno and password route
def alogin():
    if session.get('admin'):
        return redirect(url_for('admindashboard'))
    if request.method=='POST':
        adminid=request.form['adminid']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from admin where adminid=%s and password=%s',[adminid,password])#if the count is 0 then either username or password is wrong or if it is 1 then it is login successfully
        count=cursor.fetchall()[0]
        if count==0:
            flash('Invalid username or password')
            return render_template('alogin.html')
        else:
            session['admin']=adminid
            return redirect(url_for('admindashboard'))
    return render_template('alogin.html')

   
@app.route('/admininactive')
def adinactive():
    if session.get('admin'):
        adminid=session.get('admin')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select emailstatus from admin where adminid=%s',[adminid])
        status=cursor.fetchone()[0]
        cursor.close()
        if status=='confirmed':
            return redirect(url_for('admindashboard'))
        else:
            return render_template('admininactive.html')
    else:
        return redirect(url_for('alogin'))


@app.route('/adminresendconfirmation')
def adresend():
    if session.get('admin'):
        adminid=session.get('admin')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select emailstatus from admin where adminid=%s',[adminid])
        status=cursor.fetchone()[0]
        cursor.execute('select email from admin where adminid=%s',[adminid])
        email=cursor.fetchone()[0]
        cursor.close()
        if status=='confirmed':
            flash('Email already confirmed')
            return redirect(url_for('admindashboard'))
        else:
            subject='Email Confirmation'
            confirm_link=url_for('adconfirm',token=token(email,salt1),_external=True)
            body=f"Please confirm your mail-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Confirmation link sent check your email')
            return redirect(url_for('adinactive'))
    else:
        return redirect(url_for('alogin'))
    
'''@app.route('/adminconfirm/<token>')
def adconfirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        email=serializer.loads(token,salt=salt1,max_age=120)
    except Exception as e:
        #print(e)
        abort(404,'Link expired')
    else:
        cursor=mydb.cursor(buffered=True)
        adminid=data['adminid']
        cursor.execute('select emailstatus from admin where email=%s',[email])
        status=cursor.fetchone()[0]
        cursor.close()

        if status==1:
            cursor.close()
            flash('Email already confirmed')
            return redirect(url_for('userlogin'))
        else:
            cursor=mydb.cursor(buffered=True)
            cursor.execute("update admin set emailstatus='confirmed' where email=%s",[email])
            mydb.commit()
            flash('Email confirmation success')
            return redirect(url_for('alogin'))
        else:
        cursor.execute('insert into complaint (adminid,phonenumber,email,password,) values(%s,%s,%s,%s,)',[data['adminid'],data['phonenumber'],data['email'],data['password'],])        
        mydb.commit()
        cursor.close()
        flash('Details registered!')
        return redirect(url_for('userlogin'))'''


@app.route('/adminconfirm/<token>')
def adconfirm(token):
    try:
        serializer = URLSafeTimedSerializer(secret_key)
        data = serializer.loads(token, salt=salt1, max_age=120)
    except Exception as e:
        # print(e)
        abort(404, 'Link expired')
    else:
        cursor = mydb.cursor(buffered=True)
        adminid = data['adminid']
        cursor.execute('SELECT emailstatus FROM admin WHERE adminid = %s', [adminid])
        status=cursor.fetchone()
        cursor.close()

        if status == 1:
            flash('Email already confirmed')
            return redirect(url_for('alogin'))
        else:
            cursor = mydb.cursor()
            cursor.execute('INSERT INTO admin (adminid, email, phonenumber, password) VALUES (%s, %s, %s, %s)', [data['adminid'], data['email'], data['phonenumber'], data['password']])
            mydb.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('alogin'))

        
@app.route('/adminforget',methods=['GET','POST'])
def adforgot():
    if request.method=='POST':
        email=request.form['email']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from admin where email=%s',[email])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('SELECT emailstatus from admin where email=%s',[email])
            status=cursor.fetchone()[0]
            cursor.close()
            if status!='confirmed':
                flash('Please Confirm your email first')
                return render_template('adminforgot.html')
            else:
                subject='Forget Password'
                confirm_link=url_for('adreset',token=token(email,salt=salt2),_external=True)
                body=f"Use this link to reset your password-\n\n{confirm_link}"
                sendmail(to=email,body=body,subject=subject)
                flash('Reset link sent check your email')
                return redirect(url_for('alogin'))
        else:
            flash('Invalid email id')
            return render_template('adminforgot.html')

    
@app.route('/adminreset/<token>',methods=['GET','POST'])
def adreset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        email=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update admin set password=%s where email=%s',[newpassword,email])
                mydb.commit()
                flash('Reset Successful')
                return redirect(url_for('alogin'))
            else:
                flash('Passwords mismatched')
                return render_template('adminnewpassword.html')

    
'''@app.route('/adminlogout')
def adlogout():
    if session.get('admin'):
        session.pop('admin')
        return redirect(url_for('alogin'))
    else:
        return redirect(url_for('alogin'))'''

@app.route('/alogout')
def alogout():
    if session.get('admin'):
        session.pop('admin')
        return redirect(url_for('alogin'))
    else:
        flash('u are already logged out!')
        return redirect(url_for('alogin'))
    
@app.route('/signin', methods = ['GET','POST'])
def register():
    if session.get('user'):
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password= request.form['password']
        phno= request.form['phno']
        state=request.form['state']
        address=request.form['address']
        pincode=request.form['pincode']
        cursor=mydb.cursor(buffered=True)
        # try:
        #     cursor.execute('insert into users (username,email,password,phno,state,address,pincode) values(%s,%s,%s,%s,%s,%s,%s)',(username,email,password,phno,state,address,pincode))
        # except mysql.connector.IntegrityError:
        #     flash('Username or email is already in use')
        #     return render_template('usersignin.html')
        # else:
        #     mydb.commit()
        #     cursor.close()
        #     subject='Email Confirmation'
        #     confirm_link=url_for('confirm',token=token(email,salt1),_external=True)
        #     body=f"Thanks for signing up.Follow this link-\n\n{confirm_link}"
        #     sendmail(to=email,body=body,subject=subject)
        #     flash('Confirmation link sent check your email')
        #     return render_template('usersignin.html')
        cursor.execute('select count(*) from user where username=%s',[username])
        count=cursor.fetchone()[0]
        cursor.execute('select count(*) from user where email=%s',[email])
        count1=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            flash('username already in use')
            return render_template('usersignin.html')
        elif count1==1:
            flash('Email already in use')
            return render_template('usersignin.html')
        data={'username':username,'email':email ,'password':password,'phno':phno,'state':state,'address':address,'pincode':pincode}
        subject='Email Confirmation'
        body=f"Thanks for signing up\n\nfollow this link for further steps-{url_for('confirm',token=token(data,salt1),_external=True)}"
        sendmail(to=email,subject=subject,body=body)
        flash('Confirmation link sent to mail')
        return redirect(url_for('userlogin'))
    return render_template('usersignin.html')



@app.route('/userlogin',methods=['GET','POST'])
def login():
    if session.get('user'):
        return redirect(url_for('home'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from user where username=%s',[username])
        count=cursor.fetchone()[0]
        if count==1:
            cursor.execute('select count(*) from user where username=%s and password=%s',[username,password])
            p_count=cursor.fetchone()[0]
            if p_count==1:
                session['user']=username
                cursor.execute('select emailstatus from user where username=%s',[username])
                status=cursor.fetchone()[0]
                cursor.close()
                if status!='confirmed':
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('inactive'))
            else:
                cursor.close()
                flash('invalid password')
                return render_template('userlogin.html')
        else:
            cursor.close()
            flash('invalid username')
            return render_template('userlogin.html')
    return render_template('userlogin.html')


@app.route('/inactive')
def inactive():
    if session.get('user'):
        username=session.get('user')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select emailstatus from user where username=%s',[username])
        status=cursor.fetchone()[0]
        cursor.close()
        if status=='confirmed':
            return redirect(url_for('home'))
        else:
            return render_template('inactive.html')
    else:
        return redirect(url_for('userlogin'))
    

@app.route('/resendconfirmation')
def resend():
    if session.get('user'):
        username=session.get('user')
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select emailstatus from user where username=%s',[username])
        status=cursor.fetchone()[0]
        cursor.execute('select email from user where username=%s',[username])
        email=cursor.fetchone()[0]
        cursor.close()
        if status=='confirmed':
            flash('Email already confirmed')
            return redirect(url_for('home'))
        else:
            subject='Email Confirmation'
            confirm_link=url_for('confirm',token=token(email,salt1),_external=True)
            body=f"Please confirm your mail-\n\n{confirm_link}"
            sendmail(to=email,body=body,subject=subject)
            flash('Confirmation link sent check your email')
            return redirect(url_for('inactive'))
    else:
        return redirect(url_for('userlogin'))
    
@app.route('/confirm/<token>')
def confirm(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        data=serializer.loads(token,salt=salt1,max_age=120)
    except Exception as e:
        #print(e)
        abort(404,'Link expired')
    else:
        cursor=mydb.cursor(buffered=True)
        username=data['username']
        cursor.execute('select emailstatus from user where username=%s',['username'])
        status=cursor.fetchone()
        
        if status==1:
            cursor.close()
            flash('Email already confirmed')
            return redirect(url_for('userlogin'))
        # else:
        #     cursor=mydb.cursor(buffered=True)
        #     cursor.execute("update users set emailstatus='confirmed' where email=%s",[email])
        #     mydb.commit()
        #     flash('Email confirmation success')
        #     return redirect(url_for('userlogin'))
        else:
            cursor.execute('insert into user (username,email,password,phno,state,address,pincode) values(%s,%s,%s,%s,%s,%s,%s)',[data['username'],data['email'],data['password'],data['phno'],data['state'],data['address'],data['pincode']])        

            mydb.commit()
            cursor.close()
            flash('Details registered!')
            return redirect(url_for('userlogin'))

@app.route('/forget',methods=['GET','POST'])
def forgot():
    if request.method=='POST':
        email=request.form['email']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select count(*) from user where email=%s',[email])
        count=cursor.fetchone()[0]
        cursor.close()
        if count==1:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('SELECT emailstatus from user where email=%s',[email])
            status=cursor.fetchone()[0]
            cursor.close()
            if status!='confirmed':
                flash('Please Confirm your email first')
                return render_template('forgot.html')
            else:
                subject='Forget Password'
                confirm_link=url_for('reset',token=token(email,salt=salt2),_external=True)
                body=f"Use this link to reset your password-\n\n{confirm_link}"
                sendmail(to=email,body=body,subject=subject)
                flash('Reset link sent check your email')
                return redirect(url_for('userlogin'))
        else:
            flash('Invalid email id')
            return render_template('forgot.html')
    return render_template('forgot.html')


@app.route('/reset/<token>',methods=['GET','POST'])
def reset(token):
    try:
        serializer=URLSafeTimedSerializer(secret_key)
        email=serializer.loads(token,salt=salt2,max_age=180)
    except:
        abort(404,'Link Expired')
    else:
        if request.method=='POST':
            newpassword=request.form['npassword']
            confirmpassword=request.form['cpassword']
            if newpassword==confirmpassword:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('update user set password=%s where email=%s',[newpassword,email])
                mydb.commit()
                flash('Reset Successful')
                return redirect(url_for('userlogin'))
            else:
                flash('Passwords mismatched')
                return render_template('newpassword.html')
        return render_template('newpassword.html')

@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/complaint', methods=['GET', 'POST'])
def complaint():
    if session.get('user'):
        
        if request.method == "POST":
            id1=genotp()
            email = request.form['email']
            problem = request.form['problem']
            address=request.form['address']
            image=request.files['image']
            categorie=request.form['categorie']
            cursor=mydb.cursor(buffered=True)
            filename=id1+'.jpg'
            data=cursor.execute('select * from complaint')
            print(data)
            cursor.execute('INSERT INTO complaint (id,email,problem,address,categorie) VALUES (%s,%s,%s,%s,%s)',[id1,email,problem,address,categorie]) 
            mydb.commit()
            cursor.close()
            path=r"C:\Users\Ravi\Desktop\flask_complaint\static"
            image.save(os.path.join(path,filename))
            
            subject = 'complaint deatils'
            body = 'complaint are submitted' 
            sendmail(email,subject,body)
            flash('complaint submitted')
            return redirect(url_for('home'))
        return render_template('complaintform.html')
    else:
        return redirect(url_for('login'))
        
@app.route('/admindashboard')
def admindashboard():
    if session.get('admin'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from complaint')
        details = cursor.fetchall()
        return render_template('admindashboard.html',details=details)
    else:
        return redirect(url_for('alogin'))
@app.route('/notsolved')
def notsolved():
    if session.get('admin'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from complaint where status="Not Started"')
        details=cursor.fetchall()
        '''if request.method=="POST":
            id1=request.form['id1']
            status=request.form['status']
            cursor.execute('update complaint set status=%s where id=%s',[id1,status])
            cursor.commit()'''
        return render_template('unsolved.html',details=details)
    else:
        return redirect(url_for('alogin'))
    
@app.route('/update/<id1>',methods=['GET','POST'])
def update(id1):
    if session.get('admin'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from complaint where id=%s',[id1])
        data=cursor.fetchone()
        cursor.close()
        if request.method=='POST':
            status=request.form['status']
            cursor=mydb.cursor(buffered=True)
            cursor.execute('update complaint set status=%s where id=%s',[status,id1])
            mydb.commit()
            cursor.execute('select email from complaint where id=%s',[id1])
            
            email=cursor.fetchone()[0]
            print(email)
            cursor.close()
            subject = 'complaint deatils'#--------------------
            body = f'the status of the complaint {status}' #-----------------------------
            sendmail(email,subject,body)#-----------------
            flash('updated successfully')
            cursor.close()
            flash('updated successfully')
            return redirect(url_for('notsolved'))
     
    else:
        return redirect(url_for('alogin'))
    return render_template('update.html',data=data)
@app.route('/currently')
def currently():
    if session.get('admin'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from complaint where status="In Progress"')
        details=cursor.fetchall()
        print(details)
        return render_template('inprogress.html',details=details)
    else:
        return redirect(url_for('alogin'))
@app.route('/oldcomplaint')
def oldcomplaint():
    if session.get('admin'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from complaint where status="resolved"')
        details=cursor.fetchall()
        return render_template('inprogress.html',details=details)
    else:
        return redirect(url_for('alogin'))
@app.route('/user')
def user():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from complaint where username=%s',[session.get('user')])
        details=cursor.fetchall()
        return render_template('userstatus.html',details=details)

@app.route('/view/<id1>')
def view(id1):
        path=os.path.dirname(os.path.abspath(__file__))
        static_path=os.path.join(path,'static')
        return send_from_directory(static_path,f'{id1}.jpg')
@app.route('/viewcontactus')
def contactusview():
    if session.get('user'):
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select * from contactus order by date desc')
        data=cursor.fetchall()
        return render_template('viewcontactus.html',data=data)
    else:
        return redirect(url_for('login'))


app.run(use_reloader=True,debug=True)

