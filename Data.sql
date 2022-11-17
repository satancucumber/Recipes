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

INSERT INTO Ingredients (Name, TypeId, UnitMeasureID)
VALUES
       ('Сыр', 10, 2),
       ('Хлеб', 4, 1),
       ('Чеснок', 6, 8),
       ('Сливочное масло', 10, 2),
       ('Растительное масло', 8, 8)

INSERT INTO Cuisines (Name)
VALUES
       ('Домашняя')

INSERT INTO MatrixFavorite (RecipesID)
VALUES
       ('0;0;0'),
       ('0;0;1')

INSERT INTO MatrixFridge (IngredientsID)
VALUES
       ('0;0;0;0;0'),
       ('0;0;0;0;0')

INSERT INTO MatrixIngredients (IngredientsID)
VALUES
       ('30;1;0;0;1'),
       ('30;1;10;0;1'),
       ('0;1;0;1;1')

INSERT INTO Users (UserName, UserPassword)
VALUES
       ('admin', 'adminadmin'),
       ('Gleb', 'secretpassword')