from pathlib import Path
import requests

def DownloadDataset(
        DatasetURL: str,
        ReferrerSite: str,
        DatasetPath: str,
    ):

    Headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': ReferrerSite,
    }

    dataset_path = Path(DatasetPath)
    dataset_path.parent.mkdir(parents=True,exist_ok=True)
    
    if not dataset_path.exists():
        with requests.get(DatasetURL,headers=Headers,stream=True) as response:
            with open(dataset_path,'wb') as file_dataset:
                for chunk in response.iter_content(chunk_size=1024*1024*16):
                    if chunk: 
                        file_dataset.write(chunk)
    
    return dataset_path

def DownloadPDF(PDFLink,ReferrerSite,FilePath):
    Headers = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'referer': ReferrerSite,
    }

    file_path = Path(FilePath)
    file_path.parent.mkdir(parents=True,exist_ok=True)
    
    if not file_path.exists():
        with requests.get(PDFLink,headers=Headers,stream=True) as response:
            with open(file_path,'wb') as file_pdf:
                for chunk in response.iter_content(chunk_size=1024*1024*8):
                    if chunk: 
                        file_pdf.write(chunk)
                
    return file_path