# How to Configure:

## 1. Copy file to systemd
```bash
sudo cp autorun/ros2_launch_controller_driver.service /etc/systemd/system/ros2_launch_controller_driver.service
```

## 2. Get the User name, display, and home directory
By default, the display may be `:0` and the home should be `/home/$USER`. Please ensure the correct values are used.
```bash
echo $USER
echo $DISPLAY
echo $HOME
```

## 3. Get the User ID
By default this is 1000, this may need to be changed however so check the correct value for your system.
```bash
loginctl show-user $USER | grep UID
```

## 4. Get the ROS DOMAIN ID
By default this is unset or set to 0, if the system is to interact with other nodes running oon your system, ensure this is set to a useful value.
```bash
echo $ROS_DOMAIN_ID
```

## 5. Open the file and update the values
```ini
...
Environment="ROS_DOMAIN_ID=<ROS_DOMAIN_ID>"
Environment="DISPLAY=<DISPLAY>"
Environment="DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/<UID>/bus"
Environment="XDG_RUNTIME_DIR=/run/user/<UID>"
User=<USER>
WorkingDirectory=<HOME>
ExecStartPre=/bin/mkdir -p /run/user/<UID>
ExecStartPre=/bin/chown <USER>:<USER> /run/user/<UID>
ExecStartPre=/bin/chmod 700 /run/user/<UID>
...
ExecStart=/bin/bash -c 'source /opt/ros/humble/setup.bash; source <HOME>/ros2_ws/install/setup.bash; ros2 launch controller_commands driver.launch.py'
...
```

# 6. Create and start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable ros2_launch_controller_driver.service
sudo systemctl start ros2_launch_controller_driver.service
```

# 7. Monitor the output
```bash
export ROS_MASTER_URI=<ROS_DOMAIN_ID>; ros2 topic echo /rosout | grep msg
```
