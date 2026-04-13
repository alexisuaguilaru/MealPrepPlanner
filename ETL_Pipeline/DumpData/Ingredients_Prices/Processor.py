import re
from uuid import uuid4
import numpy as np
import pandas as pd

from ..Utils import InitSemanticModel
from ...Utils import GatherIngredientsPrices_SNIIM , GatherIngredientsPrices_PROFECO 

def ProcessData():
    DataFramePrices_PROFECO = ProcessPROFECOData()
    DataFramePrices_SNIIM = ProcessSNIIMData()

    DataFrameIngredientsPrices = pd.concat([DataFramePrices_PROFECO]+DataFramePrices_SNIIM,ignore_index=True)
    DataFrameIngredientsPrices['id'] = DataFrameIngredientsPrices['Name'].apply(lambda value: uuid4())

    return ProcessEmbeddingsData(DataFrameIngredientsPrices)

def ProcessPROFECOData():
    DatasetsPricesIngredients_PROFECO = GatherIngredientsPrices_PROFECO()
    DatasetsPricesIngredients_PROFECO['Unit'] = DatasetsPricesIngredients_PROFECO['UnitMeasurement'].apply(_ReplaceUnitMeasurement_PROFECO)
    
    DataFramePrices_PROFECO = DatasetsPricesIngredients_PROFECO[['Product','Unit','Price']]
    DataFramePrices_PROFECO.rename(columns={'Product':'Name'},inplace=True)
    DataFramePrices_PROFECO['Price'] /= DatasetsPricesIngredients_PROFECO['Quantity']

    return DataFramePrices_PROFECO

def ProcessSNIIMData():
    DatasetsPricesIngredients_SNIIM = list(GatherIngredientsPrices_SNIIM())

    return [
        _ProcessSNIIM_FrutasHortalizas(DatasetsPricesIngredients_SNIIM[0]),
        _ProcessSNIIM_Granos(DatasetsPricesIngredients_SNIIM[1]),
        _ProcessSNIIM_Bov(DatasetsPricesIngredients_SNIIM[2]),
        _ProcessSNIIIM_Pol(DatasetsPricesIngredients_SNIIM[3]),
        _ProcessSNIIIM_Hue(DatasetsPricesIngredients_SNIIM[4]),
        _ProcessSNIIIM_Por(DatasetsPricesIngredients_SNIIM[5]),
        _ProcessSNIIIM_Mol(DatasetsPricesIngredients_SNIIM[6]),
        _ProcessSNIIIM_Pes(DatasetsPricesIngredients_SNIIM[7]),
    ]

def ProcessEmbeddingsData(DataFramePrices):
    SemanticModel = InitSemanticModel()

    BatchSize = 250
    NumIngredients = DataFramePrices.shape[0]
    Batches = int(np.ceil(NumIngredients/BatchSize))

    for batch in range(int(Batches)):
        batch_data = DataFramePrices.iloc[batch*BatchSize:(batch+1)*BatchSize]
        batch_data['Embedding'] = SemanticModel.encode(batch_data['Name'].to_list()).tolist()
        yield batch_data

def _ReplaceUnitMeasurement_PROFECO(Unit):
    unit = re.sub(r's+$','',Unit.lower())
    if unit in {'donita','mantecada','rollo'}: 
        return 'pieza'
    else:
        return unit

def _ProcessSNIIM_FrutasHortalizas(DatasetPrices_FrutasHortalizas):
    ProductIndexCell = np.argmax(DatasetPrices_FrutasHortalizas == 'Producto')
    IndexCol , IndexRow = divmod(ProductIndexCell,DatasetPrices_FrutasHortalizas.shape[1])
    
    DatasetPrices_FrutasHortalizas = DatasetPrices_FrutasHortalizas.iloc[IndexCol:,IndexRow:].dropna(axis=0,how='all')
    DatasetPrices_FrutasHortalizas.dropna(axis=1,how='all',inplace=True)
    
    DatasetPrices_FrutasHortalizas.columns = DatasetPrices_FrutasHortalizas.iloc[0]
    DatasetPrices_FrutasHortalizas.drop(index=3,inplace=True)
    
    DatasetPrices_FrutasHortalizas['Producto'] = DatasetPrices_FrutasHortalizas['Producto'].ffill()
    DatasetPrices_FrutasHortalizas.iloc[:,-6:] = DatasetPrices_FrutasHortalizas.iloc[:,-6:].replace('-',np.nan).replace('--',np.nan)
    DatasetPrices_FrutasHortalizas.dropna(axis=0,thresh=2,inplace=True)
    
    mask_relevant_records = np.any(DatasetPrices_FrutasHortalizas[['Presentación','Origen']] == 'Por Kilogramo',axis=1)
    DatasetPrices_FrutasHortalizas = DatasetPrices_FrutasHortalizas[mask_relevant_records]
    DatasetPrices_FrutasHortalizas.iloc[:,-6:] = DatasetPrices_FrutasHortalizas.iloc[:,-6:].astype(float)
    
    DataFramePrices_SNIIM_FrutasHortalizas = DatasetPrices_FrutasHortalizas[['Producto']]
    DataFramePrices_SNIIM_FrutasHortalizas.rename(columns={'Producto':'Name'},inplace=True)
    DataFramePrices_SNIIM_FrutasHortalizas['Price'] = np.max(DatasetPrices_FrutasHortalizas.iloc[:,-6:],axis=1)
    DataFramePrices_SNIIM_FrutasHortalizas['Unit'] = 'kg'

    return DataFramePrices_SNIIM_FrutasHortalizas

def _ProcessSNIIM_Granos(DatasetPrices_Granos):
    ProductIndexCell = np.argmax(DatasetPrices_Granos == 'Producto')
    IndexCol , IndexRow = divmod(ProductIndexCell,DatasetPrices_Granos.shape[1])
    
    DatasetPrices_Granos = DatasetPrices_Granos.iloc[IndexCol:,IndexRow:].dropna(axis=0,how='all')
    DatasetPrices_Granos.dropna(axis=1,how='all',inplace=True)
    
    DatasetPrices_Granos.columns = DatasetPrices_Granos.iloc[0]
    DatasetPrices_Granos.drop(index=1,inplace=True)
    
    DatasetPrices_Granos['Producto'] = DatasetPrices_Granos['Producto'].ffill()
    DatasetPrices_Granos.iloc[:,-6:] = DatasetPrices_Granos.iloc[:,-6:].replace('-',np.nan).replace('--',np.nan)
    DatasetPrices_Granos.dropna(axis=0,thresh=2,inplace=True)
    DatasetPrices_Granos.iloc[:,-6:] = DatasetPrices_Granos.iloc[:,-6:].astype(float)
    
    DataFramePrices_SNIIM_Granos = DatasetPrices_Granos[['Producto','PromedioMensual1']]
    DataFramePrices_SNIIM_Granos.rename(columns={'Producto':'Name','PromedioMensual1':'Price'},inplace=True)
    DataFramePrices_SNIIM_Granos['Unit'] = 'kg'

    return DataFramePrices_SNIIM_Granos

def _ProcessSNIIM_Bov(DatasetPrices_Bov):
    DatasetPrices_Bov = DatasetPrices_Bov.iloc[:,-2:].dropna()

    DataFramePrices_Bov = pd.DataFrame()
    DataFramePrices_Bov['Name'] = ['Carne de vaca','Carne de toro']
    DataFramePrices_Bov['Price'] = DatasetPrices_Bov.iloc[1:].astype(float).mean(axis=0).reset_index(drop=True)
    DataFramePrices_Bov['Unit'] = 'kg'

    return DataFramePrices_Bov

def _ProcessSNIIIM_Pol(DatasetPrices_Pol):
    DatasetPrices_Pol = DatasetPrices_Pol.iloc[[0,-1],2:]

    DataFramePrices_Pol = DatasetPrices_Pol.T

    DataFramePrices_Pol.replace(regex='P\.',value='Pollo ',inplace=True)
    DataFramePrices_Pol.replace(regex='\/',value='de ',inplace=True)
    DataFramePrices_Pol.iloc[-4,0] += ' de pollo'
    DataFramePrices_Pol.iloc[-3,0] = 'Muslo de pollo'
    DataFramePrices_Pol.iloc[-2,0] = 'Retazo de pollo'
    DataFramePrices_Pol.iloc[-1,0] = 'Visceras de pollo'

    DataFramePrices_Pol.columns = ['Name','Price']
    DataFramePrices_Pol['Unit'] = 'kg'

    return DataFramePrices_Pol

def _ProcessSNIIIM_Hue(DatasetPrices_Hue):
    DatasetPrices_Hue = DatasetPrices_Hue.iloc[3:,[2,4]]

    DataFramePrices_Hue = pd.DataFrame()
    DataFramePrices_Hue['Name'] = DatasetPrices_Hue.iloc[:,[0]]
    DataFramePrices_Hue['Price'] = DatasetPrices_Hue.iloc[:,1].replace(regex='\$',value='').astype(float)
    
    DataFramePrices_Hue = DataFramePrices_Hue.groupby('Name').mean().reset_index()
    DataFramePrices_Hue['Unit'] = 'kg'

    return DataFramePrices_Hue

def _ProcessSNIIIM_Por(DatasetPrices_Por):
    DataFramePrices_Por = pd.DataFrame()
    DataFramePrices_Por['Name'] = ['Carne de puerco']
    DataFramePrices_Por['Price'] = float(DatasetPrices_Por.iloc[3,5])
    DataFramePrices_Por['Unit'] = 'kg'

    return DataFramePrices_Por

def _ProcessSNIIIM_Mol(DatasetPrices_Mol):
    DatasetPrices_Mol = DatasetPrices_Mol.iloc[:,2:]
    DatasetPrices_Mol.columns = DatasetPrices_Mol.iloc[0]
    DatasetPrices_Mol.drop([0,1],inplace=True)

    DataFramePrices_Mol = DatasetPrices_Mol[['Producto','Pmáx']]
    DataFramePrices_Mol['Pmáx'] = DataFramePrices_Mol['Pmáx'].replace(regex=r'-+',value=np.nan)
    DataFramePrices_Mol['Pmáx'].dropna(inplace=True)
    DataFramePrices_Mol['Pmáx'] = DataFramePrices_Mol['Pmáx'].astype(float)

    DataFramePrices_Mol = DataFramePrices_Mol.groupby('Producto').mean()
    DataFramePrices_Mol = DataFramePrices_Mol.reset_index()

    DataFramePrices_Mol.rename(columns={'Producto':'Name','Pmáx':'Price'},inplace=True)
    DataFramePrices_Mol['Unit'] = 'kg'

    return DataFramePrices_Mol

def _ProcessSNIIIM_Pes(DatasetPrices_Pes):
    DatasetPrices_Pes = DatasetPrices_Pes.iloc[:,2:]
    DatasetPrices_Pes.columns = DatasetPrices_Pes.iloc[0]
    DatasetPrices_Pes.drop([0,1],inplace=True)

    ## Cleand dataset
    DataFramePrices_Pes = DatasetPrices_Pes[['Producto','Pmáx']]
    DataFramePrices_Pes['Pmáx'] = DataFramePrices_Pes['Pmáx'].replace(regex=r'-+',value=np.nan)
    DataFramePrices_Pes['Pmáx'].dropna(inplace=True)
    DataFramePrices_Pes['Pmáx'] = DataFramePrices_Pes['Pmáx'].astype(float)

    DataFramePrices_Pes = DataFramePrices_Pes.groupby('Producto').mean()
    DataFramePrices_Pes = DataFramePrices_Pes.reset_index()
    DataFramePrices_Pes.dropna(inplace=True)

    DataFramePrices_Pes.rename(columns={'Producto':'Name','Pmáx':'Price'},inplace=True)
    DataFramePrices_Pes['Unit'] = 'kg'

    return DataFramePrices_Pes