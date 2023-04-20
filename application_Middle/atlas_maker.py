from PyQt5.Qt import *
import os
class Atlas_Maker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atlas image maker")
        self.setGeometry(100, 100, 1280, 720)

        self.setAcceptDrops(True)

        self.layout = QVBoxLayout(self)

        self.m_BackImageLabel = QLabel(self)
        self.m_BackImageLabel.setAlignment(Qt.AlignLeft)
        self.m_BackImageLabel.setGeometry(50, 200, 300, 300)
        self.m_BackImageLabel.setStyleSheet("background-color: black;")
        self.layout.addWidget(self.m_BackImageLabel)

        self.m_BaseImageLabel = QLabel(self)
        self.m_BaseImageLabel.setAlignment(Qt.AlignLeft)
        self.m_BaseImageLabel.setGeometry(50, 200, 300, 300)
        self.m_BaseImageLabel.setMouseTracking(True)
        self.m_BaseImageLabel.mousePressEvent = self.get_coord_and_crop
        self.m_BaseImageLabel.mouseMoveEvent = self.draw_Rect
        self.layout.addWidget(self.m_BaseImageLabel)

        self.m_NotionLabel = QLabel(self)
        self.m_NotionLabel.setText("F1:appand Image F2:goLeftIndex F3:GoRightIndex F10:DeleteCurIndex")
        font = self.m_NotionLabel.font()
        font_metrics = QFontMetrics(font)
        text_width = font_metrics.width(self.m_NotionLabel.text())
        text_height = font_metrics.height()
        self.m_NotionLabel.setGeometry(650, 20, 300, 300)

        self.m_NotionLabel.setFixedSize(text_width, text_height)

        self.m_AppendShortcut = QAction(self)
        self.m_AppendShortcut.setShortcut(Qt.Key_F1)
        self.m_AppendShortcut.triggered.connect(self.append_image)
        self.menuBar().addAction(self.m_AppendShortcut)

        self.m_spinboxW = QSpinBox(self)
        self.m_spinboxW.setGeometry(800, 50, 250, 50)

        self.m_spinboxW.setMaximum(5000)
        self.m_spinboxW.setValue(80)

        self.m_spinboxH = QSpinBox(self)
        self.m_spinboxH.setGeometry(800, 100, 250, 50)

        self.m_spinboxH.setMaximum(5000)
        self.m_spinboxH.setValue(80)

        self.layout.addWidget(self.m_spinboxW)
        self.layout.addWidget(self.m_spinboxH)

        self.m_newLabel_list = []
        self.m_CurLabelIndex = -1
        self.new_label_append()

        self.m_LeftShortcut = QAction(self)
        self.m_LeftShortcut.setShortcut(Qt.Key_F2)
        self.m_LeftShortcut.triggered.connect(self.go_left)
        self.menuBar().addAction(self.m_LeftShortcut)

        self.m_RightShortcut = QAction(self)
        self.m_RightShortcut.setShortcut(Qt.Key_F3)
        self.m_RightShortcut.triggered.connect(self.go_right)
        self.menuBar().addAction(self.m_RightShortcut)

        self.m_DeleteShortcut = QAction(self)
        self.m_DeleteShortcut.setShortcut("F10")
        self.m_DeleteShortcut.triggered.connect(self.delete_curindex)
        self.menuBar().addAction(self.m_DeleteShortcut)


        self.m_SaveButton = QPushButton("Save", self)
        self.m_SaveButton.setGeometry(800, 300, 100, 30)
        self.m_SaveButton.clicked.connect(self.SaveImages)

        self.layout.addWidget(self.m_SaveButton)

        self.m_checkbox = QCheckBox('ClipMode', self)
        self.m_checkbox.move(800, 400)
        self.layout.addWidget(self.m_checkbox)

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            FilePath = event.mimeData().urls()[0].toLocalFile()
            pixmap = QPixmap(FilePath)
            self.BaseimageImport(pixmap)
        event.accept()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def SaveImages(self):
        if len(self.m_newLabel_list) == 0:
            return
        merged_pixmap = None
        for i, label in enumerate(self.m_newLabel_list):
            pixmap = label.pixmap()
            if pixmap is not None:
                if merged_pixmap is None:
                    merged_pixmap = pixmap.copy()
                else:
                    oldwidth, oldheight = pixmap.width(), pixmap.height()
                    oldwidth += merged_pixmap.width()
                    Temp_pixmap = QPixmap(oldwidth, oldheight)
                    Temp_pixmap.fill(Qt.transparent)
                    painter = QPainter(Temp_pixmap)
                    painter.drawPixmap(0, 0, merged_pixmap.width(), merged_pixmap.height(), merged_pixmap)
                    painter.drawPixmap(merged_pixmap.width(), 0, pixmap.width(), pixmap.height(), pixmap)
                    painter.end()
                    merged_pixmap = Temp_pixmap

        strSaveName = "newAtlasImage"
        while True:
            strmakepath = os.getcwd()+"/"+strSaveName + '.png'
            if os.path.exists(strmakepath):
                strSaveName += "1"
            else:
                break
        strSaveName += ".png"
        merged_pixmap.save(strSaveName)

    def BaseimageImport(self, PixMap):
        self.m_BaseImageLabel.setPixmap(PixMap)
        self.m_BaseImageLabel.setFixedSize(PixMap.width(), PixMap.height())
        self.resize(self.width(), PixMap.height() + 10)
        parent_rect = self.rect()
        label_geometry = self.m_BaseImageLabel.geometry()
        if not parent_rect.contains(label_geometry):
            x_diff = max(label_geometry.right() - parent_rect.right(), 0)
            y_diff = max(label_geometry.bottom() - parent_rect.bottom(), 0)
            self.m_BaseImageLabel.setGeometry(label_geometry.x(), label_geometry.y() - y_diff, label_geometry.width(),label_geometry.height())
            self.m_BackImageLabel.setGeometry(self.m_BaseImageLabel.geometry())

    def get_coord_and_crop(self, event):
        if self.m_BaseImageLabel.pixmap() is None:
            return

        x = event.pos().x()
        y = event.pos().y()

        original_pixmap = self.m_BaseImageLabel.pixmap()

        cropped_pixmap = original_pixmap.copy(int(x - self.m_spinboxW.value() / 2), int(y - self.m_spinboxH.value() / 2), self.m_spinboxW.value(), self.m_spinboxH.value())
        self.m_newLabel_list[self.m_CurLabelIndex].setFixedSize(cropped_pixmap.width(),cropped_pixmap.height())
        self.m_newLabel_list[self.m_CurLabelIndex].setPixmap(cropped_pixmap)

        # self.m_newImageLabel.setPixmap(newPixMap)

    def delete_curindex(self):
        if len(self.m_newLabel_list) <= 1:
            return
        deletelabel = self.m_newLabel_list[self.m_CurLabelIndex]
        self.m_newLabel_list.remove(deletelabel)
        deletelabel.setParent(None)
        deletelabel.deleteLater()
        self.go_left()

    def draw_Rect(self, event):
        x = event.pos().x()
        y = event.pos().y()

        if self.m_checkbox.checkState():
            if x != 0:
                x = int(x / self.m_spinboxW.value()) * self.m_spinboxW.value() + self.m_spinboxW.value() / 2
            if y != 0:
                y = int(y / self.m_spinboxH.value()) * self.m_spinboxH.value() + self.m_spinboxH.value() / 2

        original_pixmap = self.m_BaseImageLabel.pixmap()
        if original_pixmap is None:
            return
        pixmap = original_pixmap.copy()
        painter = QPainter(pixmap)
        painter.setPen(QPen(Qt.red, 3))
        painter.drawRect(int(x - self.m_spinboxW.value() / 2), int(y - self.m_spinboxH.value() / 2),
                         self.m_spinboxW.value(), self.m_spinboxH.value())
        painter.end()

         # 부분 이미지를 다른 라벨에 표시
        self.m_BackImageLabel.setPixmap(pixmap)
        self.m_BackImageLabel.setFixedSize(pixmap.width(), pixmap.height())

    def append_image(self):
        if self.m_BaseImageLabel.pixmap() is None:
            return

        self.new_label_append()
        # self.m_newImageLabel.setFixedWidth(int(# self.m_newImageLabel.geometry().width() + self.m_spinboxW.value()))

    def new_label_append(self):
        newImageLabel = QLabel(self)
        width, height = self.m_spinboxW.value(), self.m_spinboxH.value()
        newImageLabel.setGeometry(800 + (len(self.m_newLabel_list)) * width, 200, width, height)
        newImageLabel.setStyleSheet("background-color: black;")
        self.layout.addWidget(newImageLabel)
        self.m_newLabel_list.append(newImageLabel)
        newImageLabel.show()
        self.m_CurLabelIndex += 1

    def indexing_red_rect(self):
        if len(self.m_newLabel_list) < 1:
            return
        for i, label in enumerate(self.m_newLabel_list):
            if i == self.m_CurLabelIndex:
                label.setStyleSheet("color: blue;"
                                    "background-color: #000000;"
                                    "border-style: dashed;"
                                    "border-width: 3px;"
                                    "border-color: #1E90FF")
            else:
                label.setStyleSheet("background-color: black;")

    def go_left(self):
        newIndex = self.m_CurLabelIndex
        newIndex -= 1
        if -1 == newIndex:
            newIndex = len(self.m_newLabel_list) - 1
        self.m_CurLabelIndex = newIndex

    def go_right(self):
        newIndex =self.m_CurLabelIndex
        newIndex += 1
        if len(self.m_newLabel_list) == newIndex:
            newIndex = 0
        self.m_CurLabelIndex = newIndex

    def Tick(self):
        self.indexing_red_rect()

