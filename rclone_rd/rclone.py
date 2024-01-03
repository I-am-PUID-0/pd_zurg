from base import *

logger = get_logger()

def get_port_from_config(config_file_path, key_type):
    try:
        with open(config_file_path, 'r') as file:
            for line in file:
                if line.strip().startswith("port:"):
                    port = line.split(':')[1].strip()
                    return port
    except Exception as e:
        logger.error(f"Error reading port from config file: {e}")
    return '9999'  

def setup():
    logger.info("Checking rclone flags")
 
    try:
        if not RCLONEMN:
            raise Exception("Please set a name for the rclone mount")
        logger.info(f"Configuring the rclone mount name to \"{RCLONEMN}\"")

        if not RDAPIKEY and not ADAPIKEY:
            raise Exception("Please set the API Key for the rclone mount")

        if RDAPIKEY and ADAPIKEY:
            RCLONEMN_RD = f"{RCLONEMN}_RD"
            RCLONEMN_AD = f"{RCLONEMN}_AD"
        else:
            RCLONEMN_RD = RCLONEMN_AD = RCLONEMN

        config_file_path_rd = '/zurg/RD/config.yml'
        config_file_path_ad = '/zurg/AD/config.yml'

        with open("/config/rclone.config", "w") as f:
            if RDAPIKEY:
                rd_port = get_port_from_config(config_file_path_rd, 'RDAPIKEY')
                f.write(f"[{RCLONEMN_RD}]\n")
                f.write("type = webdav\n")
                f.write(f"url = http://localhost:{rd_port}/dav\n")
                f.write("vendor = other\n")
                f.write("pacer_min_sleep = 0\n")
            if ADAPIKEY:
                ad_port = get_port_from_config(config_file_path_ad, 'ADAPIKEY')
                f.write(f"[{RCLONEMN_AD}]\n")
                f.write("type = webdav\n")
                f.write(f"url = http://localhost:{ad_port}/dav\n")
                f.write("vendor = other\n")
                f.write("pacer_min_sleep = 0\n")

        with open("/etc/fuse.conf", "a") as f:
            f.write("user_allow_other\n")

        mount_names = []
        if RDAPIKEY:
            mount_names.append(RCLONEMN_RD)
        if ADAPIKEY:
            mount_names.append(RCLONEMN_AD)

        def parse_log_level_and_message(line):
            log_levels = {'DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR'}
            parts = line.split()
            log_level = None
            message_start_index = None

            for i, part in enumerate(parts):
                if part in log_levels or part.rstrip(':') in log_levels:
                    log_level = part.rstrip(':')
                    message_start_index = i + 2 
                    break

            if log_level and message_start_index and message_start_index < len(parts):
                message = ' '.join(parts[message_start_index:])
            else:
                log_level = 'UNKNOWN'
                message = line

            return log_level, message

        def monitor_stderr(process, mount_name):
            log_methods = {
                'DEBUG': logger.debug,
                'INFO': logger.info,
                'NOTICE': logger.debug,
                'WARNING': logger.warning,
                'ERROR': logger.error
            }

            for line in process.stderr:
                line = line.decode().strip()
                if line:
                    log_level, message = parse_log_level_and_message(line)
                    log_func = log_methods.get(log_level, logger.info)
                    log_func(f"rclone mount name \"{mount_name}\": {message}")

        subprocesses = []

        for idx, mn in enumerate(mount_names):
            logger.info(f"Configuring rclone for {mn}")
            subprocess.run(["umount", f"/data/{mn}"], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.makedirs(f"/data/{mn}", exist_ok=True)
    
            rclone_command = ["rclone", "mount", f"{mn}:", f"/data/{mn}", "--config", "/config/rclone.config", "--allow-other", "--poll-interval=0"]
            if not PLEXUSER or idx != len(mount_names) - 1:
                rclone_command.append("--daemon")
    
            logger.info(f"Starting rclone{' daemon' if '--daemon' in rclone_command else ''} for {mn}")
            process = subprocess.Popen(rclone_command, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            threading.Thread(target=monitor_stderr, args=(process, mn)).start()

        logger.info("rclone startup complete")

    except Exception as e:
        logger.error(e)
        exit(1)