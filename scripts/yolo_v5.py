import os
import xml.etree.ElementTree as ET
from tqdm import tqdm
from PIL import Image

script_path = os.path.abspath(__file__)
script_folder = os.path.dirname(script_path)
print(script_folder)


folder_path = script_folder + "/../images/targets"


jpg_files = []
for file_name in os.listdir(folder_path):
    if file_name.endswith(".png"):
        jpg_files.append(file_name)
sorted_jpg_files = sorted(jpg_files, key=lambda x: x.lower())


annotation_dir = script_folder + "/../annotations/bboxes"

label_dir = script_folder + "/../label"
if not os.path.exists(label_dir):
    os.mkdir(label_dir)
jpg_dir = script_folder + "/../jpg"
if not os.path.exists(jpg_dir):
    os.mkdir(jpg_dir)


for file in tqdm(sorted_jpg_files):
    #
    png_image = Image.open(folder_path + "/" + file)
    jpg_image = png_image.convert("RGB")
    jpg_image.save(jpg_dir+"/"+os.path.splitext(file)[0] + ".jpg")

    #
    xml_file = os.path.splitext(file)[0] + ".xml"
    tree = ET.parse(annotation_dir+"/"+xml_file)
    root = tree.getroot()

    #
    size_element = root.find('.//size')
    imgw = float(size_element.find('width').text)
    imgh = float(size_element.find('height').text)

    #
    label_file = os.path.splitext(file)[0]+".txt"
    with open(label_dir+"/"+label_file, "w") as txt_file:
        for obj_element in root.findall('.//object'):
            bndbox_element = obj_element.find('bndbox')
            xmin = float(bndbox_element.find('xmin').text)
            ymin = float(bndbox_element.find('ymin').text)
            xmax = float(bndbox_element.find('xmax').text)
            ymax = float(bndbox_element.find('ymax').text)

            x = xmin/imgw
            y = ymin/imgh
            w = (xmax-xmin)/imgw
            h = (ymax-ymin)/imgh

            txt_file.write("0 {:.6f} {:.6f} {:.6f} {:.6f}".format(x, y, w, h) + "\n")
    txt_file.close()
