from base import *
from plexapi.server import PlexServer

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
        with open(settings_file, "r+") as f:
            json_data = load(f)
            library_update_services = json_data.get("Library update services", [])
            plex_library_refresh = json_data.get("Plex library refresh", [])
            library_collection_service = json_data.get("Library collection service", [])
            trakt_refresh_user = json_data.get("Trakt refresh user", [])
            
            def update_with_default_services(service_type, default_values, conflicting_values=[]):
                existing_services = json_data.get(service_type, [])
                for value in conflicting_values:
                    if value in existing_services:
                        existing_services.remove(value)
                for value in default_values:
                    if value not in existing_services:
                        existing_services.append(value)
                json_data[service_type] = existing_services

            if (PLEXUSER) and (JFAPIKEY or JFADD):
                raise Exception("Plex and Jellyfin cannot be configured at the same time. Please choose one.")
            if not PLEXUSER and not (JFAPIKEY and JFADD): 
                raise Exception("Please set either PLEX_USER or JF_API_KEY and JF_ADDRESS to enable plex_debrid")

            if JFAPIKEY or JFADD:
                if not JFAPIKEY:
                    raise MissingEnvironmentVariable("JF_API_KEY") 
                if not JFADD:                  
                    raise MissingEnvironmentVariable("JF_ADDRESS")
                json_data["Jellyfin API Key"] = JFAPIKEY
                json_data["Jellyfin server address"] = JFADD
                json_data["Plex users"] = []
                json_data["Plex server address"] = "http://localhost:32400"  
                update_with_default_services("Library collection service", ["Trakt Collection"], ["Plex Library"])
                update_with_default_services("Library update services", ["Jellyfin Libraries"], ["Plex Libraries"])
                json_data["Plex library refresh"] =  []                
                logger.info("plex_debrid configured for Jellyfin")
                if not trakt_refresh_user:
                    logger.info("Addtional configuration is required for Jellyfin. Please autorized and add your Trakt user by editing the Library collection service with the plex_debrid UI!")

            if PLEXUSER:
                if not PLEXUSER:
                    raise MissingEnvironmentVariable("PLEX_USER")
                if not PLEXTOKEN:
                    raise MissingEnvironmentVariable("PLEX_TOKEN")
                if not PLEXADD:
                    raise MissingEnvironmentVariable("PLEX_ADDRESS")
                logger.info("Waiting for connection to Plex server at {}".format(PLEXADD))
                connected = False
                while not connected:
                    try:
                        plex = PlexServer(PLEXADD, PLEXTOKEN)
                        connected = True
                        os.environ['PLEX_CONNECTED'] = 'True'
                    except Exception as e:
                        logger.info("plex_debrid setup failed to connect to Plex server at {}".format(PLEXADD))
                        logger.info("Please start your plex server now.")
                        logger.info("Retrying in 5 seconds...")                        
                        time.sleep(5)         
                if not any([PLEXUSER, PLEXTOKEN] == pair for pair in json_data["Plex users"]):
                    json_data["Plex users"].append([PLEXUSER, PLEXTOKEN])
                json_data["Plex server address"] = PLEXADD
                plex_url = PLEXADD  
                plex_token = PLEXTOKEN
                plex = PlexServer(plex_url, plex_token)
                library_section_ids = [str(library.key) for library in plex.library.sections()]
                json_data["Jellyfin API Key"] = ""
                json_data["Jellyfin server address"] = "http://localhost:8096"
                if not library_collection_service or "Jellyfin Libraries" in library_update_services:   
                    json_data["Library collection service"] = ["Plex Library"]
                if not library_update_services or "Jellyfin Libraries" in library_update_services:    
                    json_data["Library update services"] = ["Plex Libraries"]
                if not plex_library_refresh:
                    json_data["Plex library refresh"] = library_section_ids
                logger.info("plex_debrid configured for Plex")
                
            if SEERRADD or SEERRAPIKEY:
                if not SEERRADD:
                    raise MissingEnvironmentVariable("SEERR_ADDRESS")
                if not SEERRAPIKEY:
                    raise MissingEnvironmentVariable("SEERR_API_KEY")
                json_data["Overseerr Base URL"] = SEERRADD
                json_data["Overseerr API Key"] = SEERRAPIKEY               
                
            if not RDAPIKEY and not ADAPIKEY:
                raise MissingAPIKeyException()
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

    except Exception as e:
        raise
    
if __name__ == "__main__":
    pd_setup()    