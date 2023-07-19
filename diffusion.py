
import os, base64, re
import socket, requests
import io, PIL, cv2

from PIL import Image
from datetime import datetime

from init import enable_api

SD_DIRECTORY = r'C:\Users\PSA56\Documents\code\stable-diffusion-webui'
OUTPUT_DIRECTORY = r'C:\Users\PSA56\Documents\code\training_image_generation\output\\'
LOCAL_HOST_LINK = 'http://127.0.0.1:7860'
PARAMETER_JSON = {
  "enable_hr": False,
  "denoising_strength": 0,
  "firstphase_width": 0,
  "firstphase_height": 0,
  "hr_scale": 2,
  "hr_upscaler": "",
  "hr_second_pass_steps": 0,
  "hr_resize_x": 0,
  "hr_resize_y": 0,
  "hr_sampler_name": "",
  "hr_prompt": "",
  "hr_negative_prompt": "",
  "prompt": ("close up of a piece of furniture in a well decorated living room, ultra realistic,"
            "ultra detailed, photograph, smooth surface, rich and detailed interior background,"
            "ultra realistic, ultra detailed, photograph, smooth surface, rich and detailed interior"
            "background, perfect viewpoint, highly detailed, wide-angle lens, hyper realistic,"  
            "polarizing filter, natural lighting, vivid colors, everything in sharp focus, HDR, UHD," 
            "64K, interior design, indoors"),
  "styles": [],
  "seed": 1116932915,
  "subseed": -1,
  "subseed_strength": 0,
  "seed_resize_from_h": -1,
  "seed_resize_from_w": -1,
  "sampler_name": "DPM++ 2M Karras",
  "batch_size": 1,
  "n_iter": 1,
  "steps": 30,
  "cfg_scale": 7,
  "width": 512,
  "height": 512,
  "restore_faces": False,
  "tiling": False,
  "do_not_save_samples": False,
  "do_not_save_grid": False,
  "negative_prompt": ("(((bad quality, worst quality))), unrealistic, distorted,low-resolution,analog,"
                      "EXTRA LIGHTS,computer graphic, graphic,art, digital art,abstract,visible lines,"
                      "visible strokes,colorless, Photoshop, video game, ugly, tiling,  out of frame, "
                      "mutation, mutated, extra limbs, extra legs, extra arms, disfigured, deformed, "
                      "body out of frame, blurry, bad art, bad anatomy, 3d render, people, person, "
                      "outdoors, outside"),
  "eta": 0,
  "s_min_uncond": 0,
  "s_churn": 0,
  "s_tmax": 0,
  "s_tmin": 0,
  "s_noise": 1,
  "override_settings": {},
  "override_settings_restore_afterwards": False,
  "script_args": [],
  "sampler_index": "DPM++ 2M Karras",
  "script_name": "",
  "send_images": True,
  "save_images": False,
  "alwayson_scripts": {
      "controlnet": {
      "args": [
        {
          "input_image": None, #insert base64 image here
          "mask" : None,
          "module" : "depth_midas", # pre-processor. turns img into depth map. make "none" to turn off
          "model": "control_v11f1p_sd15_depth [cfd03158]",
          "weight" : 1,
          "resize_mode": "Scale to Fit (Inner Fit)",
          "lowvram": True, 
          "processor_res": 512,
          "threshold_a": 64,
          "guidance_start": 0.0,
          "guidance_end": 0.5,
          "control_mode": "Balanced",
          "pixel_perfect": False
        }
      ]
    }
  }
}

def launch_backend() -> int:
    print("launching backend... 💤")
    os.chdir(SD_DIRECTORY)
    os.system('start cmd /k "webui-user --api"')
    if (server_is_free()):
        print("backend ready! 🚀")
        return 0
    else:
        return -1

def launch_backend_if_needed():
    port_number = int(LOCAL_HOST_LINK[-4:])
    if is_port_in_use(port_number):
        print("Backend is already running! 💪")
        return
    else:
        launch_backend()
        return

def set_model(model):
    response = requests.post(f'{LOCAL_HOST_LINK}/sdapi/v1/reload-checkpoint', json=model)
    print(response.json())

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def get_image(img_dir = None):
    if img_dir is not None:
        # with open(img_dir, "rb") as img_file:
        #     PARAMETER_JSON["alwayson_scripts"]["controlnet"]["args"][0]["input_image"] = str(base64.b64encode(img_file.read()))
        #     # print(PARAMETER_JSON["alwayson_scripts"]["controlnet"]["args"][0]["input_image"])
        img = cv2.imread(img_dir)
        retval, img = cv2.imencode('.png', img)
        encoded_image = base64.b64encode(img).decode('utf-8')
        PARAMETER_JSON["alwayson_scripts"]["controlnet"]["args"][0]["input_image"] = encoded_image

    print('⚒ generating image... ⚒')
    response = requests.post(f'{LOCAL_HOST_LINK}/sdapi/v1/txt2img', json=PARAMETER_JSON)
    try:
        response = response.json()['images'][:-1]
    except:
        # in case of an error print diagnostic information
        print('Reponse:')
        print(response)
        print()
        print('Reponse JSON:')
        print(response.json())
        # throw the same error to end the program
        response = response.json()['images'][:-1]
    for i in response:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))
        image.save(f"{OUTPUT_DIRECTORY}{re.sub('[_ :.]', '-', str(datetime.now()))}.png")
    print('image(s) saved! :D')
    PARAMETER_JSON["alwayson_scripts"]["controlnet"]["args"][0]["input_image"] = None

def server_is_free():
    i = 1
    while True:
        try:
            response = requests.get(LOCAL_HOST_LINK + '/login_check/')
            break
        except:
            pass
            i += 1
            if i == 50000:
                return False
    return True

if __name__ == '__main__':
    enable_api(SD_DIRECTORY)
    launch_backend_if_needed()
    get_image(r"C:\Users\PSA56\Desktop\furniture\reference_pictures\Screenshot 2023-07-11 122721.png")