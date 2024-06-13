from swap_api import swap_all_call, swap_call, upload_target_call, upload_face_call


def process_image(PARAM_DICTIONARY, TOKEN_DICTIONARY):

    FACE_NAME = PARAM_DICTIONARY.get('FACE_NAME')
    TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

    # currently, it works only with one face in both source and target images

    if FACE_NAME is None and TARGET_NAME is None:
        print('Start the full swap process')
        response_json = swap_all_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)

        links = response_json.get('links')
        face_name = response_json.get('face_name')
        target_name = response_json.get('target_name')

        print(f'links: {links}')
        print(f'face_name = {face_name}')
        print(f'target_name = {target_name}')
        PARAM_DICTIONARY['FACE_NAME'] = face_name
        PARAM_DICTIONARY['TARGET_NAME'] = target_name

    else:
        # resume, check if the images are already in the server
        if FACE_NAME is not None and TARGET_NAME is None:
            print('Uploading the target image')
            response_json = upload_target_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
            target_name = response_json.get('target_name')
            print(f'target_name: {target_name}')
            PARAM_DICTIONARY['TARGET_NAME'] = target_name

        elif FACE_NAME is None and TARGET_NAME is not None:
            print('Uploading the face image')
            response_json = upload_face_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
            face_name = response_json.get('face_name')
            print(f'face_name: {face_name}')
            PARAM_DICTIONARY['FACE_NAME'] = face_name
        else:
            print(f'Input file paths are both available, proceeding..')

        print('Resume the swap process')
        response_json = swap_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
        links = response_json.get('links')
        print(f'links: {links}')   

    return True
