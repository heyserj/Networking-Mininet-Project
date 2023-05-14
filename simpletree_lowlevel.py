#!/usr/bin/python

from mininet.node import Host, OVSSwitch, Controller
from mininet.link import Link

#Add one controller
controller = Controller( 'c0', inNamespace=False )

#Add one core switch
coreSwitch = OVSSwitch('c1', inNamespace=False )

# Obtain n from the user
n = int(input("Enter the value of n: "))

# Add n aggregation switches
index = 0
aggSwitches = []
while (index < n):
    aggSwitches.append(OVSSwitch('a' + str(index + 1), inNamespace=False ))
    index = index + 1

# Add n^2 edge switches
index = 0
edgeSwitches = []
while (index < (n**2)):
    edgeSwitches.append(OVSSwitch('e' + str(index + 1), inNamespace=False ))
    index = index + 1

# Add n^3 hosts
index = 0
hosts = []
while (index < (n**3)):
    hosts.append(Host('h' + str(index + 1)))
    index = index + 1
        
# Add links from core switch to the n aggregation switches
index = 0
while (index < n):
    Link(coreSwitch, aggSwitches[index])
    index = index + 1

# Add links from the n aggregation switches to the n^2 edge switches
index = 0
while (index < n):
    j = 0
    while (j < n):
        Link(aggSwitches[index], edgeSwitches[(index * n) + j])
        j = j + 1
    index = index + 1
            
# Add links from the n^2 aggregation switches to the n^3 hosts
index = 0
while (index < (n**2)):
    j = 0
    while (j < n):
        Link(edgeSwitches[index], hosts[(index * n) + j])
        j = j + 1
    index = index + 1

# Add IP addresses to the n^3 hosts
index = 0
while (index < (n**3)):
    hosts[index].setIP('10.0.0.' + str(index + 1) + '/24')
    index = index + 1

#Start the controller
controller.start()

#Start the core switch
coreSwitch.start([controller])

#Start the aggregation switches
index = 0
while (index < n):
    aggSwitches[index].start([controller])
    index = index + 1

#Start the edge switches
index = 0
while (index < (n**2)):
    edgeSwitches[index].start([controller])
    index = index + 1

#Ping all hosts from h1
print ('Pinging ...')
index = 1
while (index < (n**3)):
    print (hosts[0].cmd( 'ping -c3 ', hosts[index].IP() ))
    index = index + 1

#Stop the edge switches
index = 0
while (index < (n**2)):
    edgeSwitches[index].stop()
    index = index + 1

#Stop the aggregation switches
index = 0
while (index < n):
    aggSwitches[index].stop()
    index = index + 1

#Stop the core switch
coreSwitch.stop()

#Stop the controller
controller.stop()
