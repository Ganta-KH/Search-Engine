import requests
from bs4 import BeautifulSoup as BS
import os, re
from Freeman import Freeman
from DCT import DCT
import numpy as np
from PIL import Image
from math import sqrt
from DB import *

def textSearch(downloadFolder, DBpath, search):
    if search != '':
        DB, cursor = connectDB(DBpath)

        deleteImagesFromBD(cursor)


        urls = ["https://www.worldwildlife.org/species/elephant", 
                "https://www.britannica.com/animal/elephant-mammal",
                "https://www.worldwildlife.org/initiatives/forests",
                "https://www.worldwildlife.org/species/whale",
                "https://www.worldwildlife.org/species/gorilla",
                "https://www.worldwildlife.org/species/tiger"]

        try: os.mkdir(os.path.join(os.getcxd(), downloadFolder))
        except: pass
        os.chdir(os.path.join(os.getcwd(), downloadFolder))
        search = search.split(' ')
        print(search)
        name_number = 0
        for url in urls:
            print(url)
            r = requests.get(url)
            soup = BS(r.text, 'html.parser')
            html_lenght = len(soup.text)
            download = False
            titleSearch = False
            title = soup.title.text.lower() # get hte page title
            paragraphs = soup.select('p') # the paragraphs in the page
            images = soup.select('img') # all image in the page
            if all([ word.lower() in title for word in search]): download = True; titleSearch = True # search in page title
            #elif any([ all([ re.search(word.lower(), paragraph.text.lower()) for word in search]) for paragraph in paragraphs]): download = True # search in paragraphs
            
            elif not titleSearch:
                image = []
                for paragraph in paragraphs:
                    if all([ re.search(word.lower(), paragraph.text.lower()) for word in search]):
                        match = re.search(paragraph.text, r.text)
                        if match: download = True;                                                                                                                                                                                                                                                                                              break
                        if match: 
                            para_Pos = match.span()
                            txt = soup.text[para_Pos[0] - 1000 : (para_Pos[1] + 1000) % html_lenght ]
                            sp = BS(txt, "html.parser")
                            image.append( sp.select('img') )

            else: # search in image title
                for image in images:
                    imageTitle = image.attrs.get('alt', '')
                    link = image.attrs.get('src', '')
                    if all([ word.lower() in imageTitle.lower() for word in search]):
                        im = requests.get(link)
                        InsertImage(imageTitle.replace(':', '-').replace('/','-').replace(';','-') , im.content, cursor, DB)
                        print('Download: ',imageTitle)   


            if download:
                for image in images:
                    name = image.attrs.get('alt', '')
                    link = image.attrs.get('src', '') # image link

                    if name == '':
                        name_number += 1
                        name = str(name_number)
                    im = requests.get(link)
                    InsertImage(name.replace(':', '-').replace('/','-').replace(';','-') , im.content, cursor, DB)
                    print('Download: ',name)

        getImage(cursor, downloadFolder)
        closeDB(DB, cursor)


#############################################################################


def imageSearch(searchFolder, downloadFolder, DBpath, dct, chain):

    DB, cursor = connectDB(DBpath)
    deleteImagesFromBD(cursor)

    dct_threshold = 600
    freeman_threshold = 200
    if dct is not None:
        dY, dCb, dCr = dct
        for filename in os.listdir(searchFolder):
            file_path = os.path.join(searchFolder, filename)

            dY2, dCb2, dCr2 = DCT(np.array(Image.open(file_path).convert('RGB')))
            dist = sqrt(np.sum((dY - dY2) ** 2)) + sqrt(np.sum((dCb - dCb2) ** 2) ) + sqrt(np.sum((dCr - dCr2) ** 2) )
            
            if dist <= dct_threshold:
                name = file_path.split('\\')[-1]
                
                with open(file_path, 'rb') as f:
                    ImgB = f.read()
                    InsertImage(name.split('.')[0], ImgB, cursor, DB)
                    print('Download: %s' % name)

    elif chain is not None:
        for filename in os.listdir(searchFolder):
            file_path = os.path.join(searchFolder, filename)

            chain2 = Freeman(np.array(Image.open(file_path).convert('RGB')))
            dist = sqrt(np.sum((chain - chain2) ** 2))
            
            if dist <= freeman_threshold:

                name = file_path.split('\\')[-1]
                
                with open(file_path, 'rb') as f:
                    ImgB = f.read()
                    InsertImage(name.split('.')[0], ImgB, cursor, DB)
                    print('Download: %s' % name)
    
    getImage(cursor, downloadFolder)
    closeDB(DB, cursor)