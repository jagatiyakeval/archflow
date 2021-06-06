import json
import cv2
import os
import numpy as np
import webcolors as wc
from itertools import chain
from pprint import pprint

# IMAGE_DIR = r"coco_images"
# COLOR_CODE_RGB_JSON = "color_code_RGB.json"
COCO_OUPUT_FILENAME = "coco_json_generator.json"

def get_rgb_to_hsv(rgb_codes):
    hsv_codes = {}
    for categ, rgb_color in rgb_codes.items():
        bgr_color = rgb_color[::-1]
        bgr_color_arr = np.uint8([[bgr_color]])
        bgr_hsv_color = cv2.cvtColor(bgr_color_arr, cv2.COLOR_BGR2HSV)
        bgr_hsv_color_lst =  list(map(int, bgr_hsv_color[0][0]))
        hsv_codes.update({categ:bgr_hsv_color_lst})
    return hsv_codes

def get_center_of_poly(pts):       
    M = cv2.moments(np.array([pts]))
    centX = int(M["m10"] / M["m00"])
    centY = int(M["m01"] / M["m00"])
    return (centX, centY)

def get_coco_images(images_dir):
    images_name_list = [x for x in os.listdir(images_dir) if x.endswith(".png")]
    images_list = []
    for image_name in images_name_list:
        temp_image_dict = {}
        img_id = images_name_list.index(image_name) + 1
        img_path = f"{images_dir}\{image_name}"
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        height = img.shape[0]
        width = img.shape[1]
        temp_image_dict.update({"id": img_id, "width": width, "height": height, "file_name": image_name, "path": img_path})
        images_list.append(temp_image_dict)
    return images_list

def get_coco_categories(rgb_codes):
    categories_list = []
    categ_list = list(rgb_codes.keys())
    for categ, rgb_color in rgb_codes.items():    
        temp_categ_dict = {}
        cat_id = categ_list.index(categ) + 1
        hex_clr = wc.rgb_to_hex(tuple(rgb_color))
        temp_categ_dict.update({"id":cat_id, "name": categ, "color": hex_clr})
        categories_list.append(temp_categ_dict)
    return categories_list

def get_coco_annotations(coco_images_list, coco_category_list, hsv_codes):
    annot_id = 0
    annotations_list = []
    for img_dict in coco_images_list:        
        im_id = img_dict["id"]
        image = cv2.imread(img_dict["path"])        
        for categ, hsv_color in hsv_codes.items():            
            cat_id = [categ_dict["id"] for categ_dict in coco_category_list if categ == categ_dict["name"]][0]
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lower = np.array(hsv_color, dtype="uint8")
            upper = np.array(hsv_color, dtype="uint8")
            mask = cv2.inRange(hsv, lower, upper)
            contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours[0]:
                temp_coco_annotations_dict = {}
                if len(contour) > 2: 
                    annot_id += 1 
                    poly_lst = [tuple(cntr_crd[0]) for cntr_crd in contour]
                    center_of_poly = get_center_of_poly(poly_lst)  
                    flat_merged_poly = list(chain.from_iterable(poly_lst))
                    segmentation_list = list(map(float, flat_merged_poly))
                    temp_coco_annotations_dict.update({"id": annot_id, "image_id": im_id, "category_id": cat_id, "segmentation": [segmentation_list]})
                    annotations_list.append(temp_coco_annotations_dict)
    return annotations_list


def write_coco_json(out_file_name, coco_data):
    with open(out_file_name, "w") as coco_outfile: 
        json.dump(coco_data, coco_outfile)

def generate_coco(image_dir, color_code, export_json):  

    coco_dict = {}  

    with open(color_code, "r") as rgb_inputfile:
        rgb_codes = json.load(rgb_inputfile)
    coco_categories_list = get_coco_categories(rgb_codes = rgb_codes)
    coco_dict.update({"categories": coco_categories_list})
    
    coco_images_list = get_coco_images(images_dir = image_dir)
    coco_dict.update({"images": coco_images_list})    
    
    hsv_codes = get_rgb_to_hsv(rgb_codes = rgb_codes)
    coco_annotations_list = get_coco_annotations(coco_images_list = coco_images_list, coco_category_list=coco_categories_list, hsv_codes = hsv_codes)
    coco_dict.update({"annotations": coco_annotations_list})

    if export_json:
        write_coco_json(out_file_name=f'{image_dir}_{COCO_OUPUT_FILENAME}', coco_data=coco_dict)

    return coco_dict


