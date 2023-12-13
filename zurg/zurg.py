from base import *


def setup():
    logger = get_logger()
    logger.info("Setting up Zurg")
    zurg_app_override = '/config/zurg'
    zurg_app_base = '/zurg/zurg'
    zurg_config_override = '/config/config.yml'
    zurg_config_base = '/zurg/config.yml'
    
    try:
        if ZURGLOGLEVEL is not None:
            os.environ['LOG_LEVEL'] = ZURGLOGLEVEL
            logger.debug(f"'LOG_LEVEL' set to '{ZURGLOGLEVEL}' based on 'ZURG_LOG_LEVEL'")
        else:
            logger.warning("'ZURG_LOG_LEVEL' not set. Default 'LOG_LEVEL' will be used.")

    except Exception as e:
        logger.error(f"Error setting 'LOG_LEVEL' from 'ZURG_LOG_LEVEL': {e}")
        
    def update_token(file_path, token):
        logger.debug(f"Updating token in config file: {file_path}")
        with open(file_path, 'r') as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip().startswith("token:"):
                    file.write(f"token: {token}\n")
                else:
                    file.write(line)

    def update_port(file_path, port):
        logger.debug(f"Updating port in config file: {file_path} to {port}")
        with open(file_path, 'r') as file:
            lines = file.readlines()
        with open(file_path, 'w') as file:
            for line in lines:
                if line.strip().startswith("port:"):
                    file.write(f"port: {port}\n")
                else:
                    file.write(line)

    def run_zurg_instance(config_dir, token, key_type):
        zurg_executable_path = os.path.join(config_dir, 'zurg')
        config_file_path = os.path.join(config_dir, 'config.yml')

        logger.info(f"Preparing to run Zurg instance for {key_type}")
        if os.path.exists(zurg_app_override):
            logger.info(f"Copying Zurg app from override: {zurg_app_override} to {zurg_executable_path}")
            shutil.copy(zurg_app_override, zurg_executable_path)
        else:
            logger.debug(f"Copying Zurg app from base: {zurg_app_base} to {zurg_executable_path}")
            shutil.copy(zurg_app_base, zurg_executable_path)
        if os.path.exists(zurg_config_override):
            logger.debug(f"Copying Zurg config from override: {zurg_config_override} to {config_file_path}")
            shutil.copy(zurg_config_override, config_file_path)
        else:
            logger.debug(f"Copying Zurg config from base: {zurg_config_base} to {config_file_path}")
            shutil.copy(zurg_config_base, config_file_path)
        port = random.randint(9001, 9999)
        logger.debug(f"Selected port {port} for {key_type}")
        update_token(config_file_path, token)
        update_port(config_file_path, port)
        os.environ[f'ZURG_PORT_{key_type}'] = str(port)
        logger.info(f"{key_type} Zurg instance running on port: {port}")
        logger.info(f"Starting subprocess for {key_type} Zurg instance")

        try:
            process = subprocess.Popen([zurg_executable_path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=config_dir, universal_newlines=True, bufsize=1)
            subprocess_logger = SubprocessLogger(logger, "Zurg " + key_type)
            subprocess_logger.start(process)
        except Exception as e:
            logger.error(f"Error running subprocess for {key_type}: {e}")

    try:
        if not RDAPIKEY and not ADAPIKEY:
            raise Exception("Please set the API Key for the debrid service")
        logger.info("Configuring the debrid API key")

        if RDAPIKEY:
            rd_dir = '/zurg/RD/'
            logger.info(f"Setting up RealDebrid instance in directory: {rd_dir}")
            os.makedirs(rd_dir, exist_ok=True)
            run_zurg_instance(rd_dir, RDAPIKEY, "RealDebrid")

        if ADAPIKEY:
            ad_dir = '/zurg/AD/'
            logger.info(f"Setting up AllDebrid instance in directory: {ad_dir}")
            os.makedirs(ad_dir, exist_ok=True)
            run_zurg_instance(ad_dir, ADAPIKEY, "AllDebrid")

        logger.info("Zurg setup process complete")

    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError: The file was not found during zurg setup - {e}")
    except PermissionError as e:
        logger.error(f"PermissionError: Permission denied during file operation or subprocess execution for zerg setup - {e}")
    except Exception as e:
        logger.error(f"Exception: An error occurred during zurg setup - {e}")

if __name__ == "__main__":
    setup()

