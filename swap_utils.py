from swap_api import swap_call, upload_target_call, upload_face_call, handle_notifications_new_swap


def process_image(PARAM_DICTIONARY, TOKEN_DICTIONARY):

    FACE_NAME = PARAM_DICTIONARY.get('FACE_NAME')
    TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

    # currently, it works only with one face in both source and target images

    if FACE_NAME is None:
        print('Uploading the face image')
        response_json = upload_face_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
        face_name = response_json.get('face_name')
        print(f'face_name: {face_name}')
        if face_name is None:
            # server errors
            print('Server error, try again later')
            return False
        PARAM_DICTIONARY['FACE_NAME'] = face_name
    else:
        print(f'Input face is already available with code:{FACE_NAME}, proceeding..')

    if TARGET_NAME is None:
        print('Uploading the target image')
        response_json = upload_target_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
        target_name = response_json.get('target_name')
        print(f'target_name: {target_name}')
        if target_name is None:
            # most likely the swap machine is warming up, try again
            print('The swap machine is warming up, try again in 3 minutes')
            return False
        PARAM_DICTIONARY['TARGET_NAME'] = target_name
    else:
        print(f'Target image is already available with code:{TARGET_NAME}, proceeding..')

    print('Starting the swap process, async mode')
    response_json = swap_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)

    # Asynchronous API call to get the output
    FACE_NAME = PARAM_DICTIONARY.get('FACE_NAME')
    TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

    response_notifications, response_json = handle_notifications_new_swap(FACE_NAME, TARGET_NAME, TOKEN_DICTIONARY)
    if response_notifications is False:
        # Error
        return False

    links = response_json.get('links')
    print(f'links: {links}')

    return True
