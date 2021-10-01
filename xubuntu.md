After OS installs.

    ssh-keygen -t ed25519 -C "poleguy@flippy.poleguy.com"
    cat ~/.ssh/id_ed25519.pub 

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

Check out ubuntu:

    # https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu
    sudo apt update -y
    sudo apt install -y software-properties-common
    sudo apt-add-repository --yes --update ppa:ansible/ansible
    sudo apt -y install ansible
    sudo apt -y install git

Check out classical:
  
    cd
    # you won't have a key in place yet, so:
    git clone https://github.com/poleguy/classical.git
    # if you do have a key:
    # git clone git@github.com:poleguy/classical.git
    # git remote show origin
    # git remote set-url origin git@github.com:poleguy/classical.git
    # github@poleguy.com
    cd classical

To connect to dualie to peek at cherrytree for notes

    #sudo apt install cherrytree
    ./local_play --tags cherrytree
    cherrytree /mnt/dualie/home/poleguy/data/2020&
    find node: "#202007131451 ansible for ubuntu"


Set up laptop. This will set up tear-free graphics, laptop keyboard disable for tablet, palm rejection, etc.
    
    ./yoga_play 


Various:
    
    git config --global user.name "Nicholas Dietz"
    git config --global user.email "github@poleguy.com"

    sudo apt -y install emacs # snap is newer, but no.
    
Setup Yoga 260 disable keyboard on flip

    cd ~/flippy-data/bin
    bash install.sh
    
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
    
    
