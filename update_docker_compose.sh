#!/bin/bash

DOCKER_COMPOSE_FILE="docker-compose.yml"

escape_for_sed() {
    echo "$1" | sed -e 's/[\/&]/\\&/g'
}

prompt_for_value() {
    local variable=$1
    local default_value=$2
    read -p "Enter value for $variable [$default_value]: " value
    if [[ -z "$value" ]]; then
        echo "$default_value"
    else
        echo "$value"
    fi
}

update_docker_compose() {
    local variable=$1
    local new_value=$(escape_for_sed "$2")
    if grep -q "^\([[:space:]]*#\s*-\s*$variable=\)" "$DOCKER_COMPOSE_FILE"; then
        sed -i "s|^\([[:space:]]*\)#\s*-\s*$variable=.*|\1 - $variable=$new_value|" "$DOCKER_COMPOSE_FILE"
    else
        sed -i "s|^\([[:space:]]*\)-\s*$variable=.*|\1- $variable=$new_value|" "$DOCKER_COMPOSE_FILE"
    fi
}

prompt_for_group() {
    local group_vars=("${!1}")
    for var in "${group_vars[@]}"; do
        new_value=$(prompt_for_value "$var" "${env_vars[$var]}")
        update_docker_compose "$var" "$new_value"
    done
}

echo "Updating docker-compose.yml file..."

declare -A env_vars=(
    ["ZURG_ENABLED"]="true"
    ["RD_API_KEY"]=""
    ["RCLONE_MOUNT_NAME"]="pd_zurg"
    ["PD_ENABLED"]="true"
    ["PLEX_USER"]=""
    ["PLEX_TOKEN"]=""
    ["PLEX_ADDRESS"]=""
    ["PLEX_REFRESH"]="true"
    ["PLEX_MOUNT_DIR"]="/pd_zurg"
    ["ZURG_UPDATE"]="true"
    ["ZURG_VERSION"]="v0.9.2-hotfix.4"
    ["PD_UPDATE"]="true"
    ["SEERR_API_KEY"]=""
    ["SEERR_ADDRESS"]=""
)

zurg_vars=("ZURG_ENABLED" "RD_API_KEY" "RCLONE_MOUNT_NAME")
plex_debrid_vars=("PD_ENABLED" "PLEX_USER" "PLEX_TOKEN" "PLEX_ADDRESS")
plex_refresh_vars=("PLEX_REFRESH" "PLEX_MOUNT_DIR")
zurg_update_vars=("ZURG_UPDATE")
zurg_version_vars=("ZURG_VERSION")
plex_debrid_update_vars=("PD_UPDATE")
seerr_vars=("SEERR_API_KEY" "SEERR_ADDRESS")
additional_plex_vars=("PLEX_TOKEN" "PLEX_ADDRESS")

read -p "Would you like to enable Zurg? (yes/no) " zurg_choice
zurg_choice=$(echo "$zurg_choice" | tr '[:upper:]' '[:lower:]')
if [[ "$zurg_choice" == "yes" || "$zurg_choice" == "y" ]]; then
    prompt_for_group zurg_vars[@]
else
    env_vars["ZURG_ENABLED"]="false"
    update_docker_compose "ZURG_ENABLED" "false"	
fi

read -p "Would you like to enable plex_debrid? (yes/no) " plex_debrid_choice
plex_debrid_choice=$(echo "$plex_debrid_choice" | tr '[:upper:]' '[:lower:]')
if [[ "$plex_debrid_choice" == "yes" || "$plex_debrid_choice" == "y" ]]; then
    prompt_for_group plex_debrid_vars[@]
    if [[ "$zurg_choice" != "yes" && "$zurg_choice" != "y" ]]; then
        new_value=$(prompt_for_value "RD_API_KEY" "${env_vars["RD_API_KEY"]}")
        update_docker_compose "RD_API_KEY" "$new_value"
    fi  
else
    env_vars["PD_ENABLED"]="false"
    update_docker_compose "PD_ENABLED" "false"
fi

if [[ "$zurg_choice" == "yes" || "$zurg_choice" == "y" ]]; then
    read -p "Would you like to enable PLEX_REFRESH for Zurg? (yes/no) " plex_refresh_choice
    plex_refresh_choice=$(echo "$plex_refresh_choice" | tr '[:upper:]' '[:lower:]')
    if [[ "$plex_refresh_choice" == "yes" || "$plex_refresh_choice" == "y" ]]; then
        prompt_for_group plex_refresh_vars[@]
        if [[ "$plex_debrid_choice" != "yes" && "$plex_debrid_choice" != "y" ]]; then
            prompt_for_group additional_plex_vars[@]
        fi
    fi

    read -p "Would you like to enable automatic updates for Zurg? (yes/no) " choice
    choice=$(echo "$choice" | tr '[:upper:]' '[:lower:]')
    if [[ "$choice" == "yes" || "$choice" == "y" ]]; then
        prompt_for_group zurg_update_vars[@]
    fi

    read -p "Would you like to define the version of Zurg to use? (yes/no) " choice
    choice=$(echo "$choice" | tr '[:upper:]' '[:lower:]')
    if [[ "$choice" == "yes" || "$choice" == "y" ]]; then
        prompt_for_group zurg_version_vars[@]
    fi
fi

if [[ "$plex_debrid_choice" == "yes" || "$plex_debrid_choice" == "y" ]]; then
    read -p "Would you like to enable automatic updates for plex_debrid? (yes/no) " choice
    choice=$(echo "$choice" | tr '[:upper:]' '[:lower:]')
    if [[ "$choice" == "yes" || "$choice" == "y" ]]; then
        prompt_for_group plex_debrid_update_vars[@]
    fi

    read -p "Would you like to add Overseerr/Jellyseerr for use with plex_debrid? (yes/no) " choice
    choice=$(echo "$choice" | tr '[:upper:]' '[:lower:]')
    if [[ "$choice" == "yes" || "$choice" == "y" ]]; then
        prompt_for_group seerr_vars[@]
    fi
fi

echo "docker-compose.yml updated successfully."