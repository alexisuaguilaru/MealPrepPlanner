import re
from unicodedata import numeric

def CleanRecipe(Recipe: dict):
    return {
        'Name': '',
        'Total Time': CleanTime(Recipe),
        'Servings': CleanServings(Recipe),
        'Ingredients': CleanIngredients(Recipe),
        'Instructions': CleanInstructions(Recipe),
        'Image': '',
    }

def CleanTime(Recipe):
    time_hours = 0
    times_minutes = 0
    
    if Recipe.get('Times',None):
        for times in re.finditer(r'([\d\.]+) (hours?|minutes?)',Recipe['Times']):
            time , unit = times.groups() 

            if 'm' in unit: 
                times_minutes += int(time)
            elif 'h' in unit:
                time_hours += int(time)
        
    return f'{time_hours} hrs {times_minutes} mins'

def CleanServings(Recipe: dict):
    servings = re.search(r'[Ss]erves:?\s?(\d*)',Recipe['Servings']).group(1)
    return int(servings) 

def CleanIngredients(Recipe: dict):
    raw_ingredients = Recipe['Ingredients']
    ingredients = re.sub(r'</?p>','',raw_ingredients)
    
    list_ingredients = ingredients.split('<br/>\n')
    list_ingredients = map(ProcessedIngredient,list_ingredients)

    return sum(map(ExtractIngredientInfo,list_ingredients),[])

def CleanInstructions(Recipe: dict):
    return [direction['direction'] for direction in Recipe['Directions']]

def ProcessedIngredient(Ingredient: str):
    preprocessed_ingredients = ''
    for letter in Ingredient:
        if not letter.isascii(): 
            preprocessed_ingredients += f' {numeric(letter):.2f}'
        else:
            preprocessed_ingredients += letter

    return preprocessed_ingredients.strip()

def ExtractIngredientInfo(Ingredient):

    quantity_ingredient = r'((?:\d+(?:\.\d+)?\s+|plus\s+|(?:cups?|tablespoons?|tbsp|teaspoons?|tsp|oz|ounces?|g|kg|ml|l)\s+)*)(.*)'
    full_quantity , ingredient_name = re.search(quantity_ingredient,Ingredient).groups()

    if not full_quantity:
        ingredient_info = {}
        ingredient_info['quantity'] = 0
        ingredient_info['unit'] = ''
        ingredient_info['name'] = ingredient_name

        ingredients_info = [ingredient_info]

    else:
        ingredients_info = []

        full_quantity = full_quantity.lower().split('plus')       
        for quantity_unit in full_quantity:
            quantity , unit = re.search(r'([\d\. ]+)(\D+)',quantity_unit).groups()

            ingredient_info = {}
            ingredient_info['quantity'] = eval(quantity.strip().replace(' ','+'))
            ingredient_info['unit'] = unit.strip()
            ingredient_info['name'] = ingredient_name

            ingredients_info.append(ingredient_info)

    return ingredients_info