
import pymysql
from flask import *
from functions import *
from werkzeug.utils import secure_filename
import os
app=Flask(__name__)

UPLOAD_FOLDER = "static/images"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 #ACCEPT ONLY <4mbs
# functions to check sessions
ALLOWED_EXTENSIONS = {'png', 'jpg','jpeg','webp'}

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
import datetime

@app.route("/signup", methods=["POST","GET"])
def main():
    if request.method == "POST":
        names = request.form['names']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        tel = request.form['tel']


        # validation
        if ' ' not in names:
            return render_template('signup.html', message = "Names must be two words")
        elif '@' not in email:
            return render_template('signup.html', message="Invalid Email")
        elif len(password) < 8:
            return render_template('signup.html', message="Password must be 8 characters")
        elif password != confirm:
            return render_template('signup.html', message="Passwords do not match")
        elif len(tel) != 13:
            return render_template('signup.html', message="Invalid phone number. must be 13 characters")
        elif not tel.startswith("+"):
            return render_template('signup.html', message="Must start with a +")
        else:
            connection = pymysql.connect(host='localhost', user='root', password='', database='SchoolSysytem')
            sql = "INSERT INTO `signup`(`names`, `email`, `password`, `confirm`, `tel`) VALUES (%s,%s,%s,%s,%s)"
            cursor = connection.cursor()
            cursor.execute(sql, (names, email, password, confirm, tel))
            connection.commit()

            return redirect('/signin')

            # try:
            #     cursor.execute(sql, (names, email, password, confirm, tel))
            #     connection.commit()
            #     import africastalking
            #     africastalking.initialize(
            #         username='joe2022', api_key='aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a'
            #     )
            #     sms = africastalking.SMS
            #     recipient = [tel]
            #     message = "Dear {}, Congratulations, Sign up successful ".format(names)
            #     sender = "AFRICASTKNG"
            #     try:
            #         response = sms.send(message, recipient)
            #         print(response)
            #     except:
            #         print("SMS not sent")
            #         return redirect("/signin")
            # except:
            #     connection.rollback()
            #     return render_template('signup.html', message="Error occured")
    else:
        return render_template("signup.html")



# Functions to check sessions

def check_user():
    if 'user_id' in session:
        return True
    else:
        return False

def check_role():
    if 'role' in session:
        role = session['role']
        return role
    else:
        session.clear()
        return redirect('/signin')

def get_userid():
    if 'user_id' in session:
        user_id = session['user_id']
        return user_id
    else:
        session.clear()
        return redirect('/signin')


@app.route("/logout")
def logout():
    #session.pop('user_id', None)
    session.clear()
    return redirect('/signin')



# name,cost,desription,
# signin route
app.secret_key="jfkks85@3$$5678gdgsrwshs&&6$$*!@#$%^&*"
@app.route("/signin", methods=["POST", "GET"])
def signin():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        connection = pymysql.connect(host='localhost', user='root', password='', database='FleetDB')
        sql = "SELECT * FROM `users` WHERE email= %s"

        cursor = connection.cursor()
        cursor.execute(sql, (email))
        if cursor.rowcount == 0:
            return render_template('signin.html', message="Wrong Email address")
        # elif cursor.rowcount == 1:
        #     session['key'] = email
        #     return render_template('signin.html', message="Successful login")
        # else:
        #     return render_template('signin.html', message="Error!  Try Again")
        #
        else:
            row =cursor.fetchone()
            if row[5]=='inactive':
                return render_template('signin.html',message ='Account Inactive, please wait for approval')
            elif row[5]=='active':
                hashed_password=row[6] #this is hashed password from database
                print('Hashed pass', hashed_password)
                # verify that the hshed password is the same as hashed pass from the database
                status =password_verify(password, hashed_password)
                print("Login Status", status)
                if status:
                    sql='select * from users where email = %s'
                    cursor=connection.cursor()
                    cursor.execute(sql,email)
                    row=cursor.fetchone()

                    if row[14] != check_mac_address():


                        # One Way Authentication Ends Here, Redirect user to Main Dash
                        # Two Way Can be done By Sending OTP to user Phone.
                        tel = row[8]  # This phone is encrypted
                        # Decrypt it
                        decrypted_phone = decrypt(tel)
                        print("DEC PHONE", decrypted_phone)

                        otp = generate_random()
                        OS=get_OS()
                        mac_address=check_mac_address()

                        send_sms(decrypted_phone, "Your OTP is {}, Do not share with Anyone"
                                 .format(otp))
                        sqlotp = "update users set otp = %s where email = %s"
                        sqlos = "update users set OS = %s where email = %s"
                        sqlmac= "update users set mac_address =%s where email =%s"
                        cursor1 = connection.cursor()
                        cursor1.execute(sqlotp, (password_hash(otp), email))
                        cursor2 = connection.cursor()
                        cursor2.execute(sqlos,(OS,email))
                        cursor3=connection.cursor()
                        cursor3.execute(sqlmac,(mac_address,email))
                        connection.commit()
                        cursor.close()
                        # ACTIVATE SESSIONS
                        session['fname'] = row[1]  # name
                        session['role'] = row[7]  # role
                        session['user_id'] = row[0]  # user_id
                        session['email'] = row[9]  # email



                        return redirect('/confirm_otp')  # Move to another route
                    else:
                        return redirect('/')


                else:
                    return render_template('signin.html', message="Wrong Password")

            else:

                if 'user_id' in session:
                    session.clear()
                    return redirect('/a')
                else:
                    return render_template('signin.html')

    else:
        return render_template("signin.html")

@app.route('/confirm_otp', methods = ['POST','GET'])
def confirm_otp():
    if 'email' in session:
        if request.method == 'POST':
            email = session['email']
            otp = request.form['otp']
            connection = pymysql.connect(host='localhost', user='root', password='', database='FleetDB')
            sql = "select * from users where email = %s"
            cursor = connection.cursor()
            cursor.execute(sql, (email))
            row = cursor.fetchone()
            otp_hash = row[11] #hashed_otp
            otp_time =row[12] #otp time
            # convert otp time from str to datatime
            prev_time=datetime.datetime.strptime(otp_time, '%Y-%m-%d %H:%M:%S.%f')
            # get time now
            time_now=datetime.datetime.now()
            # find differnce
            diff= time_now - prev_time
            if diff.total_seconds() > 60:
                return render_template('confirm.html', message="OTP Expired")
            else:
                status = password_verify(otp, otp_hash)
                if status:
                    session['fname'] = row[1]
                    session['role'] = row[7]
                    session['user_id'] = row[0]
                    session['img'] = row[13]
                    return redirect('/') # Two way Auth OK
                else:
                    return render_template('confirm.html', message="Wrong OTP")
        else:
             return render_template('confirm.html')

    else:
         return redirect('/signin')

# add different roles

connection = pymysql.connect(host='localhost', user='root', password='', database='FleetDB')
@app.route('/')
def dashboard():
    if check_user():
        return render_template('dashboard.html')
    else:
        return redirect('/signin')


@app.route('/addMake', methods = ['POST', 'GET'])
def addmake():
    if check_user() and check_role() == "admin":
        if request.method == 'POST':
            make = request.form['make']
            if not make:
                return jsonify({'error1':'Please Enter make'})
            else:
                cursor = connection.cursor()
                sql = "insert into vehicle_make(make_name) values(%s)"
                try:
                    cursor.execute(sql, (make))
                    connection.commit()
                    return jsonify({'success': 'Make Added'})
                except:
                    connection.rollback()
                    return jsonify({'error2': 'Make Not Added'})

        else:
            return render_template('admin/addmake.html')
    else:
        return redirect('/signin')

@app.route('/addLocation', methods = ['POST', 'GET'])
def addLocation():
    if check_user() and check_role() == "admin":
        if request.method == 'POST':
            location = request.form['location']
            if not location:
                return jsonify({'error1':'Please Enter location'})
            else:
                cursor = connection.cursor()
                sql = "insert into locations(loc_name) values(%s)"
                try:
                    cursor.execute(sql, (location))
                    connection.commit()
                    return jsonify({'success': 'Location Added'})
                except:
                    connection.rollback()
                    return jsonify({'error2': 'Location Not Added'})

        else:
            return render_template('admin/addlocations.html')
    else:
        return redirect('/login')

@app.route('/addModel', methods = ['POST', 'GET'])
def addModel():
    if check_user() and check_role() == "admin":
        if request.method == 'POST':
            model = request.form['model']
            make_id = request.form['make_id']
            if not model or not make_id:
                return jsonify({'error1':'Please Empty Fields'})
            else:
                cursor = connection.cursor()
                sql = "insert into vehicle_model(make_id,model_name) values(%s, %s)"
                try:
                    cursor.execute(sql, (make_id, model))
                    connection.commit()
                    return jsonify({'success': 'Model Added'})
                except:
                    connection.rollback()
                    return jsonify({'error2': 'Model Not Added'})
        else:
            # get makes from the database
            sql = "select * from vehicle_make order by make_name asc"
            cursor = connection.cursor()
            cursor.execute(sql)
            makes = cursor.fetchall()
            return render_template('admin/addmodel.html', makes = makes)
    else:
        return redirect('/signin')


@app.route('/addType', methods = ['POST', 'GET'])
def addType():
    if check_user() and check_role() == "admin":
        if request.method == 'POST':
            type = request.form['type']
            if not type:
                return jsonify({'error1':'Please Enter Type'})
            else:
                cursor = connection.cursor()
                sql = "insert into vehicle_types(type_name) values(%s)"
                try:
                    cursor.execute(sql, (type))
                    connection.commit()
                    return jsonify({'success': 'Type Added'})
                except:
                    connection.rollback()
                    return jsonify({'error2': 'Type Not Added'})

        else:
            return render_template('admin/addtype.html')
    else:
        return redirect('/login')

@app.route('/addUser', methods = ['POST', 'GET'])
def addUser():
    if check_user() and check_role() == "admin":
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            surname = request.form['surname']
            gender = request.form['gender']
            password = generate_random()
            role = request.form['role']
            phone = request.form['phone']
            email = request.form['email']
            regex = "^\+254\d{9}"
            import re
            if not fname:
                return jsonify({'errorFname':'Please Enter First Name'})

            elif not lname:
                return jsonify({'errorLname':'Please Enter Last Name'})

            elif not surname:
                return jsonify({'errorSurname':'Please Enter Surname'})

            elif not gender:
                return jsonify({'errorGender':'Please Enter Gender'})

            elif role not in ['admin', 'finance', 'operations', 'guest', 'service']:
                return jsonify({'errorRole':'Invalid Role'})

            elif not re.match(regex, phone) :
                return jsonify({'errorPhone':'Please Enter Valid Phone i.e +254XXXXXXXXX'})

            elif not validate_email(email):
                return jsonify({'errorEmail':'Please Enter Valid Email'})

            else:
                sqlCheck = "select * from users where email = %s"
                cursor = connection.cursor()
                cursor.execute(sqlCheck, (email))
                if cursor.rowcount  > 0:
                    return jsonify({'errorEmail': 'Email Already Taken'})
                else:
                    cursor = connection.cursor()
                    sql = '''insert into users(fname, lname, surname, gender, password, role, phone, email) 
                    values(%s,%s,%s,%s,%s,%s,%s,%s)'''
                    try:
                        cursor.execute(sql, (fname, lname, surname, gender, password_hash(password),
                                             role, encrypt(phone), email))

                        connection.commit()
                        message = '''Hello {}, You are signed in as {}, Login using Your Email 
                        and Password {}'''.format(fname, role, password)
                        send_sms(phone, message)
                        return jsonify({'success': 'User Added'})
                    except:
                        connection.rollback()
                        return jsonify({'error2': 'User Not Added'})

        else:
            return render_template('admin/adduser.html')
    else:
        return redirect('/signin')

# started here

@app.route('/profile')
def profile():
    if check_user():
        user_id =  get_userid()
        sql = "select * from users where user_id = %s"
        cursor = connection.cursor()
        cursor.execute(sql, (user_id))
        row = cursor.fetchone()
        return render_template("profile.html", row = row)
    else:
        return redirect('/signin')

# more about this function
@app.template_filter()    # this function is called in a template
def data_decrypt(encrypted_data):
    decrypted = decrypt(encrypted_data)
    return decrypted



@app.route('/change_password', methods = ['POST', 'GET'])
def change_password():
    if check_user():
        if request.method == 'POST':
            user_id = get_userid()
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']

            sql = "select * from users where user_id = %s"
            cursor = connection.cursor()
            cursor.execute(sql, (user_id))
            # get row containing the current password from DB
            row = cursor.fetchone()
            hashed_password = row[6]
            status = password_verify(current_password, hashed_password)
            if status:
                 print("Current is okay")
                 response = passwordValidity(new_password)
                 print("tttttttttt", response)
                 if response == True:
                     print("New is okay")
                     if new_password != confirm_password:
                         return jsonify({'confirmWrong': "Password Do Not match!"})
                     else:
                         print("Confirm is okay")
                         sql = "update users set password = %s where user_id = %s"
                         cursor = connection.cursor()
                         try:
                            cursor.execute(sql, (password_hash(new_password) , user_id))
                            connection.commit()
                            return jsonify({'success': "Password Changed!"})
                         except:
                            connection.rollback()
                            return jsonify({'error': "Password Was Not Changed!"})
                 else:
                     return jsonify({'newWrong': response})

            else:
                return jsonify({'currentWrong': 'Current Password is Wrong!'})

        else:
            return render_template('change_password.html')
    else:
        return redirect('/signin')


@app.route('/addOwner', methods = ['POST', 'GET'])
def addOwner():
    if check_user() and check_role() == "admin":
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            surname = request.form['surname']
            email = request.form['email']
            address = request.form['address']
            loc_id = request.form['loc_id']
            # passport_pic = request.form['passport_pic']
            id_no = request.form['id_no']
            dob = request.form['dob']
            phone = request.form['phone']
            user_id = get_userid() # Logged in person
            password = generate_random()  # Generate Random Password
            files  = request.files.getlist("files[]")
            for file in files:
                if file and allowed_files(file.filename):
                    filename = secure_filename(file.filename)
                    uniquefilename = "{}{}".format(generate_random(), filename) # add random strings to filename
                    # Upload the file using the random file name.
                    try:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], uniquefilename))
                        session['uniquefilename'] = uniquefilename
                    except Exception as error:
                        session['uniquefilename'] = ""
                        print("Upload error", error)

                else:
                    return jsonify({"error":"Invalid File, Upload Only png, jpeg, "})

            if not fname:
                return jsonify({'error':'First name is Empty!'})
            elif not lname:
                return jsonify({'error':'Last name is Empty!'})
            elif not validate_email(email):
                return jsonify({'error':'Email is Invalid'})
            elif not id_no:
                return jsonify({'error':'Id no is Empty!'})
            elif not dob:
                return jsonify({'error':'Your DOB is invalid'})
            elif not check_phone(phone):
                return jsonify({'error':'Invalid Phone use +254XXXXXXXXX'})
            else:
                cursor = connection.cursor()
                sql = '''insert into owners(fname,lname, surname, phone, email, address,
                loc_id,passport_pic, id_no, dob, user_id, password) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                try:
                    cursor.execute(sql, (fname, lname, surname, encrypt(phone), email,
                                         address, loc_id, session['uniquefilename'], id_no, dob,
                                         user_id, password_hash(password)))
                    connection.commit()
                    message = '''Thank you for Joining FleetS, Download app from link 
                    Login with your email and password: {} To track your Vehicles'''.format(password)
                    send_sms(phone, message)
                    return jsonify({'success': 'Owner Added'})
                except:
                    connection.rollback()
                    return jsonify({'error2': 'Owner Not Added'})
        else:
            # get Locations from the database
            locations = getlocations()
            return render_template('admin/addowners.html', locations = locations)
    else:
        return redirect('/login')

@app.route('/addDriver', methods = ['POST', 'GET'])
def addDriver():
    if check_user() and check_role() == "admin":
        if request.method == 'POST':
            fname = request.form['fname']
            lname = request.form['lname']
            surname = request.form['surname']
            email = request.form['email']
            dl_no = request.form['dl_no']
            loc_id = request.form['loc_id']
            dl_no_expiry = request.form['dl_no_expiry']
            # passport_pic = request.form['passport_pic']

            dob = request.form['dob']
            phone = request.form['phone']
            user_id = get_userid() # Logged in person
            password = generate_random()  # Generate Random Password
            files  = request.files.getlist("files[]")
            for file in files:
                if file and allowed_files(file.filename):
                    filename = secure_filename(file.filename)
                    uniquefilename = "{}{}".format(generate_random(), filename) # add random strings to filename
                    # Upload the file using the random file name.
                    try:
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], uniquefilename))
                        session['uniquefilename'] = uniquefilename
                    except Exception as error:
                        session['uniquefilename'] = ""
                        print("Upload error", error)

                else:
                    return jsonify({"error":"Invalid File, Upload Only png, jpeg, "})

            if not fname:
                return jsonify({'error':'First name is Empty!'})
            elif not lname:
                return jsonify({'error':'Last name is Empty!'})
            elif not validate_email(email):
                return jsonify({'error':'Email is Invalid'})
            elif not dl_no:
                return jsonify({'error':'dl no is Empty!'})
            elif not dob:
                return jsonify({'error':'Your DOB is invalid'})
            elif not check_phone(phone):
                return jsonify({'error':'Invalid Phone use +254XXXXXXXXX'})
            else:
                cursor = connection.cursor()
                sql = '''insert into drivers(fname,lname, surname, phone, email, 
                dl_no,dl_no_expiry,passport_pic,
                loc_id, dob, password, user_id) 
                values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
                try:
                    cursor.execute(sql, (fname, lname, surname, encrypt(phone), email,
                                         dl_no, dl_no_expiry, session['uniquefilename'], loc_id, dob,
                                         password_hash(password),user_id))
                    connection.commit()
                    message = '''Thank you for Joining FleetS, Download app from link 
                    Login with your email and password: {} To track your Assignments'''.format(password)
                    send_sms(phone, message)
                    return jsonify({'success': 'Owner Added'})
                except:
                    connection.rollback()
                    return jsonify({'error2': 'Owner Not Added'})
        else:
            # get Locations from the database
            locations = getlocations()
            return render_template('admin/adddriver.html', locations = locations)
    else:
        return redirect('/login')

# justpaste.it/9kvae
# This function returns all locations
def getlocations():
    sql = "select * from locations order by loc_name asc"
    cursor = connection.cursor()
    cursor.execute(sql)
    locations = cursor.fetchall()
    return locations





app.run(debug=True)
