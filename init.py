

def enable_api(SD_DIRECTORY):
    text = """
    @echo off

    set PYTHON=
    set GIT=
    set VENV_DIR=
    set COMMANDLINE_ARGS= --api

    call webui.bat
    """
    file = open(SD_DIRECTORY + "\\webui-user.bat", "w")
    file.write(text)
    file.close()



