from pathlib import Path
import pandas as pd 
from uuid import uuid4
from sqlalchemy.exc import IntegrityError

from .Utils import DumpDataFrameToSQL

def MainDumpNutrients(MainLogger):
    DatasetNutrients = Path('./Datasets/SQL/Nutrients.csv')

    if not DatasetNutrients.exists():
        DataFrameNutrients = _InitDataNutrients()
        DataFrameNutrients.to_csv(DatasetNutrients,index=False)
    else:
        DataFrameNutrients = pd.read_csv(DatasetNutrients)

    try: 
        DumpDataFrameToSQL(DataFrameNutrients,'NUTRIENTS')
    except IntegrityError:
        MainLogger.info(f'Nutrients Data Preloaded')

def _InitDataNutrients():
    NutrientsNames = [
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

    NutrientsUnits = [
        'g',
        'mg',
        'mg',
        'mg',
        'mg',
        'mg',
        'mg',
        'mg',
        'mg',
        'mg',
        'mg',
        'mg',
        'mg',
        'mg',
        'mg',
        'g',
        'g',
        'g',
        'mg',
    ]

    DataFrameNutrients = pd.DataFrame(
        [NutrientsNames,NutrientsUnits]
    ).T
    DataFrameNutrients.columns = ['Name','UnitMeasurement']
    DataFrameNutrients['id'] = DataFrameNutrients['Name'].apply(lambda value: uuid4())

    return DataFrameNutrients