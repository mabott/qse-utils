

#!/bin/bash

source demo-settings.sh

[ ! -z "$1" ] && SOURCE=$1

echo "SOURCE: $SOURCE"
echo "VMPATH: $VMPATH"

for ((i = 0; i < ${#VMNAMES[@]}; i++)); do

    NAME="${VMNAMES[$i]}"

    # Deploy from ovf
    ovftool --allowExtraConfig -tt=vmx --lax --name=$NAME "$SOURCE" "$VMPATH" && echo "VMX deployed from OVF"
    # Change bridged to nat in .vmx file 'ethernet0.connectionType = "bridged"'
    sed -i .bak 's/bridged/nat/' "$VMPATH/$NAME.vmwarevm/$NAME.vmx" && echo "ethernet0.connectionType = bridged -> nat"
    # Create Snapshot
    vmrun -T fusion snapshot "$VMPATH"/"$NAME".vmwarevm $SNAPSHOTNAME && echo "Created snapshot 'Snapshot'"

done

for ((i = 0; i < ${#VMNAMES[@]}; i++)); do

    NAME="${VMNAMES[$i]}"

    # Launch it in VMware Fusion once, so it gets added to the VM inventory properly
    vmrun -T fusion start "$VMPATH"/"$NAME".vmwarevm/"$NAME".vmx && echo "Powered up demo VM and added it to inventory"
    # Power it down
    vmrun -T fusion stop "$VMPATH"/"$NAME".vmwarevm && echo "${VMNAMES[$i]}.vmwarevm has been shut down"

done

for ((i = 0; i < ${#VMNAMES[@]}; i++)); do

    NAME="${VMNAMES[$i]}"

    # Roll back to Snapshot
    vmrun -T fusion revertToSnapshot "$VMPATH"/"$NAME".vmwarevm $SNAPSHOTNAME && echo "$NAME.vmwarevm has been reverted to snapshot $SNAPSHOTNAME"

done
