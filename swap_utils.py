from swap_api import upload_target_call as SWAP_upload_target_call, upload_face_call as SWAP_upload_face_call, swap_call as SWAP_call, handle_notifications_new_swap as SWAP_handle_notifications_new
from consistent_identities_api import upload_target_call as CI_upload_target_call, upload_face_call as CI_upload_face_call, consistent_generation_call as CI_call, handle_notifications_new_swap_download as CI_handle_notifications_new


def process_image(PARAM_DICTIONARY, TOKEN_DICTIONARY):

    # distinguish the type of process based on the endpoint used
    endpoint = PARAM_DICTIONARY.get('ENDPOINT')

    # SWAP ENDPOINT, TO BE USED FOR QUICK TESTS ON PORTRAITS
    if endpoint == 'swap':
        FACE_NAME = PARAM_DICTIONARY.get('FACE_NAME')
        TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

        # currently, it works only with one face in both source and target images
        if FACE_NAME is None:
            print('Uploading the face image')
            response_json = SWAP_upload_face_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
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
            response_json = SWAP_upload_target_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
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
        response_json = SWAP_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
        print(response_json)

        # Asynchronous API call to get the output
        FACE_NAME = PARAM_DICTIONARY.get('FACE_NAME')
        TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

        response_notifications, response_json = SWAP_handle_notifications_new(FACE_NAME, TARGET_NAME, TOKEN_DICTIONARY)
        if response_notifications is False:
            # Error
            return False

        links = response_json.get('links')
        print(f'links: {links}')
            
        return True

    # CONSISTENT IDENTITIES ENDPOINT, CURRENTLY USED IN ERASEID, TO BE USED ON PRODUCTION FOR ROBUST RESULTS
    elif endpoint == 'consistent_identities':
    
        FACE_NAME = PARAM_DICTIONARY.get('FACE_NAME')
        TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

        # currently, it works only with one face in both source and target images
        if FACE_NAME is None:

            print('Uploading the face image')
            response_json = CI_upload_face_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
            FACE_NAME = response_json.get('identity_name')
            print(f'Face name: {FACE_NAME}')
            PARAM_DICTIONARY['FACE_NAME'] = FACE_NAME
        else:
            print(f'Input face is already available with code: {FACE_NAME}, proceeding..')

        if TARGET_NAME is None:
            print('Uploading the target image')
            image_id = CI_upload_target_call(PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
            print(f'Target name: {image_id}')
            PARAM_DICTIONARY['TARGET_NAME'] = image_id
        else:
            print(f'Target image is already available with code: {TARGET_NAME}, proceeding..')

        idx_face = PARAM_DICTIONARY.get('IDX_FACE', 0)  # select which person in the target image you want to swap with the input face

        # WE NEED TO ADD A VERIFICATION MECHANISM OF THE IDX_FACE, BECAUSE IF THE IDX_FACE IS LARGER THAN THE HIGHEST MODIFIABLE INDEX, IT GETS STUCK
        print(f'Generating a new face using {FACE_NAME} for idx_face: {idx_face}')
        response = CI_call(idx_face=idx_face, PARAM_DICTIONARY=PARAM_DICTIONARY, TOKEN_DICTIONARY=TOKEN_DICTIONARY)
        print(response)

        # Asynchronous API call to get the output
        TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

        flag_response, response_notifications = CI_handle_notifications_new(TARGET_NAME, TOKEN_DICTIONARY)
        if flag_response is False:
            # Error
            print('Error retrieving the generated faces. No images found after 10 attempts')
            return False

        download_link = response_notifications.get('link')
        print('new image ready for download:', download_link)

    else:
        print('Endpoint error, check the endpoint argument')
        return False