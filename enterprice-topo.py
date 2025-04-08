from mininet.topo import Topo

class EnterpriseTopo(Topo):
	def build(self):
		core=self.addSwitch('s1')
		
		dist1=self.addSwitch('s2')
		dist2=self.addSwitch('s3')
		hr=self.addHost('h1')
                sales=self.addHost('h2')
                rnd=self.addHost('h3')
                guest=self.addHost('h4')
                self.addlink(core,dist1)
                self.addlink(core,dist2)
                self.addlink(dist1,hr)
                self.addlink(dist1,sales)
                self.addlink(dist2,rnd)
                self.addlink(dist2,guest)
topos={'enterprise':(lambda: EnterpriseTopo())}
