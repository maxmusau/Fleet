
import pymysql
from flask import *
app=Flask(__name__)
@app.route("/signu", methods=["POST","GET"])
def main():
    if request.method == "POST":
        names = request.form['names']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        tel = request.form['tel']

        con=pymysql.connect(host='localhost', user='root', password='', database='SchoolSysytem')
        sql = "INSERT INTO `signup`(`names`, `email`, `password`, `confirm`, `tel`) VALUES (%s,%s,%s,%s,%s)"
        cursor = con.cursor()
        cursor.execute(sql, (names, email, password, confirm, tel))
        con.commit()
        return render_template('signup.html', message="succesful")
    else:
        return render_template('signup.html')
app.run(debug=True)