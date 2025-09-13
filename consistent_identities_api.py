import requests
import json
from io import BytesIO
import base64
from PIL import Image, ImageCms
from time import sleep
import os
from config import Config
from auth import refresh_call



# -----------READ/WRITE FUNCTIONS------------
def open_image_from_url(url):
    response = requests.get(url, stream=True)
    if not response.ok:
        print(response)

    image = Image.open(BytesIO(response.content))
    return image


def im_2_B(image):
    # Convert Image to buffer
    buff = BytesIO()

    if image.mode == 'CMYK':
        image = ImageCms.profileToProfile(image, 'ISOcoated_v2_eci.icc', 'sRGB Color Space Profile.icm', renderingIntent=0, outputMode='RGB')

    image.save(buff, format='PNG', icc_profile=image.info.get('icc_profile'))
    img_str = buff.getvalue()
    return img_str


def im_2_buffer(image):
    # Convert Image to bytes 
    buff = BytesIO()

    if image.mode == 'CMYK':
        image = ImageCms.profileToProfile(image, 'ISOcoated_v2_eci.icc', 'sRGB Color Space Profile.icm', renderingIntent=0, outputMode='RGB')

    image.save(buff, format='PNG', icc_profile=image.info.get('icc_profile'))
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





# -----------UPLOAD FUNCTIONS------------
def upload_target_call(PARAM_DICTIONARY):

    HEADSWAP = PARAM_DICTIONARY.get('HEADSWAP')

    target_full_path = PARAM_DICTIONARY.get('TARGET_PATH')
    if target_full_path is None:
        target_url = PARAM_DICTIONARY.get('TARGET_URL')
        image_response = requests.get(target_url)
        image_response.raise_for_status()  
        image_file = BytesIO(image_response.content)
        image_file.name = 'target.jpg' 
    else:
        image_file = open(target_full_path, 'rb')

    OPTIONS_DICT = {}

    if HEADSWAP:
        OPTIONS_DICT = {**OPTIONS_DICT, 'flag_hair': HEADSWAP}

    # start the generation process given the image parameters

    response = requests.post(Config.URL_API+'/consistent_identities/upload_target', 
                             headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                             files={'file': image_file},
                             data={'options': json.dumps(OPTIONS_DICT)},
                             )

    if response.status_code == 401:
        # try to refresh the token
        refresh_call()
        
        # try with new TOKEN
        response = requests.post(Config.URL_API+'/consistent_identities/upload_target', 
                                 headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"}, 
                                 files={'file': image_file},
                                 data={'options': json.dumps(OPTIONS_DICT)},
                                 )

    response_json = json.loads(response.text)
    # print(response_json)
    
    # below you find useful information if you want to create a UI
    
    # faces_dict = response_json.get('faces')  # faces dictionary
    number_of_detected_faces = len(response_json.get('faces', {}).get('approved_faces', []))  # information about the number of faces
    number_of_approved_faces = response_json.get('faces', {}).get('approved_faces', []).count(1)  # information about the number of faces approved for editing
    # indices_info = response_json.get('faces',{}).get('coordinates_list',[]) # coordiate list of all detected faces
    print('Number of detected faces:', number_of_detected_faces)
    print('Number of approved faces:', number_of_approved_faces)
    print(f'Select the face to swap with the parameter idx_face. From 0 to {number_of_detected_faces-1}. For example: --idx_face {number_of_detected_faces-1}.')
    
    image_address = response_json.get('image_id')  # image id
    return image_address


def upload_face_call(PARAM_DICTIONARY):

    face_full_path = PARAM_DICTIONARY.get('FACE_PATH')
    if face_full_path is None:
        face_url = PARAM_DICTIONARY.get('FACE_URL')
        face_response = requests.get(face_url)
        face_response.raise_for_status()  
        face_file = BytesIO(face_response.content)
        face_file.name = 'face.jpg' 
    else:
        face_file = open(face_full_path, 'rb')

    identity_name = PARAM_DICTIONARY.get('FACE_NAME')

    # start the generation process given the image parameters

    response = requests.post(Config.URL_API+'/consistent_identities/upload_face', 
                             headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                             files={'file': face_file},
                             data={'identity_name': identity_name},
                             )

    if response.status_code == 401:
        refresh_call()
        # try with new TOKEN
        response = requests.post(Config.URL_API+'/consistent_identities/upload_face', 
                                 headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"}, 
                                 files={'file': face_file},
                                 data={'identity_name': identity_name},
                                 )

    response_json = json.loads(response.text)
    # print(response_json)
    return response_json


# -----------SWAP FUNCTION------------
def consistent_generation_call(idx_face, PARAM_DICTIONARY):

    image_address = PARAM_DICTIONARY.get('TARGET_NAME')
    if image_address is None:
        return {'code':400, 'description':'id_image may not be null.'}
    
    identity_name = PARAM_DICTIONARY.get('FACE_NAME')

    SEED = PARAM_DICTIONARY.get('SEED')
    PROMPT_STRENGTH = PARAM_DICTIONARY.get('STRENGTH')
    TRANSFER_HAIR = PARAM_DICTIONARY.get('TRANSFER_HAIR')

    OPTIONS_DICT = {'flag_replace_and_download': True}

    if SEED is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'seed': SEED}

    if PROMPT_STRENGTH is not None:
        OPTIONS_DICT = {**OPTIONS_DICT, 'prompt_strength': PROMPT_STRENGTH}

    if TRANSFER_HAIR:
        OPTIONS_DICT = {**OPTIONS_DICT, 'transfer_hair': TRANSFER_HAIR}

    data = {'id_image': image_address, 'id_face': idx_face, 'identity_name': identity_name, 'options': json.dumps(OPTIONS_DICT)}
    print(f'data to send to generation: {data}')

    # start the generation process given the image parameters

    response = requests.post(Config.URL_API+'/consistent_identities/generate',
                             headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"},
                             json=data,
                             )
    # if the access token is expired
    if response.status_code == 401:
        refresh_call()
        # try with new TOKEN
        response = requests.post(Config.URL_API+'/consistent_identities/generate',
                                 headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"}, 
                                 json=data,
                                 )

    # print(response.text)
    response_json = json.loads(response.text)
    return response_json


def change_skin_call(image_address, idx_face, idx_generation):

    data = {
            'id_image': image_address, 
            'id_face': idx_face, 
            'id_generation': idx_generation, 
            'description_type': 'json', 
            'prompt': '{}'
        }
        
    print(f'data to send to skin editing: {data}')

    # start the generation process given the image parameters

    response = requests.post(Config.URL_API+'/ask_generate_skin_full_body',
                             headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"}, 
                             json=data,
                             )
    # print(response.text)
    # if the access token is expired
    if response.status_code == 401:
        refresh_call()
        # try with new TOKEN
        response = requests.post(Config.URL_API+'/ask_generate_skin_full_body',
                                 headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"}, 
                                 json=data,
                                 )
    response_json = json.loads(response.text)
    return response_json


# -----------NOTIFICATIONS FUNCTIONS------------
def get_notification_by_name(name_list):
    # name_list='new_generation, progress, error'

    response = requests.post(Config.URL_API+'/notification_by_name_json',
                             headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"}, 
                             json={'name_list': name_list},
                             # timeout=100,
                             )
    # if the access token is expired
    if response.status_code == 401:
        refresh_call()
        response = requests.post(Config.URL_API+'/notification_by_name_json',
                                 headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"}, 
                                 json={'name_list': name_list},
                                 # timeout=100,
                                 )
    # print(response.text)
    response_json = json.loads(response.text)
    return response_json.get('notifications_list',[])


def delete_notification(notification_id):
    print(f'notification_id: {notification_id}')
    response = requests.delete(Config.URL_API+'/notification/delete_json',
                               headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"}, 
                               json={'id': notification_id},
                               # timeout=100,
                               )
    # if the access token is expired
    if response.status_code == 401:
        refresh_call()
        response = requests.delete(Config.URL_API+'/notification/delete_json',
                                   headers={'Authorization': f"Bearer {os.environ['ACCESS_TOKEN']}"}, 
                                   json={'id': notification_id},
                                   # timeout=100,
                                   )
    # print(response.text)
    return response.text


def handle_notifications_new_swap_download(image_id):
    # check notifications to verify the generation status
    i = 0
    while i < 10:  # max 20 iterations -> then timeout
        i = i+1
        notifications_list = get_notification_by_name('download')
        notifications_to_remove = [n for n in notifications_list if (n.get('name') == 'download' and n.get('data').get('id_image') == image_id )]

        print(f'notifications_to_remove: {notifications_to_remove}')
        # remove notifications
        result_delete = [delete_notification(n.get('id')) for n in notifications_to_remove]
        print(result_delete)

        if len(notifications_to_remove) > 0:
            print(f'download for image_id {image_id} completed')
            return True, {**notifications_to_remove[0].get('data', {})}

        # check iteration
        if i >= 10:
            print('Timeout. Error in generating consistent faces')
            return False, {}

        # wait
        print('waiting for notification...')
        sleep(30)

    return False, {}


def handle_notifications_new_skin(image_id, idx_face):

    # check notifications to verify the generation status
    i = 0
    while i < 60:  # max 60 iterations -> then timeout
        i = i+1
        notifications_list = get_notification_by_name('new_skin,error')
        notifications_to_remove = [n for n in notifications_list if (n.get('name')=='new_skin' and n.get('data').get('address')==image_id and n.get('data').get('f')==idx_face and n.get('data').get('msg')=='done')]

        print(f'notifications_to_remove: {notifications_to_remove}')
        # remove notifications
        result_delete = [delete_notification(n.get('id')) for n in notifications_to_remove ]
        # print(result_delete)

        if len(notifications_to_remove) > 0:
            print(f'replace for face {idx_face} with full skin completed')
            return True, {**notifications_to_remove[0].get('data',{})}

        # wait
        print('waiting for notification...')
        sleep(10)

    print('Timeout. Error in editing skin')
    return False, {}
