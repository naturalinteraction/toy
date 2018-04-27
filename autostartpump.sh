cd /home/pi/toy
sudo pigpiod
echo 'waiting...'
sleep 30
sudo pigpiod
xterm -hold -e "sudo pigpiod ; python pump.py"
