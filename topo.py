from mininet.topo import Topo

class FiveSwitchTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')

        for i in range(1, 3):
            h = self.addHost(f'h{i}')
            self.addLink(h, s1)

        for i in range(3, 5):
            h = self.addHost(f'h{i}')
            self.addLink(h, s2)

        for i in range(5, 7):
            h = self.addHost(f'h{i}')
            self.addLink(h, s3)

        for i in range(7, 9):
            h = self.addHost(f'h{i}')
            self.addLink(h, s4)

        for i in range(9, 11):
            h = self.addHost(f'h{i}')
            self.addLink(h, s5)

        self.addLink(s1, s2)
        self.addLink(s2, s3)
        self.addLink(s3, s4)
        self.addLink(s4, s5)

topos = {'fiveswitchtopo': (lambda: FiveSwitchTopo())}
