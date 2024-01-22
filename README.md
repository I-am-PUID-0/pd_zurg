# pd_zurg

## Description
A combined docker image for the unified deployment of **[itsToggle's](https://github.com/itsToggle)**, **[yowmamasita's](https://github.com/yowmamasita)**, and **[ncw's](https://github.com/ncw)** projects -- **[plex_debrid](https://github.com/itsToggle/plex_debrid)**, **[zurg](https://github.com/debridmediamanager/zurg-testing)**, and **[rclone](https://github.com/rclone/rclone)**


## Features
 - [Optional independent or combined utilization of plex_debrid and zurg w/ rclone](https://github.com/I-am-PUID-0/pd_zurg/wiki#optional-independent-or-combined-utilization-of--plex_debrid-and-zurg-w-rclone)
 - [Simultaneous independent rclone mounts](https://github.com/I-am-PUID-0/pd_zurg/wiki#simultaneous-independent-rclone-mounts)
 - [Bind-mounts rclone to the host](https://github.com/I-am-PUID-0/pd_zurg/wiki#bind-mounts-rclone-to-the-host)
 - [Debrid service API Key passed to zurg and plex_debrid via docker environment variable](https://github.com/I-am-PUID-0/pd_zurg/wiki#debrid-api-key-passed-to-zurg-and-plex_debrid-via-docker-environment-variable)
 - [rclone config automatically generated](https://github.com/I-am-PUID-0/pd_zurg/wiki#rclone-config-automatically-generated)
 - [rclone flags passed via docker environment variable](https://github.com/I-am-PUID-0/pd_zurg/wiki#rclone-flags-passed-via-docker-environment-variable)
 - [Fuse.conf ```user_allow_other``` applied within the container vs. the host](https://github.com/I-am-PUID-0/pd_zurg/wiki#fuseconf-user_allow_other-applied-within-the-container-vs-the-host)
 - [Plex server values passed to plex_debrid settings.json via docker environment variables](https://github.com/I-am-PUID-0/pd_zurg/wiki#plex-server-values-passed-to-plex_debrid-settingsjson-via-docker-environment-variables)
 - [Automatic Update of plex_debrid to the latest version](https://github.com/I-am-PUID-0/pd_zurg/wiki#automatic-update-of-plex_debrid-to-the-latest-version)
 - [Automatic Update of Zurg to the latest version](https://github.com/I-am-PUID-0/pd_zurg/wiki#automatic-update-of-zurg-to-the-latest-version)
 - [Version selection of zurg to the user-defined version](https://github.com/I-am-PUID-0/pd_zurg/wiki#version-selection-of-zurg-to-the-user-defined-version)
 - [Use of .env file for setting environment variables](https://github.com/I-am-PUID-0/pd_zurg/wiki#use-of-env-file-for-setting-environment-variables)
 - [Use of Docker Secret file for setting sensitive variables](https://github.com/I-am-PUID-0/pd_zurg#docker-secrets)
 - [Duplicate Cleanup](https://github.com/I-am-PUID-0/pd_zurg/wiki#duplicate-cleanup) 

## Docker Hub
A prebuilt image is hosted on [docker hub](https://hub.docker.com/r/iampuid0/pd_zurg) 

## GitHub Container Registry
A prebuilt image is hosted on [GitHub Container Registry](https://github.com/I-am-PUID-0/pd_zurg/pkgs/container/pd_zurg)


## Docker-compose
```YAML
version: "3.8"

services:
  pd_zurg:
    container_name: pd_zurg
    image: iampuid0/pd_zurg:latest
    ## Optionally, specify a specific version of pd_zurg
    # image: iampuid0/pd_zurg:2.0.0
    stdin_open: true # docker run -i
    tty: true        # docker run -t    
    volumes:
      ## Location of configuration files. If a Zurg config.yml and/or Zurg app is placed here, it will be used to override the default configuration and/or app used at startup. 
      - /pd_zurg/config:/config
      ## Location for logs
      - /pd_zurg/log:/log
      ## Location for rclone cache if enabled
      - /pd_zurg/cache:/cache
      ## Location for Zurg RealDebrid active configuration
      - /pd_zurg/RD:/zurg/RD
      ## Location for Zurg AllDebrid active configuration -- when supported by Zurg     
      - /pd_zurg/AD:/zurg/AD   
      ## Location for rclone mount to host
      - /pd_zurg/mnt:/data:shared       
    environment:
      - TZ=
      ## Zurg Required Settings
      - ZURG_ENABLED=true      
      - RD_API_KEY=
      ## Zurg Optional Settings
     # - ZURG_LOG_LEVEL=DEBUG
     # - ZURG_VERSION=v0.9.2-hotfix.4
     # - ZURG_UPDATE=true
     # - PLEX_REFRESH=true
     # - PLEX_MOUNT_DIR=/pd_zurg 
      ## Rclone Required Settings
      - RCLONE_MOUNT_NAME=pd_zurg
      ## Rclone Optional Settings - See rclone docs for full list
     # - RCLONE_LOG_LEVEL=DEBUG
     # - RCLONE_CACHE_DIR=/cache
     # - RCLONE_DIR_CACHE_TIME=10s
     # - RCLONE_VFS_CACHE_MODE=full
     # - RCLONE_VFS_CACHE_MAX_SIZE=100G
     # - RCLONE_ATTR_TIMEOUT=8700h
     # - RCLONE_BUFFER_SIZE=32M
     # - RCLONE_VFS_CACHE_MAX_AGE=4h
     # - RCLONE_VFS_READ_CHUNK_SIZE=32M
     # - RCLONE_VFS_READ_CHUNK_SIZE_LIMIT=1G
     # - RCLONE_TRANSFERS=8
      ## Plex Debrid Required Settings
      - PD_ENABLED=true
      ## To utilize plex_debrid with Plex, the following environment variables are required
      - PLEX_USER=
      - PLEX_TOKEN=
      - PLEX_ADDRESS=
      ## To utilize plex_debrid with Jellyfin, the following environment variables are required - Note that plex_debrid will require addtional setup befor use with Jellyfin
     # - JF_ADDRESS
     # - JF_API_KEY
      ## Plex Debrid Optional Settings
     # - PD_UPDATE=true   
     # - SHOW_MENU=false
     # - SEERR_API_KEY=
     # - SEERR_ADDRESS=
      ## Special Features
     # - AUTO_UPDATE_INTERVAL=12
     # - DUPLICATE_CLEANUP=true
     # - CLEANUP_INTERVAL=1
     # - PDZURG_LOG_LEVEL=DEBUG
     # - PDZURG_LOG_COUNT=2
    # Example to attach to gluetun vpn container if realdebrid blocks IP address 
    # network_mode: container:gluetun  
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
docker build -t your-image-name https://github.com/I-am-PUID-0/pd_zurg.git
```

## Plex or Jellyfin/Emby deployment

To use plex_debrid with Plex, the following environment variables are required: PD_ENABLED, PLEX_USER, PLEX_TOKEN, PLEX_ADDRESS

To use plex_debrid with Jellyfin/Emby, the following environment variables are required: PD_ENABLED, JF_ADDRESS, JF_API_KEY

### Note: Addtional setup required for Jellyfin
plex_debrid requires the Library collection service to be set for Trakt Collection: see the plex_debrid [Trakt Collections](https://github.com/itsToggle/plex_debrid#open_file_folder-library-collection-service) for more details

## Plex Refresh

To enable Plex library refresh with Zurg, the following environment variables are required: PLEX_REFRESH, PLEX_MOUNT_DIR, PLEX_ADDRESS, PLEX_TOKEN, ZURG_ENABLED, RD_API_KEY, RCLONE_MOUNT_NAME

## SEERR Integration

To enable either Overseerr or Jellyseerr integration with plex_debrid, the following environment variables are required: SEERR_API_KEY, SEERR_ADDRESS


## Automatic Updates
If you would like to enable automatic updates for plex_debrid, utilize the ```PD_UPDATE``` environment variable. 
Additional details can be found in the [pd_zurg Wiki](https://github.com/I-am-PUID-0/pd_zurg/wiki#automatic-update-of-plex_debrid-to-the-latest-version)

If you would like to enable automatic updates for Zurg, utilize the ```ZURG_UPDATE``` environment variable. 
Additional details can be found in the [pd_zurg Wiki](https://github.com/I-am-PUID-0/pd_zurg/wiki#automatic-update-of-zurg-to-the-latest-version)

## Environment Variables

To customize some properties of the container, the following environment
variables can be passed via the `-e` parameter (one for each variable), or via the docker-compose file within the ```environment:``` section, or with a .env file saved to the config directory -- See the wiki for more info on using the [.env](https://github.com/I-am-PUID-0/pd_zurg/wiki/Settings#use-of-env-file-for-setting-environment-variables).  Value
of this parameter has the format `<VARIABLE_NAME>=<VALUE>`.

| Variable       | Description                                  | Default | Required for rclone| Required for plex_debrid| Required for zurg|
|----------------|----------------------------------------------|---------|:-:|:-:|:-:|
|`TZ`| [TimeZone](http://en.wikipedia.org/wiki/List_of_tz_database_time_zones) used by the container |  |
|`RD_API_KEY`| [RealDebrid API key](https://real-debrid.com/apitoken) |  | | :heavy_check_mark:| :heavy_check_mark:|
|`AD_API_KEY`| [AllDebrid API key](https://alldebrid.com/apikeys/) |  | | :heavy_check_mark:| :heavy_check_mark:|
|`RCLONE_MOUNT_NAME`| A name for the rclone mount |  | :heavy_check_mark:|
|`RCLONE_LOG_LEVEL`| [Log level](https://rclone.org/docs/#log-level-level) for rclone | `NOTICE` |
|`RCLONE_LOG_FILE`| [Log file](https://rclone.org/docs/#log-file-file) for rclone |  |
|`RCLONE_DIR_CACHE_TIME`| [How long a directory should be considered up to date and not refreshed from the backend](https://rclone.org/commands/rclone_mount/#vfs-directory-cache) #optional, but recommended is 10s. | `5m` |
|`RCLONE_CACHE_DIR`| [Directory used for caching](https://rclone.org/docs/#cache-dir-dir). |  |
|`RCLONE_VFS_CACHE_MODE`| [Cache mode for VFS](https://rclone.org/commands/rclone_mount/#vfs-file-caching) |  |
|`RCLONE_VFS_CACHE_MAX_SIZE`| [Max size of the VFS cache](https://rclone.org/commands/rclone_mount/#vfs-file-caching) | |
|`RCLONE_VFS_CACHE_MAX_AGE`| [Max age of the VFS cache](https://rclone.org/commands/rclone_mount/#vfs-file-caching) |  |
|`PLEX_USER`| The [Plex Username](https://app.plex.tv/desktop/#!/settings/account) for your account | || :heavy_check_mark:|
|`PLEX_TOKEN`| The [Plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) associated with PLEX_USER |  || :heavy_check_mark:|
|`PLEX_ADDRESS`| The URL of your Plex server. Example: http://192.168.0.100:32400 or http://plex:32400 - format must include ```http://``` or ```https://``` and have no trailing characters after the port number (32400). E.g., ```/``` ||| :heavy_check_mark:|
|`PLEX_REFRESH`| Set the value "true" to enable Plex library refresh called by the Zurg process  | `false ` | | | |
|`PLEX_MOUNT_DIR`| Set the value to the mount location used within Plex to enable Plex library refresh called by the Zurg process  |  | | | |
|`SHOW_MENU`| Enable the plex_debrid menu to show upon startup, requiring user interaction before the program runs. Conversely, if the plex_debrid menu is disabled, the program will automatically run upon successful startup. If used, the value must be ```true``` or ```false``` | `true` |
|`PD_ENABLED`| Set the value "true" to enable the plex_debrid process | `false ` | | :heavy_check_mark: | |
|`PD_LOGFILE`| Log file for plex_debrid. The log file will appear in the ```/config``` as ```plex_debrid.log```. If used, the value must be ```true``` or ```false``` | `false` |
|`PD_UPDATE`| Enable automatic updates of plex_debrid. Adding this variable will enable automatic updates to the latest version of plex_debrid locally within the container. | `false` |
|`AUTO_UPDATE_INTERVAL`| Interval between automatic update checks in hours. Vaules can be any positive [whole](https://www.oxfordlearnersdictionaries.com/us/definition/english/whole-number) or [decimal](https://www.oxfordreference.com/display/10.1093/oi/authority.20110803095705740;jsessionid=3FDC96CC0D79CCE69702661D025B9E9B#:~:text=The%20separator%20used%20between%20the,number%20expressed%20in%20decimal%20representation.) point based number. Ex. a value of .5 would yield thirty minutes, and 1.5 would yield one and a half hours | `24` |
|`DUPLICATE_CLEANUP`| Automated cleanup of duplicate content in Plex.  | `false` |
|`CLEANUP_INTERVAL`| Interval between duplicate cleanup in hours. Values can be any positive [whole](https://www.oxfordlearnersdictionaries.com/us/definition/english/whole-number) or [decimal](https://www.oxfordreference.com/display/10.1093/oi/authority.20110803095705740;jsessionid=3FDC96CC0D79CCE69702661D025B9E9B#:~:text=The%20separator%20used%20between%20the,number%20expressed%20in%20decimal%20representation.) point based number. Ex. a value of .5 would yield thirty minutes and 1.5 would yield one and a half hours | `24` |
|`PDZURG_LOG_LEVEL`| The level at which logs should be captured. See the python [Logging Levels](https://docs.python.org/3/library/logging.html#logging-levels) documentation for more details  | `INFO` |
|`PDZURG_LOG_COUNT`| The number logs to retain. Result will be value + current log  | `2` |
|`ZURG_ENABLED`| Set the value "true" to enable the Zurg process | `false ` | | | :heavy_check_mark:|
|`ZURG_VERSION`| The version of Zurg to use. If enabled, the value should contain v0.9.x or v0.9.x-hotfix.x format | `latest` | | | |
|`ZURG_UPDATE`| Enable automatic updates of Zurg. Adding this variable will enable automatic updates to the latest version of Zurg locally within the container. | `false` | | | |
|`ZURG_LOG_LEVEL`| Set the log level for Zurg | `INFO` | | | |
|`JF_API_KEY`| The Jellyfin/Emby API Key ||| :heavy_check_mark:||
|`JF_ADDRESS`| The URL of your Jellyfin/Emby server. Example: http://192.168.0.101:8096 or http://jellyfin:8096 - format must include ```http://``` or ```https://``` and have no trailing characters after the port number (8096). E.g., ```/``` ||| :heavy_check_mark:|
|`SEERR_API_KEY`| The Jellyseerr or Overseerr API Key ||| :heavy_check_mark:||
|`SEERR_ADDRESS`| The URL of your Jellyseerr or Overseerr server. Example: http://192.168.0.102:5055 or http://Overseerr:5055 - format must include ```http://``` or ```https://``` and have no trailing characters after the port number (8096). E.g., ```/``` ||| :heavy_check_mark:|


## Data Volumes

The following table describes the data volumes used by the container.  The mappings
are set via the `-v` parameter or via the docker-compose file within the ```volumes:``` section.  Each mapping is specified with the following
format: `<HOST_DIR>:<CONTAINER_DIR>[:PERMISSIONS]`.

| Container path  | Permissions | Description |
|-----------------|-------------|-------------|
|`/config`| rw | This is where the application stores the rclone.conf, plex_debrid settings.json, and any files needing persistence. CAUTION: rclone.conf is overwritten upon start/restart of the container. Do NOT use an existing rclone.conf file if you have other rclone services |
|`/log`| rw | This is where the application stores its log files |
|`/data`| rshared  | This is where rclone will be mounted. Not required when only utilizing plex_debrid   |
|`/zurg/RD`| rw| This is where Zurg will store the active configuration and data for RealDebrid. Not required when only utilizing plex_debrid   |
|`/zurg/AD`| rw | This is where Zurg will store the active configuration and data for AllDebrid. Not required when only utilizing plex_debrid   |

## Docker Secrets

pd_zurg supports the use of docker secrets for the following environment variables:

| Variable       | Description                                  | Default | Required for rclone| Required for plex_debrid| Required for zurg|
|----------------|----------------------------------------------|---------|:-:|:-:|:-:|
|`RD_API_KEY`| [RealDebrid API key](https://real-debrid.com/apitoken) | ` ` | | :heavy_check_mark:| :heavy_check_mark:|
|`AD_API_KEY`| [AllDebrid API key](https://alldebrid.com/apikeys/) | ` ` | | :heavy_check_mark:| :heavy_check_mark:|
|`PLEX_USER`| The [Plex USERNAME](https://app.plex.tv/desktop/#!/settings/account) for your account | ` ` || :heavy_check_mark:|
|`PLEX_TOKEN`| The [Plex Token](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) associated with PLEX_USER | ` ` || :heavy_check_mark:|
|`PLEX_ADDRESS`| The URL of your Plex server. Example: http://192.168.0.100:32400 or http://plex:32400 - format must include ```http://``` or ```https://``` and have no trailing characters after the port number (32400). E.g., ```/``` | ` ` || :heavy_check_mark:|
|`JF_API_KEY`| The Jellyfin API Key | ` ` || :heavy_check_mark:||
|`JF_ADDRESS`| The URL of your Jellyfin server. Example: http://192.168.0.101:8096 or http://jellyfin:8096 - format must include ```http://``` or ```https://``` and have no trailing characters after the port number (8096). E.g., ```/``` | ` ` || :heavy_check_mark:|
|`SEERR_API_KEY`| The Jellyseerr or Overseerr API Key | ` ` || :heavy_check_mark:||
|`SEERR_ADDRESS`| The URL of your Jellyseerr or Overseerr server. Example: http://192.168.0.102:5055 or http://Overseerr:5055 - format must include ```http://``` or ```https://``` and have no trailing characters after the port number (8096). E.g., ```/``` | ` ` || :heavy_check_mark:|

To utilize docker secrets, remove the associated environment variables from the docker-compose, create a file with the case-sensitive naming convention identified and secret value, then reference the file in the docker-compose file as shown below:
```YAML
version: '3.8'

services:
  pd_zurg:
    image: iampuid0/pd_zurg:latest
    secrets:
      - rd_api_key
      - ad_api_key
      - plex_user
      - plex_token
      - plex_address
      - jf_api_key
      - jf_address
      - seerr_api_key
      - seerr_address

secrets:
  rd_api_key:
    file: ./path/to/rd_api_key.txt
  ad_api_key:
    file: ./path/to/ad_api_key.txt
  plex_user:
    file: ./path/to/plex_user.txt
  plex_token:
    file: ./path/to/plex_token.txt
  plex_address:
    file: ./path/to/plex_address.txt
  jf_api_key:
    file: ./path/to/jf_api_key.txt
  jf_address:
    file: ./path/to/jf_address.txt
  seerr_api_key:
    file: ./path/to/seerr_api_key.txt
  seerr_address:
    file: ./path/to/seerr_address.txt
```


## TODO

See the [pd_zurg roadmap](https://github.com/users/I-am-PUID-0/projects/4) for a list of planned features and enhancements.

## Deployment

pd_zurg allows for the simultaneous or individual deployment of plex_debrid and/or Zurg w/ rclone

For additional details on deployment, see the [pd_zurg Wiki](https://github.com/I-am-PUID-0/pd_zurg/wiki/Setup-Guides#deployment-options)
## Community

### pd_zurg
- For questions related to pd_zurg, see the GitHub [discussions](https://github.com/I-am-PUID-0/pd_zurg/discussions)
- or create a new [issue](https://github.com/I-am-PUID-0/pd_zurg/issues) if you find a bug or have an idea for an improvement.
- or join the pd_zurg [discord server](https://discord.gg/EPSWqmeeXM)

### plex_debrid
- For questions related to plex_debrid, see the GitHub [discussions](https://github.com/itsToggle/plex_debrid/discussions) 
- or create a new [issue](https://github.com/itsToggle/plex_debrid/issues) if you find a bug or have an idea for an improvement.
- or join the plex_debrid [discord server](https://discord.gg/u3vTDGjeKE) 


## Buy **[itsToggle](https://github.com/itsToggle)** a beer/coffee? :)

If you enjoy the underlying projects and want to buy itsToggle a beer/coffee, feel free to use the real-debrid [affiliate link](http://real-debrid.com/?id=5708990) or send a virtual beverage via [PayPal](https://www.paypal.com/paypalme/oidulibbe) :)

## Buy **[yowmamasita](https://github.com/yowmamasita)** a beer/coffee? :)

If you enjoy the underlying projects and want to buy yowmamasita a beer/coffee, feel free to use the [GitHub sponsor link](https://github.com/sponsors/debridmediamanager)

## Buy **[ncw](https://github.com/ncw)** a beer/coffee? :) 

If you enjoy the underlying projects and want to buy Nick Craig-Wood a beer/coffee, feel free to use the website's [sponsor links](https://rclone.org/sponsor/)

## GitHub Workflow Status
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/I-am-PUID-0/pd_zurg/docker-image.yml)
