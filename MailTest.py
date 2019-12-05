from flask import Flask, render_template, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from wtforms import Form, StringField, PasswordField, BooleanField, validators
from werkzeug.utils import secure_filename


app = Flask(__name__)
mailFrom = "GroupTenSemesterProject@gmail.com"
mailPass = "\"#q=P'3-K]g[)7H*"


class SubmissionForm(Form):
    name = StringField('name', [validators.Length(min=2, max=40, message='Name must be more than 2 characters ')])
    password = PasswordField('password', [validators.DataRequired(message='Password must be filled '),
                                          validators.EqualTo('confirm', message='Passwords must match ')])
    email = StringField('email', [validators.Length(min=6, max=35, message='Email must be at least 6 characters '),
                                  validators.Email(message='Not a valid Email format ')])
    confirm = PasswordField('confirm', [validators.Length(min=4, max=250,
                                                          message='Password must be at least 4 characters ')])
    consent = BooleanField('consent', [validators.DataRequired(message='Box must be checked ')])


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/uploader/', methods=['POST'])
def uploadfile():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return render_template('home.html', Status="success")
    return render_template('home.html', Status="")


@app.route('/sendMail/', methods=['POST'])
def sendmail():
    if request.method == 'POST':
        error = ""
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
            return render_template('home.html', error="success")

        else:
            for field, err in form.errors.items():
                error = error + "Error! " + ''.join(err) + " "
            return render_template('home.html', error=error)
    return render_template('home.html', error="")


if __name__ == '__main__':
    app.run(debug=True)
