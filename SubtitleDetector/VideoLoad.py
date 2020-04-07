import cv2 as cv


class VideoParser:
    def __init__(self):
        self.img=[]
        self.__img_frame=[]

    def LoadVideo(self, src):
        self.video = cv.VideoCapture(src)
        self.fps = self.video.get(cv.CAP_PROP_FPS)
        self.width = self.video.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.frames = self.video.get(cv.CAP_PROP_FRAME_COUNT)


    def Solve(self,rate,ymin,ymax,xmin,xmax):
        rate = self.fps * rate
        i = 0
        self.img.clear()
        self.__img_frame.clear()
        self.video.set(cv.CAP_PROP_POS_FRAMES,0)
        while(True):
            flag,frame = self.video.read()
            if flag is False:
                break
            elif i % rate == 0 :
                image = frame[ymin:ymax,xmin:xmax]
                if self.JudgeSubtitle(image):
                    if self.img:
                        last_image=self.img[-1]
                        if self.Mse(image,last_image) > 0.3:
                            self.__img_frame.append(i)
                            self.img.append(image)
                    else:
                        self.__img_frame.append(i)
                        self.img.append(image)
            i+=1


    def Binary(self,img):
        img = cv.cvtColor(img,cv.COLOR_RGB2GRAY)
        _,img = cv.threshold(img, 240, 255, cv.THRESH_BINARY)
        return img

    def Mse(self,img_a,img_b):
        img_a = self.Binary(img_a)
        img_b = self.Binary(img_b)
        e=(((img_a-img_b)**2).sum())/img_a.size*100
        return e

    def JudgeSubtitle(self,frame):
        frame = self.Binary(frame)
        h = frame.shape[0]
        w = frame.shape[1]
        temp = (frame**2).sum()/frame.size*100
        if temp < 0.1:
            return False
        return True

    def frameTotime(self,frame,fps):
        s = int(frame/fps%60)
        f = int(frame/fps/60%60)
        img_name= '{0:02d}-{1:02d}'.format(f,s)
        return img_name

    def SaveFrame(self,output):
        length = len(self.img)
        for i in range(length):
            img = self.img[i]
            img_name = self.frameTotime(self.__img_frame[i],self.fps)
            cv.imwrite(output+'/'+img_name+'.png',img)



