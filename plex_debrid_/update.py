from base import *
from update.auto_update import BaseUpdate


class PlexDebridUpdate(BaseUpdate):
    def start_process(self, process_name, config_dir="/", key_type=""):
        super().start_process(process_name, config_dir, ['python', './plex_debrid/main.py', '--config-dir', '/config'], key_type)
          
    def update_check(self):
        self.logger.info("Checking for available plex_debrid updates")
    
        with open('./config/settings.json', 'r') as f:
            json_data = load(f)
            version = json_data['version'][0]
            self.logger.info(f"Currently installed [v{version}]")

        try:
            response = requests.get('https://raw.githubusercontent.com/itsToggle/plex_debrid/main/ui/ui_settings.py', timeout=0.25)
            response = response.content.decode('utf8')

            if regex.search("(?<=')([0-9]+\.[0-9]+)(?=')", response):
                v = regex.search("(?<=')([0-9]+\.[0-9]+)(?=')", response).group()

                if float(version) < float(v):
                    from .download import get_latest_release
                    download_release, error = get_latest_release()
                    if not download_release:
                        self.logger.error(f"Failed to download update for plex_debrid: {error}")
                    else:    
                        self.logger.info(f"Automatic update installed for plex_debrid [v{v}]")
                        self.logger.info("Restarting plex_debrid")
                        if self.process:
                            self.process.kill()
                        self.start_process('plex_debrid')
                else:
                    self.logger.info("Automatic update not required for plex_debrid")
        except Exception as e:
            self.logger.error(f"Automatic update failed for plex_debrid: {e}")
