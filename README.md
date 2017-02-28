## Object tracking and robotic arm control

### Introduction
This is a small project to use OpenCV 3 to control [OWI robotic arm](https://www.amazon.com/OWI-OWI-535-Robotic-Arm-Edge/dp/B0017OFRCY/ref=sr_1_1?ie=UTF8&qid=1487966592&sr=8-1&keywords=owi+arm)

It is based on couple of other projects

* https://github.com/dannystaple/robot_arm
* http://blog.aicookbook.com/2010/06/building-a-face-tracking-robot-headroid1-with-python-in-an-afternoon/
* [OpenCV Python tutorial](http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_gui/py_table_of_contents_gui/py_table_of_contents_gui.html)

It will track your fist (left hand) and move OWI robotic arm according your movement in x or y direction


### Installation
If you are using anaconda python dist, you will need to install OpenCV
``` 
conda install -f  -c menpo opencv3
```
and install pyusb
```
pip install pyusb
```