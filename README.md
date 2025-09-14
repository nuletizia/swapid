<p align="center">
  <img src="https://id.piktid.com/logo.svg" alt="SwapID by PiktID logo" width="150">
  </br>
  <h3 align="center"><a href="[https://studio.piktid.com](https://studio.piktid.com/swap)">SwapID by PiktID</a></h3>
</p>


# SwapID - v3.3.1
[![Official Website](https://img.shields.io/badge/Official%20Website-piktid.com-blue?style=flat&logo=world&logoColor=white)](https://piktid.com)
[![Discord Follow](https://dcbadge.vercel.app/api/server/FJU39e9Z4P?style=flat)](https://discord.com/invite/FJU39e9Z4P)

Face Swap implementation by PiktID, also available online at <a href="https://studio.piktid.com/swap">studio.piktid.com</a>

This implementation relies on the <a href="https://github.com/piktid/eraseid">EraseID infrastructure and APIs</a>. 

## Getting Started
<a target="_blank" href="https://colab.research.google.com/drive/1thetaQymYgpHtFu1nAUwbsq3Su3vxXAC?usp=sharing">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

The following instructions suppose you have already installed a recent version of Python. For a general overview, please visit the <a href="https://api.piktid.com/docs">API documentation</a>.
To use any PiktID API, an access token is required.

> **Step 0** - Register <a href="https://studio.piktid.com">here</a>. 10 credits are given for free to all new users.

> **Step 1** - Clone the SwapID library
```bash
# Installation commands
$ git clone https://github.com/piktid/swapid.git
$ cd swapid
```

> **Step 2** - Export the email and password as environmental variables
```bash
$ export PIKTID_EMAIL={Your email here}
$ export PIKTID_PASSWORD={Your password here}
```

or the authenticaton tokens - get them in https://studio.piktid.com/profile -> Tokens & Sessions
```bash
$ export ACCESS_TOKEN={Your access token}
$ export REFRESH_TOKEN={Your refresh token}
```

> **Step 3** - You can provide both the absolute path of the target and face image (containing a person). Add the arguments
```python
...
--target_path 'mydir/mytarget.jpg'
or
--face_path 'mydir/mysource.jpg'
...
```

Alternatively, you can provide the url of the target and face image, as in the default example with the Einstein face on the Monalisa image.
```python
...
--target_url 'https://images.piktid.com/frontend/studio/swapid/target/monalisa.jpg'
or
--face_url 'https://images.piktid.com/frontend/studio/swapid/face/einstein.jpg'
...
```

> **Step 4** - Run the main function with the selected images
```bash
$ python3 main_swap.py --target_path 'mydir/mytarget.jpg' --face_path 'mydir/mysource.jpg'
```

Without any additional argument, SwapID will upload both images into PiktID's servers and provide (read the logs) the codes for both images, which you can reuse for further re-generations, one for the target 'abc' and one for the face 'xyz'. The swap asynchronously elaborates your images. It reads the notifications, and once the swap process is over, it extracts the link of the swapped image.

> **Step 5** - Rerun the main function with PiktID's codes
```bash
$ python3 main_swap.py --target_name 'abc' --face_name 'xyz'
```

> **Step 6** - Play with the parameters

If the result is not satisfactory enough, we recommend either changing the seed or strength of the source image (lower strength results in low influence of the source on the output)
```bash
$ python3 main_swap.py --target_name 'abc' --face_name 'xyz' --seed 1234 --strength '0.55'
```

> **Step 7** - Multiple faces

If you have a **target image** with multiple subjects, you need to inform the system, via the **idx_face** integer argument, which face to swap. As an example:
```bash
$ python3 main_swap.py --target_path 'mydir/mytarget.jpg' --face_path 'mydir/mysource.jpg' --idx_face 0
```

## Head Swap and Hair Transfer
It is also possible to include the hair in the swapping process. To do that, you need to run the command 
```bash
$ python3 main_swap.py --target_path 'mydir/mytarget.jpg' --face_path 'mydir/mysource.jpg' --hair
```

If you want to completely transfer the hairstyle of the source to the target, you can use the following command (which works for a strength greater than 0.5)
```bash
$ python3 main_swap.py --target_path 'mydir/mytarget.jpg' --face_path 'mydir/mysource.jpg' --hair --transfer_hair
```

## Skin Swap
If you want to adjust the body skin of the swapped image, you can use the following command
```bash
$ python3 main_swap.py --target_path 'mydir/mytarget.jpg' --face_path 'mydir/mysource.jpg' --skin
```
Please contact us for more details.

## Contact
office@piktid.com
