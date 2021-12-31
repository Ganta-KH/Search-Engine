from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog
from PyQt5.uic import loadUi
from SearchEngine import *
import glob, shutil

from tools import is_grayScale

class widget(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("assets/Search Engine.ui",self)
        self.setWindowTitle("Search Engine")
        self.startSearch.clicked.connect(self.deleteFiles)
        self.startSearch.clicked.connect(self.search)
        self.imgUpload.clicked.connect(self.deleteFiles)
        self.imgUpload.clicked.connect(self.UploadImage)

        self.path = os.getcwd()+'\\Download' #"C:/Users/lenovo/Documents/Python Scripts/Search Engine/Download"
        self.searchPath = os.getcwd()+'\\Images' #"C:/Users/lenovo/Documents/Python Scripts/Search Engine/Images"
        self.DBPath = os.getcwd()+'\\assets\\SearchEngine.db' #"C:/Users/lenovo/Documents/Python Scripts/Search Engine/assets/SearchEngine.db"
        self.pixel = None
        self.DCT = None
        self.Chains = None

    def UploadImage(self):
        #try:
            imageFile = QFileDialog.getOpenFileName(None, "Open image", self.searchPath, "Image Files (*.png *.jpg *.bmp *.jpeg *.png *.jfif)")
            self.imagename = str(imageFile[0])
            self.pixel = np.array(Image.open(self.imagename).convert('RGB'))
            GrayScale = is_grayScale(self.pixel)
            if GrayScale:
                print('Method: Freeman')
                self.Chains = Freeman(self.pixel)
            else:
                print('Method: DCT')
                self.DCT = DCT(self.pixel)

            imageSearch(self.searchPath, self.path, self.DBPath, self.DCT, self.Chains)
            self.showImage()
            self.DCT = None
            self.Chains = None

        #except: pass
    
    def showImage(self):
        os.chdir(self.path)
        row, column = 0, -1
        for file in glob.glob("*"):
            column += 1
            if column >= 4:
                row += 1
                column = 0
            pixmap = QtGui.QPixmap(self.path+"/"+file)
            pixmap = pixmap.scaled(270, 270)
            label = QLabel()
            label.setPixmap(pixmap)
            self.gridL.addWidget(label, row, column)

    def search(self):
        textSearch(self.path, self.DBPath, self.searchBar.text())
        self.showImage()
        

    def deleteFiles(self):
        for filename in os.listdir(self.path):
            file_path = os.path.join(self.path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        for i in reversed(range(self.gridL.count())):
            self.gridL.itemAt(i).widget().setParent(None)

app = QApplication([])
window = widget()
window.show()
app.exec_()
