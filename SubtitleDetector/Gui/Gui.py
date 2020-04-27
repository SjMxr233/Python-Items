from Gui.DetectorForm import *
from PyQt5.QtMultimedia import QMediaContent
from VideoLoad.VideoLoad import VideoParser
from PyQt5.Qt import QUrl,QThread,pyqtSignal
import os

class DetectThread(QThread):
    completed_signal = pyqtSignal()
    def __init__(self,videoParser):
        super().__init__()
        self.videoParser = videoParser

    def setSolveArgs(self,rate,ymin,ymax,xmin,xmax):
        self.rate = rate
        self.ymin = ymin
        self.ymax = ymax
        self.xmin = xmin
        self.xmax = xmax

    def run(self):
        self.videoParser.Solve(self.rate,
                               self.ymin,self.ymax,
                               self.xmin,self.xmax)
        self.completed_signal.emit()

class ProcessBar(ProcessBarForm):
    def __init__(self):
        super().__init__()
        self.setupUI()

class Gui(MainWindowForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setMinimumWidth(700)
        self.setMinimumHeight(475)
        self.videoParser = VideoParser()
        self.process = ProcessBar()
        self.DetectThread = DetectThread(self.videoParser)
        self.DetectThread.completed_signal.connect(self.CloseProcessBar)

    def OpenFile(self):
        fileName,fileType=QtWidgets.QFileDialog.getOpenFileName(self,'文件读取',os.getcwd(),
                                                     "Video Files (*.mp4 *.avi)")

        if fileName != '':
            self.videoParser.LoadVideo(fileName)
            w = int(self.videoParser.width)
            h = int(self.videoParser.height)
            self.SetLabelInitText(w,h,self.videoParser.frames,self.videoParser.fps,fileName)
            self.SetVideoInitState(fileName)
            self.SetButtonInitState()
            self.SetRectItem(w,h)


    def SetRectItem(self,w,h):
        # [w,h] =[320,240] videoItem.size
        self.factor = w / 320
        self.hh = h / self.factor
        self.rectItem.setRect(0, (240 - self.hh) / 2, 320, self.hh)
        self.rectItem.updateHandlesPos()
        self.rectItem.setHH(self.hh, self.factor)


    def SetVideoInitState(self,fileName):
        self.video.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
        self.video.setVolume(0)
        self.video.play()
        self.video.pause()

    def SetLabelInitText(self,weight,height,frames,fps,fileName):
        s = int(frames / fps % 60)
        f = int(frames / fps / 60 % 60)
        self.totalTime = '{0:02d}:{1:02d}'.format(f, s)
        self.currentTime = '00:00'

        self.videoPath.setText(fileName)
        self.fps.setText(str(int(fps)))
        self.duration.setText(str(int(frames)))
        self.size.setText(str(weight) + 'X' + str(height))
        self.timeline.setText(self.currentTime + '/' + self.totalTime)
        self.clip.setText(str(weight) + 'X' + str(height))

    def SetButtonInitState(self):
        self.play.setEnabled(True)
        self.rectItem.setVisible(True)
        self.ctpn.setEnabled(True)
        self.save.setEnabled(False)

    def PlayVideo(self):
        if self.video.state() == QMediaPlayer.PlayingState:
            self.video.pause()
        else:
            self.video.play()

    def PositionChanged(self,pos):
        self.gv.fitInView(self.videoItem, QtCore.Qt.KeepAspectRatio)
        self.horizontalSlider.blockSignals(True)
        self.horizontalSlider.setValue(pos)
        self.horizontalSlider.blockSignals(False)
        s = self.video.position()//1000
        f = s//60
        s %= 60
        self.currentTime = '{0:02d}:{1:02d}'.format(f,s)
        self.timeline.setText(self.currentTime + '/' + self.totalTime)

    def DurationChanged(self,duration):
        self.horizontalSlider.setRange(0,duration)

    def MoveSliderPos(self,pos):
        self.video.setPosition(pos)

    def ClickSliderPos(self,pos):
        self.video.setPosition(pos)

    def resizeEvent(self, *args, **kwargs):
        self.gv.fitInView(self.videoItem,QtCore.Qt.KeepAspectRatio)

    def CtpnDetect(self):
        self.process.show()
        rate = int(self.cutRate.text())
        lt,rb = self.rectItem.getCropBox()
        f = self.factor
        offsetY = (240-self.hh)/2
        ymin = int((lt.y()-offsetY)*f)
        ymax = int((rb.y()-offsetY)*f)
        xmin = int(lt.x()*f)
        xmax = int(rb.x()*f)
        self.DetectThread.setSolveArgs(rate,ymin,ymax,xmin,xmax)
        self.DetectThread.start()


    def CloseProcessBar(self):
        self.process.close()
        self.save.setEnabled(True)

    def SaveResult(self):
        fileName = QtWidgets.QFileDialog.getExistingDirectory(self,'文件保存',os.getcwd())
        if fileName != '':
            # self.videoParser.SaveFrame(fileName)
            self.videoParser.SaveResult(fileName)

