import cv2


# Using raw string paths for images
shami = cv2.imread(r"D:/omar/Scanned Report to EHR/OCR/Template Matching/Shami_test.jpg", 0)
katrangi = cv2.imread(r"D:/omar/Scanned Report to EHR/OCR/Template Matching/Katrangi.jpg", 0)
wasara = cv2.imread(r"D:/omar/Scanned Report to EHR/OCR/Template Matching/wasara.jpg", 0)
teshren = cv2.imread(r"D:/omar/Scanned Report to EHR/OCR/Template Matching/Teshren.jpg", 0)
abnsena = cv2.imread(r"D:/omar/Scanned Report to EHR/OCR/Template Matching/Abnsena.jpg", 0)


katrangi = cv2.resize(katrangi, (400, 400), interpolation=cv2.INTER_AREA)
shami = cv2.resize(shami, (400, 400), interpolation=cv2.INTER_AREA)
wasara = cv2.resize(wasara, (400, 400), interpolation=cv2.INTER_AREA)
teshren = cv2.resize(teshren, (400, 400), interpolation=cv2.INTER_AREA)
abnsena = cv2.resize(abnsena, (400, 400), interpolation=cv2.INTER_AREA)
finder = cv2.SIFT_create()

# finder = cv2.xfeatures2d.SIFT_create()
kp_shami, des_shami = finder.detectAndCompute(shami, None)
kp_katrangi, des_katrangi = finder.detectAndCompute(katrangi, None)
kp_wasara, des_wasara = finder.detectAndCompute(wasara, None)
kp_teshren, des_teshren = finder.detectAndCompute(teshren, None)
kp_abnsena, des_abnsena = finder.detectAndCompute(abnsena, None)

lowe_ratio = 0.5
bf = cv2.BFMatcher()
def tm(image):
    img = cv2.imread(image)
    img1 = cv2.imread(image, 0)
    img1 = cv2.resize(img1, (700, 700), interpolation=cv2.INTER_AREA)
    img = cv2.resize(img, (700, 700), interpolation=cv2.INTER_AREA)
    kp1, des1 = finder.detectAndCompute(img1, None)
    matches_shami = bf.knnMatch(des1,des_shami, k=2)
    matches_katrangi = bf.knnMatch(des1 , des_katrangi ,k=2)
    matches_wasara = bf.knnMatch(des1, des_wasara, k=2)
    matches_teshren = bf.knnMatch(des1, des_teshren, k=2)
    matches_abnsena = bf.knnMatch(des1 ,des_abnsena ,k=2)

    s = []
    k = []
    w = []
    t = []
    a = []
    final = []
    for m1,n1 in matches_shami:
        if m1.distance < lowe_ratio*n1.distance:
            s.append([m1])
    final.append((len(s) ,'S'))
    for m2,n2 in matches_katrangi:
        if m2.distance < lowe_ratio*n2.distance:
            k.append([m2])
    final.append((len(k) ,'K'))
    for m3,n3 in matches_wasara:
        if m3.distance < lowe_ratio*n3.distance:
            w.append([m3])
    final.append((len(w) , 'W'))
    for m4,n4 in matches_teshren:
        if m4.distance < lowe_ratio*n4.distance:
            t.append([m4])
    final.append((len(t) , 'T'))
    for m5,n5 in matches_abnsena:
        if m5.distance < lowe_ratio*n5.distance:
            a.append([m5])
    final.append((len(a) , 'A'))
    final.sort()

    if final[-1][1] == 'K' and final[-1][0]>=15:
        # print('ktrangiii')
        return final[-1][1]
    elif final[-1][1] == 'S' and final[-1][0]>=20:
        return final[-1][1]
    elif final[-1][1] == 'W' and final[-1][0]>=15:
        return final[-1][1]
    elif final[-1][1] == 'T' and final[-1][0]>=15:
        return final[-1][1]
    elif final[-1][1] == 'A' and final[-1][0]>=15:
        return final[-1][1]
    else:return 'None'