#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Simone Caronni <negativo17@gmail.com>
# Licensed under the GNU General Public License Version or later

import json
import re
import os
import shutil
import subprocess
import sys
import tarfile
from urllib.request import Request, urlopen

def main():
    repo_url = 'http://api.snapcraft.io/v2/snaps/info/authy'

    request = Request(repo_url)
    request.add_header('Snap-Device-Series', '16')
    response = urlopen(request).read()
    repo_url_raw = json.loads(response)

    for channel_map in repo_url_raw['channel-map']:
        if 'stable' in channel_map['channel']['name']:
            version = channel_map['version']
            snap_url = channel_map['download']['url']

    with open('authy.spec', 'r') as file:
        for line in file:
            if re.search('^Version:.*' + version, line, re.I):
                print("SPEC file already contains the latest version: " + version + ".")
                sys.exit(0)

    print("New version available: " + version + " (" + snap_url + ")")

    print("Updating SPEC file...", end = " ")
    rpmdev_bumpspec_comment = ("Update to version " + version + ".")
    subprocess.run(["rpmdev-bumpspec", "-D", "-c", rpmdev_bumpspec_comment, "-n", version, "authy.spec" ])
    print("done.")

    tarball = ("authy-" + version)
    
    print("Downloading snap file " + tarball + ".snap" + "...", end=" ", flush=True)
    request = Request(snap_url)
    response = urlopen(request).read()
    open(tarball + ".snap", 'wb').write(response)
    print("done.")

    print("Unpacking " + tarball + ".snap" + "...", end=" ", flush=True)
    subprocess.run(["unsquashfs", "-q", "-n", "-f", "-d", tarball, tarball + ".snap"])
    shutil.rmtree(tarball + "/data-dir")
    shutil.rmtree(tarball + "/lib")
    shutil.rmtree(tarball + "/gnome-platform")
    shutil.rmtree(tarball + "/scripts")
    shutil.rmtree(tarball + "/usr")
    os.remove(tarball + "/command.sh")
    os.remove(tarball + "/desktop-common.sh")
    os.remove(tarball + "/desktop-gnome-specific.sh")
    os.remove(tarball + "/desktop-init.sh")
    os.remove(tarball + "/meta/snap.yaml")
    os.remove(tarball + ".snap")
    print("done.")

    print("Creating tarball " + tarball + ".tar.xz...", end=" ", flush=True)
    tar = tarfile.open(tarball + ".tar.xz", "w:xz")
    tar.add(tarball)
    tar.close()
    shutil.rmtree(tarball)
    print("done.")

if __name__ == "__main__":
    main()
