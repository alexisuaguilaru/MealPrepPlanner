from functools import partial
from fractions import Fraction
from unicodedata import numeric
from math import modf
import re

def CleanFieldIngredients(Recipe):
    IngredientsList = Recipe.get('Ingredients',[])
    RecipeName = CleanFieldRecipeName(Recipe)
    Ingredients = map(partial(_CleanIngredient,RecipeName=RecipeName),IngredientsList)
    return list(Ingredients)

def CleanFieldRecipeName(Recipe):
    return Recipe.get('Name','').capitalize()

def _CleanIngredient(Ingredient,RecipeName):
    Quantity = Ingredient.get('quantity')

    Unit = Ingredient.get('unit')
    Unit = Unit.lower() if Unit else ''

    Name = Ingredient.get('name')
    Name = Name.capitalize()

    return RecipeName , *_FormatQuantity(Quantity) , Unit , Name

def _FormatQuantity(Quantity):
    if not Quantity:
        return 0 , ''
    
    if isinstance(Quantity,str):
        DepuratedQuantity = _DepurateStrQuantity(Quantity)
        if DepuratedQuantity != Quantity:
            Quantity = eval('+'.join(DepuratedQuantity.split()))
        else:
            QuantityNum = eval('+'.join(Quantity.split()))
            QuantityStr = Quantity
    if isinstance(Quantity,int) or isinstance(Quantity,float):
        QuantityNum = Quantity
        fractionary_part , integer_part = modf(Quantity)
        integer_part = str(int(integer_part)) if integer_part else ''
        fractionary_part = _FormatFraction(fractionary_part)
        QuantityStr = ' '.join([integer_part,fractionary_part]).strip()
    
    return QuantityNum , QuantityStr

def _DepurateStrQuantity(Quantity):
    Quantity = re.sub(r'â…“','1/3',Quantity)
    Quantity = re.sub(r'â…”','2/3',Quantity)
    quantity = ''
    for character in Quantity:
        if not character.isascii():
            try:
                quantity += f' {numeric(character):.2f}'
            except:
                continue
        elif character.isdecimal():
            quantity += character
    quantity = re.sub(r'[^\d\.\/\s]','',quantity)
    return quantity.strip()

def _FormatFraction(FractionaryPart):
    if FractionaryPart:
        return str(Fraction(FractionaryPart).limit_denominator(10))
    return ''