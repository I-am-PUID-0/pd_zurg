from base import *
from plex_debrid_ import update, setup 
from rclone_rd import rclone
from cleanup import duplicate_cleanup
from zurg import zurg


def main():
    logger = get_logger()

    version = '0.0.1'

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
        if not DUPECLEAN:
            pass
        elif DUPECLEAN:
            duplicate_cleanup.duplicate_cleanup()
    except Exception as e:
        logger.error(e)
        
    try:
        if ZURG is None or str(ZURG).lower() == 'false':
            pass
        elif str(ZURG).lower() == 'true':
            zurg.setup()
    except Exception as e:
        logger.error(e)
        
    try:
        if RDAPIKEY or ADAPIKEY:
            if RCLONEMN:
                rclone.setup()
        else:
            raise MissingAPIKeyException()
    except Exception as e:
        logger.error(e)

    try:
        if PLEXUSER:
            setup.pd_setup()
            if AUTOUPDATE:
                update.auto_update()
            else:
                update.update_disabled()
    except:
        pass

if __name__ == "__main__":
    main()