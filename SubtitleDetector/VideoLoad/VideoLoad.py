import cv2 as cv
import numpy as np
from Ctpn.ctpn_predict import get_det_boxes
import time
class VideoParser:
    def __init__(self,model,device):
        self.__img = []
        self.__img_frame = []

        self.__ret = []
        self.__ret_frame= []

        self.__model = model
        self.__device = device

    def GetVideoInfo(self, src):
        self.video = cv.VideoCapture(src)
        self.fps = self.video.get(cv.CAP_PROP_FPS)
        self.width = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.frames = self.video.get(cv.CAP_PROP_FRAME_COUNT)

    def Solve(self,rate,ymin,ymax,xmin,xmax):
        time0 = time.time()
        rate = int(self.fps) * rate
        i = 0
        self.__img.clear()
        self.__img_frame.clear()
        self.video.set(cv.CAP_PROP_POS_FRAMES, 0)
        while (True):
            flag, frame = self.video.read()
            if flag is False:
                break
            elif i % rate == 0:
                image = frame[ymin:ymax, xmin:xmax]
                binaryImage = self.Binary(image)
                if self.JudgeSubtitle(binaryImage):
                    if self.__img:
                        lastImage = self.Binary(self.__img[-1])
                        if self.CosineSimilarity(binaryImage, lastImage) < 0.9:
                            self.__img_frame.append(i)
                            self.__img.append(image)
                    else:
                        self.__img_frame.append(i)
                        self.__img.append(image)
            i += 1
        print("VideoSolve time： {}".format(time.time()-time0))

    def Detect(self):
        time0 = time.time()
        self.__ret.clear()
        self.__ret_frame.clear()
        length = len(self.__img)
        for i in range(length):
            image = get_det_boxes(self.__img[i],self.__model,self.__device)
            for j in image:
                self.__ret.append(j)
                self.__ret_frame.append(self.__img_frame[i])
        print("Detect time： {}".format(time.time() - time0))


    def Binary(self,img):
        img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
        kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(12,12))
        temp_img = cv.morphologyEx(img,cv.MORPH_TOPHAT,kernel)
        #output = cv.subtract(img,temp_img)
        _,output = cv.threshold(temp_img, 240, 255, cv.THRESH_BINARY)
        return output

    def Mse(self,img_a,img_b):
        e=(((img_a-img_b)**2).sum())/img_a.size*100
        #print(e)
        return e

    def CosineSimilarity(self,img_a,img_b):
        #avoid uint8 dot overflow
        x = np.array(img_a,dtype=np.int)
        y = np.array(img_b,dtype=np.int)
        x = x.flatten()
        y = y.flatten()
        dotnum = x.dot(y)
        norm1 = np.linalg.norm(x)
        norm2 = np.linalg.norm(y)
        e = dotnum / norm1 /norm2
        #print(e)
        return e

    def JudgeSubtitle(self,frame):
        temp = (frame**2).sum()/frame.size*100
        if temp < 0.06:
            return False
        return True

    def FrameTotime(self,frame,fps):
        s = int(frame/fps%60)
        f = int(frame/fps/60%60)
        img_name= '{0:02d}-{1:02d}'.format(f,s)
        return img_name

    def SaveFrame(self,output):
        length = len(self.__img)
        for i in range(length):
            img = self.__img[i]
            img_name = self.FrameTotime(self.__img_frame[i],self.fps)
            cv.imwrite(output+'/'+img_name+'.png',img)

    def SaveResult(self,output):
        length = len(self.__ret)
        last_name = ''
        cnt = 0
        for i in range(length):
            img = self.__ret[i]
            img_name = self.FrameTotime(self.__ret_frame[i],self.fps)
            if img_name == last_name:
                cnt += 1
                cv.imwrite(output + '/' + img_name + '(' + str(cnt) + ')' + '.png', img)
            else:
                cnt = 0
                cv.imwrite(output + '/' + img_name + '.png', img)
            if i!=0:
                last_name = img_name

# from Ctpn.ctpn_model import CTPN
# import Ctpn.config as config
# import torch,os
# model = CTPN()
# weights = 'D:/school/mxr/Ctpn/checkpoints/ctpn_0.2899.pth'
# device = torch.device('cuda:0')
# model.load_state_dict(torch.load(weights, map_location=device)['model_state_dict'])
# model.to(device)
# model.eval()
# t=VideoParser(model,device)
# t.GetVideoInfo('D:/school/mxr/TestVideo/zero.mp4')
# since = time.time()
# t.Solve(1,640,720,0,1280)
# t.Detect()
# print("Total time：",time.time()-since)
# t.SaveResult('D:/school/mxr/TestResult')

# import matplotlib.pyplot as plt
# with open(r"D:\data.txt",'r') as p:
#     str = p.read()
#     lists = str.split('\n')[:-1]
#     x = range(0,400)
#     lenth = len(lists)
#     print(lenth)
#     for i in range(lenth):
#         temp = float(lists[i])
#         lists[i] = temp/(i+1)
#     y = lists
#     plt.plot(x,y,'-')
#     plt.xlabel("batch")
#     plt.ylabel("total loss")
#     plt.show()
