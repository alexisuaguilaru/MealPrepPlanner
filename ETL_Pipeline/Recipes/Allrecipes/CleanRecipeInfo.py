def CleanTimeServings(Recipe: list[list[dict]]):
    clean_times = {}
    for item in Recipe[0]:
        item_label = item['Label']
        if item_label == 'Total Time:':
            clean_times['Total Time'] = item['Value']
        elif item_label == 'Servings:':
            clean_times['Servings'] = item['Value']
    return clean_times

def CleanIngredients(Recipe: list[list[dict]]):
    ingredients = []
    for section_ingredients in Recipe[1]:
        ingredient_list = section_ingredients['Ingredients']
        ingredients.extend(ingredient['ingredient'] for ingredient in ingredient_list)
    return ingredients

def CleanInstructions(Recipe: list[list[dict]]):
    instructions = []
    instructions.extend(step['step'] for step in Recipe[2][0]['Steps'])
    return instructions

def CleanNutritionalFacts(Recipe: list[list[dict]]):
    nutritional_facts = {}
    recipe_facts = Recipe[3][0]
    nutritional_facts['Calories'] = recipe_facts['Calories']
    for nutritional_fact in recipe_facts['Nutritional Facts']:
        nutritional_facts[nutritional_fact['label']] = nutritional_fact['value']
    return nutritional_facts