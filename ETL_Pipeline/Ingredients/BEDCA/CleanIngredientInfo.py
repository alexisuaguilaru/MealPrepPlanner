import re

def CleanNutritionalFacts(NutritionalFacts: list[dict]):
    not_null_values = lambda nutrient: all(value != '' for value in nutrient.values())
    valid_nutrients = filter(not_null_values,NutritionalFacts)

    clean_nutrients = []
    for nutrient in valid_nutrients:
        if nutrient['Nutrient'] == 'energía, total':
           clean_calories = float(re.search(r'\((\d+)\)',nutrient['Value']).groups()[0])
           break
        clean_nutrients.append(nutrient)
    clean_nutrients.extend([*valid_nutrients])

    return clean_calories , clean_nutrients