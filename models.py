from peewee import *
# docker run --name postgres -p 5432:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_DB=postgres postgres:13.3

conn = PostgresqlDatabase(
            host="localhost",
            database="postgres",
            user="postgres",
            port="5432",
            password="mysecretpassword")

class BaseModel(Model):
    class Meta:
        database = conn

class Type(BaseModel):
    id = PrimaryKeyField(column_name='id')
    name = CharField(column_name='name')
    class Meta:
        table_name = 'types'

class UnitMeasure(BaseModel):
    id = PrimaryKeyField(column_name='id')
    name = CharField(column_name='name')
    class Meta:
        table_name = 'unitmeasures'

class Ingredient(BaseModel):
    id = PrimaryKeyField(column_name='id')
    name = CharField(column_name='name')
    typeid = ForeignKeyField(Type, to_field='id')
    unitmeasureid = ForeignKeyField(UnitMeasure, to_field='id')
    class Meta:
        table_name = 'ingredients'

class Cuisine(BaseModel):
    id = PrimaryKeyField(column_name='id')
    name = CharField(column_name='name')
    class Meta:
        table_name = 'cuisines'

class Recipe(BaseModel):
    id = PrimaryKeyField(column_name='id')
    name = CharField(column_name='name')
    inf = CharField(column_name='information', null=True)
    cuisineid = ForeignKeyField(Cuisine, to_field='id')
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
    userid = ForeignKeyField(User, to_field='id')
    ingredientsid = CharField(column_name='ingredientsid')
    class Meta:
        table_name = 'matrixfridge'

class StrIngredient(BaseModel):
    recipeid = ForeignKeyField(Recipe, to_field='id')
    ingredientsid = CharField(column_name='ingredientsid')
    class Meta:
        table_name = 'matrixingredients'

class StrFavorite(BaseModel):
    id = PrimaryKeyField(column_name='userid')
    recipesid = CharField(column_name='recipesid')
    class Meta:
        table_name = 'matrixfavorite'

maxusers = 50

def favorite_to_matrix():
    query = StrFavorite.select()
    str_selected = query.dicts().execute()
    mid = 0
    cingr = 0
    for str in str_selected:
        cingr = len(str["recipesid"].split(';'))
        mid = max(mid, str["id"])
    matrix = [[0]*cingr]*mid
    for str in str_selected:
        a = str["recipesid"].split(';')
        for i in range(cingr):
            matrix[str["id"]-1][i] = int(a[i])   #id start with 1; index start with 0
    return matrix

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



