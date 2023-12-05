from base import *


logger = get_logger()

def start_plex_debrid():    
    global pd 
    pd = subprocess.Popen(['python', './plex_debrid/main.py', '--config-dir', '/config'], start_new_session=True)

def update_disabled():
    logger.info("Automatic update disabled")
    start_plex_debrid()
    pd.wait()

def update_enabled():
    logger.info("Automatic update enabled")
    start_plex_debrid()

def update_available():
    logger.info("Checking for available updates")
    
    with open('./config/settings.json', 'r') as f:
        json_data = load(f)
        version = json_data['version'][0]
        logger.info(f"Currently installed [v{version}]")

    try:
        response = requests.get('https://raw.githubusercontent.com/itsToggle/plex_debrid/main/ui/ui_settings.py', timeout=0.25)
        response = response.content.decode('utf8')

        if regex.search("(?<=')([0-9]+\.[0-9]+)(?=')", response):
            v = regex.search("(?<=')([0-9]+\.[0-9]+)(?=')", response).group()

            if float(version) < float(v):
                target = './plex_debrid'

                with requests.get('https://github.com/itsToggle/plex_debrid/archive/refs/heads/main.zip') as r:
                    z = zipfile.ZipFile(io.BytesIO(r.content))

                    for file_info in z.infolist():
                        if file_info.is_dir():
                            continue
                        file_path = file_info.filename

                        if not file_path.startswith('plex_debrid-main/'):
                            continue

                        fpath = file_path.split('/', 1)[1]
                        fpath = os.path.join(target, fpath)
                        os.makedirs(os.path.dirname(fpath), exist_ok=True)

                        with open(fpath, 'wb') as dst:
                            with z.open(file_info, 'r') as src:
                                shutil.copyfileobj(src, dst)

                logger.info(f"Automatic update installed [v{v}]")
                logger.info("Restarting plex_debrid")
                pd.kill()
                start_plex_debrid()
            else:
                logger.info("Automatic update not required")
    except:
        logger.error("Automatic update failed")

def update_schedule():
    update_enabled()
    update_available()
    interval = auto_update_interval()
    interval_minutes = int(interval * 60)
    schedule.every(interval_minutes).minutes.do(update_available)

    while True:
        schedule.run_pending()
        time.sleep(1)

def auto_update_interval():
    if os.getenv('AUTO_UPDATE_INTERVAL') is None:
        interval = 24
    else:
        interval = float(os.getenv('AUTO_UPDATE_INTERVAL'))

    return interval

def auto_update():
    AUTOUPDATE = os.getenv('AUTO_UPDATE')

    if AUTOUPDATE is None:
        update_disabled()
    elif AUTOUPDATE is not None and auto_update_interval() == 24:
        logger.info("Automatic update interval missing")
        logger.info("Defaulting to " + format_time(auto_update_interval()))
        update_schedule()
    elif not (AUTOUPDATE is None):
        logger.info("Automatic update interval set to " + format_time(auto_update_interval()))
        update_schedule()