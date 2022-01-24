from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, LoginForm,PostForm
from app.models import User,Post


@app.route ('/')
def index():
    posts= Post.query.all()
    return render_template('index.html',posts=posts)


@app.route('/register',methods=["GET","POST"])
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
        user = User.query.filter_by(username=username)
        if not user or not user.check_password(password):
            flash('That username and/or password is incorrect', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        flash('You have succesfully logged in', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/posts/<int:post_id>')
def post_info(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts.html', post = post)

@app.route('/posts/<int:post_id>', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    if not current_user.is_admin:
        flash("Sorry! You can't edit this one!!", "warning")
        return redirect(url_for('index'))
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        post.title = title
        post.body = body
        post.save()
        flash(f"{post.title} has been updated", "primary")
        return redirect(url_for('posts.html', post_id=post.id))

    return render_template('posts.html', post = post, form=form)


