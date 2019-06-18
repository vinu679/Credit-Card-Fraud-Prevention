from flask import Flask, url_for,request, render_template
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
import smtplib
#import uuid

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config.from_pyfile('config.cfg')




s= URLSafeTimedSerializer('')

@app.route('/' , methods=['GET','POST'])
def index():
    if request.method == 'GET':
        me = "n140679vinu@gmail.com"
        you = "n140777@rguktn.ac.in"
        msg = MIMEMultipart()
        msg['Subject'] = "Alert from credit card"
        msg['From'] = me
        msg['To'] = you
        access = "Vijayawada"
        #access = input("Enter Location:")
        #token = uuid.uuid4().hex
        token = s.dumps('heelo',salt='email-confirm')
        #token1 = s.dumps('heelo',salt='email-reject')
        #print(token)
        link =url_for('confirm_email', token=token , _external=True)
        link1=url_for('reject_email', token=token , _external=True)
        html = """\
        <html>
        <head>
        <title>Verification</title>
            <style>
            .button {
              display: inline-block;
              padding: 10px 15px;
              font-size: 15px;
              cursor: pointer;
              text-align: center;
              text-decoration: none;
              outline: none;
              color: #fff;
              background-color: #4CAF50;
              border: none;
              border-radius: 15px;
              box-shadow: 0 5px #999;
            }

            .button:hover {background-color: #3e8e41}

            .button:active {
              background-color: #3e8e41;
              box-shadow: 0 5px #666;
              transform: translateY(4px);
            }
            </style>
            </head>
            <body bgcolor="gray">
            
            <p>Hi!<br>
                you purchase at %s<br>
                Are you accept?<br>
            </p>
            <a href=%s class="button" style="color:white;">YES</a>&nbsp;&nbsp;
            <a href=%s class="button" style="background-color: red;color:white;">NO</a>    
        </body>
        </html>
         """ %(access,link,link1)
        #print('hi')
        part2 = MIMEText(html, 'html')
        msg.attach(part2)
        ser = smtplib.SMTP('smtp.gmail.com',587)
        ser.starttls()
        ser.login('n140679vinu@gmail.com','7995497591')
        ser.sendmail(me, you, msg.as_string())
        return 'you get confirmation mail click yes for accept'

    
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token,salt='email-confirm',max_age=3600)
    except SignatureExpired:
        return '<h1> the token is expired</h1>'
    return render_template("v.html")
@app.route('/reject_email/<token>')
def reject_email(token):
    try:
        email = s.loads(token,salt='email-confirm',max_age=3600)
    except SignatureExpired:
        return '<h1> the token is expired</h1>'
    return '<h1>Transaction Terminated</h1>'

if __name__ == '__main__':
    app.run()
