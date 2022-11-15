from sqlite3 import Row
from tkinter.tix import ROW
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import pyodbc


auth = Blueprint('auth', __name__)
#auth = Blueprint('auth', __name__)
cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=MSI\ASQL;"
            "Database=pharma;"
            "Trusted_Connection=yes;")
cnxn = pyodbc.connect(cnxn_str)
cursor = cnxn.cursor()


@auth.route('/login', methods=['GET', 'POST'])
def login():
    #User.query.delete()
    if request.method == 'POST':
        email = request.form.get('email')
        print(email)
        print(User.query.all())
        password = request.form.get('password')
        userdt = User.query.filter_by(email=email).first()
        print(userdt)
        cursor.execute(f"SELECT  * FROM Shops WHERE shop_email = '{email}'")
        user=cursor.fetchone()
        """
        for r in user:
            user=r 
            break
        """
        #user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.shop_password, password):
                flash('Logged in successfully!', category='success')
                login_user(userdt, remember=True)
                return redirect(url_for('views.home',user=current_user))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#@app.route('/')
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        shopname=request.form.get('shopname')
        location=request.form.get('location')
        email = request.form.get('email')
        #first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print("inside auth")
        userdt = User.query.filter_by(email=email).first()
        query=f"SELECT  * FROM Shops WHERE shop_email = '{email}'"
        cursor.execute(query)
        user=cursor.fetchone()
        #print("the user is : "+user)
        #print(user.shop_email)
        print("query executed")
        #userrow=user
        """
        for row in user:
            print("inside the for loop")
            print("row is : "+row)
            userrow=row 
            break 
        """
        #print("the user data is "+userrow.shop_email)
        print(user)
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            password=generate_password_hash(password1, method='sha256')

            cursor.execute(f"insert into Shops values('{shopname}','{location}','{email}','{password}')")
            cnxn.commit()
            
            new_user = User(email=email, store_name=shopname, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
