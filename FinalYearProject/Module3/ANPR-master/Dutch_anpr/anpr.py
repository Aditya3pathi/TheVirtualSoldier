from engine import detect, process, recognise, detect_belg, post_process
import cv2
import pandas as pd
import numpy as np
import argparse
import os
import glob
import sys
import time
import requests
from xlrd import open_workbook
import csv
from csv import DictReader
url = "https://www.fast2sms.com/dev/bulk"

parser = argparse.ArgumentParser()
parser.add_argument('--i', '-image', help="Input image path", type= str)
parser.add_argument('--v', '-video', help="Input video path", type= str)


args = parser.parse_args()
abs_path = os.path.dirname(sys.executable)


if args.i:
    start = time.time()
    try:
        os.mkdir('temp')
    except:
        files = glob.glob('tmp')
        for f in files:
            os.remove(f)

    input_image = cv2.imread(args.i)
    detection, crops = detect(input_image)

    i = 1
    for crop in crops:

        crop = process(crop)

        cv2.imwrite('temp/crop' + str(i) + '.jpg', crop)
        recognise('temp/crop' + str(i) + '.jpg', 'temp/crop'+str(i))
        post_process('temp/crop' + str(i) + '.txt')



        i += 1
        details = r'C:\\Users\\laptop\\Desktop\\FinalYearProject\\Module3\\ANPR-master\\Dutch_anpr\\CarData.csv'
        sheet1 = pd.read_csv(details)
        print(sheet1)

        with open("temp\crop1.txt", "r") as f:
            adi = f.readline().replace('\n',"")
            # word = adi.read.replace('\n',"")
            print(adi)


        # with open("CarData.csv", "rb") as f:
        #     csvreader = csv.reader(f, delimiter=",")
        #     for row in csvreader:
        #         if "56ZFDL" in row[0].values:
        #             print("56ZFDL spotted")

        with open('CarData.csv', 'r') as read_obj:
            csv_dict_reader = DictReader(read_obj)
            for row in csv_dict_reader:
                # print(adi)
                # print(row['NumberPlate'], row['Name'])
                if adi == row['NumberPlate'] :
                    Flag = 1
                    print(row['PhoneNumber'])
                    print(row['Name'])
                    break
                    # print("\nThis value exists in Dataframe")
  
                else:
                    # print("\nThis value does not exists in Dataframe")
                    Flag = 0
        if Flag == 1:
            print("exists")
            payload = "sender_id=FSTSMS&message= Dear "+ row['Name'] + "\nYour Car Just Passed Gate No 1&language=english&route=p&numbers="+ row['PhoneNumber'] + "" 
            headers = {
                        'authorization': "FkGn92thyupYK3aDmTRoicl6MCH7VJEjgbqfAXUPz4ZB0OvrL1eoM062IUZDsicThzG3AbJKjO8a7Cd1",
                        'Content-Type': "application/x-www-form-urlencoded",
                        'Cache-Control': "no-cache",
                        }
            response = requests.request("POST", url, data=payload, headers=headers)
            print(response.text)

        else:
            print("Not Existts")

        # creating a Dataframe object 
        # df = pd.DataFrame(details, columns = ['NumberPlate', 'Name', 'PhoneNumber'],index = ['0', '1'])
        # # print(df.NumberPlate)
        # # print("Dataframe: \n\n", df)
  
        # # chcek 'Ankit' exist in dataframe or not
        # if '56ZFDL' in df.values :
        #     print("\nThis value exists in Dataframe")
  
        # else :
        #     print("\nThis value does not exists in Dataframe")
        
    cv2.imwrite('temp/detection.jpg', detection)
    finish = time.time()
    print('Time processing >>>>>>  '+ str(finish-start))
elif args.v:
    cap = cv2.VideoCapture(0)

    # Check if camera opened successfully
    if cap.isOpened() == False:
        print("Error opening video stream or file")

    while (cap.isOpened()):
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret == True:

            frame, crop = detect(frame)
            # Display the resulting frame

            cv2.putText(frame, 'Press \'Q\' to exit !',(50, 50),cv2.FONT_HERSHEY_SIMPLEX,1,(0, 0, 255), 2)
            cv2.imshow('Frame', frame)

            # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

        # Break the loop
        else:
            break

    # When everything done, release the video capture object
    cap.release()

    # Closes all the frames
    cv2.destroyAllWindows()

else:
	print("--i : input image file path\n--v : input video file path")



# def runCode():
#     payload = "sender_id=FSTSMS&message=Car Number mesg&language=english&route=p&numbers=9819123607"
#     headers = {
#                 'authorization': "FkGn92thyupYK3aDmTRoicl6MCH7VJEjgbqfAXUPz4ZB0OvrL1eoM062IUZDsicThzG3AbJKjO8a7Cd1",
#                 'Content-Type': "application/x-www-form-urlencoded",
#                 'Cache-Control': "no-cache",
#                 }
#     response = requests.request("POST", url, data=payload, headers=headers)
#     print(response.text)
