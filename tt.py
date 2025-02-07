import cv2


image_path = r'C:\Users\omarz\Desktop\Project\Scanned Report to EHR\OCR\Template Matching\Katrangi.jpg'

#Read the image using OpenCV
image = cv2.imread(image_path)

#Check if the image was successfully loaded
if image is None:
    print(f"Error: Unable to load the image from '{image_path}'")
else:
    #Display the image
    cv2.imshow("Image", image)

    #Wait until any key is pressed to close the window
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print("Image loaded and displayed successfully.")
