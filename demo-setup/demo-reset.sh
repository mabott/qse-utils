#!/bin/bash

source demo-settings.sh

echo "Shutting down all Qumulo VMs..."
for ((i = 0; i < ${#VMNAMES[@]}; i++))
do
    vmrun -T fusion stop "$VMPATH"/"${VMNAMES[$i]}".vmwarevm && echo "${VMNAMES[$i]}.vmwarevm has been shut down"
done

echo "Reverting all Qumulo VMs to snapshot $SNAPSHOTNAME..."
for ((i = 0; i < ${#VMNAMES[@]}; i++))
do
    vmrun -T fusion revertToSnapshot "$VMPATH"/"${VMNAMES[$i]}".vmwarevm $SNAPSHOTNAME && echo "${VMNAMES[$i]}.vmwarevm has been reverted to snapshot $SNAPSHOTNAME"
done
