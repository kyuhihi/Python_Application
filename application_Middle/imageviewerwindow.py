import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QPainter
from PyQt5.QtWidgets import *

make_Move_Size = (320, 640) # 가로 기준 세로는 160

g_ext_list = [".png", ".jpg"]
class ImageViewerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setFixedSize(1280, 720)
        self.setAcceptDrops(True)
        self.m_ImageLabel = []
        self.layout = QVBoxLayout(self)
        self.m_bHasImage = [False,False]
        self.m_clear_button = []

        for n in range(2):
            self.m_ImageLabel.append(QLabel(self))
            self.m_ImageLabel[n].setAlignment(Qt.AlignLeft)
            self.m_ImageLabel[n].setGeometry(make_Move_Size[n] - 300, 160, 300, 300)

            self.m_ImageLabel[n].setStyleSheet("background-color: yellow;")
            font = QFont()
            font.setPointSize(15)
            self.m_ImageLabel[n].setFont(font)
            self.m_ImageLabel[n].setText(f"Drag and Drop {n}")
            self.layout.addWidget(self.m_ImageLabel[n])
            new_push_button = QPushButton("Clear", self)
            new_push_button.setGeometry(self.m_ImageLabel[n].geometry().x(),self.m_ImageLabel[n].geometry().y(),100,30)
            self.m_clear_button.append(new_push_button)

            self.m_ImageLabel[n].setGraphicsEffect(QGraphicsDropShadowEffect())


        self.m_clear_button[0].clicked.connect(lambda : self.clear_Image(0))
        self.m_clear_button[1].clicked.connect(lambda : self.clear_Image(1))

        self.combine_button = QPushButton("CombineImages",self)
        self.combine_button.setGeometry(850, 390, 200, 50)
        self.combine_button.setStyleSheet("background-color: #ff0000; color: #ffffff;")
        self.combine_button.clicked.connect(self.combine_images)

        self.m_bGaro_Combile = True
        self.slide_button = QPushButton("직렬", self)
        self.slide_button.setGeometry(850, 150, 200, 50)
        self.layout.addWidget(self.slide_button)
        self.slide_button.clicked.connect(self.toggle_slide_state)

        self.m_strSaveName = "newone.png"
        self.text_input = QLineEdit(self)
        self.text_input.setGeometry(850, 230, 200, 50)
        self.text_input.setPlaceholderText("Enter New Texture Name")

        self.m_extComboBox = QComboBox(self)
        for n in g_ext_list:
            self.m_extComboBox.addItem(n)
        self.m_extComboBox.currentIndexChanged.connect(self.handle_combobox)
        self.m_extComboBox.setGeometry(850, 310, 200, 50)



        self.m_lerp_time_delta = 0.0
        self.m_bMove = False

    def handle_combobox(self, index):
        self.m_extComboBox.setCurrentIndex(index)
        self.m_extComboBox.setCurrentText(self.sender().currentText())
    def toggle_slide_state(self):
        self.m_bGaro_Combile = not self.m_bGaro_Combile
        self.m_bMove = True
        if self.m_bGaro_Combile:
            self.slide_button.setText("직렬")
        else:
            self.slide_button.setText("병렬")

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            FilePath = event.mimeData().urls()[0].toLocalFile()
            pixmap = QPixmap(FilePath)
            # pixmap.de(2)
            iInsertImageIndex = 0
            if self.m_bHasImage[0] == True:
                iInsertImageIndex = 1
            self.m_ImageLabel[iInsertImageIndex].setPixmap(pixmap.scaled(self.m_ImageLabel[iInsertImageIndex].width(), self.m_ImageLabel[iInsertImageIndex].height(), Qt.KeepAspectRatio))
            self.m_bHasImage[iInsertImageIndex] = True

        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def combine_images(self):
        # Get the two images as QPixmap objects
        pixmap1 = self.m_ImageLabel[0].pixmap()
        pixmap2 = self.m_ImageLabel[1].pixmap()

        combine_width = pixmap1.width() + pixmap2.width()
        combine_height = pixmap1.height()

        bSero = False
        if self.m_bGaro_Combile == False:
            combine_width = pixmap1.width()
            combine_height = pixmap1.height() + pixmap2.height()
            bSero = True

        combined_pixmap = QPixmap(combine_width, combine_height)

        combined_pixmap.fill(Qt.transparent)

        painter = QPainter(combined_pixmap)

        painter.drawPixmap(0, 0, pixmap1)

        if bSero == False:
            painter.drawPixmap(pixmap1.width(), 0, pixmap2)
        else:
            painter.drawPixmap(0,pixmap1.height(),pixmap2)
        painter.end()

        self.m_strSaveName = self.text_input.text()
        new_name = self.m_strSaveName + self.m_extComboBox.currentText()

        for file in os.listdir('.'):
            if file.endswith(self.m_extComboBox.currentText()) and file.startswith(self.m_strSaveName):
                error_message = f"An occurred: 같은 이름이 있어."
                QMessageBox.critical(self, "저장 실패", error_message, QMessageBox.Ok)
                return

        if combined_pixmap.save(new_name):
            self.m_bHasImage[0] = False
            self.m_bHasImage[1] = False

            for n in self.m_ImageLabel:
                n.clear()
        else:
            error_message = f"An occurred: pixmap module error"
            QMessageBox.critical(self, "저장 실패", error_message, QMessageBox.Ok)




    def lerp(self, start, end):
        fMakeTime = self.m_lerp_time_delta
        self.m_lerp_time_delta += 0.016

        if self.m_lerp_time_delta > 1.0:
            self.m_bMove = False
            self.m_lerp_time_delta = 0.0
            return end

        return start + (end - start) * fMakeTime

    def call_lerp(self):
        if self.m_bGaro_Combile:
            for n in range(2):
                moveX = self.lerp(self.m_ImageLabel[n].geometry().x(), make_Move_Size[n]-300)
                moveY = self.lerp(self.m_ImageLabel[n].geometry().y(), 160)
                self.m_ImageLabel[n].setGeometry(int(moveX), int(moveY), 300, 300)
        else:
            for n in range(2):
                moveX = self.lerp(self.m_ImageLabel[n].geometry().x(), 160)
                moveY = self.lerp(self.m_ImageLabel[n].geometry().y(), make_Move_Size[n]-300)
                self.m_ImageLabel[n].setGeometry(int(moveX), int(moveY), 300, 300)

    def clear_Image(self, number):
        self.m_ImageLabel[number].clear()
        self.m_bHasImage[number] = False

    def always_move_button(self):
        for n in range(2):
            any = self.m_clear_button[n].geometry()
            self.m_clear_button[n].setGeometry(self.m_ImageLabel[n].geometry().x(),self.m_ImageLabel[n].geometry().y() + 200,any.width(),any.height())

    def Tick(self):
        if self.m_bMove == True:
            self.call_lerp()
        self.always_move_button()

