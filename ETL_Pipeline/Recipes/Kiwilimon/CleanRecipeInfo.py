import re

def CleanRecipe(Recipe: list[list[dict]]) -> dict:
    return {
        'Name': '',
        **CleanTime(Recipe),
        **CleanServingsIngredients(Recipe),
        'Instructions': CleanInstructions(Recipe),
        'Image': '',
    }

def CleanTime(Recipe):
    RecipeTimes = Recipe[0][0].values()
    time_hours = 0
    times_minutes = 0
    for times in RecipeTimes:
        time_hour = re.search(r'(\d+)hs?',times)
        time_mins = re.search(r'(\d+) ?mins?',times)

        if time_hour: time_hours += int(time_hour.group(1))
        if time_mins: times_minutes += int(time_mins.group(1))
        
    return {'Total Time': f'{time_hours} hrs {times_minutes} mins'}

def CleanServingsIngredients(Recipe):
    clean_servings_ingredients = {}
    clean_servings_ingredients['Servings'] = int(Recipe[1][0]['Servings'])
    clean_servings_ingredients['Ingredients'] = list(map(ExtractIngredientInfo,Recipe[1][0]['Ingredients']))

    return clean_servings_ingredients

def CleanInstructions(Recipe):
    return [step['step'] for step in Recipe[2][0]['Steps']]

def ExtractIngredientInfo(Ingredient):
    ingredient_info = Ingredient['ingredient']
    extracted_info = {}
    
    regex_info_type1 = r'([\d/ ]+)(tazas?|cucharadas?|gramos?|militros?|litros?|cucharaditas?|manojos?|kilos?|kilogramos?) de ([\w ,]+)'
    match_info = re.search(regex_info_type1,ingredient_info)
    if match_info: 
        extracted_info['quantity'] = match_info[1].strip()
        extracted_info['unit'] = match_info[2]
        extracted_info['name'] = match_info[3]

        return extracted_info
    
    regex_info_type2 = r'^([\d/ ]+)(.*)'
    match_info = re.search(regex_info_type2,ingredient_info)
    if match_info: 
        extracted_info['quantity'] = match_info[1].strip()
        extracted_info['unit'] = ''
        extracted_info['name'] = match_info[2]

        return extracted_info
    
    extracted_info['quantity'] = ''
    extracted_info['unit'] = ''
    extracted_info['name'] = ingredient_info
    
    return extracted_info