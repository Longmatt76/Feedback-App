from flask import Flask, redirect, render_template, session, flash 
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import UserForm, LoginForm, FeedbackForm 



app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    """redirects to the register page"""
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_user():
    """registers a new user and hashes their password"""
    form = UserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
       

        user = User.register(username, password, email, first_name, last_name)
        
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")

    else:
        return render_template("/register.html", form=form)


@app.route('/login', methods=['GET','POST'])
def login_user():
    """authenticates an existing user"""

    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
   
        user = User.authenticate(username,password)
        if user:
            session['username'] = user.username
            return redirect(f'/users/{user.username}')

        else: 
            form.username.errors = ['Invalid username or password']
          

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def show_user(username):
    """displays the user if user is registered and logged in otherwise 
       it redirects home """
    if "username" not in session or username != session['username']:
        flash('You must be logged in to perform this operation')
        return redirect('/login')

    else:
        user = User.query.get(username)
        return render_template('user.html', user=user)

  
    
@app.route('/logout')
def log_out_user():
    '''logs out user and redirects to home'''
    session.pop('username')
    return redirect('/')


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """delete user and remove from db"""
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop('username')
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """lets user create feedback"""
    if 'username' not in session or username != session['username']:
        flash("Please login first")
        return redirect('/login')
    
    form = FeedbackForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title,content=content,username=username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/users/{username}')
    

    return render_template('add_feedback.html', form=form)



@app.route('/feedback/<int:feedback_id>/update', methods=['GET','POST'])
def update_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("must be logged in to perform this operation")
        return redirect('/login')

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
       
        db.session.commit()
        return redirect(f'/users/{feedback.username}')

    else:
        return render_template('update_feedback.html', form=form)


@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("must be logged in to perform this operation")
        return redirect('/login')
 
    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.username}')