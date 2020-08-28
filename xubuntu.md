After OS installs.

Mount dualie.

sudo apt install sshfs

  sudo mkdir /mnt/dualie

  sudo chown helen:helen /mnt/dualie

  # sshfs -p 8022 poleguy@dualie.poleguy.com /mnt/dualie
  sshfs -p 8022 poleguy@192.168.1.110 /mnt/dualie
  sudo umount /mnt/dualie # if 'Transport endpoint is not connected'
  
  
