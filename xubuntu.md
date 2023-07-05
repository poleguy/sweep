After OS installs.

    ssh-keygen -t ed25519 -C "poleguy@flippy.poleguy.com"
    cat ~/.ssh/id_ed25519.pub 
    
Push key to github.
    Paste the key to https://github.com/settings/keys

Install barrier
    

Install emacs, ansible, git:

    # https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu
    sudo apt update
    sudo apt upgrade
    # sudo apt install -y software-properties-common
    # sudo apt-add-repository --yes --update ppa:ansible/ansible
    sudo apt install ansible
    sudo apt install git
    sudo apt install emacs

Check out classical:
  
    cd
    git clone git@github.com:poleguy/classical.git
    # git remote show origin
    # git remote set-url origin git@github.com:poleguy/classical.git
    # github@poleguy.com
    cd classical

Optional for yoga laptops. This will set up tear-free graphics, laptop keyboard disable for tablet, palm rejection, etc.
    
    ./yoga_play 
    
Standard setup (desktop/laptop)
    
    ./local_play --check --tags yum_apps
    ./local_play --tags yum_apps
    ./local_play --check
    -/local_play

Setup Yoga 260 disable keyboard on flip

    cd ~/flippy-data/bin
    bash install.sh


Various:
    
    git config --global user.name "Nicholas Dietz"
    git config --global user.email "github@poleguy.com"

    #sudo apt -y install emacs # snap is newer, but no.
     
Set up .dotfiles

    # to bootstrap a new machine:
    cd ~
    curl -Lks https://raw.githubusercontent.com/poleguy/dotfiles/master/dotfiles_setup | /bin/bash

Set up editor for poleguy.com

    # to install:
    cd ~/flippy-data/2021/poleguy.com/
    emacs ./install
    # change anything that looks sketchy
    source ./install
    
    
Mount dualie.

    sudo apt -y install sshfs
    sudo mkdir /mnt/dualie
    sudo chown $USER:$USER /mnt/dualie
    sshfs -p 8080 poleguy@dualie.poleguy.com:/ /mnt/dualie
    # sshfs -p 8080 poleguy@192.168.1.110:/ /mnt/dualie
    sudo umount /mnt/dualie # if 'Transport endpoint is not connected'
    
    sudo apt -y install meld
    meld ~/.ssh /mnt/dualie/home/poleguy/.ssh
    # copy across credentials

To connect to dualie to peek at cherrytree for notes

    #sudo apt install cherrytree
    ./local_play --tags cherrytree
    cherrytree /mnt/dualie/home/poleguy/data/2020&
    find node: "#202007131451 ansible for ubuntu"

Set up network DNS:
    click on Edit Connections...
    IPv4 Settings
    Select Automatic (DHCP) addresses only
    DNS: 127.0.1.1 (or 1.1.1.1 if dns isn't set up yet)
    sudo systemctl restart NetworkManager
    
Setup emacs:
    to not display startup screen
    CUA mode
    
TODO: Install krita
    Screensaver settings
        30 min
        Disable lock screen
    
