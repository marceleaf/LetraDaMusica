import requests
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator

class Lyric:
    def __init__(self, songautor:str, songname:str, translate:bool = False, desirelang:str = 'pt'):
        self.songautor = songautor.replace(" ", "+").lower()
        self.songname = songname.replace(" ", "+").lower()
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        self.translate = translate
        self.desireLang = desirelang

    def Print(self):
        searchUrl = f'https://www.letras.mus.br/{self.songautor}/{self.songname}/'

        response = requests.get(searchUrl, headers=self.header)
        if response.status_code != 200:
            return 'Não foi possível carregar o url'

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('h1', class_='textStyle-primary').get_text().replace(" ", "")
        autor = soup.find('h2', class_='textStyle-secondary').get_text().replace(" ", "")
        
        lyricDiv = soup.find('div', class_='lyric-original') 
        lyric = lyricDiv.get_text(separator='\n')   

        if self.translate == False:
            return f'\nTítulo: {title.replace('\n', "")}\nAutor: {autor.replace('\n', "")}\n{lyric}'
        else:
            return f'\nTítulo: {title.replace('\n', "")}\nAutor: {autor.replace('\n', "")}\n\n{GoogleTranslator(source='auto', target=self.desireLang).translate(lyric)}'
    
