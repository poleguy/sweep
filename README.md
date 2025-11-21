# sweep

catch all for usefull stuff

public so it's easy to get

secrets aren't saved here

## install teams_chrome_status

Set it up to start at bootup. 
```
sudo cp teams_chrome_status.service /etc/systemd/system/
sudo systemctl daemon-reload 
sudo systemctl start teams_chrome_status.service
```


## setup:

``` bash
scripts/setup_python
source scripts/activate_python
killall chrome
google-chrome·--app=https://teams.microsoft.com·--remote-debugging-port=9222·--remote-allow-origins=http://localhost:9222
python3 teams_chrome_status.py
```



# ansible/

contains a pull mode ansible playbook to set up pinephone
