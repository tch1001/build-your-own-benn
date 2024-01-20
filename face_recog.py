import face_recognition as fr
import os,pickle

sampleData = None #sample encodings

def init():
    global sampleData
    if os.path.exists('presaved.dat'):
        file=open('presaved.dat','rb')
        sampleData = pickle.load(file)
        file.close()
        return None

    dir='sample_pics'
    img_files = [f'{dir}/{file}' for file in os.listdir(dir) if file!='.DS_Store']
    sampleData = []
    xx=[]
    yy=[]

    #process images one by one to reduce RAM consumed
    for filename in img_files:
        image = fr.load_image_file(filename)
        encoding = fr.face_encodings(image)
        for enc in encoding:sampleData.append(enc)
        # if len(encoding)!=1:print(filename, len(encoding))

    file=open('presaved.dat','wb')
    pickle.dump(sampleData,file)
    file.close()

def checkIsBenn(filename):
    image = fr.load_image_file(filename)
    faceLoc = fr.face_locations(image)#,model='cnn')
    faceEncodings = fr.face_encodings(image,faceLoc)

    for encoding in faceEncodings:
        vecDist = fr.face_distance(sampleData,encoding)
        vecDist.sort()
        extremeLimit = vecDist.shape[0]//10

        vecDist2 = vecDist[extremeLimit:-extremeLimit] #remove top and bottom 10%: noisy

        if vecDist2.mean()<0.55:
            return True

    return False

init()

if __name__=='__main__':
    while True:
        f=input("File: ")
        if checkIsBenn(f): print("Yes")
        else: print("No")
