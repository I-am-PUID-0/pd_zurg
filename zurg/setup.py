from base import *


def zurg_setup():
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
            logger.info("'ZURG_LOG_LEVEL' not set. Default log level INFO will be used for Zurg.")

    except Exception as e:
        logger.error(f"Error setting Zurg log level from 'ZURG_LOG_LEVEL': {e}")
        
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

    def check_and_set_zurg_version(dir_path):
        zurg_binary_path = os.path.join(dir_path, 'zurg')
        if os.path.exists(zurg_binary_path) and not ZURGVERSION:
            try:
                result = subprocess.run([zurg_binary_path, 'version'], capture_output=True, text=True)
                if result.returncode == 0:
                    version_info = result.stdout.strip()
                    version = version_info.split('\n')[-1].split(': ')[-1]
                    os.environ['ZURG_CURRENT_VERSION'] = version
                    logger.info(f"Found Zurg version {version} in {dir_path}")
                else:
                    logger.error("Error checking Zurg version")
            except Exception as e:
                logger.error(f"Exception occurred while checking Zurg version: {e}")
        else:
            from .download import version_check
            version_check()

    def setup_zurg_instance(config_dir, token, key_type):
        try:    
            zurg_executable_path = os.path.join(config_dir, 'zurg')
            config_file_path = os.path.join(config_dir, 'config.yml')
            logger.info(f"Preparing Zurg instance for {key_type}")
        
            if os.path.exists(zurg_app_override):
                logger.debug(f"Copying Zurg app from override: {zurg_app_override} to {zurg_executable_path}")
                shutil.copy(zurg_app_override, zurg_executable_path)
                os.chmod(zurg_executable_path, 0o755)
                logger.debug("Set 'zurg' file as executable")            
            elif not os.path.exists(zurg_executable_path) or not os.environ.get('ZURG_CURRENT_VERSION') or ZURGVERSION:
                logger.debug(f"Copying Zurg app from base: {zurg_app_base} to {zurg_executable_path}")
                shutil.copy(zurg_app_base, zurg_executable_path)
            elif os.environ.get('ZURG_CURRENT_VERSION') == ZURGVERSION and os.path.exists(zurg_executable_path):
                logger.info(f"Using Zurg app found for {key_type} in {config_dir}")
            else:
                logger.info(f"Using Zurg app found for {key_type} in {config_dir}")
            
            if os.path.exists(zurg_config_override):
                logger.debug(f"Copying Zurg config from override: {zurg_config_override} to {config_file_path}")
                shutil.copy(zurg_config_override, config_file_path)
            elif not os.path.exists(config_file_path):
                logger.debug(f"Copying Zurg config from base: {zurg_config_base} to {config_file_path}")
                shutil.copy(zurg_config_base, config_file_path)
            else:
                logger.info(f"Using Zurg config found for {key_type} in {config_dir}")
            
            port = random.randint(9001, 9999)
            logger.debug(f"Selected port {port} for Zurg w/ {key_type} instance")
        
            update_token(config_file_path, token)
            update_port(config_file_path, port)
            os.environ[f'ZURG_PORT_{key_type}'] = str(port)       
            logger.debug(f"Zurg w/ {key_type} instance configured to port: {port}")
        except Exception as e:
            logger.error(f"Error setting up Zurg instance for {key_type}: {e}")        

    try:
        if not RDAPIKEY and not ADAPIKEY:
            raise Exception("Please set the API Key for the debrid service")
        logger.debug("Configuring the debrid API key for Zurg")

        if RDAPIKEY:
            rd_dir = '/zurg/RD/'
            logger.info(f"Setting up Zurg w/ RealDebrid instance in directory: {rd_dir}")
            os.makedirs(rd_dir, exist_ok=True)
            check_and_set_zurg_version(rd_dir)            
            setup_zurg_instance(rd_dir, RDAPIKEY, "RealDebrid")

        if ADAPIKEY:
            ad_dir = '/zurg/AD/'
            logger.info(f"Setting up Zurg w/ AllDebrid instance in directory: {ad_dir}")
            os.makedirs(ad_dir, exist_ok=True)
            check_and_set_zurg_version(rd_dir)               
            setup_zurg_instance(ad_dir, ADAPIKEY, "AllDebrid")

        logger.info("Zurg setup process complete")

    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError: The file was not found during zurg setup - {e}")
    except PermissionError as e:
        logger.error(f"PermissionError: Permission denied during file operation or subprocess execution for zerg setup - {e}")
    except Exception as e:
        logger.error(f"Exception: An error occurred during zurg setup - {e}")

if __name__ == "__main__":
    zurg_setup()

