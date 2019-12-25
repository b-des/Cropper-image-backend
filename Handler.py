from Cropper import Cropper
from urllib.parse import urlparse
import string
import random
import os
import io
import threading


class Handler:

    def __init__(self, images):
        self.images = images

    def to_pixel(self, value, multiplier=5) -> int:
        return int(int(value) * 2.835 * multiplier)

    def process(self, item):
        image_path = f"{item['dest'][0]}{os.path.normpath(urlparse(item['url']).path)}"

        if min(int(item['size']['width']), int(item['size']['height'])) > 300:
            multiplier = 2
        else:
            multiplier = 5
        dest_width = self.to_pixel(item['size']['width'], multiplier)
        dest_height = self.to_pixel(item['size']['height'], multiplier)
        with open(image_path, "rb") as f:
            filename, ext = os.path.splitext(os.path.basename(image_path))

            b = io.BytesIO(f.read())
            cropper = Cropper(b)

            # if need to rotate
            if int(item['rotate']) != 0:
                cropper.rotate(int(item['rotate']), False) 

            # if need to crop image
            if item['crop'] and item['crop'] != "false":
                # if width and height exist
                if int(item['crop']['w']) != 0 and int(item['crop']['h']) != 0:
                    crop = self.normalize_offsets(item['crop'])
                    cropper.crop(crop['x'], crop['y'], crop['w'], crop['h'])
                    cropper.resize(dest_width, dest_height)
                else:
                    # auto crop image at center
                    cropper.crop_center(dest_width, dest_height)
            else:
                # if no need to crop - fit image to container
                cropper.fit_to_container(dest_width, dest_height)

            # if need draw border
            if item['border'] != "none":
                cropper.add_border(self.to_pixel(item['borderThickness']), item['border'])

            # f"File name  is {filename} and extension is {ext}"
            salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            file = f"{filename}-{salt}-{item['size']['width']}-{item['size']['height']}.jpg"
            cropper.save(os.path.join(item['dest'][0], item['dest'][1]), file)
            del cropper

    def normalize_offsets(self, crop) -> dict:
        if crop["x"] < 0:
            crop["x"] = 0

        if crop["y"] < 0:
            crop["y"] = 0

        if crop["h"] > 100:
            crop["h"] = 100

        if crop["w"] > 100:
            crop["w"] = 100

        if crop["x"] + crop["w"] > 100:
            k = (crop["x"] + crop["w"] - 100) / 2
            crop["x"] -= k
            crop["w"] -= k

        if crop["y"] + crop["h"] > 100:
            k = (crop["y"] + crop["h"] - 100) / 2
            crop["y"] -= k
            crop["h"] -= k

        return crop

    def start(self):
        for i, item in enumerate(self.images):
            
            if item['original'] == False or item['original'] == "false":
                print(f"Start working on {i + 1} item of {len(self.images)}")
                # threading.Thread(target=self.process, args=[item]).start()
                self.process(item)

    def rotate(self, item):
        image_path = f"{item['dest'][0]}{os.path.normpath(urlparse(item['url']).path)}"
        with open(image_path, "rb") as f:
            filename, ext = os.path.splitext(os.path.basename(image_path))

            b = io.BytesIO(f.read())
            cropper = Cropper(b)
            cropper.rotate(int(item['deg']))
            salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            file = f"{filename}-{salt}-rotated{ext}"
            cropper.save(os.path.join(item['dest'][0], item['dest'][1], "tmp"), file)
            #return response.json(Object.assign({filename: file.replace(/\\/g, '/')}, {url, dest, uid, deg}));
            resp = {"filename": os.path.join(item['dest'][1], "tmp", file), "url": item['url'], "uid": item['uid'], "deg": item['deg']}
            print(resp)
            return {"filename": os.path.join(item['dest'][1], "tmp", file), "url": item['url'], "uid": item['uid'], "deg": item['deg']}
