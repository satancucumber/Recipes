# from flask import Flask, render_template, session, redirect, url_for, escape, request, jsonify, abort
# import flask
from flask import Flask, jsonify, request, abort, render_template, Response, url_for, flash, redirect, session
from server.app import app
# from flask_restful import Resource, Api, reqparse
from server.app.models import *
# import requests
from flask_login import current_user, login_user
from server.app.models import User
from server.app.forms import LoginForm, RegistrationForm, EditPassForm, NewProductForm, TypeForm, ProductForm, AmountForm
from flask_login import logout_user, login_required
# import jinja2
# from werkzeug.urls import url_parse
# api = Api(app)

def get_types_name():
    out = []
    query = Type.select()
    type_selected = query.dicts().execute()
    for type in type_selected:
        out.append(type["name"])
    return out


def get_ingredients_name(ingredientsid):
    out = []
    for id in ingredientsid:
        ingredient = Ingredient.get(Ingredient.id == id)
        out.append(ingredient.name)
    return out
@app.route('/new_product1/<m>', methods=['GET', 'PATCH', 'POST'])
def new_product2(m):
    form3 = AmountForm()
    ing = Ingredient.get(Ingredient.id==id)
    unit = UnitMeasure.get(UnitMeasure.id == m)
    unit1 = 'Укажите количество продукта в ' + unit.name
    if form3.validate_on_submit():
        try:
            amount = form3.dataa.data
            fridge = StrFridge.get(StrFridge.userid == current_user.id)
            fridge.ingredientsid[ing.id-1] = amount
            fridge.save()
        except:
            flash('Ошибка')
        return redirect(url_for('fridge'))
    return render_template('new_product.html', title='Добавление нового продукта в холодильник', mess=unit1,
                           form=form3)
@app.route('/new_product/<id>', methods=['GET', 'PATCH', 'POST'])
def new_product1(id):
    form2 = ProductForm()
    type = Type.get(Type.id == id)
    meow = get_ingredients_name(type.search_ingredients_id())
    if form2.validate_on_submit():
        try:
            ing = Ingredient.get(Ingredient.name == form2.dataa.data)
            m = ing.unitmeasureid
        except:
            flash('Неправильное название ингредиента')
            return redirect(url_for('fridge'))
        return redirect(url_for('new_product2', m=m))

    return render_template('new_product.html', title='Добавление нового продукта в холодильник', data=meow,
                           form=form2)


@app.route('/new_product', methods=['GET', 'PATCH', 'POST'])
def new_product():
    form1 = TypeForm()
    types = get_types_name()
    if form1.validate_on_submit():
        try:
            type = Type.get(Type.name == form1.dataa.data)
            id = type.id
        except:
            flash('Неправильно введено название типа продукта')
            return redirect(url_for('fridge'))
        return redirect(url_for('new_product1', id=id))
    return render_template('new_product.html', title='Выбор типа нового продукта в холодильник', data=types, form=form1)


def ingr():
    fridge = StrFridge.get(StrFridge.userid == current_user.id)
    fr = fridge.ingredientsid
    ing = []
    for i in range(len(fr)):
        if fr[i] != 0:
            ingr = Ingredient.get(Ingredient.id == i+1)
            unit = UnitMeasure.get(UnitMeasure.id == ingr.unitmeasureid)
            ing.append(ingr.name+' '+str(fr[i])+' '+unit.name)
    return ing


@app.route('/fridge', methods=['GET', 'POST', 'PATCH'])
def fridge():
    ing = ingr()
    form = NewProductForm()
    if form.validate_on_submit():
        return redirect(url_for('new_product'))
    return render_template('fridge.html', title='Холодильник', fridge=ing, form=form)




@app.route('/')
@app.route('/index')
@login_required
def index():
    user = User.get(User.id == session['id'])
    if len(user.likes) <= 5:
        flash('Заполните холодильник, чтобы получить рекомедации')
        return redirect(url_for('fridge'))
    return render_template('main.html', title='Интеллектуальная система подборки рецептов')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.get(User.name == form.username.data)
        except:
            user = None
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        session['id'] = user.id
        return redirect(url_for('index'))
    return render_template('login.html', title='Вход', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/registration', methods = ['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user()
        User.create(name=form.username.data, password_hash='fssfsf')
        user = User.get(User.name == form.username.data)
        user.set_password(form.password.data)
        user.save()
        flash('Поздравляю, вы успешно зарегистрировались!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Регистрация', form=form)

@app.route('/user', methods = ['GET', 'POST'])
@login_required
def user():
    form = EditPassForm()
    user = User.get(name=current_user.name)
    if form.validate_on_submit():
        if user.check_password(form.curr_pass.data):
            user.set_password(form.new_pass.data)
            user.save()
            flash('Смена пароля произошла успешно')
            return redirect(url_for('user'))
        else:
            flash('Текущий пароль введен неверно')
    return render_template('user.html', user=user, form=form, title='Профиль')


'''

class index(Resource):
    def get(self):
        form = LoginForm()
        print(form.name.data, ' ', form.password.data)
        if form.validate_on_submit():
            url = "http://127.0.0.1:5000/api/v1/login"
            request = {"name": form.name.data, "password": form.password.data}
            print(request)
            r = requests.get(url, json=request)
            if r == '<Response [200]>':
                return redirect(url_for('api/v1/login'))
        return Response(render_template('base.html'),mimetype='text/html')

class type(Resource):
    def get(self):
        type_id = request.args.get('type_id')
        if type_id:
            return search_id("type", int(type_id))      #record by id
        query = Type.select()
        type_selected = query.dicts().execute()
        output = []
        for type in type_selected:
            output.append(type)
        return output                     #all records

    def post(self):
        data = request.get_json()   # {"name" : "Грибы"}
        if search_name("type", data["name"]) == -1:
            Type.create(name=data["name"])
            return "Type post!"
        return "Such an type already exists!"

class unitmeasure(Resource):
    def get(self):
        id = request.args.get('id')
        if id:
            return search_id("unitmeasure", int(id))    #record by id
        query = UnitMeasure.select()
        unit_selected = query.dicts().execute()
        output = []
        for unit in unit_selected:
            output.append(unit)
        return output                         #all records

    def post(self):
        data = request.get_json()   # {"name" : "уп"}
        if search_name("unitmeasure", data["name"]) == -1:
            UnitMeasure.create(name=data["name"])
            return "Unit measure post!"
        return "Such an unit measure already exists!"

class ingredient(Resource):
    def get(self):
        id = request.args.get('id')
        name = request.args.get('name')
        type_id = request.args.get('type_id')
        user_id = request.args.get('user_id')
        recipe_id = request.args.get('recipe_id')
        query = Ingredient.select()
        ing_selected = query.dicts().execute()
        output = []
        if id:
            return search_id("ingredient", id)              #record by id
        if name and type_id:
            for ing in ing_selected:
                if ing["typeid"] == int(type_id) and name in ing["name"]:
                    output.append(ing)
            return output                                 #records by name and type_id
        if type_id:
            for ing in ing_selected:
                if ing["typeid"] == int(type_id):
                    output.append(ing)
            return output                             #records by type_id
        if name:
            for ing in ing_selected:
                if name in ing["name"]:
                    output.append(ing)
            return output                       #records by name
        if user_id:
            user_str = fridge_to_matrix()[int(user_id)-1]
            for ing in ing_selected:
                if user_str[ing["id"]-1] != 0:
                    output.append(ing)
                    output.append(user_str[ing["id"]-1])
            return output                                     #records by user_id
        if recipe_id:
            recipe_str = ingredient_to_matrix()[int(recipe_id) - 1]
            for ing in ing_selected:
                if recipe_str[ing["id"] - 1] != 0:
                    output.append(ing)
                    output.append(recipe_str[ing["id"] - 1])
            return output                                  #ingredients with count for recipe with recipe_id
        for ing in ing_selected:
            output.append(ing)
        return output                #all records

    def post(self):
        data = request.get_json()   # {"name" : "Огурец", "typeid" = 1, "unitmeasureid" = 1}
        if search_name("ingredient", data["name"]) == -1:
            new_ingredient()
            Ingredient.create(name=data["name"], typeid=data["typeid"], unitmeasureid=data["unitmeasureid"])
            return "Ingredient post!"
        return "Such an ingredient already exists!"

class cuisine(Resource):
    def get(self):
        id = request.args.get('id')
        if id:
            return search_id("cuisine", int(id))   #record by id
        query = Cuisine.select()
        unit_selected = query.dicts().execute()
        output = []
        for unit in unit_selected:
            output.append(unit)
        return output               #all records

    def post(self):
        data = request.get_json()   # {"name" : "Японская"}
        if search_name("cuisine", data["name"]) == -1:
            Cuisine.create(name=data["name"])
            return "Cuisine post!"
        return "Such an cuisine already exists!"

class recipe(Resource):
    def get(self):
        id = request.args.get('id')
        name = request.args.get('name')
        cuisine_id = request.args.get('cuisine_id')
        user_id = request.args.get('user_id')
        query = Recipe.select()
        recipe_selected = query.dicts().execute()
        output = []
        if id:
            record = Recipe.get(Recipe.id == id)
            output.append(record.name)
            output.append(record.inf)
            recordcuisine = Cuisine.get(Cuisine.id == record.cuisineid)
            output.append(recordcuisine.name)
            ingredients = StrIngredient.get(StrIngredient.recipeid == id)
            k = 0
            ingred = []
            for i in range(len(ingredients.ingredientsid)):
                if ingredients.ingredientsid[i] != 0:
                    k += 1
                    ing = []
                    recordingredients = Ingredient.get(Ingredient.id == i+1)
                    ing.append(recordingredients.name)
                    ing.append(ingredients.ingredientsid[i])
                    recordunitmesure = UnitMeasure.get(UnitMeasure.id == recordingredients.unitmeasureid)
                    ing.append(recordunitmesure.name)
                    ingred.append(ing)
            output.append(k)
            output.append(ingred)
            output.append(record.countsteps)
            output.append(record.steps)
            return output     #record by id
        if name and cuisine_id:
            for rec in recipe_selected:
                if rec["cuisineid"] == int(cuisine_id) and name in rec["name"]:
                    output.append(rec)
            return output                     #records by name and cuisine_id
        if name:
            return search_substring("recipe", name)                 #records by name
        if cuisine_id:
            for rec in recipe_selected:
                if rec["cuisineid"] == int(cuisine_id):
                    output.append(rec)
            return output               #records by cuisine_id
        if user_id:
            user_str = favorite_to_matrix()[int(user_id) - 1]
            for rec in recipe_selected:
                if user_str[rec["id"] - 1] == 1:
                    output.append(rec)
            return output                   #favorite user with user_id
        for rec in recipe_selected:
            output.append(rec)
        return output      #all records

    def post(self):
        data = request.get_json()  # {"ingredients" : "2;6;1;2;1" ,"name" : "Тост с огурцом", "inf" : "Хрустящий хлеб с огурцом", "cuisineid" : 1, "countsteps" : 2, "steps" : "Пожарить хлеб с двух сторон до хрустящей корочки*Положить на хлеб порезанный огурец"}
        if search_name("recipe", data["name"]) == -1:
            new_recipe(data["ingredients"])
            arraysteps = data["steps"].split("*")
            Recipe.create(name=data["name"], inf=data["inf"], cuisineid=data["cuisineid"], countsteps=data["countsteps"], steps=arraysteps)
            return "Recipe post!"
        return "Such an recipe already exists!"

    def patch(self):
        id = request.args.get('id')
        user_id = request.args.get('userid')
        like = request.args.get('like')
        dislike = request.args.get('dislike')

        if user_id and id:
            record = StrFavorite.get(StrFavorite.userid == int(user_id))
            if like:
                if record.recipesid[int(id)-1] == 0:
                    record.recipesid[int(id) - 1] = 1
                    record.save()
                    return "Like put!"
                else:
                    record.recipesid[int(id) - 1] = 0
                    record.save()
                    return "Like unput!"
            if dislike:
                if record.recipesid[int(id)-1] == -1:
                    record.recipesid[int(id) - 1] = 0
                    record.save()
                    return "Dislike unput!"
                else:
                    record.recipesid[int(id) - 1] = -1
                    record.save()
                    return "Dislike put!"
            return "No information about like/dislike!"
        return "No information about user and recipe!"



class user(Resource):
    def get(self):
        query = User.select()
        user_selected = query.dicts().execute()
        data = request.get_json()
        if "id" in data :
            return search_id("user", int(data["id"]))        #record by id
        elif "name" in data and "password" in data:
            for user in user_selected:
                if user["name"] == data["name"]:
                    if user["password"] == data["password"]:
                        return "You login!"
                    return "Invalid password!"
            return "Invalid username!"
        else:
            users = []
            for user in user_selected:
                users.append(user)
            return users                 #all users

    def post(self):
        query = User.select()
        user_selected = query.dicts().execute()
        data = request.get_json()  # {"name" : "Mila", "password" : "ilikekittys", "repeat" : "ilikekittys"}
        for user in user_selected:
            if user['name'] == data['name']:
                return "A user with this name already exists!"
        if data['password'] == data['repeat']:
            new_user()
            User.create(name=data['name'], password=data['password'])
            return "You are registered!"
        return "Passwords don't match!"

    def patch(self):
        query = User.select()
        user_selected = query.dicts().execute()
        data = request.get_json()  # {"name" : "Mila", "password" : "toastwithcucumber", "new_name" : "", "new_password" : "", "repeat" : ""}
        if "name" in data and "password" in data:
            for user in user_selected:
                if user["name"] == data["name"]:
                    if user["password"] == data["password"]:
                        user_change = User(id=user["id"])
                        if "new_name" in data:
                            if search_name("user", data["new_name"]) == -1:
                                user_change.name = data["new_name"]
                                user_change.save()
                                return "Name changed!"
                            return "A user with this name already exists!"
                        if "new_password" in data and "repeat" in data:
                            if data["new_password"] == data["repeat"]:
                                user_change.password = data["new_password"]
                                user_change.save()
                                return "Password changed!"
                            return "Passwords don't match!"
                    return "Invalid password!"
            return "Invalid username!"

#class recomendation(Resource):
#    def get(self):
#        user_id = request.args.get('user_id')
#        return rec(user_id)                   #input: user_id; output: [{}, {}, {}, ...]

api.add_resource(index, '/')
api.add_resource(user, '/api/v1/login', endpoint='login')
api.add_resource(type, '/api/v1/type', endpoint='type')
api.add_resource(ingredient, '/api/v1/ingredient', endpoint='ingredient')
api.add_resource(recipe, '/api/v1/recipe', endpoint='recipe')
api.add_resource(cuisine, '/api/v1/cuisine', endpoint='cuisine')
api.add_resource(unitmeasure, '/api/v1/unitmeasure', endpoint='unitmeasure')
#api.add_resource(recimendation, '/api/v1/recimendation', endpoint='recimendation')


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return 

        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
        




@app.route('/logout')
def logout():
    # удалить из сессии имя пользователя, если оно там есть
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

'''


