'''
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
    submit = SubmitField("Добавить/изменить/удалить продукт")


class TypeForm(FlaskForm):
    dataa = StringField("Введите тип продукта, который хотите добавить/изменить/удалить:", validators=[DataRequired()])
    submit = SubmitField("Выбрать")


class ProductForm(FlaskForm):
    dataa = StringField("Выберите продукт, который хотите добавить/изменить/удалить, из списка:", validators=[DataRequired()])
    amount = StringField("Введите количество продукта(жидкости в мл, яйца в штуках, все остальное в гр)", validators=[DataRequired()])
    submit = SubmitField("Выбрать")


class Search1(FlaskForm):
    submit = SubmitField("Поиск по кухням")


class Search2(FlaskForm):
    submit = SubmitField("Поиск по названию рецепта")
'''
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


class SearchForm(FlaskForm):
    gender = SelectField('Введите пол', choices=[
        ('М', 'Мальчик'),
        ('Ж', 'Девочка'),
    ])
    age = SelectField('Введите возраст', choices=[
        (2, '2 года'),
        (3, '3 года'),
        (4, '4 года'),
        (5, '5 лет'),
        (6, '6 лет'),
        (7, '7 лет'),
        (8, '8 лет'),
        (9, '9 лет'),
        (10, '10 лет'),
        (11, '11-13 лет'),
        (12, '14-17 лет'),
        (13, '18-20 лет'),
        (14, '21-29 лет'),
        (15, '30-39 лет'),
        (16, '40-49 лет'),
        (17, '50-60 лет'),
    ])
    activity = SelectField('Введите тип физической активности', choices=[
        ('Низкая', 'Низкая'),
        ('Умеренная', 'Умеренная'),
        ('Высокая', 'Высокая'),
    ])
    submit = SubmitField('Показать рацион')


