<p align="center">
  <img src="https://id.piktid.com/logo.svg" alt="EraseID by PiktID logo" width="150">
  </br>
  <h3 align="center"><a href="[https://studio.piktid.com](https://id.piktid.com)">SwapID by PiktID</a></h3>
</p>


# SwapID - v3.1.0
[![Official Website](https://img.shields.io/badge/Official%20Website-piktid.com-blue?style=flat&logo=world&logoColor=white)](https://piktid.com)
[![Discord Follow](https://dcbadge.vercel.app/api/server/FJU39e9Z4P?style=flat)](https://discord.com/invite/FJU39e9Z4P)

FaceSwap implementation by PiktID (Beta version).

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
$ git clone https://github.com/nuletizia/swapid.git
$ cd swapid
```

> **Step 2** - Export the email and password as environmental variables
```bash
$ export SWAPID_EMAIL={Your email here}
$ export SWAPID_PASSWORD={Your password here}
```

> **Step 3** - You can provide both the absolute path of the target and face image (containing a person). Add the arguments
```python
...
--target_path 'mydir/mytarget.jpg'
or
--face_path 'mydir/mysource.jpg'
...
```

Alternatively, you can provide the url of the target and face image, as in the default example
```bash
$ python3 main_swap.py --target_url 'https://images.piktid.com/frontend/studio/swapid/target/monalisa.jpg' --face_url 'https://images.piktid.com/frontend/studio/swapid/face/einstein.jpg'
```

> **Step 4** - Run the main function
```bash
$ python3 main_swap.py --target_path 'mydir/mytarget.jpg' --face_path 'mydir/mysource.jpg'
```

Without any additional argument, SwapID will upload both images into PiktID's servers and provide (read the logs) the codes for both images, which you can reuse for further re-generations, one for the target 'abc' and one for the face 'xyz'. The swap asynchronously elaborates your images. It reads the notifications, and once the swap process is over, it extracts the link of the swapped image.

> **Step 5** - Rerun the main function with PiktID's codes
```bash
$ python3 main_swap.py --target_name 'abc' --face_name 'xyz' 
```

> **Step 6** - If the result is not satisfactory enough, we recommend changing the seed
```bash
$ python3 main_swap.py --target_name 'abc' --face_name 'xyz' --seed 1234
```



## Contact
office@piktid.com
