from flask import Flask, redirect,render_template, session, flash
from flask_bcrypt import Bcrypt
from models import db, connect_db,User, Feedback
from forms import Registration_form, login, feedback_form

app = Flask(__name__)
bcrypt = Bcrypt(app)


app.app_context().push()
app.debug = True
app.config['SECRET_KEY'] = 'SEKRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)

@app.route('/')
def show_home_page():
    """SHOW HOMEPAGE WHERE USER CAN LOGIN OR REGISTER TO BEING"""
    
    return render_template('home.html')

@app.route('/login', methods= ['GET', 'POST'])
def handle_login():
    """SHOW AND HANDLE LOGIN FORM"""
    form = login()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate_user(username,password)

        if user:
            flash("Welcome back!")
            session['username'] = user.username
           
            return redirect(f'/users/{user.username}')
        
        else:
            flash("Incorrect username or password!")
            return render_template('login.html', form=form)
    
    
    return render_template('login.html', form=form)


    

@app.route('/logout')
def logout():
    """LOGS USER OUT"""
    session.pop('username')

    return redirect('/')

        

@app.route('/register')
def show_registration_form():
    """RETURN TEMPLATE FOR NEW USER REGISTRATION"""
    form = Registration_form()

    return render_template('register.html', form=form )

@app.route('/register/handle', methods=['POST'])
def handle_registration():
    """HANDLES REGISTRATION FORM"""
    form = Registration_form()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name= form.last_name.data

        hashed_password = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed_password.decode("utf8")

        user = User.register_user(username, password,email,first_name,last_name)
        db.session.commit()

        session['username'] = user.username
        return render_template('user.html', user=user)
    
    else:
        return render_template('register.html', form=form)
    
@app.route('/users/all')
def show_all_users():
    users = User.query.all()

    return render_template('all_users.html', users=users)


@app.route('/users/<username>')
def show_user(username):
    """SHOWS DETAIL ABOUT A SPECIFIC USER"""
    user = User.query.get_or_404(username)

    return render_template('user.html', user=user)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """DELETES USER"""
    user = User.query.get_or_404(username)

    if session['username'] == username:
        db.session.delete(user)
        db.session.commit()

        flash(f"{user.username} successfully deleted!")
        session.pop('username')

        return redirect('/')
    
    else:
        flash("You do not have permission to delete someone else's profile")
        return ('/')

        

##################################FEEDBACK################################
@app.route('/feedbacks', methods=['GET'])
def show_all_feedbacks():

    all_feedbacks = Feedback.query.all()

    return render_template('all_feedback.html',all_feedbacks=all_feedbacks)


@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):

    form = feedback_form()
    user = User.query.get_or_404(username)
    
    if 'username' in session:
        if form.validate_on_submit():
            title= form.title.data
            content=form.content.data

            new_feedback = Feedback(title=title,content=content, username=user.username)
            db.session.add(new_feedback)
            db.session.commit()
            print(new_feedback.title)
            print(new_feedback.content)

            return redirect('/feedbacks')
    
    else:
            flash("Must be logged in to create a new post")
            return redirect('/')
        
    return render_template('create_feedback.html', form=form,user=user)
    
@app.route("/feedback/<int:feedbackID>/delete",  methods=['POST'])
def delete_feedback(feedbackID):

    feedback = Feedback.query.get_or_404(feedbackID)

    if session['username']:
        db.session.delete(feedback)
        db.session.commit()

        return redirect('/feedbacks')

    else: 
        flash("You do not have permission to delete this post")
        return redirect('/feedbacks')


@app.route("/feedback/<int:feedbackID>/edit",  methods=['POST'])
def edit_feedback(feedbackID):

    feedback = Feedback.query.get_or_404(feedbackID)
    form = feedback_form()


    if 'username' in session:
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            feedback.username = feedback.username

            db.session.commit()
        
            return redirect('/feedbacks')

    else: 
            flash("You do not have permission to edit this post")
            return redirect('/feedbacks')
    
    
    return render_template('edit_feedback.html',form=form, feedback=feedback)



    
