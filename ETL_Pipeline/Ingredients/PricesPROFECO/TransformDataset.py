import re

def MainTransform(CompleteDataset):
    TransformedDataset = CompleteDataset[['producto','presentacion','precio']].copy()
    TransformedDataset.rename(columns={'producto':'Product','presentacion':'Presentation','precio':'Price'},inplace=True)

    presentation_regex = r'(\d+) ([a-zA-Z]+)\.'
    presentation_matches = TransformedDataset['Presentation'].apply(lambda value: re.search(presentation_regex,value))
    valid_matches = (presentation_matches == presentation_matches)

    TransformedDataset = TransformedDataset[valid_matches]
    TransformedDataset[['Quantity','UnitMeasurement']] = [*(presentation_matches[valid_matches].apply(lambda match: match.groups()))]
    TransformedDataset.drop(columns=['Presentation'],inplace=True)

    return TransformedDataset