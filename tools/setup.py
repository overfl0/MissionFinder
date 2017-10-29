#!/usr/bin/env python3

#######################
#  Frontline Setup Script  #
#######################

import ctypes
import os
import pip
import subprocess
import sys
import winreg

######## GLOBALS #########
PROJECTDIR = "MissionFinder"
##########################

def satisfy_requirements(filename):
    if pip.main(['install', '-r', filename]) != 0:
        print('Error while installing python requirements, exiting...')
        sys.exit(1)


def main():
    print("""
  ###########################################
  # Frontline Development Environment Setup #
  ###########################################

  This script will create your Frontline dev environment for you.

  This script will create two hard links on your system, both pointing to your Frontline project folder:
    [Arma 3 Missions folder] 		=> DynamicFrontline\Missions
    [Arma 3 Installation folder]   	=> python
  """)
    print("\n")

    satisfy_requirements(os.path.join(os.path.dirname(__file__), '..', 'requirements.txt'))

    try:
        reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        key = winreg.OpenKey(reg,
                r"SOFTWARE\Wow6432Node\bohemia interactive\arma 3")
        armapath = winreg.EnumValue(key,1)[1]
    except:
        print("Failed to determine Arma 3 Path.")
        return 1

    scriptpath = os.path.realpath(__file__)
    projectpath = os.path.dirname(os.path.dirname(scriptpath))
    pythonpath = os.path.join(armapath, "python")

    print("# Detected Paths:")
    print("  Arma Path:     {}".format(armapath))
    print("  Repository Path:  {}".format(projectpath))

    repl = input("\nAre these correct? (y/n): ")
    if repl.lower() != "y":
        return 3

    print("\n# Creating links ...")

    try:
        if not os.path.exists(pythonpath):
            os.mkdir(pythonpath)

        subprocess.call(["cmd", "/c", "mklink", "/D", "/J", os.path.join(pythonpath, PROJECTDIR), os.path.join(projectpath, 'python')])

    except:
        raise
        print("Something went wrong during the link creation. Please finish the setup manually.")
        return 6

    print("# Links created successfully.")

    return 0


if __name__ == "__main__":
    exitcode = main()

    if exitcode > 0:
        print("\nSomething went wrong during the setup. Make sure you run this script as administrator.")
    else:
        print("\nSetup successfully completed.")

    input("\nPress enter to exit ...")
    sys.exit(exitcode)
