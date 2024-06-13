import requests
import json
from io import BytesIO
import base64
from PIL import Image, ImageCms


# -----------READ/WRITE FUNCTIONS------------
def open_image_from_url(url):
    response = requests.get(url, stream=True)
    if not response.ok:
        print(response)

    image = Image.open(BytesIO(response.content))
    return image


def open_image_from_path(path):
    f = open(path, 'rb')
    buffer = BytesIO(f.read())
    image = Image.open(buffer)
    return image

    return BytesIO(response.content)


def im_2_B(image):
    # Convert Image to buffer
    buff = BytesIO()

    if image.mode == 'CMYK':
        image = ImageCms.profileToProfile(image, 'ISOcoated_v2_eci.icc', 'sRGB Color Space Profile.icm', renderingIntent=0, outputMode='RGB')

    image.save(buff, format='PNG',icc_profile=image.info.get('icc_profile'))
    img_str = buff.getvalue()
    return img_str


def im_2_buffer(image):
    # Convert Image to bytes 
    buff = BytesIO()

    if image.mode == 'CMYK':
        image = ImageCms.profileToProfile(image, 'ISOcoated_v2_eci.icc', 'sRGB Color Space Profile.icm', renderingIntent=0, outputMode='RGB')

    image.save(buff, format='PNG',icc_profile=image.info.get('icc_profile'))
    return buff


def b64_2_img(data):
    # Convert Base64 to Image
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)
    

def im_2_b64(image):
    # Convert Image 
    buff = BytesIO()
    image.save(buff, format='PNG')
    img_str = base64.b64encode(buff.getvalue()).decode('utf-8')
    return img_str


# -----------PROCESSING FUNCTIONS------------
def start_call(email, password, server_mode='production'):
    # Get token
    if server_mode == 'production':
        URL_API = 'https://api.piktid.com/api'
    else:
        print('Error server mode, exiting..')
        return {}
    print(f'Logging to: {URL_API}')

    response = requests.post(URL_API+'/tokens', data={}, auth=(email, password))
    response_json = json.loads(response.text)
    ACCESS_TOKEN = response_json['access_token']
    REFRESH_TOKEN = response_json['refresh_token']

    return {'access_token': ACCESS_TOKEN, 'refresh_token': REFRESH_TOKEN, 'url_api': URL_API, 'server_mode': server_mode}


def refresh_call(TOKEN_DICTIONARY):
    # Get token using only access and refresh tokens, no mail and psw
    URL_API = TOKEN_DICTIONARY.get('url_api')
    response = requests.put(URL_API+'/tokens', json=TOKEN_DICTIONARY)
    response_json = json.loads(response.text)
    ACCESS_TOKEN = response_json['access_token']
    REFRESH_TOKEN = response_json['refresh_token']

    return {'access_token': ACCESS_TOKEN, 'refresh_token': REFRESH_TOKEN, 'url_api': URL_API}


# UPLOAD ENDPOINTS
def upload_target_call(PARAM_DICTIONARY, TOKEN_DICTIONARY):

    target_full_path = PARAM_DICTIONARY.get('TARGET_PATH')

    OPTIONS_DICT = {}

    # start the generation process given the image parameters
    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/swap/target', 
                             headers={'Authorization': 'Bearer '+TOKEN},
                             files={'target': open(target_full_path, 'rb')},
                             data={'options': json.dumps(OPTIONS_DICT)},
                             )

    if response.status_code == 401:
        TOKEN_DICTIONARY = refresh_call(TOKEN_DICTIONARY)
        TOKEN = TOKEN_DICTIONARY.get('access_token', '')
        # try with new TOKEN
        response = requests.post(URL_API+'/swap/target', 
                                 headers={'Authorization': 'Bearer '+TOKEN},
                                 files={'target': open(target_full_path, 'rb')},
                                 data={'options': json.dumps(OPTIONS_DICT)},
                                 )

    response_json = json.loads(response.text)

    return response_json


def upload_face_call(PARAM_DICTIONARY, TOKEN_DICTIONARY):

    face_full_path = PARAM_DICTIONARY.get('FACE_PATH')

    OPTIONS_DICT = {}

    # start the generation process given the image parameters
    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/swap/face', 
                             headers={'Authorization': 'Bearer '+TOKEN},
                             files={'face': open(face_full_path, 'rb')},
                             data={'options': json.dumps(OPTIONS_DICT)},
                             )

    if response.status_code == 401:
        TOKEN_DICTIONARY = refresh_call(TOKEN_DICTIONARY)
        TOKEN = TOKEN_DICTIONARY.get('access_token', '')
        # try with new TOKEN
        response = requests.post(URL_API+'/swap/face', 
                                 headers={'Authorization': 'Bearer '+TOKEN},
                                 files={'face': open(face_full_path, 'rb')},
                                 data={'options': json.dumps(OPTIONS_DICT)},
                                 )

    response_json = json.loads(response.text)

    return response_json


# SWAP FACES
def swap_all_call(PARAM_DICTIONARY, TOKEN_DICTIONARY):

    face_full_path = PARAM_DICTIONARY.get('FACE_PATH')
    target_full_path = PARAM_DICTIONARY.get('TARGET_PATH')

    SEED = PARAM_DICTIONARY.get('SEED')
    NUM_GENERATIONS = PARAM_DICTIONARY.get('NUM_GENERATIONS')

    OPTIONS_DICT = {}
    if SEED is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'seed': SEED}
    if NUM_GENERATIONS is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'num_generations': NUM_GENERATIONS}

    # start the generation process given the image parameters
    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/swap/all', 
                             headers={'Authorization': 'Bearer '+TOKEN},
                             files={'face': open(face_full_path, 'rb'), 'target': open(target_full_path, 'rb')},
                             data={'options': json.dumps(OPTIONS_DICT)},
                             )

    if response.status_code == 401:
        TOKEN_DICTIONARY = refresh_call(TOKEN_DICTIONARY)
        TOKEN = TOKEN_DICTIONARY.get('access_token', '')
        # try with new TOKEN
        response = requests.post(URL_API+'/swap/all',
                                 headers={'Authorization': 'Bearer '+TOKEN},
                                 files={'face': open(face_full_path, 'rb'), 'target': open(target_full_path, 'rb')},
                                 data={'options': json.dumps(OPTIONS_DICT)},
                                 )

    response_json = json.loads(response.text)

    return response_json


def swap_call(PARAM_DICTIONARY, TOKEN_DICTIONARY):

    SEED = PARAM_DICTIONARY.get('SEED')
    FACE_NAME = PARAM_DICTIONARY.get('FACE_NAME')
    TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')
    NUM_GENERATIONS = PARAM_DICTIONARY.get('NUM_GENERATIONS')

    OPTIONS_DICT = {}
    if SEED is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'seed': SEED}
    if NUM_GENERATIONS is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'num_generations': NUM_GENERATIONS}

    # start the generation process given the image parameters
    TOKEN = TOKEN_DICTIONARY.get('access_token', '')
    URL_API = TOKEN_DICTIONARY.get('url_api')

    response = requests.post(URL_API+'/swap/generate', 
                             headers={'Authorization': 'Bearer '+TOKEN},
                             data={'face_name': FACE_NAME, 'target_name': TARGET_NAME, 'options': json.dumps(OPTIONS_DICT)},
                             )

    if response.status_code == 401:
        TOKEN_DICTIONARY = refresh_call(TOKEN_DICTIONARY)
        TOKEN = TOKEN_DICTIONARY.get('access_token', '')
        # try with new TOKEN
        response = requests.post(URL_API+'/swap/generate', 
                                 headers={'Authorization': 'Bearer '+TOKEN},
                                 data={'face_name': FACE_NAME, 'target_name': TARGET_NAME, 'options': json.dumps(OPTIONS_DICT)},
                                 )

    response_json = json.loads(response.text)

    return response_json
