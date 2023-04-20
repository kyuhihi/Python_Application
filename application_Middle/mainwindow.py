from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QDesktopWidget, QMainWindow, \
    QPushButton, QVBoxLayout

from atlas_maker import Atlas_Maker
from factorfont_maker import factorfont_maker
from imageviewerwindow import ImageViewerWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.m_timer = QTimer(self)
        self.m_timer.timeout.connect(self.Tick)
        self.m_timer.start(10)

        self.setWindowTitle("Main Window")
        screen_size = QDesktopWidget().screenGeometry()
        width, height = 800, 600
        self.setGeometry((screen_size.width() - width) // 2, (screen_size.height() - height) // 2, width, height)

        layout = QVBoxLayout()

        self.background_image = QLabel(self)
        self.background_image.setGeometry(0, 0, width, height)
        self.background_image.setScaledContents(True)
        self.background_image.setPixmap(QPixmap("Logo.png"))
        layout.addWidget(self.background_image)

        self.ImageViewerOpen = QPushButton('이미지 합치기',self)
        self.ImageViewerOpen.clicked.connect(self.open_image_viewer)
        self.ImageViewerOpen.setGeometry(300, 360, 200, 50)
        layout.addWidget(self.ImageViewerOpen)

        self.FactorFontMakerOpen = QPushButton('Factor font', self)
        self.FactorFontMakerOpen.clicked.connect(self.open_factor_font_maker)
        self.FactorFontMakerOpen.setGeometry(300, 440, 200, 50)
        layout.addWidget(self.FactorFontMakerOpen)

        self.AtlasOpen = QPushButton('Atlas Maker', self)
        self.AtlasOpen.clicked.connect(self.open_Atlase_Maker)
        self.AtlasOpen.setGeometry(300, 520, 200, 50)
        layout.addWidget(self.AtlasOpen)

        self.m_Imageviewer = None
        self.m_FactorFontMaker = None
        self.m_AtlasMaker = None



    def open_image_viewer(self):
        if not self.m_Imageviewer:
            self.m_Imageviewer = ImageViewerWindow()
        self.m_Imageviewer.show()

    def open_factor_font_maker(self):
        if not self.m_FactorFontMaker:
            self.m_FactorFontMaker = factorfont_maker()
        self.m_FactorFontMaker.show()

    def open_Atlase_Maker(self):
        if not self.m_AtlasMaker:
            self.m_AtlasMaker = Atlas_Maker()
        self.m_AtlasMaker.show()

    def Tick(self):
        if self.m_Imageviewer is not None:
            self.m_Imageviewer.Tick()
        if self.m_FactorFontMaker is not None:
            self.m_FactorFontMaker.Tick()
        if self.m_AtlasMaker is not None:
            self.m_AtlasMaker.Tick()
