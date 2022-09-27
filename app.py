
import pymysql
from flask import *
from functions import *
app=Flask(__name__)

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
                    # One Way Authentication Ends Here, Redirect user to Main Dash
                    # Two Way Can be done By Sending OTP to user Phone.
                    tel = row[8]  # This phone is encrypted
                    # Decrypt it
                    decrypted_phone = decrypt(tel)
                    print("DEC PHONE", decrypted_phone)

                    otp = generate_random()
                    send_sms(decrypted_phone, "Your OTP is {}, Do not share with Anyone"
                             .format(otp))
                    sqlotp = "update users set otp = %s where email = %s"
                    cursor = connection.cursor()
                    cursor.execute(sqlotp, (password_hash(otp), email))
                    connection.commit()
                    cursor.close()
                    # ACTIVATE SESSIONS
                    session['fname'] = row[1]  # name
                    session['role'] = row[7]  # role
                    session['user_id'] = row[0]  # user_id
                    session['email'] = row[9]  # email
                    return redirect('/confirm_otp')  # Move to another route
                else:
                    return render_template('signin.html', message="Wrong Password")

            else:

                if 'user_id' in session:
                    session.clear()
                    return render_template('signin.html')
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
                    return redirect('/dashboard') # Two way Auth OK
                else:
                    return render_template('confirm.html', message="Wrong OTP")
        else:
             return render_template('confirm.html')

    else:
         return redirect('/signin')



app.run(debug=True)
