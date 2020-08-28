After OS installs.

Mount dualie.

sudo apt install sshfs

sudo mkdir /mnt/dualie

sudo chown helen:helen /mnt/dualie

sshfs -P 8022 dualie.poleguy.com /mnt/dualie
