import xlsxwriter
import cv2
from os.path import join, exists
from os import listdir, makedirs

# Create an new Excel file and add a worksheet.
workbook = xlsxwriter.Workbook('demo.xlsx')
worksheet = workbook.add_worksheet()
worksheet.set_column('A:A', 20)
bold = workbook.add_format({'bold': True})

root = "/home/duytk/RABILOO/OCR/ALL_DATA/org_detect"
file = open("/home/duytk/RABILOO/OCR/E2E/PaddleOCR/test_result2.txt", 'r')
i=2
worksheet.write('A1', "Image name", bold)
worksheet.write('B1', "conf", bold)
worksheet.write('C1', "Pred", bold)
worksheet.write('D1', "Fix", bold)
worksheet.write('E1', "Image", bold)



for line in file.readlines():
    line = line.strip()
    img_name, text, conf = line.split('\t')
    img_path = join(root, img_name)
    image = cv2.imread(img_path)
    scale = image.shape[0]/60
    worksheet.write('A{}'.format(i), img_name)
    worksheet.write('C{}'.format(i), text)
    worksheet.write('D{}'.format(i), text)
    worksheet.write('B{}'.format(i), round(float(conf), 4))
    worksheet.insert_image('E{}'.format(i), img_path, {'x_scale': 1/scale, 'y_scale':1/scale})
    i+=5
workbook.close()