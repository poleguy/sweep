This is a bash script to replace gdebi with a call to sudo apt and a pop-up terminal.

I wanted to be able to install .deb files from a firefox download without typing extra stuff at the command line.
gdebi was needed because ubuntu's software center wasn't installing downloaded deb files at all.
gdebi worked for a while, but recently  started failing with dependency errors, and it seems abandoned.

so now we have apt-instal-deb

install with:
sudo install -m 755 apt-install-deb /usr/local/bin/apt-install-deb

Then set it as the default app for .deb files.