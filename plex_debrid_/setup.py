from base import *


logger = get_logger()

def pd_setup():
    logger.info("Configuring plex_debrid")
    settings_file = "./config/settings.json"
    ignored_file = "./config/ignored.txt"

    if not os.path.exists(settings_file):
        subprocess.run(
            ["touch", ignored_file], check=True
        )
    if not os.path.exists(settings_file):
        subprocess.run(
            ["cp", "./plex_debrid_/settings-default.json", settings_file], check=True
        )

    try:
        if not PLEXUSER:
            raise MissingEnvironmentVariable("PLEX_USER")
        if not PLEXTOKEN:
            raise MissingEnvironmentVariable("PLEX_TOKEN")
        if not RDAPIKEY and not ADAPIKEY:
            raise MissingAPIKeyException()
        if not PLEXADD:
            raise MissingEnvironmentVariable("PLEX_ADDRESS")
        with open(settings_file, "r+") as f:
            json_data = load(f)
            json_data["Plex users"][0] = [PLEXUSER, PLEXTOKEN]   
            json_data["Plex server address"] = PLEXADD
            json_data["Debrid Services"] = []
            if RDAPIKEY:
                json_data["Real Debrid API Key"] = RDAPIKEY
                json_data["Debrid Services"].append("Real Debrid")
            if ADAPIKEY:
                json_data["All Debrid API Key"] = ADAPIKEY 
                json_data["Debrid Services"].append("All Debrid")                
            if SHOWMENU:
                json_data["Show Menu on Startup"] = SHOWMENU.lower()
            if LOGFILE:
                json_data["Log to file"] = LOGFILE.lower()
            f.seek(0)
            dump(json_data, f, indent=4)
            f.truncate()
        logger.info("plex_debrid configuration complete")
        logger.info("Starting plex_debrid")            
    except Exception as e:
        logger.error("An error occurred while configuring plex_debrid. Exiting...")
        logger.error(str(e))
        raise