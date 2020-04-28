print("loaded")
import os
from pycocotools import coco
from shutil import copyfile
dataFolder = "/mnt/d/cocodata/2017/"

def GetDataSet():

    #c = coco.COCO(dataFolder + "annotations/captions_train2017.json")
    c = coco.COCO(dataFolder + "annotations/instances_train2017.json")
    #c = coco.COCO(dataFolder + "annotations/person_keypoints_train2017.json")
    #c = coco.COCO(dataFolder + "annotations/stuff_train2017.json")
    
    print(c.info())
    
    for i in c.dataset:
        s = c.dataset[i]
        print("%s: %s" % (i, len(s)))
        if i == "info":
            next
        else:
            try:
                print("\t%s" % s[0])
            except:
                pass
        #for x in c.datai:
        #    print("\t%s: %s" % (x, len(x)))
    
    #print(c.dataset["info"])
    #print(c.dataset["images"][0])
    #print(c.dataset["annotations"][0])
    
    #for i in c.dataset["categories"]:
    #    print(i)
    return c

def GetAnnotations(c, name = "giraffe", maxnum = None, copy=True, filenamelist = True):

    print("============")
    print("Getting: %s" % name)

    imageCount = 0
    annotationCount = 0

    inputfolder= dataFolder + "train2017" 
    outputfolder = dataFolder + name


    if filenamelist:
        names = open(dataFolder + "names_" + name + ".txt","w")

    try:
        os.mkdir( outputfolder ) 
    except FileExistsError:
        pass

    catIds = c.getCatIds(catNms = [name]) 
    cats = c.loadCats(catIds)
    imageIds = c.getImgIds( catIds= catIds )
    images = c.loadImgs(imageIds)
    
    print("number of images: %s" % (len(imageIds)))
    for image in images[:maxnum]:
        imageCount += 1
        print("\n%s" % (image))
        iid = image["id"]
        annIds = c.getAnnIds(imgIds=[iid], catIds = catIds)
        annotations = c.loadAnns(annIds)
        annoString = ""
        for a in annotations:
            annotationCount += 1
            string = ProcessAnnotation(image, a)
            print("\t" + string)
            annoString += string + "\n"
        print("\t" + annoString)

        fname = image["file_name"] 
        fnameonly,ext = fname.split(".")

        inputFile = inputfolder + "/" + fname
        outputFile = outputfolder + "/" + fname
        if filenamelist:
            names.write(outputFile + "\n")

        if copy:
            copyfile(inputFile , outputFile)
            ftxt = open(outputfolder + "/" + fnameonly + ".txt", "w")
            ftxt.write(annoString)
            ftxt.close()

    if filenamelist:
        names.close()

    return imageCount,annotationCount



fdata = {'license': 1, 'file_name': '000000376858.jpg', 'coco_url': 'http://images.cocodataset.org/train2017/000000376858.jpg', 'height': 508, 'width': 640, 'date_captured': '2013-11-16 14:25:35', 'flickr_url': 'http://farm5.staticflickr.com/4081/4919780905_ae902040ea_z.jpg', 'id': 376858}
annotation = {'segmentation': [[170.09, 484.31, 164.9, 456.29, 171.13, 346.28, 162.83, 379.49, 122.35, 412.7, 158.68, 351.47, 186.7, 287.13, 226.13, 265.34, 262.46, 238.35, 305.01, 197.88, 289.45, 180.23, 302.93, 177.12, 314.34, 155.32, 328.88, 163.63, 335.11, 176.09, 348.59, 171.93, 350.67, 180.23, 326.8, 211.36, 306.04, 231.09, 283.21, 281.93, 291.51, 322.41, 280.1, 340.05, 291.51, 424.12, 255.2, 458.36, 261.42, 483.27, 247.93, 494.69, 234.43, 490.53, 225.1, 466.66, 232.37, 447.99, 206.42, 402.32, 207.46, 357.7, 189.81, 385.71, 182.55, 491.57, 171.13, 491.57]], 'area': 25402.263250000004, 'iscrowd': 0, 'image_id': 376858, 'bbox': [122.35, 155.32, 228.32, 339.37], 'category_id': 25, 'id': 595318}

# convierts the box pixel coordinates found in the annotations to a proportion sutiable for neral training
def ProcessAnnotation(f,a):
    w = f['width']
    h = f['height']
    box = a['bbox']

    wout = box[2]/w
    hout = box[3]/h
    
    xout = box[0]/w+0.5*wout
    yout = box[1]/h+0.5*hout

    string = "0 %s %s %s %s" % (xout,yout,wout,hout)

    return string


#print(ProcessAnnotation(fdata, annotation))

c = GetDataSet()
name = "giraffe"
ic,ac = GetAnnotations(c, name,maxnum = None, copy = True,filenamelist = True)
print("Processed %s %s images and found %s %s(s)" % (ic,name,ac,name))
