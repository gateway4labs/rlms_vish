#!/bin/bash

# Not needed at all. Just handy while developing (it auto-setups the app whenever it is changed)

while true; do
    python setup.py install
    inotifywait -e modify g4l_rlms_vish.py;
done

