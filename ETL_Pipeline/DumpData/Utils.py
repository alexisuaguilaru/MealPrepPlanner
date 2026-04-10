import os
import pandas as pd

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