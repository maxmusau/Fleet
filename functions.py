import bcrypt
def password_hash(password):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    print("Bytes ", bytes)
    print("Salt ", salt)
    print("Hash ", hash.decode())
    return hash.decode()
password_hash("nairobi")
# what is the hashed password
def password_verify(input_password, hash):
    userBytes = input_password.encode()
    result = bcrypt.checkpw(userBytes, hash.encode())
    print("Status ", result)
    return result
# send sms
import africastalking
def send_sms(phone, message):
    africastalking.initialize(
        username="joe2022",
        api_key="aab3047eb9ccfb3973f928d4ebdead9e60beb936b4d2838f7725c9cc165f0c8a"
        # justpaste.it/1nua8
    )
    sms = africastalking.SMS
    recipient = [phone]
    sender = "AFRICASTKNG"
    try:
        response = sms.send(message, recipient)
        print(response)
    except Exception as error:
        print("Execption is ", error)

# send email address
def send_email(receiver_address, mail_content, subject):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    sender_address = 'musaumaxwell@gmail.com'
    sender_pass = '!@#$Mwas@@#2'
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')

def generate_random():
    # initializing size of string
    import string
    import random  # define the random module
    S = 10  # number of characters in the string.
    # call random.choices() string module to find the string in Uppercase + numeric data.
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits,
                                 k=S))
    print("The randomly generated string is : " + str(ran))  # print the random data
    return str(ran)

#generate_random()
from cryptography.fernet import  Fernet
def write_key():
    key = Fernet.generate_key()
    with open('key.key', "wb") as key_file:
        key_file.write(key)

#write_key()
def load_key():
    return open("key.key", "rb").read()


def encrypt(data):
    key = load_key()
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    print("Before Encr", data)
    print("After Encr ", encrypted_data.decode())
    return encrypted_data.decode()
def get_OS():
    import platform
    plt=platform.system()
    print(plt)
    return plt

encrypt("+254703353657")
#b'gAAAAABjIYV6HGcxidgjeXrvAgmOGFQvGWtOyI-xMW9i1RICxTkahv1G5ABpy352ODFzpd-Y-CsTmOL4GStDDBCesTelea7PPQ=='
def decrypt(data):
    key = load_key()
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(data)
    print("Decrypted ", decrypted_data.decode())
    return decrypted_data.decode()

# validate email
import re
def validate_email(s):
   pat = "^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-z]{1,3}$"
   if re.match(pat,s):
      return True
   return False

# check mac_address
def check_mac_address():
    from getmac import get_mac_address as gma
    print(gma())
    return gma()
check_mac_address()
# decrypt("gAAAAABjLZJ7YWig8gbnPDgQSe0n2ekiXRGdUH0A8CXQP2XoUBf2rHJ86-l7nMokkjXjQl7WbTpcoJjN7lADjOS3HAlT8TfvjQ==")

