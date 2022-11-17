CREATE TABLE Types
(
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(256) NOT NULL
);

CREATE TABLE UnitMeasures
(
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(256) NOT NULL
);

CREATE TABLE Ingredients
(
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(256) NOT NULL,
    TypeId INT REFERENCES Types (Id) NOT NULL DEFAULT 1,
    UnitMeasureID INT REFERENCES UnitMeasures (Id) NOT NULL DEFAULT 1
);

CREATE TABLE Cuisines
(
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(256) NOT NULL
);

CREATE TABLE Recipes
(
    Id SERIAL PRIMARY KEY,
    Name VARCHAR(256) NOT NULL,
    Information VARCHAR(256),
    CuisineID INT REFERENCES Cuisines (Id) NOT NULL,
    CountSteps INT NOT NULL DEFAULT 1,
    Steps VARCHAR(4048) NOT NULL,
    CountLikes INT NOT NULL DEFAULT 0
);

CREATE TABLE Users
(
    Id SERIAL PRIMARY KEY,
    UserName VARCHAR(256) NOT NULL,
    UserPassword VARCHAR(256) NOT NULL
);

CREATE TABLE MatrixFridge
(
    UserID SERIAL PRIMARY KEY,
    IngredientsID VARCHAR(2048) NOT NULL
);

CREATE TABLE MatrixIngredients
(
    RecipeID SERIAL PRIMARY KEY,
    IngredientsID VARCHAR(2048) NOT NULL
);

CREATE TABLE MatrixFavorite
(
    UserID SERIAL PRIMARY KEY,
    RecipesID VARCHAR(2048) NOT NULL
);


INSERT INTO Types (Name)
VALUES
       ('Овощи'),
       ('Фрукты'),
       ('Крупы'),
       ('Злаки'),
       ('Бобовые'),
       ('Приправы'),
       ('Травы'),
       ('Растительные масла'),
       ('Орехи'),
       ('Молочные продукты'),
       ('Яйца'),
       ('Морепродукты'),
       ('Мясо')

INSERT INTO UnitMeasures (Name)
VALUES
       ('шт'),
       ('гр'),
       ('кг'),
       ('мл'),
       ('ст. л'),
       ('ч. л'),
       ('ст'),
       ('по вкусу')
