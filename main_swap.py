import os
import sys
import argparse
from random import randint

from swap_utils import process_image
from auth import piktid_auth


def check_range(value):
    ivalue = int(value)
    if ivalue < 0 or ivalue > 29:
        raise argparse.ArgumentTypeError("%s Only a maximum of 30 faces in the same photo is currently supported" % value)
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
    parser.add_argument('--strength', help='Input face have low impact on the output for low values of the strength (range 0-1)', type=float, default=None)

    # Consistent identities parameters
    parser.add_argument('--hair', help='Modify the hair of the target image', action='store_true')
    parser.add_argument('--transfer_hair', help='Transfer source hair to target when possible', action='store_true')
    parser.add_argument('--skin', help='Change also the skin', action='store_true')
    parser.add_argument('--idx_face', help='Index of the person to change in the target image', type=check_range, default=0)

    args = parser.parse_args()

    # Consistent identities parameters
    HEADSWAP = args.hair  # True if the swap shall include the hair (Head-swap)
    TRANSFER_HAIR = args.transfer_hair  # True if to transfer source hair into target
    CHANGE_SKIN = args.skin  # True if to change the skin of the target image

    IDX_FACE = args.idx_face  # index of the person in the target image to swap

    # Parameters
    # to be added

    # Generation parameters
    SEED = args.seed
    STRENGTH = args.strength
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

    # to add many more
    PARAM_DICTIONARY = {
            'HEADSWAP': HEADSWAP,
            'TRANSFER_HAIR': TRANSFER_HAIR,
            'IDX_FACE': IDX_FACE,
            'TARGET_PATH': TARGET_PATH,
            'TARGET_URL': TARGET_URL,
            'FACE_PATH': FACE_PATH,
            'FACE_URL': FACE_URL,
            'TARGET_NAME': TARGET_NAME,
            'FACE_NAME': FACE_NAME,
            'SEED': SEED,
            'STRENGTH': STRENGTH,
            'CHANGE_SKIN': CHANGE_SKIN,
        }

    # Authenticate and get the access token
    if not piktid_auth():
        print('Authentication failed, please check your credentials')
        sys.exit()
    
    response = process_image(PARAM_DICTIONARY)
