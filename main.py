from base import *
import plex_debrid_ as p
import zurg as z 
from rclone_rd import rclone
from cleanup import duplicate_cleanup
from update import auto_update


def main():
    logger = get_logger()

    version = '2.0.3'

    ascii_art = f'''
                                                                          
 _______  ______       _______           _______  _______ 
(  ____ )(  __  \     / ___   )|\     /|(  ____ )(  ____ \\
| (    )|| (  \  )    \/   )  || )   ( || (    )|| (    \/
| (____)|| |   ) |        /   )| |   | || (____)|| |      
|  _____)| |   | |       /   / | |   | ||     __)| | ____ 
| (      | |   ) |      /   /  | |   | || (\ (   | | \_  )
| )      | (__/  )     /   (_/\| (___) || ) \ \__| (___) |
|/       (______/_____(_______/(_______)|/   \__/(_______)
                (_____)                                   
                        Version: {version}                                    
'''

    logger.info(ascii_art.format(version=version)  + "\n" + "\n")

    def healthcheck():
        while True:
            time.sleep(10)
            try:
                result = subprocess.run(['python', 'healthcheck.py'], capture_output=True, text=True) 
                if result.stderr:
                    logger.error(result.stderr.strip())
            except Exception as e:
                logger.error('Error running healthcheck.py: %s', e)
            time.sleep(50)
    thread = threading.Thread(target=healthcheck)
    thread.daemon = True
    thread.start()
       
    try:
        if ZURG is None or str(ZURG).lower() == 'false':
            pass
        elif str(ZURG).lower() == 'true':
            try:
                if RDAPIKEY or ADAPIKEY:
                    try:
                        z.setup.zurg_setup() 
                        z_updater = z.update.ZurgUpdate()
                        if ZURGUPDATE:
                            z_updater.auto_update('Zurg',True)
                        else:
                            z_updater.auto_update('Zurg',False)
                    except Exception as e:
                        raise Exception(f"Error in Zurg setup: {e}")
                    try:    
                        if RCLONEMN:
                            try:
                                if not DUPECLEAN:
                                    pass
                                elif DUPECLEAN:
                                    duplicate_cleanup.setup()
                                rclone.setup()      
                            except Exception as e:
                                logger.error(e)                         
                    except Exception as e:
                        raise Exception(f"Error in setup: {e}")                          
                else:
                    raise MissingAPIKeyException()
            except Exception as e:
                logger.error(e)                    
    except Exception as e:
        logger.error(e)
        
    try:
        if PLEXDEBRID is None or str(PLEXDEBRID).lower() == 'false':
            pass
        elif str(PLEXDEBRID).lower() == 'true':
            try:
                p.setup.pd_setup()
                pd_updater = p.update.PlexDebridUpdate()
                if PDUPDATE:
                    pd_updater.auto_update('plex_debrid',True)
                else:
                    pd_updater.auto_update('plex_debrid',False)
            except Exception as e:
                logger.error(f"An error occurred in the plex_debrid setup: {e}")
    except:
        pass
    def perpetual_wait():
        stop_event = threading.Event()
        stop_event.wait()
    perpetual_wait()    
if __name__ == "__main__":
    main()