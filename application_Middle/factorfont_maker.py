from PyQt5.Qt import *

class factorfont_maker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Factor Font maker")
        self.setFixedSize(1280, 720)

        # self.setFont(QFont("Ubuntu", 20, QFont.Bold))

        self.layout = QVBoxLayout(self)

        self.m_FontComboBox = QComboBox(self)

        self.m_font_families = self.get_system_font_list()

        for font in self.m_font_families:
            self.m_FontComboBox.addItem(font)

        self.m_FontComboBox.currentIndexChanged.connect(self.handle_combobox)
        self.m_FontComboBox.setGeometry(100, 100, 250, 50)

        self.layout.addWidget(self.m_FontComboBox)

        self.m_text_input = QLineEdit(self)
        self.m_text_input.setGeometry(850, 230, 200, 50)
        self.m_text_input.setPlaceholderText("Enter str")

        self.combine_button = QPushButton("Show Image!!", self)
        self.combine_button.setGeometry(850, 390, 200, 50)
        # self.combine_button.setStyleSheet("background-color: #ff0000; color: #ffffff;")
        self.combine_button.clicked.connect(self.save_text_to_png)

        self.layout.addWidget(self.combine_button)
        self.m_previewLabel = QLabel(self)
        self.m_previewLabel.setGeometry(100, 160, 200, 100)
        self.m_previewLabel.setStyleSheet("color: blue;"
                              "background-color: #000000;"
                              "border-style: dashed;"
                              "border-width: 3px;"
                              "border-color: #1E90FF")

        self.m_SaveButton = QPushButton("Save Image!!",self)
        self.m_SaveButton.setGeometry(250, 360, 120, 50)
        self.m_SaveButton.clicked.connect(self.save_image)

        self.m_spinbox = QSpinBox(self)
        self.m_spinbox.setGeometry(100, 50, 250, 50)

        self.m_spinbox.setValue(6)
        self.m_spinbox.setMaximum(5000)

        self.layout.addWidget(self.m_previewLabel)
        self.layout.addWidget(self.m_SaveButton)
        self.layout.addWidget(self.m_spinbox)


        self.m_img = None
        self.m_pixmap = None

    def get_system_font_list(self):
        font_db = QFontDatabase()

        font_families = font_db.families()
        for n in font_families:
            font_db.addApplicationFont(n + ".ttf")



        return font_families

    def save_text_to_png(self):

        font_size = 72
        font = self.m_font_families[self.m_FontComboBox.currentIndex()]

        painter = QPainter()

        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

        painterfont = QFont(font, font_size, QFont.Bold)
        painterfont.setFamilies(self.m_font_families)

        painter.setFont(QFont(font, font_size, QFont.Bold))

        font_metrics = QFontMetrics(painter.font())

        text_width = font_metrics.width(self.m_text_input.text()) * self.m_spinbox.value()
        text_height = font_metrics.height() * self.m_spinbox.value()
        self.m_img = QImage(text_width, text_height, QImage.Format_ARGB32)
        self.m_img.fill(QColor(0, 0, 0, 0))

        painter.begin(self.m_img)
        pen = QPen(Qt.white)

        painter.setPen(pen)
        painter.scale(self.m_spinbox.value(),self.m_spinbox.value())
        # painter.setFont(QFont(font, font_size, QFont.Bold))

        painter.drawText(self.m_img.rect(), Qt.AlignLeft, self.m_text_input.text())
        painter.end()

        self.m_pixmap = QPixmap.fromImage(self.m_img)

        self.m_previewLabel.setPixmap(self.m_pixmap)
        self.m_previewLabel.setFixedSize(self.m_pixmap.width(), self.m_pixmap.height())

        self.m_previewLabel.update()


    def save_image(self):
        if self.m_img is None:
            return

        savefilename = self.m_text_input.text() + '.png'

        self.m_img.save(savefilename)
        self.m_img = None
        self.m_text_input.clear()

    def handle_combobox(self, index):
        self.m_FontComboBox.setCurrentIndex(index)
        self.m_FontComboBox.setCurrentText(self.sender().currentText())
        self.font().setFamily(self.sender().currentText())

        font = self.m_FontComboBox.font()
        font.setFamily(self.sender().currentText())

        self.m_FontComboBox.update()
        self.update()
    def Tick(self):
        iTest = 1

