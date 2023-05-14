from mininet.topo import Topo

class MyFirstTopo( Topo ):
    "High-level API topology example."
    def __init__( self ):
        "Create custom topo."
        # Initialize topology
        Topo.__init__( self )

        #Add one core switch
        coreSwitch = self.addSwitch('c1')

        # Obtain n from the user
        n = int(input("Enter the value of n: "))

        # Add n aggregation switches
        index = 0
        aggSwitches = []
        while (index < n):
            aggSwitches.append(self.addSwitch('a' + str(index + 1)))
            index = index + 1

        # Add n^2 edge switches
        index = 0
        edgeSwitches = []
        while (index < (n**2)):
            edgeSwitches.append(self.addSwitch('e' + str(index + 1)))
            index = index + 1

        # Add n^3 hosts
        index = 0
        hosts = []
        while (index < (n**3)):
            hosts.append(self.addHost('h' + str(index + 1)))
            index = index + 1
        
        # Add links from core switch to the n aggregation switches
        index = 0
        while (index < n):
            self.addLink(coreSwitch, aggSwitches[index])
            index = index + 1

        # Add links from the n aggregation switches to the n^2 edge switches
        index = 0
        while (index < n):
            j = 0
            while (j < n):
                self.addLink(aggSwitches[index], edgeSwitches[(index * n) + j])
                j = j + 1
            index = index + 1
            
        # Add links from the n^2 aggregation switches to the n^3 hosts
        index = 0
        while (index < (n**2)):
            j = 0
            while (j < n):
                self.addLink(edgeSwitches[index], hosts[(index * n) + j])
                j = j + 1
            index = index + 1

topos = { 'myfirsttopo': ( lambda: MyFirstTopo() ) }