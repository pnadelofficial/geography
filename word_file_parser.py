import zipfile
import os
import re
from docx import Document
from pathlib import Path
import pandas as pd
from typing import List, Tuple

class WordFileParser:
    def __init__(self, zip_path: str) -> None:
        """Takes in a path to a zip file"""
        self.zip_path = zip_path
    
    def get_internal_zips(self) -> List:
        """Returns list of all relevant zip files"""
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            zip_ref.extractall()
            return [f for f in zip_ref.namelist() if f.endswith('.ZIP')]
    
    def extract_zips(self, zip_paths) -> List:
        """Extracts all relevant zip files. Returns list of extracted parent paths"""       
        paths = []
        for i, zp in enumerate(zip_paths):
            if '__MACOSX' in zp:
                continue
            dest_path = Path(f"{zp.split('.')[0]}_{i}")
            dest_path.mkdir(parents=True, exist_ok=True)
            paths.append(dest_path)

            print(f"Extracting {zp} to {dest_path}")
            with zipfile.ZipFile(zp, 'r') as zip_ref:
                zip_ref.extractall(dest_path)
        return paths
    
    def parse_docx(self, docx_path) -> Tuple | None:
        """Parses a single docx file. Returns a tuple of (title, news_source, date, body_text)"""
        if 'doclist' not in docx_path:
            doc = Document(docx_path)
            paragraphs = [p.text for p in doc.paragraphs]
            newspaper = paragraphs[4]
            date = paragraphs[5]
            full_text = "\n".join(paragraphs)
            body_text = full_text[re.search("Body", full_text).span()[1]:].strip()
            return docx_path.split('.')[0], newspaper, date, body_text
        else:
            return None
    
    def parse_docx_files(self, paths) -> List[Tuple]:
        """Parses all docx files in a list of paths. Returns a list of tuples of (title, news_source, date, body_text)"""
        data = [] 
        for path in paths:
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.endswith('.DOCX'):
                        docx_path = os.path.join(root, file)
                        data.append(self.parse_docx(docx_path))
        return data
        
    def format_as_df(self, data) -> pd.DataFrame:
        """Formats a list of tuples into a pandas DataFrame"""
        df = pd.DataFrame([d for d in data if d is not None], columns=['title', 'news_source', 'date', 'body_text'])
        return df
    
    def __call__(self, to_csv=True) -> pd.DataFrame:
        """Unzips and parses all data and returns a pandas DataFrame of the parsed data"""
        self.get_internal_zips()
        zip_paths = self.get_internal_zips()
        paths = self.extract_zips(zip_paths)
        data = self.parse_docx_files(paths)
        df = self.format_as_df(data)
        if to_csv:
            df.to_csv(f"{self.zip_path.strip('.ZIP')}.csv", index=False)
        return df
