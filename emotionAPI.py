from Tkinter import *
import tkMessageBox
import httplib, urllib, base64
import tkFileDialog
'''
Emotion Demo 

author : momogary

date : 2016.03.31

using microsoft emotion free api, website :  https://www.microsoft.com/cognitive-services/en-us/emotion-api
'''

def faceDetection(image):
    
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': 'xxxxxxxx',
    }

    '''
    params = urllib.urlencode({
    'url': 'http://i.epochtimes.com/assets/uploads/2011/03/110312195005100445.jpg',
    })
    '''

    data = open(image, 'rb').read()
    
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        print "connect host"

        conn.request("POST", "/emotion/v1.0/recognize" , data , headers)
        print "sent request"

        response = conn.getresponse()
        print "get response"

        data = response.read()
        #print(data)
        data = eval(data)  # type list
        #print type(data)
        #print data
        conn.close()
        print "close connection"
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

    return data

def drawBBox(response , image):
    #from PIL import Image
    print "draw bounding box..."
    '''
    response = [
        {"faceRectangle":{"height":113,"left":624,"top":109,"width":113},"scores":{"anger":3.094097E-06,"contempt":5.47389654E-08,"disgust":1.40311486E-05,"fear":2.1335E-09,"happiness":0.9999826,"neutral":1.21930185E-07,"sadness":2.03058121E-08,"surprise":7.509437E-08}},
        {"faceRectangle":{"height":112,"left":230,"top":145,"width":112},"scores":{"anger":1.62075583E-12,"contempt":8.48001E-13,"disgust":4.43286114E-13,"fear":1.20183927E-15,"happiness":1.0,"neutral":5.69783977E-12,"sadness":2.131319E-14,"surprise":3.8522345E-12}},
        {"faceRectangle":{"height":103,"left":525,"top":184,"width":103},"scores":{"anger":5.1391353E-11,"contempt":1.26054183E-13,"disgust":6.300444E-11,"fear":2.00125181E-12,"happiness":1.0,"neutral":1.11211517E-12,"sadness":5.692164E-14,"surprise":6.25029639E-10}},
        {"faceRectangle":{"height":100,"left":348,"top":186,"width":100},"scores":{"anger":1.46614942E-10,"contempt":6.196312E-10,"disgust":3.89794273E-11,"fear":1.38707434E-10,"happiness":1.0,"neutral":4.158724E-09,"sadness":5.360124E-12,"surprise":1.9608418E-08}},
        {"faceRectangle":{"height":98,"left":121,"top":205,"width":98},"scores":{"anger":8.750456E-07,"contempt":1.87719866E-06,"disgust":6.564448E-07,"fear":4.57608245E-08,"happiness":0.999996245,"neutral":2.52363776E-07,"sadness":3.497753E-08,"surprise":3.27670975E-08}}
    ]
    '''

    import cv2
    import operator

    color = (255,0,0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    sortField = operator.itemgetter(1)
    textGap = 15

    im = cv2.imread(image)
    for rect in response:
        height = rect["faceRectangle"]["height"]
        width = rect["faceRectangle"]["width"]
        start_point = (rect["faceRectangle"]["left"],rect["faceRectangle"]["top"])
        end_point = ( start_point[0] + width , start_point[1] + height )
        cv2.rectangle(im, start_point, end_point, color, 2)

        emotions = rect["scores"]
        emotions = sorted(emotions.iteritems(),key=sortField,reverse=True)

        cnt = 1
        for tup in emotions:
            if tup[1] < 0.1:
                continue
            cv2.putText(im, "%s %.2f" % ( tup[0] ,tup[1]) ,( start_point[0], end_point[1] + textGap * cnt ), font, 0.4,(0,0,255),1)
            cnt += 1

    cv2.namedWindow("face detection")
    cv2.imshow("face detection", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

class ConfigWindow(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.master.title('Face and Emotion Detection') 
        self.master.geometry('500x300') 
        self.master.resizable(False, False) 
        self.pack(side = TOP,expand = YES,fill = BOTH) 
        bt = Button(self,text='choose file',command=self.showWin32Dialog) 
        bt.pack(side=TOP,expand=NO,fill=Y,pady=20,padx=20) 

    def showWin32Dialog(self):
        filetypes = ["jpg" , "bmp" , "png"]
        image = tkFileDialog.askopenfilename(initialdir = r'C:\Users\v-jingwc\Desktop\\')
        if image.split(".")[-1] in filetypes:
            response =  faceDetection(image)
            drawBBox(response , image)
        elif image == "":
            pass
        else:
            tkMessageBox.showinfo('Warning','this app just support image of type .jpg/.bmp/.png')

if __name__ == '__main__':
    ConfigWindow().mainloop()


