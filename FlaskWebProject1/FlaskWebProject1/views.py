"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
#from flask_application1 import app
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
#from .models import Note
from . import db

views = Blueprint('views', __name__)

"""
@views.route('/', methods=['GET', 'POST'])
@login_required
def sign_up():
    print("inside view")
    
    return render_template(
        'sign_up.html',
        title='sign up Page',
        year=datetime.now().year,
        
    )

"""

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
   
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,user=current_user
    )

@views.route('/contact')
@login_required
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='This webpage is being developed by team unknown from conestoga.',user=current_user
    )

@views.route('/about')
@login_required
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.',user=current_user
    )
