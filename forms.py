from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import InputRequired

class Registration_form(FlaskForm):
    """FORM FOR REGISTERING NEW USER"""

    username = StringField("username", validators=[InputRequired(message="username is required")])
    password = PasswordField("Password", validators=[InputRequired(message="password is required")])
    email = EmailField("Email", validators=[InputRequired(message="email is required")])
    first_name = StringField("First name", validators=[InputRequired(message="first name is required")])
    last_name = StringField("Last name", validators=[InputRequired(message="last name is required")])

class login(FlaskForm):
    """Form FOR EXISTING USER LOGIN"""


    username = StringField("username", validators=[InputRequired(message="username is required")])
    password = PasswordField("Password", validators=[InputRequired(message="password is required")])

class feedback_form(FlaskForm):
    """FORM FOR CREATING A FEEDBACK POST"""

    title= StringField("title", validators=[InputRequired(message="please enter a title")])
    content = StringField("content", validators=[InputRequired(message="content required to create a post")])
    
