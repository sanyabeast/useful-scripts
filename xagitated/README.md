

## dependencies

```
sudo apt install xprintidle
```

```
pip install 
```

## checking service status

service status:

```
systemctl --user status xagitated.service 
```

serice journal:

```
journalctl --user -u xagitated.service  -f
```


xagitated.service file content:

```
[Unit]
Description=xagitated

[Service]
ExecStart=runuser -l retr0 -c "/home/retr0/Projects/useful-scripts/xagitated/xagitated.sh"
Restart=always

[Install]
WantedBy=multi-user.target
```

setting service up for the first time:

```
systemctl --user daemon-reload
systemctl --user enable xagitated.service 
systemctl --user start xagitated.service 

```