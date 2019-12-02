from Cropper import Cropper


class Handler:

    def __init__(self, images):
        self.images = images

    def start(self):
        for i, val in enumerate(self.images):
           # print(val['url'])
            cropper = Cropper(val['url'])
            # cropper.crop_center(500, 500)
            cropper.fit_to_container(2520, 200).add_border(int(10 * 2.835), "#ff0000")
            #cropper.add_border(int(10 * 2.835), "#acbdab")
            cropper.save('uploads', val['url'])
            del cropper
