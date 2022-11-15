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
    type_id = IntegerField(column_name='id')
    name = CharField(column_name='name', null=True)
    vegetable = BooleanField(column_name='vegetable')
    fruit = BooleanField(column_name='fruit')
    mushroom = BooleanField(column_name='mushroom')
    meat = BooleanField(column_name='meat')
    eggs = BooleanField(column_name='eggs')
    seafood = BooleanField(column_name='seafood')
    milk = BooleanField(column_name='milk')
    class Meta:
        table_name = 'types'

class UnitMeasure(BaseModel):
    unitmeasure_id = IntegerField(column_name='id')
    name = CharField(column_name='name', null=True)
    class Meta:
        table_name = 'unitmeasures'

class Ingredient(BaseModel):
    ingredient_id = IntegerField(column_name='id')
    name = CharField(column_name='name', null=True)
    type_id = ForeignKeyField(column_name='typeid')
    unitmeasure_id = ForeignKeyField(column_name='unitmeasureid')
    class Meta:
        table_name = 'ingredients'

class Cuisine(BaseModel):
    cuisine_id = IntegerField(column_name='id')
    name = CharField(column_name='name', null=True)
    class Meta:
        table_name = 'cuisines'

class Step(BaseModel):
    step_id = IntegerField(column_name='id')
    text = CharField(column_name='text', null=True)
    class Meta:
        table_name = 'steps'

class Recipe(BaseModel):
    recipe_id = IntegerField(column_name='id')
    name = CharField(column_name='name', null=True)
    inf = CharField(column_name='information', null=True)
    cuisine_id = ForeignKeyField(column_name='cuisineid')
    count_steps = IntegerField(column_name='countsteps')
    first_step_id = IntegerField(column_name='firststepid')
    count_likes = IntegerField(column_name='countlikes')
    class Meta:
        table_name = 'recipes'

class User(BaseModel):
    user_id = IntegerField(column_name='id')
    name = CharField(column_name='username', null=True)
    password = CharField(column_name='userpassword', null=True)
    class Meta:
        table_name = 'users'



