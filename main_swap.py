import os
import sys
import argparse
from random import randint

from swap_utils import process_image
from swap_api import start_call


def check_range(value):
    ivalue = int(value)
    if ivalue <= 0 or ivalue > 1:
        raise argparse.ArgumentTypeError("%s is an invalid integer, only 1 generation is currently supported" % value)
    return ivalue


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--target_path', help='Input image file absolute path', type=str, default=None)
    parser.add_argument('--target_url', help='Input image url, use only if no target path was given', type=str, default='https://images.piktid.com/frontend/studio/swapid/target/monalisa.jpg')

    parser.add_argument('--face_path', help='Input face file absolute path', type=str, default=None)
    parser.add_argument('--face_url', help='Input face url, use only if no face path was given', type=str, default='https://images.piktid.com/frontend/studio/swapid/face/einstein.jpg')

    parser.add_argument('--target_name', help='Target image code name, it overwrites the target path', type=str, default=None)
    parser.add_argument('--face_name', help='Face image code name, it overwrites the face path', type=str, default=None)

    parser.add_argument('--seed', help='Generation seed', type=int, default=randint(0, 100000))

    args = parser.parse_args()

    # be sure to export your email and psw as environmental variables
    EMAIL = os.getenv("SWAPID_EMAIL")
    PASSWORD = os.getenv("SWAPID_PASSWORD")

    # Parameters
    # to be added

    # Generation parameters
    SEED = args.seed
    # to add more

    # Image parameters
    TARGET_PATH = args.target_path
    TARGET_URL = args.target_url
    TARGET_NAME = args.target_name

    # Swap parameters
    FACE_PATH = args.face_path
    FACE_URL = args.face_url
    FACE_NAME = args.face_name

    if TARGET_PATH is not None:
        if os.path.exists(TARGET_PATH):
            print(f'Using as input image the file located at: {TARGET_PATH}')
        else:
            print('Wrong filepath, check again')
    else:
        print('Target filepath not assigned, check again')
        if TARGET_URL is not None:
            print(f'Using the input image located at: {TARGET_URL}')
        else:
            print('Wrong target url, check again')
            sys.exit()

    if FACE_PATH is not None:
        if os.path.exists(FACE_PATH):
            print(f'Using the input face located at: {FACE_PATH}')
        else:
            print('Wrong face path, check again')
            sys.exit()
    else:
        if FACE_URL is not None:
            print(f'Using the input face located at: {FACE_URL}')
        else:
            print('Wrong face url, check again')
            sys.exit()

    # log in
    TOKEN_DICTIONARY = start_call(EMAIL, PASSWORD)

    # to add many more
    PARAM_DICTIONARY = {
            'TARGET_PATH': TARGET_PATH,
            'TARGET_URL': TARGET_URL,
            'FACE_PATH': FACE_PATH,
            'FACE_URL': FACE_URL,
            'TARGET_NAME': TARGET_NAME,
            'FACE_NAME': FACE_NAME,
            'SEED': SEED,
        }

    response = process_image(PARAM_DICTIONARY, TOKEN_DICTIONARY)
