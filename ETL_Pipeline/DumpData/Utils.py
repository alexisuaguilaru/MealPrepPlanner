import os
import pandas as pd
from sentence_transformers import SentenceTransformer

from ..Database import CreateConnectionToSQL

SCHEMA_DB = os.getenv('SCHEMA_DB','meal_prep')

def DumpDataFrameToSQL(DataFrame,TableSQL):
    NumRows = DataFrame.to_sql(
        TableSQL,
        CreateConnectionToSQL(),
        schema = SCHEMA_DB,
        index = False,
        if_exists = 'append',
    )
    return NumRows

def InitSemanticModel():
    SemanticModel = SentenceTransformer(
        'microsoft/harrier-oss-v1-270m',
        model_kwargs = {'dtype': 'auto'}
    )
    return SemanticModel