qse-utils/demo-setup - A few utilities to automate demo housekeeping commonly performed manually by Qumulo SEs.
by Mike Bott <mbott@qumulo.com>


MANIFEST:

demo-settings.sh - Set variables the scripts consume

demo-deploy.sh <qkiosk_full_path.ova> - Takes a path to a Qumulo .ova, deploys 5 nodes, Snapshots them, adds to inventory

demo-reset.sh - Reset a bunch of Qumulo VMs on VMware Fusion using vmrun

bash_profile - Two $PATH additions for vmrun and ovftool, you can cat them into your ~/.bash_profile.

WARNING: These scripts might crash versions of Fusion prior to 7.1.0, but apart from that work as intended. For obvious
reasons, you should only run demo-reset.sh AFTER you are done giving a demo. Also, ovftool is really chatty so
demo-deploy.sh is too.


DEPENDENCIES:

You must be running Version 7 of VMware Fusion or greater, or this will break.

You must have the 'vmrun' executable in your path. If you are having a hard time locating vmrun, do this in a terminal:
sudo find / -name vmrun -print
By default mine got installed here: /Applications/VMware Fusion.app/Contents/Library/vmrun

You must also have the ovftool utility (4.0.0 or greater) installed and in your path. Try this if you don't know where
it is: sudo find / -name ovftool -print
By default mine got installed here: /Applications/VMware Fusion.app/Contents/Library/VMware OVF Tool/ovftool

Add the above directories to your PATH like so:
export PATH="$PATH:/Applications/VMware Fusion.app/Contents/Library"
export PATH="$PATH:/Applications/VMware Fusion.app/Contents/Library/VMware OVF Tool"

You can put those lines in your .bash_profile in your home directory and it will run every time you restore a terminal.
From the demo-setup directory dols

cat bash_profile >> ~/.bash_profile
You will have to open a new terminal/shell or login again for the change to your path to take effect.


CONFIGURATION

There are only 3 variables at the top of demo-settings.sh that you might need to modify based on your local setup:

# This should be the full name of the path to where you store your demo VMs
VMPATH="${HOME}/Documents/Virtual Machines.localized"


# These are the names of the virtual machines you use for your demo. Please note that you need to backslash escape
# spaces and other characters that are interesting to bash.
VMNAMES=(demotest-1 demotest-2 demotest-3 demotest-4 demotest-5)

# This is the name of the snapshot you roll back to when cleaning up after a demo. You should use the same baseline
# snapshot name for all Qumulo VMs when first setting up your demo. "Snapshot" is the default under VMware Fusion.
SNAPSHOTNAME=Snapshot

The last variable, SOURCE, is only used if you don't supply a path to an OVA when running demo-deploy.sh.


CHANGELOG

2015-02-10 Updated for Qumulo 1.1.1