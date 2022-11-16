import os
from io import StringIO
import pandas as pd
from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename

# import pandas as pd
# import pyspark
# from pyspark.sql import SparkSession
# from pyspark.sql.functions import *

UPLOAD_FOLDER = 'C:/Users/rpagadal/OneDrive - Capgemini/Documents/OneDrive - Capgemini/Documents/vs_code/uploads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = "secret"
app.config['JSON_SORT_KEYS'] = False


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        if (username == "user") & (password == "password"):
            return render_template('home.html', approver=username)
        # return render_template('index.html', username = username, password = password)
        else:
            msg = 'Incorrect username/password'
    return render_template('login.html', msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    errors = {}
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if not username or not username.strip():
            errors['username'] = 'Username should not be empty'
        if not email or not email.strip() or '@' not in email:
            errors['email'] = 'Email should not be empty'
        if not password or not password.strip():
            errors['password'] = 'Password should not be empty'
        if not confirm_password or not confirm_password.strip() or not password != confirm_password:
            errors['confirm_password'] = 'Confirm Password should not be empty'
        print("Errors", errors)
    return render_template('register.html', errors=errors)


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('home'))


################################
@app.route('/status', methods=['GET', 'POST'])
def get_data():
    """
    get the data from sources

    Parameters
       No params are required
    Returns
    ------
    response : dict
       dictionary object
    Exceptions
    ------
       Raises exception if fails to get the data
    """
    file = request.files["bank_file"]
    # name = request.form["approvername"]
    temp_dataframe = pd.read_csv(file)
    temp_dataframe["Approver"] = ''
    temp_dataframe.insert(temp_dataframe.columns.get_loc("Approver") + 1, column='<input type="checkbox" onclick="toggle(this)" />',
                          value='<input type="checkbox" name="action" />')
    # temp_dataframe.insert(temp_dataframe.columns.get_loc("Approver") + 1, column='Action',
    #                       value='<a href="#" class="accept">ACCEPT <span class="fa fa-check"></span></a> <a href="#" class="reject">REJECT <span class="fa fa-close"></span></a>')
    temp_dataframe['Status'] = ''
    print(temp_dataframe)
    temp_dataframe = temp_dataframe.style
    # temp_list_headers = temp_dataframe.columns.values.tolist()
    # temp_list = temp_dataframe.values.tolist().
    # return render_template('home.html', table=temp_list, headers=temp_list_headers)
    return render_template('home.html', tables=[temp_dataframe.to_html(classes='data')],
                           titles=temp_dataframe.columns.values)

@app.route('/send', methods = ['GET','POST'])
def send_data():
    if request.method == "POST":
        data = request.form['title']
        return data

@app.route('/accept', methods=['GET', 'POST'])
def accept_data():
    print('Accepted')
    return 'nothing'

@app.route('/reject', methods=['GET', 'POST'])
def reject_data():
    print('Rejected')
    return 'nothing'

if __name__ == "__main__":
    app.run(debug=True)
