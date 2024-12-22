#把labelImg標註好的voc格式轉換成yolo要用的格式

import os
import xml.etree.ElementTree as ET

def voc_to_yolo(xml_folder, img_folder, output_folder, label_map):
    os.makedirs(output_folder, exist_ok=True)

    for xml_file in os.listdir(xml_folder):
        if not xml_file.endswith('.xml'):
            continue

        xml_path = os.path.join(xml_folder, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        img_name = root.find('filename').text
        img_path = os.path.join(img_folder, img_name)

        # 確認圖片是否存在
        if not os.path.exists(img_path):
            print(f"Image {img_path} not found, skipping...")
            continue

        img_width = int(root.find('size/width').text)
        img_height = int(root.find('size/height').text)

        # 開始處理標註
        yolo_lines = []
        for obj in root.findall('object'):
            class_name = obj.find('name').text
            if class_name not in label_map:
                print(f"Class {class_name} not in label map, skipping...")
                continue
            class_id = label_map[class_name]

            bbox = obj.find('bndbox')
            xmin = float(bbox.find('xmin').text)
            ymin = float(bbox.find('ymin').text)
            xmax = float(bbox.find('xmax').text)
            ymax = float(bbox.find('ymax').text)

            # 轉換為 YOLO 格式
            x_center = ((xmin + xmax) / 2) / img_width
            y_center = ((ymin + ymax) / 2) / img_height
            width = (xmax - xmin) / img_width
            height = (ymax - ymin) / img_height

            yolo_lines.append(f"{class_id} {x_center} {y_center} {width} {height}")

        # 輸出為 YOLO 格式的 .txt 檔案
        txt_file = os.path.join(output_folder, os.path.splitext(img_name)[0] + ".txt")
        with open(txt_file, "w") as f:
            f.write("\n".join(yolo_lines))
        print(f"Converted {xml_file} to {txt_file}")

# 範例使用
xml_folder = "ex/ann"
img_folder = "ex/img"
output_folder = "ex/VtoY_output"
label_map = {"enemy": 0, "non":1}  # 修改為你的標籤對應
voc_to_yolo(xml_folder, img_folder, output_folder, label_map)
