#from flask import Flask, render_template, session, redirect, url_for, escape, request, jsonify, abort
from flask import Flask, jsonify, request, abort, render_template
from server.app import app
from flask_restful import Resource, Api
from server.app.models import *
api = Api(app)

class index(Resource):
    def get(self):
        return "Hello, Word!"

class user(Resource):
    def get(self, id, name, password):
        query = User.select()
        user_selected = query.dicts().execute()
        if id:
            return search_id("user", id)
        elif name and password:
            for user in user_selected:
                if user["id"] == name:
                    if user["password"] == password:
                        return "You login!"
                return "Invalid password!"
            return "Invalid username!"
        else:
            users = []
            for user in user_selected:
                users.append(user)
            return users

    def post(self):
        query = User.select()
        user_selected = query.dicts().execute()
        data = request.get_json()  # {"name" : "Mila", "password" : "ilikekittys", "replay" : "ilikekittys"}
        for user in user_selected:
            if user['name'] == data['name']:
                return "A user with this name already exists!"
        if data['password'] == data['replay']:
            new_user()
            User.create(name=data['name'], password=data['password'])
            return "You are registered!"
        return "Passwords don't match!"

class type(Resource):
    def get(self, type_id):   #data = "search words"
        if type_id:
            return search_id("type", type_id)
        query = Type.select()
        type_selected = query.dicts().execute()
        output = []
        for type in type_selected:
            output.append(type)
        return output

class ingredient(Resource):
    def get(self, id, name, type_id):
        query = Ingredient.select()
        ing_selected = query.dicts().execute()
        output = []
        if id:
            return search_id("ingredient", id)
        if name and type_id:
            for ing in ing_selected:
                if ing["typeid"] == type_id and name in ing["name"]:
                    output.append(ing)
            return output
        if type_id:
            for ing in ing_selected:
                if ing["typeid"] == type_id:
                    output.append(ing)
            return output
        if name:
            for ing in ing_selected:
                if name in ing["name"]:
                    output.append(ing)
            return output
        for ing in ing_selected:
            output.append(ing)
        return output

'''
class recipe(Resource):
    def get(self, id, name, user_id):
        query = Recipe.select()
        recipe_selected = query.dicts().execute()
        for recipe in recipe_selected:
            if recipe["id"] == recipe_id:
                return recipe
            abort(404)
    def post(self):
        query = Recipe.select()
        recipe_selected = query.dicts().execute()
        data = request.get_json() # {"ingredients" = "counting;id;count;..." ,"name" = "", "inf" = "", "cuisineid" = int, "countsteps" = int, "steps" = "", "countlikes" = int}
        for recipe in query.dicts().execute():
            if recipe["name"] == data["name"]:
                abort(404)
        Recipe.create(name=data["name"], inf=data["inf"], cuisineid=data["cuisineid"], steps=data["steps"], countlikes=0)
        recipe = Recipe.get(Recipe.id == recipe["id"]+1)
        query = StrFavorite.update(name=StrFavorite.recipesid + ';0').where(StrFavorite.id > 0)  #добавляем новый рецепт в матрицу избранного
        query.execute()
        StrIngredient.create(id=recipe.id)

        return recipe
class favorite(Resource):
    def get(self, user_id):
        query = Recipe.select()
        recipe_selected = query.dicts().execute()
        output = []
        likes = favorite_to_matrix()[user_id-1]
        for recipe in recipe_selected:
            if likes[recipe["id"] - 1] != 0:
                output.append(recipe)
        if output == []:
            abort(404)
        return output
    def put(self, user_id, recipe_id):
        str = StrFavorite.get(StrFavorite.id == user_id)
        change = str.recipesid
        change = change.split(';')
        if change[recipe_id-1] == '0':
            change[recipe_id-1] = '1'
        elif change[recipe_id-1] == '1':
            change[recipe_id-1] = '0'
        str.recipesid = ";".join(change)
        str.save()
'''

api.add_resource(index, '/')
api.add_resource(user, '/api/v1/login')
api.add_resource(type, '/api/v1/type')
api.add_resource(ingredient, '/api/v1/ingredient')


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


