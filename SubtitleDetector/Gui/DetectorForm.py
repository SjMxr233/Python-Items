
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5 import QtCore, QtGui, QtWidgets,QtMultimediaWidgets
from Gui.GraphicsRectItem import GraphicsRectItem
from Gui.Utils import Utils
class slider(QtWidgets.QSlider):
    def __init__(self,*args):
        super().__init__(*args)

    def mousePressEvent(self, QMouseEvent):
        per = QMouseEvent.pos().x()/self.width()
        duration = self.maximum() - self.minimum()
        val = per * duration
        self.setValue(val)
        super().mousePressEvent(QMouseEvent)

class GraphicsView(QtWidgets.QGraphicsView):
    def __init__(self,*args):
        super().__init__(*args)

    def wheelEvent(self, QWheelEvent):
        pass

class ProcessBarForm(QtWidgets.QWidget):
    def setupUI(self):
        self.setFixedSize(300,50)
        self.setWindowTitle('Detecting')
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint|QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.bar = QtWidgets.QProgressBar(self)
        self.bar.setGeometry(38,15,255,20)
        self.bar.setMinimum(0)
        self.bar.setMaximum(0)


class MainWindowForm(QtWidgets.QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.resize(700, 475)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.videoPathLabel = QtWidgets.QLabel(self.centralwidget)
        self.videoPath = QtWidgets.QLabel(self.centralwidget)
        self.videoPath.setText("None")

        self.verticalLayout.addWidget(self.videoPathLabel)
        self.verticalLayout.addWidget(self.videoPath)


        self.fpsLabel = QtWidgets.QLabel(self.centralwidget)
        self.fps = QtWidgets.QLabel(self.centralwidget)
        self.sizeLabel = QtWidgets.QLabel(self.centralwidget)
        self.size = QtWidgets.QLabel(self.centralwidget)

        self.horizontalLayout_2.addWidget(self.fpsLabel)
        self.horizontalLayout_2.addWidget(self.fps)
        self.horizontalLayout_2.addWidget(self.sizeLabel)
        self.horizontalLayout_2.addWidget(self.size)


        self.durationLabel = QtWidgets.QLabel(self.centralwidget)
        self.duration = QtWidgets.QLabel(self.centralwidget)
        self.clipLabel = QtWidgets.QLabel(self.centralwidget)
        self.clip = QtWidgets.QLabel(self.centralwidget)

        self.horizontalLayout_3.addWidget(self.durationLabel)
        self.horizontalLayout_3.addWidget(self.duration)
        self.horizontalLayout_3.addWidget(self.clipLabel)
        self.horizontalLayout_3.addWidget(self.clip)

        self.cutRateLabel = QtWidgets.QLabel(self.centralwidget)
        self.cutRate = QtWidgets.QLineEdit(self.centralwidget)
        regex = QtCore.QRegExp('^([1-9]|10)$')
        rangeNum =QtGui.QRegExpValidator(regex,self.cutRate)
        self.cutRate.setValidator(rangeNum)
        self.cutRate.setText('1')

        self.horizontalLayout_4.addWidget(self.cutRateLabel)
        self.horizontalLayout_4.addWidget(self.cutRate)

        self.ctpn = QtWidgets.QPushButton(self.centralwidget)
        self.ctpn.setEnabled(False)
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setEnabled(False)
        self.readme = QtWidgets.QLabel(self.centralwidget)
        pix = QtGui.QPixmap('./Gui/Asset/Help.png')
        self.readme.setPixmap(pix)

        self.verticalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_3.addWidget(self.ctpn)
        self.verticalLayout_3.addWidget(self.save)
        self.verticalLayout_3.addWidget(self.readme,2)


        #video
        self.video = QMediaPlayer(None,QMediaPlayer.VideoSurface)
        self.videoItem = QtMultimediaWidgets.QGraphicsVideoItem()
        self.scene = QtWidgets.QGraphicsScene()
        self.gv = GraphicsView(self.scene)
        self.gv.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gv.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.gv.setStyleSheet("background-color: black")
        self.scene.addItem(self.videoItem)
        self.video.setVideoOutput(self.videoItem)
        #video rect cover
        self.rectItem = GraphicsRectItem(self.videoItem)
        self.rectItem.setClip(self.clip)
        self.rectItem.setVisible(False)


        self.horizontalSlider = slider(self.centralwidget)
        self.horizontalSlider.setRange(0,0)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setStyleSheet(Utils.LoadQss('Gui/Asset/style.qss'))

        self.timeline = QtWidgets.QLabel(self.centralwidget)
        self.play = QtWidgets.QPushButton(self.centralwidget)
        self.play.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_MediaPlay))
        self.play.setEnabled(False)

        self.horizontalLayout.addWidget(self.play)
        self.horizontalLayout.addWidget(self.horizontalSlider)
        self.horizontalLayout.addWidget(self.timeline)

        self.verticalLayout_2.addWidget(self.gv)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_5.addLayout(self.verticalLayout_3,1)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2,8)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.toolBar = QtWidgets.QToolBar(MainWindow)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menuFile = QtWidgets.QMenu(self.menubar)


        self.actionLoadVideo = QtWidgets.QAction(MainWindow)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionLoadVideo)

        MainWindow.setCentralWidget(self.centralwidget)
        MainWindow.setMenuBar(self.menubar)
        MainWindow.setStatusBar(self.statusbar)
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.menuFile.triggered.connect(self.OpenFile)
        self.play.clicked.connect(self.PlayVideo)
        self.video.positionChanged.connect(self.PositionChanged)
        self.video.durationChanged.connect(self.DurationChanged)
        self.horizontalSlider.sliderMoved.connect(self.MoveSliderPos)
        self.horizontalSlider.valueChanged.connect(self.ClickSliderPos)
        self.ctpn.clicked.connect(self.CtpnDetect)
        self.save.clicked.connect(self.SaveResult)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        LabelFont = QtGui.QFont("微软雅黑",8,QtGui.QFont.Bold)
        DataFont = QtGui.QFont("Arial", 7, QtGui.QFont.Normal)
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SubtitleDetector"))
        self.videoPathLabel.setFont(LabelFont)
        self.videoPathLabel.setText(_translate("MainWindow", "Video Location："))
        self.videoPath.setFont(DataFont)

        self.fpsLabel.setFont(LabelFont)
        self.fpsLabel.setText(_translate("MainWindow", "FPS："))
        self.fps.setFont(DataFont)
        self.fps.setText(_translate("MainWindow", "None"))

        self.sizeLabel.setFont(LabelFont)
        self.sizeLabel.setText(_translate("MainWindow", "Video Size："))
        self.size.setFont(DataFont)
        self.size.setText(_translate("MainWindow", "None"))

        self.durationLabel.setFont(LabelFont)
        self.durationLabel.setText(_translate("MainWindow", "Frames："))
        self.duration.setFont(DataFont)
        self.duration.setText(_translate("MainWindow", "None"))

        self.clipLabel.setFont(LabelFont)
        self.clipLabel.setText(_translate("MainWindow", "Cut Size："))
        self.clip.setFont(DataFont)
        self.clip.setText(_translate("MainWindow", "None"))

        self.ctpn.setFont(LabelFont)
        self.ctpn.setText(_translate("MainWindow", "detect"))
        self.save.setFont(LabelFont)
        self.save.setText(_translate("MainWindow", "save"))

        self.timeline.setFont(LabelFont)
        self.timeline.setText(_translate("MainWindow", "--/--"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionLoadVideo.setText(_translate("MainWindow", "Load"))

        self.cutRateLabel.setFont(LabelFont)
        self.cutRateLabel.setText(_translate("MainWindow","Detect Rate(1s-10s)："))
