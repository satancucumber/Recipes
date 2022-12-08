#from flask import Flask, render_template, session, redirect, url_for, escape, request, jsonify, abort
from flask import Flask, jsonify, request, abort, render_template
from server.app import app
from flask_restful import Resource, Api, reqparse
from server.app.models import *
api = Api(app)

class index(Resource):
    def get(self):
        return "Hello, Word!"

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
    '''
    def patch(self):
        data = request.get_json()   # {"ingredientid" : 6, "user_id" : 1, "recipe_id" : 2, "new_count" = 2}
        if "ingredientid" in data:
            if "user_id" in data and "new_count" in data:
                fridge = fridge_to_matrix()[data["user_id"]]
                str_user = list(map(str, fridge))
                str_user[data["ingredientid"]-1] = str(data["new_count"])
                string = StrFridge(userid=data["user_id"])
                string.ingredientsid = ";".join(str_user)
                string.save()
                return "Ingredient changed!"
            if "recipe_id" in data and "new_count" in data:
                str = StrIngredient(userid=data["recipe_id"])
                str_recipe = str.ingredientsid.split(";")
                str_recipe[data["ingredientid"] - 1] = data["new_count"]
                str.ingredientsid = ";".join(str_recipe)
                str.save()
                return "Ingredient changed!"
    '''

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
            return search_id("recipe", int(id))         #record by id
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

class user(Resource):
    def get(self):
        query = User.select()
        user_selected = query.dicts().execute()
        id = request.args.get('id')
        name = request.args.get('name')
        password = request.args.get('password')
        if id:
            return search_id("user", int(id))        #record by id
        elif name and password:
            for user in user_selected:
                if user["name"] == name:
                    if user["password"] == password:
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

'''
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
    return '''
'''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
        
'''

'''

@app.route('/logout')
def logout():
    # удалить из сессии имя пользователя, если оно там есть
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

'''


