from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms.validators import DataRequired, EqualTo
from models import NewPerson

class RegisterForm(FlaskForm):
  userid = StringField('userid', validators=[DataRequired()])
  username = StringField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired(), EqualTo('repassword')])# equalto 비밀번호가 같은지 확인
  repassword = PasswordField('repassword', validators=[DataRequired()])

class LoginForm(FlaskForm):
  class UserPassword(object):

      def __init__(self, message=None):
        self.message = message

      def __call__(self, form, field):
        userid = form['userid'].data
        password = field.data

        newper = NewPerson.query.filter_by(userid=userid).first()
        if newper.password != password:
          raise ValueError('Wrong Password')

  userid = StringField('userid', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired(), UserPassword()])