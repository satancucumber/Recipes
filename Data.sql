CREATE TABLE Types
(
    Id INT PRIMARY KEY,
    Name VARCHAR(256) NOT NULL,
    Vegetable BOOL,
    Fruit BOOL,
    Mushroom BOOL,
    Meat BOOL,
    Eggs BOOL,
    Seafood BOOL,
    Milk BOOL
);

CREATE TABLE UnitMeasures
(
    Id INT PRIMARY KEY,
    Name VARCHAR(256) NOT NULL
);

CREATE TABLE Ingredients
(
    Id INT PRIMARY KEY,
    Name VARCHAR(256) NOT NULL,
    TypeId INT REFERENCES Types (Id),
    UnitMeasureID INT REFERENCES UnitMeasures (Id)
);

CREATE TABLE Cuisines
(
    Id INT PRIMARY KEY,
    Name VARCHAR(256) NOT NULL
);

CREATE TABLE Steps
(
    Id INT PRIMARY KEY,
    Text VARCHAR(1024) NOT NULL
);

CREATE TABLE Recipes
(
    Id INT PRIMARY KEY,
    Name VARCHAR(256) NOT NULL,
    Information VARCHAR(256) NOT NULL,
    CuisineID INT REFERENCES Cuisines (Id),
    CountSteps INT,
    FirstStepID INT REFERENCES Steps (Id),
    CountLikes INT
);

CREATE TABLE Users
(
    Id INT PRIMARY KEY,
    UserName VARCHAR(256) NOT NULL,
    UserPassword VARCHAR(256) NOT NULL
);

CREATE TABLE MatrixFridge
(
    UserID INT REFERENCES Users (Id),
    IngredientsID VARCHAR(2048)
);

CREATE TABLE MatrixIngredients
(
    RecipeID INT REFERENCES Recipes (Id),
    IngredientsID VARCHAR(2048)
);

CREATE TABLE MatrixFavorite
(
    UserID INT REFERENCES Users (Id),
    RecipesID VARCHAR(1024)
);


