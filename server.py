#from flask import Flask, render_template, session, redirect, url_for, escape, request, jsonify, abort
from flask import Flask, jsonify, request, abort
from flask_restful import Resource, Api
from  models import *

app = Flask(__name__)
api = Api(app)


class index(Resource):
    def get(self):
        return jsonify({'message': 'index'})
    def post(self):
        data = request.get_json()
        return data['input']
class login(Resource):
    def get(self):
        return jsonify({'message': 'login'})
    def post(self):
        query = User.select()
        user_selected = query.dicts().execute()
        data = request.get_json()
        for user in user_selected:
            if user['name'] == data['name']:
                if user['password'] == data['password']:
                    return user
                abort(401)
        abort(401)

class registration(Resource):
    def get(self):
        return jsonify({'message': 'registration'})
    def post(self):
        query = User.select()
        user_selected = query.dicts().execute()
        data = request.get_json() #{"name" : "Mila", "password" : "ilikekittys", "replay" : "ilikekittys"}
        for user in user_selected:
            if user['name'] == data['name']:
                abort(401)
        if data['password'] == data['replay']:
            User.create(id=user['id']+1, name=data['name'], password=data['password'])
            user = User.get(User.id == user['id']+1)
            return user
        abort(401)

class search(Resource):
    def get(self, input):   #input = "search words"
        query = Recipe.select()
        recipe_selected = query.dicts().execute()
        output = []
        for recipe in recipe_selected:
            if input in recipe["name"]:
                output.append(recipe)
        if output == []:
            abort(404)
        return output

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

class recipe(Resource):
    def get(self, recipe_id):
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
        Recipe.create(id=recipe["id"]+1, name=data["name"], inf=data["inf"], cuisineid=data["cuisineid"], steps=data["steps"], countlikes=0)
        recipe = Recipe.get(Recipe.id == recipe["id"]+1)
        query = StrFavorite.update(name=StrFavorite.recipesid + ';0').where(StrFavorite.id > 0)  #добавляем новый рецепт в матрицу избранного
        query.execute()
        StrIngredient.create(id=recipe.id)

        return recipe










api.add_resource(index, '/')
api.add_resource(login, '/login')
api.add_resource(registration, '/registration')
api.add_resource(search, '/search')
api.add_resource(favorite, '/favorite')
api.add_resource(recipe, '/recipe')
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

if __name__ == '__main__':
    app.run(debug=True)
