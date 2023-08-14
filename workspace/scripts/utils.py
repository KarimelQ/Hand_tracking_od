import xml.etree.cElementTree as ET
import xml.dom.minidom
import os
import cv2 

def generate_xml_annotation(folder, filename, xmin, ymin, xmax, ymax, width, height):
    annotation = ET.Element("annotation")

    folder_elem = ET.SubElement(annotation, "folder")
    folder_elem.text = folder

    filename_elem = ET.SubElement(annotation, "filename")
    filename_elem.text = filename.split('.')[0].split('/')[-1]+'.jpg'

    path_elem = ET.SubElement(annotation, "path")
    path_elem.text = filename

    source_elem = ET.SubElement(annotation, "source")
    database_elem = ET.SubElement(source_elem, "database")
    database_elem.text = "Unknown"

    size_elem = ET.SubElement(annotation, "size")
    width_elem = ET.SubElement(size_elem, "width")
    width_elem.text = str(width)
    height_elem = ET.SubElement(size_elem, "height")
    height_elem.text = str(height)
    depth_elem = ET.SubElement(size_elem, "depth")
    depth_elem.text = "3"

    segmented_elem = ET.SubElement(annotation, "segmented")
    segmented_elem.text = "0"

    object_elem = ET.SubElement(annotation, "object")
    
    name_elem = ET.SubElement(object_elem, "name")
    if('background' in filename):
        name_elem.text = "background"
    else:
        name_elem.text = "hand"

    pose_elem = ET.SubElement(object_elem, "pose")
    pose_elem.text = "Unspecified"
    truncated_elem = ET.SubElement(object_elem, "truncated")
    truncated_elem.text = "0"
    difficult_elem = ET.SubElement(object_elem, "difficult")
    difficult_elem.text = "0"
    bndbox_elem = ET.SubElement(object_elem, "bndbox")

    xmin_elem = ET.SubElement(bndbox_elem, "xmin")
    xmin_elem.text = str(xmin)
    ymin_elem = ET.SubElement(bndbox_elem, "ymin")
    ymin_elem.text = str(ymin)
    xmax_elem = ET.SubElement(bndbox_elem, "xmax")
    xmax_elem.text = str(xmax)
    ymax_elem = ET.SubElement(bndbox_elem, "ymax")
    ymax_elem.text = str(ymax)


    # Create a formatted XML string with line breaks and indentation
    xml_string = xml.dom.minidom.parseString(ET.tostring(annotation)).toprettyxml()

    return xml_string


def extract_from_xml(file):
    tree = ET.parse(file)
    root = tree.getroot()

    # extract the values
    path = root.find('path').text
    xmin = int(root.find('.//xmin').text)
    ymin = int(root.find('.//ymin').text)
    xmax = int(root.find('.//xmax').text)
    ymax = int(root.find('.//ymax').text)

    return path,xmin,ymin, xmax, ymax

def show_image_with_box(xml_path, xml_name, ext='.png'):
    xml = os.path.join(xml_path,xml_name)
    image_path = os.path.join(xml_path,xml_name.split('.')[-2]+ ext)
    image_name,xmin, ymin, xmax, ymax = extract_from_xml(xml)
    w = xmax-xmin
    h = ymax-ymin
    image = cv2.imread(image_path, cv2.COLOR_BGR2RGB)
    # cv2.rectangle(image, (xmin, ymin), (xmin +  w, ymax + h), (0, 255, 0), 2)
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    cv2.imshow('hand',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()