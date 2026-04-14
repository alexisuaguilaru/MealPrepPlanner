from pathlib import Path
import pandas as pd
from sqlalchemy.exc import IntegrityError

from .Processor import ProcessData , ProcessEmbeddingsData
from ..Utils import DumpDataFrameToSQL

import logging

def MainDumpIngredients(MainLogger):
    DatasetIngredients = Path('./Datasets/SQL/Ingredients.csv')

    if not DatasetIngredients.exists():
        IngredientsDataFrame = ProcessData(DatasetIngredients)
    else:
        IngredientsDataFrame = pd.read_csv(DatasetIngredients)

    try:
        DumpDataFrameToSQL(IngredientsDataFrame,'INGREDIENTS')
    except IntegrityError:
        MainLogger.info('Ingredients Data Preloaded')

def MainDumpIngredientsEmbeddings(MainLogger: logging.Logger):
    DatasetIngredients = Path('./Datasets/SQL/Ingredients.csv')
    DatasetIngredientsEmbeddings = Path('./Datasets/SQL/IngredientsEmbeddings.csv')

    if not DatasetIngredientsEmbeddings.exists():
        EmbeddingsDataFrame = []
        for index , batch_embeddings in enumerate(ProcessEmbeddingsData(DatasetIngredients)):
            try:
                DumpDataFrameToSQL(batch_embeddings,'INGREDIENTS_EMBEDDINGS')
            except IntegrityError:
                MainLogger.info(f'Ingredients Embeddings {index} Data Preloaded')
            EmbeddingsDataFrame.append(batch_embeddings)

        IngredientsEmbeddingsDataFrame: pd.DataFrame = pd.concat(EmbeddingsDataFrame,ignore_index=True)
        IngredientsEmbeddingsDataFrame.to_csv(DatasetIngredientsEmbeddings,index=False)
    else:
        BatchIngredientsEmbeddingsDataFrame = pd.read_csv(DatasetIngredientsEmbeddings,chunksize=250)
        for index , batch_data in enumerate(BatchIngredientsEmbeddingsDataFrame):
            try:
                DumpDataFrameToSQL(batch_data,'INGREDIENTS_EMBEDDINGS')
            except IntegrityError:
                MainLogger.info(f'Ingredients Embeddings {index} Data Preloaded')