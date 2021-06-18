After OS installs.

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
    # git show origin
    # git remote set-url origin git@github.com:poleguy/classical.git
    # github@poleguy.com
    cd classical

To connect to dualie to peek at cherrytree for notes

    #sudo apt install cherrytree
    ./local_play --tags cherrytree
    cherrytree /mnt/dualie/home/poleguy/data/2020&
    find node: "#202007131451 ansible for ubuntu"

Various:
    
    git config --global user.name "Nicholas Dietz"
    git config --global user.email "github@poleguy.com"

    sudo apt -y install emacs # snap is newer, but no.
    
    sudo apt
