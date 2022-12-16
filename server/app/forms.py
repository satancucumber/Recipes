from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    name = StringField("Имя пользователя: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min= 8, max= 50)])
    submit = SubmitField("Войти")

class EditPass(FlaskForm):
    curr_pass = PasswordField("Текущий пароль: ", validators=[DataRequired(), Length(min= 8, max= 50)])
    new_pass = PasswordField("Новый пароль: ", validators=[DataRequired(), Length(min= 8, max= 50)])
    repeat_pass = PasswordField("Повторите новый пароль: ", validators=[[DataRequired(), Length(min= 8, max= 50)]])
    submit = SubmitField("Сменить пароль")

class Regist(FlaskForm):
    name = StringField("Имя пользователя: ", validators=[DataRequired()])
    pas = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=8, max=50)])
    repeat_pass = PasswordField("Повторите пароль: ", validators=[[DataRequired(), Length(min=8, max=50)]])
    submit = SubmitField("Зарегистрироваться")