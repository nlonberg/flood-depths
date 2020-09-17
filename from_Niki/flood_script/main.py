import sys
from PIL import Image
import detect_objects as detect
import estimate_depth as depth
import io

water_level_dict = {
    1: "0cm-30cm",
    2: "30cm-60cm",
    3: "60cm-90cm",
    4: "90cm-120cm",
    5: "120cm-150cm",
    6: "150cm-180cm",
    7: "180cm-210cm"
}

def get_depth(img):
    flood_height_sum = 0
    for annotation in img:
        flood_height_sum += depth.predict_image(annotation)

    avg_flood_height = round(flood_height_sum/len(img))
    return avg_flood_height

def main(arg_list):
    img_paths = []
    arg_num = 0
    parse_true = True
    while parse_true :
        try:
            img = Image.open(arg_list[arg_num])
            img_paths.append(arg_list[arg_num])
        except:
            parse_true = False
        arg_num += 1
    
    if len(img_paths) == 0:
        print("Error: invalid image paths.")
        sys.exit(1)

    cropped_imgs = detect.crop_flooded_objects_boundary(img_paths)
    
    flood_heights = []
    for i in range(len(cropped_imgs)):
        print(f"Image {i}: {water_level_dict[get_depth(cropped_imgs[i])]}")

    

if __name__ == "__main__":
    main(sys.argv[1:])