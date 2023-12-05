from base import *


def check_plex_debrid():
    try:
        process = "python ./plex_debrid/main.py --config-dir /config"
        subprocess.check_output(f"pgrep -f '{process}'", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

try:
    error_messages = []

    if RDAPIKEY and ADAPIKEY and RCLONEMN:
        RCLONEMN_RD = f"{RCLONEMN}_RD"
        RCLONEMN_AD = f"{RCLONEMN}_AD"
    else:
        RCLONEMN_RD = RCLONEMN_AD = RCLONEMN

    if RDAPIKEY and RCLONEMN:
        DIR = f'/data/{RCLONEMN_RD}/movies'
        if not os.path.isdir(DIR):
            error_messages.append("The RealDebrid rclone mount is not accessible")

    if ADAPIKEY and RCLONEMN:
        DIR = f'/data/{RCLONEMN_AD}/movies'
        if not os.path.isdir(DIR):
            error_messages.append("The AllDebrid rclone mount is not accessible")

    if os.getenv("PLEX_USER"):
        if not check_plex_debrid():
            error_messages.append("The plex_debrid process is not running.")

    if error_messages:
        raise Exception(" | ".join(error_messages))

except Exception as e:
    print(str(e), file=sys.stderr)
    exit(1)
