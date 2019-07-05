import sys
import os
import cv2
import numpy as np

def process_image(image, output_folder):
    '''
    image : image name.
    output_folder : output folder name.
    '''
    image_name = image.split("/")[-1].split(".")[0]
    img = cv2.imread(image)
    ret, thresh1 = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    kernel = np.ones((1,1),np.uint8)  
    thresh1 = cv2.erode(thresh1, kernel)

    alpha = 255 - np.expand_dims(thresh1[:,:,0], axis=2)
    RGB = np.zeros(thresh1.shape)
    img = np.concatenate([RGB, alpha], axis=2)

    raw_height, raw_width, _  = img.shape
    scale = 2000/max(raw_height, raw_width)
    height = round(raw_height * scale)
    width = round(raw_width * scale)
    img = cv2.resize(img, (width,height))
    
    output_image_name = output_folder + image_name + ".png"
    print(output_image_name)

    cv2.imwrite(output_image_name, img)


def process_image_folder(input_folder, output_folder):
    '''
    input_folder : "folder_1/"
    output_folder : "folder_2/"
    '''
    for file in os.listdir(input_folder):
        if file.endswith("tif"):
            process_image(input_folder+file, output_folder)

if __name__ == "__main__" :
    input_folder, output_folder = sys.argv[1], sys.argv[2]
    process_image_folder(input_folder, output_folder)
