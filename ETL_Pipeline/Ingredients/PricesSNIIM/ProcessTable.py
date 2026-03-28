import pandas as pd

def MainProcessJsonTable(JsonTable):
    TableRows = []
    for row in JsonTable:
        data_row = row['row']
        TableRows.append([data['entry'] for data in data_row])
    return pd.DataFrame(TableRows)