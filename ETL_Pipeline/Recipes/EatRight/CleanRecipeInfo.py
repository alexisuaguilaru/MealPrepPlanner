import re
from unicodedata import numeric

def CleanRecipe(Recipe: dict):
    return {
        'Name': '',
        'Total Time': CleanTime(Recipe),
        'Servings': CleanServings(Recipe),
        'Ingredients': CleanIngredients(Recipe),
        'Instructions': CleanInstructions(Recipe),
        'NutritionalFacts': CleanNutritionalFacts(Recipe),
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
    try:
        raw_servings = re.sub(r'<.*?>','',Recipe['Servings Nutritional Facts'])
        servings = re.search(r'[Ss]erv(ing|e)s?:?\s*?(\d+)',raw_servings).group(2)
        return int(servings)
    except:
        return 1

def CleanIngredients(Recipe: dict):
    raw_ingredients = Recipe['Ingredients']
    ingredients = re.sub(r'</?p>','',raw_ingredients)
    
    list_ingredients = ingredients.split('<br/>\n')
    list_ingredients = map(ProcessedIngredient,list_ingredients)

    return sum(map(ExtractIngredientInfo,list_ingredients),[])

def CleanInstructions(Recipe: dict):
    return [direction['direction'] for direction in Recipe['Directions']]

def CleanNutritionalFacts(Recipe):
    paragraphs = Recipe['Servings Nutritional Facts']
    list_paragraphs = paragraphs.split('</p>\n')
    
    for paragraph in list_paragraphs:
        if 'alories' in paragraph: break
    for nutrients_paragraph in paragraph.split('<br/>'):
        if 'alories' in nutrients_paragraph: break

    nutrients_paragraph = re.sub(r'<.*?>','',nutrients_paragraph)
    nutrients_paragraph = nutrients_paragraph.strip()
    nutrients_paragraph = nutrients_paragraph.replace('<','')
    nutrients_paragraph = nutrients_paragraph.replace('>','')
    nutrients_paragraph = nutrients_paragraph.replace('&lt;','')
    nutrients_paragraph = nutrients_paragraph.replace('&gt;','')

    nutritional_info_form_1 = r'([\w ]+):?\s*?([\d\.]+[\w\s]*|[Nn]\/?[Aa])'
    nutritional_info_form_2 = r'([\d\.]+\s?[gmGMUI]*|[Nn]\/?[Aa]):?\s?([\w ]+)'
    
    nutritional_facts_info = {}  
    if (nutrients:=re.findall(nutritional_info_form_1,nutrients_paragraph)):
        for nutrient , value in nutrients:
            if len(nutrient) < 3: break
            nutritional_facts_info[nutrient.strip().title()] = value
        if len(nutrient) > 3: return nutritional_facts_info

    nutritional_facts_info = {}
    if (nutrients:=re.findall(nutritional_info_form_2,nutrients_paragraph)):
        for value , nutrient  in nutrients:
            if len(nutrient) < 3: break
            nutritional_facts_info[nutrient.strip().title()] = value
        if len(nutrient) > 3: return nutritional_facts_info

def ProcessedIngredient(Ingredient: str):
    preprocessed_ingredients = ''
    for letter in Ingredient:
        if not letter.isascii():
            try:
                preprocessed_ingredients += f' {numeric(letter):.2f}'
            except:
                preprocessed_ingredients += letter
        else:
            preprocessed_ingredients += letter

    return preprocessed_ingredients.strip()

def ExtractIngredientInfo(Ingredient):

    quantity_ingredient = r'((?:\d+(?:\.\d+)?\s+|plus\s+|(?:cups?|tablespoons?|tbsp|teaspoons?|tsp|oz|ounces?|g|kg|ml|l)\s+)*)(.*)'
    full_quantity , ingredient_name = re.search(quantity_ingredient,Ingredient).groups()

    if not full_quantity:
        ingredient_info = {}
        ingredient_info['quantity'] = ''
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