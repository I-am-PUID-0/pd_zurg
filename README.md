# pd_zurg

## Description
A combined docker image for the unified deployment of **[itsToggle's](https://github.com/itsToggle)**, **[yowmamasita's](https://github.com/yowmamasita)**, and **[ncw's](https://github.com/ncw)** projects -- **[plex_debrid](https://github.com/itsToggle/plex_debrid)**, **[zurg](https://github.com/debridmediamanager/zurg-testing)**, and **[rclone](https://github.com/rclone/rclone)**


## Features
 - [Optional independent or combined utilization of zurg/rclone and plex_debrid](https://github.com/I-am-PUID-0/pd_zurg/wiki#optional-independent-or-combined-utilization-of-rclone-and-plex_debrid)
 - [Simultaneous independent rclone mounts](https://github.com/I-am-PUID-0/pd_zurg/wiki#simultaneous-independent-rclone-mounts)
 - [Bind-mounts rclone to the host](https://github.com/I-am-PUID-0/pd_zurg/wiki#bind-mounts-rclone-to-the-host)
 - [Debrid service API Key passed to zurg and plex_debrid via docker environment variable](https://github.com/I-am-PUID-0/pd_zurg/wiki#debrid-api-key-passed-to-rclone-and-plex_debrid-via-docker-environment-variable)
 - [rclone config automatically generated](https://github.com/I-am-PUID-0/pd_zurg/wiki#rclone-config-automatically-generated)
 - [rclone flags passed via docker environment variable](https://github.com/I-am-PUID-0/pd_zurg/wiki#rclone-flags-passed-via-docker-environment-variable)
 - [Fuse.conf ```user_allow_other``` applied within the container vs. the host](https://github.com/I-am-PUID-0/pd_zurg/wiki#fuseconf-user_allow_other-applied-within-the-container-vs-the-host)
 - [Plex server values passed to plex_debrid settings.json via docker environment variables](https://github.com/I-am-PUID-0/pd_zurg/wiki#plex-server-values-passed-to-plex_debrid-settingsjson-via-docker-environment-variables)
 - [Automatic Update of plex_debrid to the latest version](https://github.com/I-am-PUID-0/pd_zurg/wiki#automatic-update-of-plex_debrid-to-the-latest-version)
 - [Use of .env file for setting environment variables](https://github.com/I-am-PUID-0/pd_zurg/wiki#use-of-env-file-for-setting-environment-variables)
 - [Duplicate Cleanup](https://github.com/I-am-PUID-0/pd_zurg/wiki#duplicate-cleanup) 

## Docker Hub
A prebuilt image is hosted on [docker hub](https://hub.docker.com/r/iampuid0/pd_zurg) 


## Docker-compose
```
version: "3.8"

services:
  pd_zurg:
    container_name: pd_zurg
    image: iampuid0/pd_zurg:latest
    stdin_open: true # docker run -i
    tty: true        # docker run -t    
    volumes:
      # Location of configuration files. If a Zurg config.yml and/or Zurg app is placed here, it will be used to override the default configuration and/or app used at startup 
      - /pd_zurg/config:/config
      # Location for logs
      - /pd_zurg/log:/log
      # Location for rclone cache if enabled
      - /pd_zurg/cache:/cache
      # Location for Zurg RealDebrid active configuration
      - /pd_zurg/RD:/zurg/RD
      # Location for Zurg AllDebrid active configuration -- when supported by Zurg     
      - /pd_zurg/AD:/zurg/AD   
      # Location for rclone mount to host
      - /pd_zurg/mnt:/data:shared       
    environment:
      - TZ=
      # Zurg Required Settings
      - ZURG_ENABLED=true      
      - RD_API_KEY=
      # Rclone Required Settings
      - RCLONE_MOUNT_NAME=pd_zurg
      # Rclone Optional Settings - See rclone docs for full list
      - RCLONE_LOG_LEVEL=INFO
      - RCLONE_CACHE_DIR=/cache
      - RCLONE_DIR_CACHE_TIME=10s
      - RCLONE_VFS_CACHE_MODE=full
      - RCLONE_VFS_CACHE_MAX_SIZE=100G
      - RCLONE_ATTR_TIMEOUT=8700h
      - RCLONE_BUFFER_SIZE=32M
      - RCLONE_VFS_CACHE_MAX_AGE=4h
      - RCLONE_VFS_READ_CHUNK_SIZE=32M
      - RCLONE_VFS_READ_CHUNK_SIZE_LIMIT=1G
      - RCLONE_TRANSFERS=8
      # Plex Debrid Required Settings
      - PLEX_USER=
      - PLEX_TOKEN=
      - PLEX_ADDRESS=
      # Plex Debrid Optional Settings
      - AUTO_UPDATE=true
      - AUTO_UPDATE_INTERVAL=12
      - SHOW_MENU=true
      # Special Features
      - DUPLICATE_CLEANUP=true
      - CLEANUP_INTERVAL=1
      - PDZURG_LOG_LEVEL=INFO
      - PDZURG_LOG_COUNT=2
    # attach to gluetun vpn container if realdebrid blocks IP address 
    network_mode: container:gluetun  
    devices:
      - /dev/fuse:/dev/fuse:rwm
    cap_add:
      - SYS_ADMIN     
    security_opt:
      - apparmor:unconfined    
      - no-new-privileges
```

## Docker Build

### Docker CLI

```
docker build -t yourimagename https://github.com/I-am-PUID-0/pd_zurg.git
```


## Automatic Updates
If you would like to enable automatic updates for plex_debrid, utilize the ```AUTO_UPDATE``` environment variable. 
Additional details can be found in the [pd_zurg Wiki](https://github.com/I-am-PUID-0/pd_zurg/wiki/Settings#automatic-updates)


## Environment Variables

To customize some properties of the container, the following environment
variables can be passed via the `-e` parameter (one for each variable), or via the docker-compose file within the ```environment:``` section, or with a .env file saved to the config directory -- See the wiki for more info on using the [.env](https://github.com/I-am-PUID-0/pd_zurg/wiki/Settings#use-of-env-file-for-setting-environment-variables).  Value
of this parameter has the format `<VARIABLE_NAME>=<VALUE>`.

| Variable       | Description                                  | Default | Required for rclone| Required for plex_debrid|
|----------------|----------------------------------------------|---------|:-:|:-:|
|`TZ`| [TimeZone](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones) used by the container | ` ` |
|`RD_API_KEY`| [RealDebrid API key](https://real-debrid.com/apitoken) | ` ` | :heavy_check_mark:| :heavy_check_mark:|
|`AD_API_KEY`| [AllDebrid API key](https://alldebrid.com/apikeys/) | ` ` | :heavy_check_mark:| :heavy_check_mark:|
|`RCLONE_MOUNT_NAME`| A name for the rclone mount | ` ` | :heavy_check_mark:|
|`RCLONE_LOG_LEVEL`| [Log level](https://rclone.org/docs/#log-level-level) for rclone | `NOTICE` |
|`RCLONE_LOG_FILE`| [Log file](https://rclone.org/docs/#log-file-file) for rclone | ` ` |
|`RCLONE_DIR_CACHE_TIME`| [How long a directory should be considered up to date and not refreshed from the backend](https://rclone.org/commands/rclone_mount/#vfs-directory-cache) #optional, but recommended is 10s. | `5m` |
|`RCLONE_CACHE_DIR`| [Directory used for caching](https://rclone.org/docs/#cache-dir-dir). | ` ` |
|`RCLONE_VFS_CACHE_MODE`| [Cache mode for VFS](https://rclone.org/commands/rclone_mount/#vfs-file-caching) | ` ` |
|`RCLONE_VFS_CACHE_MAX_SIZE`| [Max size of the VFS cache](https://rclone.org/commands/rclone_mount/#vfs-file-caching) | ` ` |
|`RCLONE_VFS_CACHE_MAX_AGE`| [Max age of the VFS cache](https://rclone.org/commands/rclone_mount/#vfs-file-caching) | ` ` |
|`PLEX_USER`| The [Plex USERNAME](https://app.plex.tv/desktop/#!/settings/account) for your account | ` ` || :heavy_check_mark:|
|`PLEX_TOKEN`| The [Plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) associated with PLEX_USER | ` ` || :heavy_check_mark:|
|`PLEX_ADDRESS`| The URL of your Plex server. Example: http://192.168.0.100:32400 or http://plex:32400 - format must include ```http://``` or ```https://``` and have no trailing characters after the port number (32400). E.g., ```/``` | ` ` || :heavy_check_mark:|
|`SHOW_MENU`| Enable the plex_debrid menu to show upon startup, requiring user interaction before the program runs. Conversely, if the plex_debrid menu is disabled, the program will automatically run upon successful startup. If used, the value must be ```true``` or ```false``` | `true` |
|`PD_LOGFILE`| Log file for plex_debrid. The log file will appear in the ```/config``` as ```plex_debrid.log```. If used, the value must be ```true``` or ```false``` | `false` |
|`AUTO_UPDATE`| Enable automatic updates of plex_debrid. Adding this variable will enable automatic updates to the latest version of plex_debrid locally within the container. No values are required. | `false` |
|`AUTO_UPDATE_INTERVAL`| Interval between automatic update checks in hours. Vaules can be any positive [whole](https://www.oxfordlearnersdictionaries.com/us/definition/english/whole-number) or [decimal](https://www.oxfordreference.com/display/10.1093/oi/authority.20110803095705740;jsessionid=3FDC96CC0D79CCE69702661D025B9E9B#:~:text=The%20separator%20used%20between%20the,number%20expressed%20in%20decimal%20representation.) point based number. Ex. a value of .5 would yield thirty minutes and 1.5 would yield one and a half hours | `24` |
|`DUPLICATE_CLEANUP`| Automated cleanup of duplicate content in Plex.  | `false` |
|`CLEANUP_INTERVAL`| Interval between duplicate cleanup in hours. Vaules can be any positive [whole](https://www.oxfordlearnersdictionaries.com/us/definition/english/whole-number) or [decimal](https://www.oxfordreference.com/display/10.1093/oi/authority.20110803095705740;jsessionid=3FDC96CC0D79CCE69702661D025B9E9B#:~:text=The%20separator%20used%20between%20the,number%20expressed%20in%20decimal%20representation.) point based number. Ex. a value of .5 would yield thirty minutes and 1.5 would yield one and a half hours | `24` |
|`PDZURG_LOG_LEVEL`| The level at which logs should be captured. See the python [Logging Levels](https://docs.python.org/3/library/logging.html#logging-levels) documentation for more details  | `INFO` |
|`PDZURG_LOG_COUNT`| The number logs to retain. Result will be value + current log  | `2` |

## Data Volumes

The following table describes data volumes used by the container.  The mappings
are set via the `-v` parameter or via the docker-compose file within the ```volumes:``` section.  Each mapping is specified with the following
format: `<HOST_DIR>:<CONTAINER_DIR>[:PERMISSIONS]`.

| Container path  | Permissions | Description |
|-----------------|-------------|-------------|
|`/config`| rw | This is where the application stores the rclone.conf, plex_debrid settings.json, and any files needing persistence. CAUTION: rclone.conf is overwritten upon start/restart of the container. Do NOT use an existing rclone.conf file if you have other rclone services |
|`/log`| rw | This is where the application stores its log files |
|`/mnt`| rw | This is where rclone will be mounted. Not required when only utilizing plex_debrid   |

## TODO

See the [pd_zurg roadmap](https://github.com/users/I-am-PUID-0/projects/2) for a list of planned features and enhancements.

## Deployment

pd_zurg allows for the simultaneous or individual deployment of plex_debrid and/or rclone

For additional details on deployment, see the [pd_zurg Wiki](https://github.com/I-am-PUID-0/pd_zurg/wiki/Settings#deployment)
## Community

### pd_zurg
- For questions related to pd_zurg, see the GitHub [discussions](https://github.com/I-am-PUID-0/pd_zurg/discussions)
- or create a new [issue](https://github.com/I-am-PUID-0/pd_zurg/issues) if you find a bug or have an idea for an improvement.
- or join the pd_zurg [discord server](https://discord.gg/n5nQRYtrw2)

### plex_debrid
- For questions related to plex_debrid, see the GitHub [discussions](https://github.com/itsToggle/plex_debrid/discussions) 
- or create a new [issue](https://github.com/itsToggle/plex_debrid/issues) if you find a bug or have an idea for an improvement.
- or join the plex_debrid [discord server](https://discord.gg/u3vTDGjeKE) 


## Buy **[itsToggle](https://github.com/itsToggle)** a beer/coffee? :)

If you enjoy the underlying projects and want to buy itsToggle a beer/coffee, feel free to use the real-debrid [affiliate link](http://real-debrid.com/?id=5708990) or send a virtual beverage via [PayPal](https://www.paypal.com/paypalme/oidulibbe) :)

## Buy **[yowmamasita](https://github.com/yowmamasita)** a beer/coffee? :)

If you enjoy the underlying projects and want to buy yowmamasita a beer/coffee, feel free to use the [GitHub sponsor link](https://github.com/sponsors/debridmediamanager)

## Buy **[ncw](https://github.com/ncw)** a beer/coffee? :) 

If you enjoy the underlying projects and want to buy Nick Craig-Wood a beer/coffee, feel free to use the website's [sponsor links](hhttps://rclone.org/sponsor/)

## GitHub Workflow Status
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/I-am-PUID-0/pd_zurg/docker-image.yml)
