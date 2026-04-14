from uuid import uuid4
import pandas as pd
from joblib import Parallel , delayed , cpu_count
from functools import partial

from ..Utils import InitSemanticModel
from ...Utils import GatherIngredientsNutritional_JSON , GatherIngredientsNutritional_CSV

NutrientsNames = [
    'Carbohydrates',
    'Proteins',
    'Fats',
    'Fiber',
    'Calcium',
    'Iron',
    'Zinc',
    'VitaminC',
    'VitaminB1',
    'VitaminB2',
    'VitaminB3',
    'VitaminB6',
    'VitaminB9',
    'VitaminB12',
    'VitaminA',
    'VitaminE',
    'VitaminD',
    'VitaminK',
    'SaturatedFat',
    'MonounsaturatedFat',
    'PolyunsaturatedFat',
    'Cholesterol',
]
NotNullColumns = [
    'Name',
    'Calories',
]
def ProcessTabularData(DatasetIngredients):
    DataFrameIngredientNutrients_INSP = _GetDataFrameIngredients_INSP()
    DataFrameIngredientNutrients_BEDCA = _GetDataFrameIngredients_BEDCA()
    
    DataFrameIngredientNutrients = pd.concat([DataFrameIngredientNutrients_BEDCA,DataFrameIngredientNutrients_INSP],ignore_index=True)
    DataFrameIngredientNutrients['id'] = DataFrameIngredientNutrients['Name'].apply(lambda value: uuid4())

    NutrientsValues = DataFrameIngredientNutrients[NutrientsNames].map(_CleanNotNumericValues).astype(float)
    DataFrameIngredientNutrients[NutrientsNames] = NutrientsValues

    DataFrameIngredientNutrients.to_csv(DatasetIngredients,index=False)
    return DataFrameIngredientNutrients

def ProcessEmbeddingsData(DatasetIngredients):
    SemanticModel = InitSemanticModel()

    BatchIngredientsDataFrame = pd.read_csv(
        DatasetIngredients,
        chunksize = 250,
    )

    for batch_data in BatchIngredientsDataFrame:
        batch_data['Embedding'] = SemanticModel.encode(batch_data['Name'].to_list()).tolist()
        yield batch_data

def ProcessPricesData(BatchIngredients,SemanticModel,ConnectionToAPI):
    QueryVectors = SemanticModel.encode(BatchIngredients['Name'].to_list()).tolist()

    IngredientPricesIDs = []
    for query_vector in QueryVectors:
        response = ConnectionToAPI.rpc('search_prices',{
            'query_vec': query_vector,
            'limit_results': 1,
            'threshold': 0.25,
        }).execute()
        ingredient_id = response.data[0]['id']
        IngredientPricesIDs.append(ingredient_id)
    
    BatchIngredients['id_price'] = IngredientPricesIDs

RenamingColummns_CSV = {
    'nombre_del_alimento': 'Name', 
    'energ_kcal': 'Calories', 
    'carbohydrt': 'Carbohydrates', 
    'lipid_tot': 'Proteins',
    'protein': 'Fats',
    'fiber_td': 'Fiber',
    'calcium': 'Calcium',
    'iron': 'Iron',
    'zinc': 'Zinc',
    'vit_c': 'VitaminC',
    'thiamin': 'VitaminB1',
    'riboflavin': 'VitaminB2',
    'niacin': 'VitaminB3',
    'vit_b6': 'VitaminB6',
    'folic_acid': 'VitaminB9',
    'vit_b12': 'VitaminB12',
    'vit_a_rae': 'VitaminA',
    'vit_e': 'VitaminE',
    'vit_d_iu': 'VitaminD',
    'vit_k': 'VitaminK',
    'fa_sat': 'SaturatedFat',
    'fa_mono': 'MonounsaturatedFat',
    'fa_poly': 'PolyunsaturatedFat',
    'chole': 'Cholesterol',
}
def _GetDataFrameIngredients_INSP():
    DatasetIngredients_INSP = GatherIngredientsNutritional_CSV()
    return DatasetIngredients_INSP.rename(columns=RenamingColummns_CSV)[RenamingColummns_CSV.values()]

RenamingColummns_JSON = {
    'carbohidratos': 'Carbohydrates',
    'proteina, total': 'Proteins',
    'grasa, total (lipidos totales)': 'Fats',
    'fibra, dietetica total': 'Fiber',
    'calcio': 'Calcium',
    'hierro, total': 'Iron',
    'zinc (cinc)': 'Zinc',
    'Vitamina C (ácido ascórbico)': 'VitaminC',
    'tiamina': 'VitaminB1',
    'riboflavina': 'VitaminB2',
    'equivalentes de niacina, totales': 'VitaminB3',
    'Vitamina B-6, Total': 'VitaminB6',
    'folato, total': 'VitaminB9',
    'Vitamina B-12': 'VitaminB12',
    'Vitamina A equivalentes de retinol de actividades de retinos y carotenoides': 'VitaminA',
    'Viamina E equivalentes de alfa tocoferol de actividades de vitámeros E': 'VitaminE',
    'Vitamina D': 'VitaminD',
    'potasio': 'VitaminK',
    'ácidos grasos saturados totales': 'SaturatedFat',
    'ácidos grasos, monoinsaturados totales': 'MonounsaturatedFat',
    'ácidos grasos, poliinsaturados totales': 'PolyunsaturatedFat',
    'colesterol': 'Cholesterol',
}
def _GetDataFrameIngredients_BEDCA():
    DatasetNutrients_BEDCA = list(map(_ExtractRelevantDataFromJSON_BEDCA,GatherIngredientsNutritional_JSON()))
    DatasetNutrients_BEDCA = list(filter(lambda dataframe: dataframe is not None,DatasetNutrients_BEDCA))
    DataFrameIngredientNutrients_BEDCA = pd.concat(DatasetNutrients_BEDCA,ignore_index=True)
    return DataFrameIngredientNutrients_BEDCA.rename_axis('',axis='columns')

def _ExtractRelevantDataFromJSON_BEDCA(IngredientNutrients_JSON):
    IngredientNutrients = None
    try:
        IngredientNutrients = pd.DataFrame(IngredientNutrients_JSON['Nutrients'])[['Nutrient','Value']].T
    except Exception as e:
        return None

    try:
        IngredientNutrients.columns = IngredientNutrients.iloc[0]
        IngredientNutrients.reset_index(drop=True,inplace=True)
        IngredientNutrients.drop(index=0,inplace=True)

        IngredientNutrients = IngredientNutrients.rename(columns=RenamingColummns_JSON)
        for nutrient_name in RenamingColummns_JSON.values():
            try:
                IngredientNutrients[nutrient_name]
            except:
                IngredientNutrients[nutrient_name] = 0
        IngredientNutrients = IngredientNutrients[RenamingColummns_JSON.values()]
        
        IngredientNutrients['Name'] = IngredientNutrients_JSON['Spanish Name']
        IngredientNutrients['Calories'] = IngredientNutrients_JSON['Calories']
        return IngredientNutrients
    except Exception as e:
        raise

def _CleanNotNumericValues(Value):
    if isinstance(Value,str):
        try:
            return float(Value)
        except:
            return 0
    return Value