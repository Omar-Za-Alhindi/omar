import cv2
from OCR import RC, Processing as pr
from OCR import TemplateMatching

column_number = -1
template = ''

def main(image):
    global column_number
    global template

    template = TemplateMatching.tm(image)
    print('Template :', template)
    RC.Tmatching(image, template)
    img = cv2.imread('OCR/new_image.jpg')
    c = RC.get_Column('OCR/test.jpg')
    column_number = len(c)
    if template == 'S':
        column_number+=1
    print(c)
    print('Column :', len(c))
    r = RC.get_Rows('OCR/rows_crop.jpg')


    if template == 'K':
        x0 = 0
        x1 = c[1][0] + 5
        x2 = pr.Avg(c[1][0] + c[1][2], c[2][0]) + 10
        x3 = pr.Avg(c[2][0] + c[2][2], c[3][0]) - 10
        x4 = c[4][0]
        x5 = img.shape[1]
        ax = [int(x0), int(x1), int(x2), int(x3), int(x4), int(x5)]
        a = len(c) * len(r)
    if template == 'S':
        x0 = 0
        x1 = c[1][0]
        x2 = c[1][0] + c[1][2]
        x3 = c[2][0] - 10
        x4 = img.shape[1]
        ax = [x0, x1, x2, x3, x4]

    r1 = 0
    counter = 0
    for i in range(len(r) - 1):
        for j in range(len(ax) - 1):
            new_img = img.copy()
            new_img1 = img.copy()

            s_img = new_img[int(r[i]):int(r[i+1]),ax[j]:ax[j+1]]
            cv2.imwrite('OCR/images/' + str(counter)+'.jpg',s_img)
            counter = counter+1