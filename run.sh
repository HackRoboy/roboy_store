setsid roslaunch rosbridge_server rosbridge_websocket.launch >/dev/null 2>&1 < /dev/null &
setsid node-red >/dev/null 2>&1 < /dev/null&
