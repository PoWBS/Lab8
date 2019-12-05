from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from wtforms import Form, StringField, PasswordField, BooleanField, validators

app = Flask(__name__)
mailFrom = "GroupTenSemesterProject@gmail.com"
mailPass = "\"#q=P'3-K]g[)7H*"


class SubmissionForm(Form):
    name = StringField('name', [validators.Length(min=10, max=40)])
    password = PasswordField('password', [validators.DataRequired(),
                                          validators.EqualTo('confirm', message='Passwords must match')])
    email = StringField('email', [validators.Length(min=6, max=35), validators.Email()])
    confirm = PasswordField('confirm', [validators.Length(min=1, max=250)])
    consent = BooleanField('consent', [validators.DataRequired()])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/sendMail/', methods=['GET', 'POST'])
def sendmail():
    form = SubmissionForm(request.form)
    if form.validate():
        name = request.form['name']
        password = request.form['password']
        recipient = request.form['email']
        tosend = "Hello " + name + "!\nYou Signed up with password: " + password

        s = smtplib.SMTP(host='smtp.gmail.com', port=587)
        s.starttls()
        s.login(mailFrom, mailPass)

        msg = MIMEMultipart()

        msg['From']=mailFrom
        msg['To']=recipient
        msg['Subject']="BackendMail"
        msg.attach(MIMEText(tosend, 'plain'))

        s.send_message(msg)
        del msg

        s.quit()
        return render_template('home.html')
    else:
        return "You Done goofed"


if __name__ == '__main__':
    app.run(debug=True)