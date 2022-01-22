from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user
from app.forms import RegisterForm, LoginForm
from app.models import User


@app.route ('/')
def index():
    return render_template('index.html')


@app.route('/register',methods=["GET", "POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        
        username=form.username.data
        email=form.username.data
        password=form.password.data

        user_exists = User.query.filter((User.username == username)|(User.email == email)).all()

        if user_exists:
            flash(f"User with username {username} or email {email} already exists", "danger")
            return redirect(url_for('register'))
    


        User(username=username, email=email, password=password)
        flash("Thank you for registering!", "primary")
        return redirect (url_for('index.html'))
    return render_template('register.html',form=form)
  
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        username = form.username.data
        password = form.password.data
       
        user = User.query.filter_by(username=username).first()
        
        
        if not user or not user.check_password(password):
            
            flash('That username and/or password is incorrect', 'danger')
            return redirect(url_for('login'))
        
       
        login_user(user)
        flash('You have succesfully logged in', 'success')
        return redirect(url_for('index'))

    return render_template('login.html', form=form)

