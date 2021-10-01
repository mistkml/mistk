##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

import os
import base64

from mistk import logger


def encode_image(image_path):
    """
    Encodes an image file into a base64 bytes string

    :param image_path: Path to the image file to encode
    :returns: A string representation (UTF-8) of image encoded in base64
    """
    encoded = None
    with open(image_path, 'rb') as imgfile:
        encoded = base64.b64encode(imgfile.read())
    return encoded.decode('UTF-8')

def dict_from_images(image_dir, valid_exts=['.jpeg', '.jpg', '.png']):
    """
    Builds a dict of decoded images (UTF-8) given a dir containing images

    :param image_dir: Path to the directory containing the desired image files
    :param valid_exts: List of valid file extensions, in lower-case;
        defaults to ['.jpeg', '.jpg', '.png']
    :returns: Dict of UTF-8 decoded images, keyed by image file name
    """
    image_files = os.listdir(image_dir)
    image_dict = {}
    for image_file in image_files:
        image_name, image_ext = os.path.splitext(image_file)
        if image_ext.lower() not in valid_exts:
            logger.info(f"Skipping '{image_name}', it is not a valid file type")
            continue # skip files without an appropriate file extension
        image_path = os.path.join(image_dir, image_file)
        image_dict[image_name] = encode_image(image_path)
    return image_dict
