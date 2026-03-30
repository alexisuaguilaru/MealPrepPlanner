import re

def CleanTitle(MetadataArticle):
    no_tittle_pattern = r'[^\d\w\s]*'
    clean_title = re.sub(no_tittle_pattern,' ',MetadataArticle)
    return re.sub(r'\s*',' ',clean_title)


def CleanLastUpdate(MetadataPage):
    date_pattern = r'([Pp]ublished|[Rr]eviewed):?\s*?(.+)'
    for date in list(MetadataPage.values())[::-1]:
        date_match = re.search(date_pattern,date)
        if date_match: 
            return date_match.group(2)
    
    return ''