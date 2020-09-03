After OS installs.

Mount dualie.

    sudo apt install sshfs
    sudo mkdir /mnt/dualie
    sudo chown $USER:$USER /mnt/dualie
    sshfs -p 8080 poleguy@dualie.poleguy.com:/ /mnt/dualie
    # sshfs -p 8080 poleguy@192.168.1.110:/ /mnt/dualie
    sudo umount /mnt/dualie # if 'Transport endpoint is not connected'

To connect to dualie to peek at cherrytree for notes

    sudo apt install cherrytree
    cherrytree /mnt/dualie/home/poleguy/data/2020&
    find node: "#202007131451 ansible for ubuntu"

Check out ubuntu:

    # https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-on-ubuntu
    sudo apt update
    sudo apt install software-properties-common
    sudo apt-add-repository --yes --update ppa:ansible/ansible
    sudo apt install ansible
    sudo apt install git

Check out classical:
  
    cd
    git clone https://github.com/poleguy/classical.git
    #github@poleguy.com
    cd classical
    
Various:
    
    git config --global user.name "Nicholas Dietz"
    git config --global user.email "github@poleguy.com"
