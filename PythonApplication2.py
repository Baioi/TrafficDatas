import cv2
import csv
import os
import glymur
import shutil
import random
from create_Annotations import *
from PIL import Image
def getFileList(filepath):
    f = open(filepath, 'r')
    lines = f.readlines()
    f.close()
    return lines
# 用来统计以及输出
def count(list, outpath):
    f = open(outpath, 'w')
    dict = {}
    for line in list:
        terms = line.split(';')
        classid = terms[5]
        classname = terms[11]
        if classname == 'D1b_schuin_rechts':
            classname = 'D1b_rechts_onder'
        if classid == '-1':
            continue
        if not classname in dict:
            dict[classname] = 1
        else:
            dict[classname] += 1
    list1= sorted(dict.iteritems(), key=lambda d:d[1], reverse = True)
    for classname in list1:
        f.write(classname[0] + ' ' + str(classname[1]) + '\n')
    f.close()
# 格式转换
def convert(path, outpath):
    extList = ['jp2']
    i = 6000
    for dirpath,dirnames,filenames in os.walk(path):
        #filelists = random.sample(filenames, 1)
        for file in filenames:
            # if i > 6000:
            #    return
            terms = file.split('.')
            ext = terms[len(terms)-1]
            # filename = str(i)
            # filename = filename.zfill(6)
            filename = terms[1]
            filename += ".jpg"
            try:
                if ext in extList:
                    filepath = os.path.join(dirpath, file)
                    jp2 = glymur.Jp2k(filepath)
                    r = jp2[:,:,0]
                    g = jp2[:,:,1]
                    b = jp2[:,:,2]

                    fullres = cv2.merge([b, g, r])
                    cv2.imwrite(os.path.join(outpath, filename), fullres)
            except:
                print terms[1]
            i += 1
def filter(path, outpath, list, imgpath):
    f = open(path, 'r')
    out = open(outpath,'w')
    lines = f.readlines()
    for line in lines:
        line = line.rstrip('\n')
        terms = line.split(';')
        try:
            if not terms[11] in list:
                continue
        except:
            print terms
            print '\n'
            print line
            print '\n'
            exit(1)
        name = terms[0].split('.')[1]
        name = name + '.jpg'
        if not os.path.exists(os.path.join(imgpath, name)):
            image = os.path.join('./BelgiumTS4Detection/images', name)
            shutil.copy(image, imgpath)
        terms[0] = name
        for term in terms:
            if term != '':
                out.write(term + ';')
        out.write('\n')
    out.close()
    f.close()

if __name__ == '__main__':
    
    
    '''-------------------------COUNT初步统计各标志的个数-------------------------'''
    COUNT = 0
    AnnoTestPath = './BelgiumTSD_annotations/BTSD_testing_GT.txt'
    AnnoTrainPath = './BelgiumTSD_annotations/BTSD_training_GT.txt'
    CountTestPath = './count/testing.txt'
    CountTrainPath = './count/training.txt'
    CountBothPath = './count/data_count.txt'

    '''-------------------CONVERT转换图片格式jp2->jpg----------------------'''
    CONVERT_FLAG = 0
    OVERWRITE = 0
    ImagePath = './BelgiumTS4Detection/'
    ImageOutPath = './BelgiumTS4Detection/images'
    # ImagePath = r'C:\Users\38317\Downloads\NonTS_TrainingBG1\NonTSImages\TrainingBG'
    # ImageOutPath = r'C:\Users\38317\Downloads\NonTS_TestingBG\NonTSImages\TestingBG\Images'
    
    '''-------------FILTER过滤掉抛弃的类--------------'''
    FILTER = 0
    TXTPath = './BelgiumTSD_annotations/BTSD_GT.txt'
    TXTOutPath1 = './BelgiumTSD_annotations/BTSD_GT_FILTER1.txt'
    TXTOutPath2 = './BelgiumTSD_annotations/BTSD_GT_FILTER2.txt'
    FilterImageOutPath1 = './BelgiumTS4Detection/filterimages1'
    FilterImageOutPath2 = './BelgiumTS4Detection/filterimages2'
    ValidList = ['C43', 'D7', 'C1', 'B1', 'B9', 'begin', 'D1b_rechts_onder', 'D9', 'F29', 'E1', 'B15A', 'A23', 'F4a', 'F19', 'D1b', 'B17', 'einde', 'F4b', 'E9b', 'C3', 'm3', 'F45', 'E3', 'E9a', 'C35', 'A14', 'A51', 'D5', 'F49', 'lang', 'F50', 'm2', 'F34A', 'F23A', 'F3a_h']
    ValidListFiltered = ['C43', 'D7', 'C1', 'B1', 'B9', 'D1b_rechts_onder', 'D9', 'F29', 'E1', 'B15A', 'A23', 'F4a', 'F19', 'D1b', 'B17', 'E9b', 'C3', 'F45', 'E3', 'E9a', 'C35', 'A14', 'A51', 'D5', 'F49', 'F50', 'F23A', 'F3a_h']
    
    '''---------------TRANSLATE制作XML----------------'''
    TRANSLATE = 0
    # _IMAGE_PATH = FilterImageOutPath1
    _IMAGE_PATH = FilterImageOutPath2
    # _TXT_PATH = TXTOutPath1
    _TXT_PATH = TXTOutPath2
    # _ANNOTATION_SAVE_PATH = 'Annotations1'
    _ANNOTATION_SAVE_PATH = 'Annotations2'

    '''-----------------制作ImageSets-----------------'''
    IMAGESETS = 1
    _IMAGE_SETS_PATH = 'ImageSets1'
    # _IMAGE_SETS_PATH = 'ImageSets2'
    _MAin_PATH = 'ImageSets1\\Main'
    # _MAin_PATH = 'ImageSets2\\Main'
    _XML_FILE_PATH = 'Annotations1'
    # _XML_FILE_PATH = 'Annotations2'

    '''-----------------DetailedImageSets-------------'''
    DETAIL = 1
    _VALID_LIST = ValidList
    # _VALID_LIST = ValidListFiltered
    _TXT_PATH = TXTOutPath1
    # _TXT_PATH = TXTOutPath2
    _MAin_PATH = 'ImageSets1\\Main'
    # _MAin_PATH = 'ImageSets2\\Main'
    _XML_FILE_PATH = 'Annotations1'
    # _XML_FILE_PATH = 'Annotations2'


    # 统计
    if COUNT == 1:
        if not os.path.exists('./count'):
            os.mkdir('./count')
        TestList = getFileList(AnnoTestPath)
        TrainList = getFileList(AnnoTrainPath)
        BothList = TestList + TrainList
        count(TestList, CountTestPath)
        count(TrainList, CountTrainPath)
        count(BothList, CountBothPath) 



    # 格式转换为jpg
    if CONVERT_FLAG == 1:
        if os.path.exists(ImageOutPath):
            if OVERWRITE == 1:
                shutil.rmtree(ImageOutPath)
                os.mkdir(ImageOutPath)
        else:
            os.mkdir(ImageOutPath)
        convert(ImagePath, ImageOutPath)



    # TXT_DATA改名
    if FILTER == 1:
        filter(TXTPath, TXTOutPath1, ValidList, FilterImageOutPath1)
        filter(TXTPath, TXTOutPath2, ValidListFiltered, FilterImageOutPath2)

    

    # 转换XML文件
    if TRANSLATE == 1:
        ouput_file = open(_TXT_PATH, 'r')
        current_dirpath = os.path.dirname(os.path.abspath('__file__'))

        if not os.path.exists(_ANNOTATION_SAVE_PATH):
            os.mkdir(_ANNOTATION_SAVE_PATH)

        lines = ouput_file.readlines()
        for line in lines:
            s = line.rstrip('\n')
            array = s.split(';')
            # 格式：name, class, xmin, ymin, xmax, ymax
            # [image];[x1];[y1];[x2];[y2];[class id];[superclass id];[pole id];[number on pole];[camera number];[frame number];[class label]
            attrs = dict()
            attrs['name'] = array[0]
            attrs['classification'] = array[11]
            attrs['xmin'] = array[1]
            attrs['ymin'] = array[2]
            attrs['xmax'] = array[3]
            attrs['ymax'] = array[4]

            # 构建XML文件名称
            xml_file_name = os.path.join(_ANNOTATION_SAVE_PATH, (attrs['name'].split('.'))[0] + '.xml')
            # print(xml_file_name)

            if os.path.exists( xml_file_name):
                # print('do exists')
                existed_doc = xml.dom.minidom.parse(xml_file_name)
                root_node = existed_doc.documentElement
            
                # 如果XML存在了, 添加object节点信息即可
                object_node = createObjectNode(existed_doc, attrs)
                root_node.appendChild(object_node)

                # 写入文件
                writeXMLFile(existed_doc, xml_file_name)
            
            else:
                # print('not exists')
                # 如果XML文件不存在, 创建文件并写入节点信息
                img_name = attrs['name']
                img_path = os.path.join(current_dirpath, _IMAGE_PATH, img_name)
                # 获取图片信息
                img = Image.open(img_path)
                width, height = img.size
                img.close()
            
                # 创建XML文件
                createXMLFile(attrs, width, height, xml_file_name)

    if IMAGESETS == 1:
        if os.path.exists(_IMAGE_SETS_PATH):
            print 'ImageSets dir is already exists'
            if os.path.exists(_MAin_PATH):
                print('Main dir is already in ImageSets')
        else:
            os.mkdir(_IMAGE_SETS_PATH)
            os.mkdir(_MAin_PATH)

        f_test = open(os.path.join(_MAin_PATH, 'test.txt'), 'w')
        f_train = open(os.path.join(_MAin_PATH, 'trainval.txt'), 'w')

        # 遍历XML文件夹
        for root, dirs, files in os.walk(_XML_FILE_PATH):
            print len(files)
            n = len(files)
            testlist = random.sample(files, int(n/3))
            for f in testlist:
                f_test.write(f.split('.')[0] + '\n')
            trainlist = [train for train in files if not train in testlist]
            for f in trainlist:
                f_train.write(f.split('.')[0] + '\n')

        f_test.close()
        f_train.close()

    if DETAIL == 1:
        f_test = open(os.path.join(_MAin_PATH, 'test.txt'), 'r')
        f_train = open(os.path.join(_MAin_PATH, 'trainval.txt'), 'r')
        xmls = os.listdir(_XML_FILE_PATH)
        xmlnames = xmls[:]
        for i in range(len(xmlnames)):
            xmlnames[i] = xmlnames[i].split('.')[0]
        testlist = []
        trainlist = []
        for line in f_test.readlines():
            line = line.rstrip('\n')
            if line != '':
                testlist.append(line)
        for line in f_train.readlines():
            line = line.rstrip('\n')
            if line != '':
                trainlist.append(line)
        for clas in _VALID_LIST:
            detailedtestfile = open(os.path.join(_MAin_PATH, clas + '_test.txt'), 'w')
            detailedtrainfile = open(os.path.join(_MAin_PATH, clas + '_trainval.txt'), 'w')
            for term in testlist:
                #打开XML文件
                xmlpath = os.path.join(_XML_FILE_PATH, xmls[xmlnames.index(term)])
                dom = xml.dom.minidom.parse(xmlpath)
                root = dom.documentElement
                namenodes = root.getElementsByTagName('name')
                names = []
                for name in namenodes:
                    if name.firstChild.data == 'Peic':
                        continue
                    else:
                        names.append(name.firstChild.data)
                if clas in names:
                    detailedtestfile.write(term + ' 1\n')
                else:
                    detailedtestfile.write(term + ' -1\n')
                
            for term in trainlist:
                #打开XML文件
                xmlpath = os.path.join(_XML_FILE_PATH, xmls[xmlnames.index(term)])
                dom = xml.dom.minidom.parse(xmlpath)
                root = dom.documentElement
                namenodes = root.getElementsByTagName('name')
                names = []
                for name in namenodes:
                    if name.firstChild.data == 'Peic':
                        continue
                    else:
                        names.append(name.firstChild.data)
                if clas in names:
                    detailedtrainfile.write(term + ' 1\n')
                else:
                    detailedtrainfile.write(term + ' -1\n')

        