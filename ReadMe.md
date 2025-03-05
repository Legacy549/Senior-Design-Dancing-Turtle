# Dancing Turtle

Hello! This is the official GitHub Repository for Dancing Turtle. Here we wish to provide you with the instructions on how to run, edit and debug our code. Although simple in nature, it can get complicated real fast. 


# Dance Control Script

The Dance Control script is comprised of four sections. A socket server that interacts with our GUI to user input, a socket server that interacts with the Turtle's Raspberry Pi 4B to send angle data, a .csv file reader to read prerecorded dances from a list and lastly, motion tracking API control using NUI Track. I will go into each section in detail and how it functions as well how to run the script itself. 

## GUI Socket Client

This portion receives commands from our GUI on what to send to the Turtle **Under Construction**

## GUI Socket Sender

This sends angle data to our Turtle using a socket server. The IP address variable refers to your target IP that you want to send this data to, in this case, our turtle's IP. The data sends angles in a certain order. The pi will read it in a specific order so if additional limbs are added or removed, the pi's script will need to be updated. 

## NUI Track API Calls

You will notice a bunch of functions that relate to formatting openGL and authorizing sensors. These are essential for the function of the motion tracking. DO NOT remove these and make sure they are called when running the script. These will also read the tracking data and do some trigonometry to find each joints angle. 

## CSV File Reader
**Under Construction**

# GUI
**Under Construction**

## GUI #1
**Under Construction**

## GUI #2
**Under Construction**


# Sevo Controller


**Under Construction**

## Sevo Controller #1


**Under Construction**

## Sevo Controller #2

**Under Construction**


![enter image description here](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT3bE569CgtR00xSlfYP9e3m5ITXL1iM5OWhQ&s)
