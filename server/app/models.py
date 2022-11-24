from peewee import *
# docker run --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=postgres postgres:13.3

#connection with database

conn = PostgresqlDatabase(
            host="localhost",
            database="postgres",
            user="postgres",
            port="5432",
            password="mysecretpassword")

#initialization tables

class BaseModel(Model):
    class Meta:
        database = conn

class Type(BaseModel):
    id = AutoField(column_name='id')
    name = CharField(column_name='name')
    class Meta:
        table_name = 'types'

class UnitMeasure(BaseModel):
    id = AutoField(column_name='id')
    name = CharField(column_name='name')
    class Meta:
        table_name = 'unitmeasures'

class Ingredient(BaseModel):
    id = AutoField(column_name='id')
    name = CharField(column_name='name')
    typeid = IntegerField(column_name='typeid')
    unitmeasureid = IntegerField(column_name='unitmeasureid')
    class Meta:
        table_name = 'ingredients'

class Cuisine(BaseModel):
    id = AutoField(column_name='id')
    name = CharField(column_name='name')
    class Meta:
        table_name = 'cuisines'

class Recipe(BaseModel):
    id = AutoField(column_name='id')
    name = CharField(column_name='name')
    inf = CharField(column_name='information', null=True)
    cuisineid = IntegerField(column_name='cuisineid')
    countsteps = IntegerField(column_name='countsteps')
    steps = CharField(column_name='steps')
    countlikes = IntegerField(column_name='countlikes')
    class Meta:
        table_name = 'recipes'

class User(BaseModel):
    id = AutoField(column_name='id')
    name = CharField(column_name='username')
    password = CharField(column_name='userpassword')
    class Meta:
        table_name = 'users'

class StrFridge(BaseModel):
    userid = AutoField(column_name='userid')
    ingredientsid = CharField(column_name='ingredientsid')
    class Meta:
        table_name = 'matrixfridge'

class StrIngredient(BaseModel):
    recipeid = AutoField(column_name='recipeid')
    ingredientsid = CharField(column_name='ingredientsid')
    class Meta:
        table_name = 'matrixingredients'

class StrFavorite(BaseModel):
    userid = AutoField(column_name='userid')
    recipesid = CharField(column_name='recipesid')
    class Meta:
        table_name = 'matrixfavorite'

#query by name of the table

def object(table):
    if table == "type":
        return Type.select()
    elif table == "unitmeasure":
        return UnitMeasure.select()
    elif table == "ingredient":
        return Ingredient.select()
    elif table == "cuisine":
        return Cuisine.select()
    elif table == "recipe":
        return Recipe.select()
    elif table == "user":
        return User.select()

#count of rows in the table

def cnt(table):
    query = object(table)
    table_selected = query.dicts().execute()
    cnt = 0
    for value in table_selected:            # {"id" = 1, "name" = "admin", "password" = "adminadmin"}
        cnt += 1
    return cnt

#from table to matrix

def fridge_to_matrix():
    query = StrFridge.select()
    str_selected = query.dicts().execute()
    matrix = [[0]] * cnt("user")
    for str in str_selected:
        ingredientsid = list(map(int, str["ingredientsid"].split(';')))
        matrix[str["userid"] - 1] = ingredientsid  # id start with 1; index start with 0
    return matrix
def ingredient_to_matrix():
    query = StrIngredient.select()
    str_selected = query.dicts().execute()
    matrix = [[0]] * cnt("recipe")
    for str in str_selected:
        ingredientsid = list(map(int, str["ingredientsid"].split(';')))
        matrix[str["recipeid"] - 1] = ingredientsid  # id start with 1; index start with 0
    return matrix
def favorite_to_matrix():
    query = StrFavorite.select()
    str_selected = query.dicts().execute()
    matrix = [[0]]*cnt("user")
    for str in str_selected:      # {"userid" : 1, "recipesid" :}
        recipesid = list(map(int, str["recipesid"].split(';')))
        matrix[str["userid"]-1] = recipesid   #id start with 1; index start with 0
    return matrix



def new_user():
    StrFridge.create(ingredientsid = ";".join(['0'] * cnt("ingredient")))
    StrFavorite.create(recipesid = ";".join(['0'] * cnt("recipe")))
    return 0
#new_user()
def new_recipe(data): # data = "cnt_id;id;cnt;id;cnt;..."
    input = data.split(";")   # ["7", "1", "10", ...]
    cnt_id = int(input.pop(0))
    new = ['0']*cnt("ingredient")  # ['0', ...]
    for i in range(cnt_id):
        new[int(input[i*2])-1] = input[i*2+1]
    StrIngredient.create(ingredientsid = ";".join(new))
    query = StrFavorite.update(recipesid = StrFavorite.recipesid + ';0')  # добавляем новый рецепт в матрицу избранного
    query.execute()
    return 0
def new_ingredient():
    query = StrIngredient.update(ingredientsid=StrIngredient.ingredientsid + ";0")  # добавляем новый ингредиент в матрицу ингредиентов
    query.execute()
    query = StrFridge.update(ingredientsid=StrFridge.ingredientsid + ";0")  # добавляем новый ингредиент в матрицу холодильника
    query.execute()
    return 0

def search_name(table, data):  # data = "name"
    query = object(table)
    table_selected = query.dicts().execute()
    for value in table_selected:
        if value["name"] == data:
            return value
    return -1
def search_id(table, data):  #data = int id
    query = object(table)
    table_selected = query.dicts().execute()
    for value in table_selected:
        if value["id"] == data:
            return value
    return -1

def search_substring(table, data):  # data = "name"
    query = object(table)
    table_selected = query.dicts().execute()
    output = []
    for value in table_selected:
        if data in value["name"]:
            output.append(value)
    if output != []:
        return output
    return -1

def search_typeid(data):
    query = Ingredient.select()
    table_selected = query.dicts().execute()
    output = []
    for value in table_selected:
        if value["typeid"] == int(data):
            output.append(value)
    if output != []:
        return output
    return -1

def post_item(table, data):
    if search_name(table, data["name"]) == -1:
        table.create(name=data["name"])
        return table, " post!"
    return "Such ",  table, " already exists!"


#def new_user_name(data): # {"name" = "Mila", "password" = }

#print(Recipe.get(Recipe.id == 1))



#print(favorite_to_matrix())

#user = User.get(User.id == 1)
#print(user.name, user.password)

#request = {"name" : "Mila", "password" : "ilikekittys", "replay" : "ilikekittys"}
#User.create(id = 3, name = request["name"], password = request["password"])    #auto increment???????
#user = User.get(User.id == 3)
#user.save()

#user = User.get(User.id == 3)
#print(user)


