from base import *
from update.auto_update import BaseUpdate


class ZurgUpdate(BaseUpdate):
    def terminate_zurg_instance(self, config_dir, key_type):
        regex_pattern = re.compile(rf'{re.escape(config_dir)}/zurg.*--preload', re.IGNORECASE)
        found_process = False
        self.logger.debug(f"Attempting to terminate Zurg process for {key_type} in {config_dir}")

        for proc in psutil.process_iter():
            try:
                cmdline = ' '.join(proc.cmdline())
                self.logger.debug(f"Checking process: PID={proc.pid}, Command Line='{cmdline}'")
                if regex_pattern.search(cmdline):
                    found_process = True
                    proc.kill()
                    self.logger.debug(f"Terminated Zurg process: PID={proc.pid}, Command Line='{cmdline}'")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if not found_process:
            self.logger.debug(f"No matching Zurg process found for {key_type} in {config_dir}")
        
    def start_process(self, process_name, config_dir=None):
        directories_to_check = ["/zurg/RD", "/zurg/AD"]

        for dir_to_check in directories_to_check:
            zurg_executable = os.path.join(dir_to_check, 'zurg')
            if os.path.exists(zurg_executable):
                if dir_to_check == "/zurg/RD":
                    key_type = "RealDebrid"
                elif dir_to_check == "/zurg/AD":
                    key_type = "AllDebrid"            
                command = [zurg_executable]         
                super().start_process(process_name, dir_to_check, command, key_type)
        
    def update_check(self):
        try:
            if ZURGVERSION:
                self.logger.info(f"ZURG_VERSION is set to: {ZURGVERSION}. Automatic updates will not be applied!")
                return
            
            from .download import get_latest_release  
            current_version = os.getenv('ZURG_CURRENT_VERSION')
            latest_release, error = get_latest_release(repo_owner='debridmediamanager', repo_name='zurg-testing')
            
            if error:
                self.logger.error(f"Failed to fetch the latest release: {error}")
                return
            
            self.logger.info(f"Current version: {current_version}")
            self.logger.debug(f"Latest available version: {latest_release}")
            
            if current_version == latest_release:
                self.logger.info("Zurg is already up to date.")
            else:
                self.logger.info("A new version of Zurg is available. Applying updates.")
                architecture = os.getenv('CURRENT_ARCHITECTURE')
                from .download import download_and_unzip_release
                base_url = os.getenv('BASE_URL')
                download_and_unzip_release(base_url, latest_release, architecture)
                directories_to_check = ["/zurg/RD", "/zurg/AD"]
                zurg_presence = {dir_to_check: os.path.exists(os.path.join(dir_to_check, 'zurg')) for dir_to_check in directories_to_check}

                for dir_to_check in directories_to_check:
                    if zurg_presence[dir_to_check]:
                        key_type = "RealDebrid" if dir_to_check == "/zurg/RD" else "AllDebrid"
                        zurg_app_base = '/zurg/zurg'
                        zurg_executable_path = os.path.join(dir_to_check, 'zurg')
                        self.terminate_zurg_instance(dir_to_check, key_type)
                        shutil.copy(zurg_app_base, zurg_executable_path)
                        self.start_process('Zurg', dir_to_check)
                
        except Exception as e:
            self.logger.error(f"An error occurred in update_check: {e}")
