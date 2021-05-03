import cv2

thres = 0.45 # Threshold to detect object
#選擇第一隻攝影機
cap = cv2.VideoCapture(0)
#設置影片撥放的大小
cap.set(3,1920)
cap.set(4,1080)


classNames= []
classFile = 'a.names'
with open(classFile,'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

n = cv2.dnn_DetectionModel(weightsPath,configPath)
n.setInputSize(320,320)
n.setInputScale(1.0/ 127.5)
n.setInputMean((127.5, 127.5, 127.5))
n.setInputSwapRB(True)
#持續開著Cam
while True:
    success,img = cap.read()
    classIds, confs, bbox = n.detect(img,confThreshold=thres)
    print(classIds,bbox)
  
    if len(classIds) != 0:
        for classId, confidence,box in zip(classIds.flatten(),confs.flatten(),bbox):
            cv2.rectangle(img,box,color=(0,255,0),thickness=2)
            cv2.putText(img,classNames[classId-1].upper(),(box[0]+10,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
            cv2.putText(img,str(round(confidence*100,2)),(box[0]+200,box[1]+30),
                        cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                
        
    
                        
   #顯示視窗，視窗名字Cam
    cv2.imshow("Cam",img)
    #延遲1ms，延遲不能為0，否則讀取的結果會為靜態圖  若按下q鍵退去cam
    if cv2.waitKey(1)& 0xFF == ord('q'):  
         break