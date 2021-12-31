import sqlite3, io
from PIL import Image


def connectDB(DB_path):
    DB = sqlite3.connect(DB_path) # 'assets/tutorial.db'
    cursor = DB.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS Images ( id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, Photo longblob NOT NULL)")
    return DB, cursor


def InsertImage(name, ImgB, cursor, DB):
    cursor.execute("INSERT INTO images (name, Photo) VALUES (?, ?)", (name, ImgB))
    DB.commit()


def getImage(cursor, path):
    ImagesDB = cursor.execute("SELECT * FROM images")
    for imageDB in ImagesDB:
        name = imageDB[1]
        image = imageDB[2]

        try:
            with open(path+'/'+name+'.png', 'wb') as f:
                f.write(image)
        except: pass


def deleteImagesFromBD(cursor):
    cursor.execute("DELETE FROM images")


def closeDB(DB, cursor):
    DB.commit()
    cursor.close()
    DB.close()

