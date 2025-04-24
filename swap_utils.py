from .consistent_identities_api import upload_target_call as CI_upload_target_call, upload_face_call as CI_upload_face_call, consistent_generation_call as CI_call, handle_notifications_new_swap_download as CI_handle_notifications_new


def process_image(PARAM_DICTIONARY, TOKEN_DICTIONARY):

    # CONSISTENT IDENTITIES ENDPOINT, CURRENTLY USED IN ERASEID, TO BE USED ON PRODUCTION FOR ROBUST RESULTS
    
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
    print('response CI_call:',response)
    if response.get('code') is not None:
        return False, ''

    # Asynchronous API call to get the output
    TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

    flag_response, response_notifications = CI_handle_notifications_new(TARGET_NAME, TOKEN_DICTIONARY)
    if flag_response is False:
        # Error
        print('Error retrieving the generated faces. No images found after 10 attempts')
        return False, ''

    download_link = response_notifications.get('link_hd')  # high quality version - pro user
    if download_link is None:
        download_link = response_notifications.get('link')  # low quality version
    if isinstance(download_link, dict) and not download_link:
        download_link = response_notifications.get('link')  # low quality version
    if download_link == '':
        download_link = response_notifications.get('link')  # low quality version
    
    # print(response_notifications)
    print('new image ready for download:', download_link)
    return True, download_link