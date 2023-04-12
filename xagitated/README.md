

## dependencies

```
sudo apt install xprintidle
```

## checking service status

service status:

```
sudo systemctl status xagitated.service 
```

serice journal:

```
sudo journalctl -u xagitated.service  -f
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
sudo systemctl daemon-reload
sudo systemctl enable xagitated.service 
sudo systemctl start xagitated.service 

```