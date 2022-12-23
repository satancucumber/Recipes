from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from server.app.models import User


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class RegistrationForm(FlaskForm):
    username = StringField("Имя пользователя: ", validators=[DataRequired()])
    password = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=8, max=50), EqualTo('password_repeat', message='Пароли должны совпадать')])
    password_repeat = PasswordField("Повторите пароль: ", validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField("Зарегистрироваться")
    def validate_username(self, username):
        try:
            user = User.get(User.name == username.data)
        except:
            user = None
        if user is not None:
            raise ValidationError('Имя пользователя уже используется.')



class EditPassForm(FlaskForm):
    curr_pass = PasswordField("Текущий пароль: ", validators=[DataRequired(), Length(min= 8, max= 50)])
    new_pass = PasswordField("Новый пароль: ", validators=[DataRequired(), Length(min= 8, max= 50), EqualTo('password_repeat', message='Пароли должны совпадать')])
    password_repeat = PasswordField("Повторите новый пароль: ", validators=[DataRequired(), Length(min= 8, max= 50)])
    submit = SubmitField("Сменить пароль")


class NewProductForm(FlaskForm):
    submit = SubmitField("Добавить новый продукт")


class TypeForm(FlaskForm):
    dataa = StringField("Введите тип продукта, который хотите добавить:", validators=[DataRequired()])
    submit = SubmitField("Выбрать")


class ProductForm(FlaskForm):
    dataa = StringField("Выберите продукт, который хотите добавить, из списка:", validators=[DataRequired()])
    submit = SubmitField("Выбрать")


class AmountForm(FlaskForm):
    dataa = StringField("Введите количество продукта:", validators=[DataRequired(), Length(min=1, max=5)])
    submit = SubmitField("Выбрать")

