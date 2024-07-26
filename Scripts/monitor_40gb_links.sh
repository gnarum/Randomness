#!/bin/bash

DESIRED_MTU="65520"
HOSTNAME_REGEX="^cn*"
INTERFACES="en05 en06"
MTU_CORRECT=0
NUM_INTERFACES=$(echo $INTERFACES | wc -w )
NUM_NODES=3
SYSTEM_CHANGED=0
UP_INTERFACES=0

# If we're not running as root, exit, there is no point
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root"
    exit 1
fi

# Function recheck interface
# if "$(ip link show <INTERFACE> | awk '{print $9}')" -eq "UP"; then <INTERFACE>=1;
function is_interface_up() {
    INTERFACE_STATUS=$(ip link show $1 | awk '/state/ {print $9}')
    [ $INTERFACE_STATUS == UP ]
    echo $?
}

# Function check interface MTU
function is_mtu_correct() {
    INTERFACE_MTU=$(ip link show $1 | awk '/mtu/ {print $5}')
    [[ $INTERFACE_MTU -eq $DESIRED_MTU ]]
    echo $?
}

# Loop until both flags are set
while :
do
    for i in $INTERFACES; do
        # if interface is not up, turn it on
        if [ $(is_interface_up $i) -ne 0 ]; then
            /usr/sbin/ifup $i
            let SYSTEM_CHANGED++
        fi
        # if interface is up, count it as up
        if [ $(is_interface_up $i) -eq 0 ]; then
            let UP_INTERFACES++
        fi
        # chck if the MTU is set correctly
        # if not set correctly, set it
        if [ $(is_mtu_correct $i) -ne 0 ]; then
            /usr/sbin/ip link set mtu 65520 $i
            let SYSTEM_CHANGED++
        fi
        # check if the MTU is set correctly
        # if it is, count it
        if [ $(is_mtu_correct $i) -eq 0 ]; then
            let MTU_CORRECT++
        fi
    done
    # All interfaces are correct
    if [[ $UP_INTERFACES == $NUM_INTERFACES && $MTU_CORRECT == $NUM_INTERFACES ]]; then
        break
    else
        UP_INTERFACES=0
        MTU_CORRECT=0
    fi
done

# Once we're here, our interfaces are up and our MTU is set.
# Check and fix the routing tables

while :; do
    CURRENT_NODES=$(vtysh -c "show openfabric topology" | grep -E "$HOSTNAME_REGEX" | awk '{print $1}' | wc -l)
    if [[ $CURRENT_NODES -eq $NUM_NODES ]]; then
        # echo "Number of nodes matches the expected value: $NUM_NODES"
        break
    else
        # echo "Current number of nodes ($CURRENT_NODES) does not match the expected value ($NUM_NODES). Retrying..."
        systemctl restart frr.service
        # Wait 20 seconds to try again
        sleep 20
    fi
done

# Work complete, exiting.
