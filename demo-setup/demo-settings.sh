#!/bin/bash

# This should be the full name of the path to where you store your demo vms
VMPATH="${HOME}/Documents/Virtual Machines.localized"
# Names of all your demo VMs
VMNAMES=(qumulo-1 qumulo-2 qumulo-3 qumulo-4 qumulo-5)
# Name of the base-state snapshot on each VM (Snapshots must all be identically named)
SNAPSHOTNAME=Snapshot
# Complete path to the ova we're going to setup. This option gets used if the file is not specified on the command line
SOURCE="${HOME}/Downloads/qkiosk-39204.1.12.ova"


