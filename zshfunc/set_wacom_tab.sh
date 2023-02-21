#!/bin/sh
TABLET='HUION Huion Tablet_H640P Pad pad'
if (command -v xsetwacom) && (xsetwacom --list devices | grep -q $TABLET)
then
    xsetwacom --set $TABLET Button 1 "key +ctrl +z -z -ctrl"
    xsetwacom --set $TABLET Button 2 "key e"
    xsetwacom --set $TABLET Button 3 "key b"
    xsetwacom --set $TABLET Button 8 "key +"
    xsetwacom --set $TABLET Button 9 "key -"
    # set last button to ctrl+alt+m that would toggle mic using `amixer set Capture toggle`
    xsetwacom --set $TABLET Button 10 "key +ctrl +alt +m -m -alt -ctrl"
fi
