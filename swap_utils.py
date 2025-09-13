from consistent_identities_api import upload_target_call as CI_upload_target_call, upload_face_call as CI_upload_face_call, consistent_generation_call as CI_call, handle_notifications_new_swap_download as CI_handle_notifications_new, handle_notifications_new_skin as CI_handle_notifications_new_skin, change_skin_call as CI_change_skin_call


def process_image(PARAM_DICTIONARY):

    # CONSISTENT IDENTITIES ENDPOINT, CURRENTLY USED IN ERASEID, TO BE USED ON PRODUCTION FOR ROBUST RESULTS
    
    FACE_NAME = PARAM_DICTIONARY.get('FACE_NAME')
    TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

    # currently, it works only with one face in both source and target images
    if FACE_NAME is None:

        print('Uploading the face image')
        response_json = CI_upload_face_call(PARAM_DICTIONARY=PARAM_DICTIONARY)
        FACE_NAME = response_json.get('identity_name')
        print(f'Face name: {FACE_NAME}')
        PARAM_DICTIONARY['FACE_NAME'] = FACE_NAME
    else:
        print(f'Input face is already available with code: {FACE_NAME}, proceeding..')

    if TARGET_NAME is None:
        print('Uploading the target image')
        image_id = CI_upload_target_call(PARAM_DICTIONARY=PARAM_DICTIONARY)
        print(f'Target name: {image_id}')
        PARAM_DICTIONARY['TARGET_NAME'] = image_id
    else:
        print(f'Target image is already available with code: {TARGET_NAME}, proceeding..')

    idx_face = PARAM_DICTIONARY.get('IDX_FACE', 0)  # select which person in the target image you want to swap with the input face

    print(f'Generating a new face using {FACE_NAME} for idx_face: {idx_face}')
    response = CI_call(idx_face=idx_face, PARAM_DICTIONARY=PARAM_DICTIONARY)
    print(response)

    # Asynchronous API call to get the output
    TARGET_NAME = PARAM_DICTIONARY.get('TARGET_NAME')

    flag_response, response_notifications = CI_handle_notifications_new(TARGET_NAME)
    if flag_response is False:
        # Error
        print('Error retrieving the generated faces. No images found after 10 attempts')
        return False

    download_link = response_notifications.get('link_hd')  # high quality version - pro user
    if download_link is None:
        download_link = response_notifications.get('link')  # low quality version
    if isinstance(download_link, dict) and not download_link:
        download_link = response_notifications.get('link')  # low quality version
    if download_link == '':
        download_link = response_notifications.get('link')  # low quality version

    CHANGE_SKIN = PARAM_DICTIONARY.get('CHANGE_SKIN')
    if CHANGE_SKIN:
        # pick does not to be called when changing skin
        idx_generation = 0 # select the first generation
        print('Editing the skin')
        response = CI_change_skin_call(image_address=image_id, idx_face=idx_face, idx_generation=idx_generation, PARAM_DICTIONARY=PARAM_DICTIONARY)
        print(f'Skin editing response:{response}')
        # Asynchronous API call
        response_notifications, skin_data = CI_handle_notifications_new_skin(image_id, idx_face)
        if response_notifications is False:
            # Error
            return False
        download_link = [skin_data.get("link").get("l")]
    
    # print(response_notifications)
    print('new image ready for download:', download_link)
    return True