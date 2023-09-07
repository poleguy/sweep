#!/usr/bin/env bash
	       
# This is a do nothing script. Run it and follow the instructions.
# Run this with:
# https://gist.github.com/jwebcat/5122366
# https://stackoverflow.com/questions/63131569/how-to-use-curl-to-download-a-raw-file-in-a-git-repository-from-git-hosting-site
# wget https://raw.githubusercontent.com/poleguy/sweep/master/xubuntu.md
# becaus curl isn't installed by default
# then run
# bash xubuntu.md
set -eu

wait() {
    echo
    echo $1
    read -p "Press [enter] when ready. "
}

echo "After OS installs."

#echo "Install and configure barrier"
#if [ ! -f "$HOME/.config/Debauchee/Barrier.conf" ]; then
#
#    sudo apt install barrier -y
#    #rm ~/.local/share/barrier/SSL/Fingerprints/TrustedServers.txt
#    cp Barrier.conf ~/.config/Debauchee/Barrier.conf
#    
#    echo " "
#    echo "Set the autoHide value:"
#    echo "autoHide=true"
#    echo "autoStart=true"
#    echo "serverHostname=elgar.local"
#    wait "About to edit Barrier.conf"
#    emacs  ~/.config/Debauchee/Barrier.conf
#    
#    # todo: if barrier is not running
#    barrier &
#    disown
#    # make sure screen is clear
#    #sleep 3
#    #echo " "
#    #wait "Configure barrier as client, with server IP: 192.168.1.162 (elgar) if appropriate, and accept ssl fingerprint"
#fi
#
#
#echo "if not done already:"
#if [ ! -f "$HOME/.ssh/id_ed25519" ]; then
#    #ssh-keygen -t ed25519 -C "poleguy@flippy.poleguy.com"
#    # no passphrase, no interaction
#    ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519b -N ""
#fi
#
#echo "push key to dualie"
#    ssh-copy-id -i ~/.ssh/id_ed25519.pub poleguy@dualie.poleguy.com
#
#    cat ~/.ssh/id_ed25519.pub 
#    # todo: use xclip to put it right in the clipboard, or fully automate this    
#echo "Push key to github."
#
#wait "Paste the key to https://github.com/settings/keys"
#
#echo "Install emacs, ansible, git:"
#
#    # https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu
#
#echo "Update system"
#    sudo apt update
#    sudo apt upgrade
#
#echo "if not done already, log state of system after install/update"
#if [ ! -f "$HOME/installed.txt" ]; then
#    cd ~
#    apt list --installed > installed.txt
#fi
#
## sudo apt install -y software-properties-common
#    # sudo apt-add-repository --yes --update ppa:ansible/ansible
#    sudo apt install ansible -y
#    sudo apt install git -y
#    sudo apt install emacs -y
#
#echo "Mount dualie."
#
## move to ansible:
#sudo apt install sshfs -y
#MOUNTED=0
#mount | grep dualie.poleguy.com && MOUNTED=1
#if [ ! $MOUNTED  ]; then
#    mkdir -p ~/dualie
#    #sudo chown $USER:$USER /mnt/dualie
#    #sshfs -p 8080 poleguy@dualie.poleguy.com:/ /mnt/dualie
#    sshfs poleguy@dualie.poleguy.com:/ ~/dualie
#    # sshfs -p 8080 poleguy@192.168.1.110:/ /mnt/dualie
#    #sudo umount /mnt/dualie # if 'Transport endpoint is not connected'
#fi
## move to ansible:
#    sudo apt install meld -y
#    wait "About to run meld to diff .ssh directories. Please copy across ssh credentials if necessary. (systems_key, config?)"
#    meld ~/.ssh ~/dualie/home/poleguy/.ssh
#
#echo "To connect to dualie to peek at cherrytree for notes"
#
##./local_play --tags cherrytree
#    sudo apt install cherrytree -y
#    cherrytree ~/dualie/home/poleguy/flippy-data/poleguy_notes.ctb &
#    wait 'find node: "#202007131451 ansible for ubuntu"'
#
#
#rsync -rahP dualie.poleguy.com:/misc/images /misc/images
    
echo "Check out classical:"

if [ ! -d "$HOME/classical" ]; then
    cd
    git clone git@github.com:poleguy/classical.git
    # git remote show origin
    # git remote set-url origin git@github.com:poleguy/classical.git
    # github@poleguy.com
fi


echo "Optional for yoga laptops. This will set up tear-free graphics, laptop keyboard disable for tablet, palm rejection, etc."

RESULT=$(sudo dmidecode -s system-version)
if [[ "$RESULT" == "ThinkPad Yoga 260" ]]; then
    echo "This is a laptop"
    cd ~/classical
    ./yoga_play

    echo "Setup Yoga 260 disable keyboard on flip"

    echo    cd ~/flippy-data/bin
    echo    bash install.sh
    
    wait "Where does this come from?"

fi

echo "Standard setup (desktop/laptop)"
cd ~/classical
    
#    ./loca	l_play --check --tags yum_apps
#    ./local_play --tags yum_apps
#    ./local_play --check
    ./local_play


echo "Various:"
    
#    git config --global user.name "Nicholas Dietz"
#    git config --global user.email "github@poleguy.com"

     
echo "Set up .dotfiles"

    # to bootstrap a new machine:
    cd ~
# move to ansible:
    sudo apt install curl -y
# move to ansible:
    curl -Lks https://raw.githubusercontent.com/poleguy/dotfiles/master/dotfiles_setup | /bin/bash

echo "Set up editor for poleguy.com"

    # to install:
    cd ~/flippy-data/2021/poleguy.com/
    emacs ./install
    # change anything that looks sketchy
    source ./install

echo " "
echo "Set up network DNS:"
echo "click on Edit Connections..."
echo "    IPv4 Settings"
echo "   Select Automatic (DHCP) addresses only"
wait "   "DNS: 127.0.1.1 (or 1.1.1.1 if dns isn't set up yet)"

    sudo systemctl restart NetworkManager
    
echo "Setup emacs:"
echo "    to not display startup screen"
wait "    CUA mode"
    
echo "TODO: Install krita"

echo "Screensaver settings"
echo "        30 min"
wait "        Disable lock screen"
    
