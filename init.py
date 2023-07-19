

def enable_api(SD_DIRECTORY, MODEL_FILE):
    text = f"""
    @echo off

    set PYTHON=
    set GIT=
    set VENV_DIR=
    set COMMANDLINE_ARGS= --api --ckpt {SD_DIRECTORY}\\models\\Stable-diffusion\\{MODEL_FILE}

    call webui.bat
    """
    file = open(SD_DIRECTORY + "\\webui-user.bat", "w")
    file.write(text)
    file.close()

if __name__ == "__main__":
    SD_DIRECTORY = r'C:\Users\PSA56\Documents\code\stable-diffusion-webui'
    enable_api(SD_DIRECTORY)


