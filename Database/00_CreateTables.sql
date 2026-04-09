\set schema_name `echo "$SCHEMA_DB"`

CREATE SCHEMA IF NOT EXISTS :"schema_name";
SET search_path TO :"schema_name";

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS "RECIPES" (
	"id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	"Name" TEXT NOT NULL,
	"TotalTime" INTEGER NOT NULL,
	"Servings" INTEGER NOT NULL,
	"PricePerServing" REAL,
	"Instructions" TEXT NOT NULL,
	"Calories" INTEGER,
	"Carbohydrates" INTEGER,
	"Proteins" INTEGER,
	"Fats" INTEGER,
	"Image" TEXT,
	"Source" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "RECIPES_EMBEDDINGS" (
	"id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	"IngredientName" TEXT NOT NULL,
	"Embedding" vector(640)	
);


CREATE TABLE IF NOT EXISTS "INGREDIENTS" (
	"id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	"Name" TEXT NOT NULL,
	"Calories" INTEGER NOT NULL,
	"Carbohydrates" INTEGER,
	"Proteins" INTEGER,
	"Fats" INTEGER,
	"Price" REAL
);
CREATE TABLE IF NOT EXISTS "INGREDIENTS_EMBEDDINGS" (
	"id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	"Embedding" vector(640)	
);


CREATE TABLE IF NOT EXISTS "NUTRIENTS" (
	"id" UUID PRIMARY KEY DEFAULT gen_random_uuid(),
	"Name" TEXT NOT NULL,
	"UnitMeasurement" TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS "RECIPES_INGREDIENTS" (
	"recipe_id" UUID NOT NULL,
	"ingredient_id" UUID NOT NULL,
	"NumericAmount" REAL NOT NULL,
	"StringAmount" TEXT NOT NULL,
	"UnitMeasurement" TEXT,
	CONSTRAINT foreign_recipes FOREIGN KEY("recipe_id") REFERENCES "RECIPES"("id"),
	CONSTRAINT foreign_ingredients FOREIGN KEY("ingredient_id") REFERENCES "INGREDIENTS"("id")
);


CREATE TABLE IF NOT EXISTS "RECIPES_NUTRIENTS" (
	"recipe_id" UUID NOT NULL,
	"nutrient_id" UUID NOT NULL,
	"Amount" REAL NOT NULL,
	CONSTRAINT foreign_recipes FOREIGN KEY("recipe_id") REFERENCES "RECIPES"("id"),
	CONSTRAINT foreign_nutrients FOREIGN KEY("nutrient_id") REFERENCES "NUTRIENTS"("id")
);


CREATE TABLE IF NOT EXISTS "INGREDIENTS_NUTRIENTS" (
	"ingredient_id" UUID NOT NULL,
	"nutrient_id" UUID NOT NULL,
	"Amount" REAL NOT NULL,
	CONSTRAINT foreign_ingredients FOREIGN KEY("ingredient_id") REFERENCES "INGREDIENTS"("id"),
	CONSTRAINT foreign_nutrients FOREIGN KEY("nutrient_id") REFERENCES "NUTRIENTS"("id")
);