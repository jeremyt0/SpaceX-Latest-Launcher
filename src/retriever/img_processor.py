import os
import sys

class Img_processor:

    # Downloads image from URL and saves it to local images directory
    @staticmethod
    def save_image(image_url, image_name):
        import urllib.request 
        # Save image from url
        img_dir = os.path.join(os.path.dirname(sys.argv[0]), 'interface', 'static', 'images')
        img_file = f'{img_dir}/{image_name}'

        urllib.request.urlretrieve(image_url, img_file)

        # Return image folder src
        return img_file.replace('/', '--2F--').replace('\\', '--5C--').replace(':', '--3A--')