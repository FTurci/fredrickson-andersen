from __future__ import print_function
import numpy as np
#from numba import jit
import sys

np.random.seed(0)

class FA1d(object):
  def __init__(self,N,T):
    super(FA1d, self).__init__()
    self.N = N
    self.T = T
    self.beta = 1./T
    self.lattice = np.zeros(N)
    self.lattice[0]=1
    self.facilitation()
    self.boltzmann = np.exp(-self.beta)
    self.time_integrated_excitations = 0.0
    
  def set(self,conf):
    self.lattice = conf
  def get(self):
    return self.lattice
    
  def load(self,filename, snapshot= -1):
    """Loadsystem's state from file"""
    print ("Loading",filename)
    table = np.loadtxt(filename)
    assert table.shape[1] == self.N
    self.lattice= table[snapshot] 
    self.facilitation()

  def at(self,value):
    return value%self.N
  
  def fw_probabilitiy(self,site):
    if self.lattice[site]==0:
      return self.constraint[site]*self.boltzmann
    else:
      return self.constraint[site]
  
  def bw_probabilitiy(self,site):
    if self.lattice[site]==1:
      return self.constraint[site]*self.boltzmann
    else:
      return self.constraint[site]
  

  def flip(self, site):
    self.lattice[site] = 0 if self.lattice[site] else 1
    
    if self.lattice[site]==1:
      self.constraint[self.at(site-1)] = 1
      self.constraint[self.at(site+1)]= 1
    else:
      for i in [-1,0,1]:
        idx = self.at(site+i)
        idm1 = self.lattice[self.at(idx-1)]
        idp1 = self.lattice[self.at(idx+1)]
        self.constraint[idx] =idp1+idm1-idm1*idp1

  def facilitation(self):
    np1=np.roll(self.lattice,-1)
    nm1=np.roll(self.lattice,1)
    self.constraint = np1+nm1-np1*nm1
  

  #@jit(nopython=False)
  def fw_run(self,nsweeps, integrate_excitations=False):
    for i in range(nsweeps):
      for p in range(self.N):
        #pick a site
        s = np.random.randint(self.N)
        pb = self.fw_probabilitiy(s)
        #print(s,pb, self.lattice[s])
        if np.random.uniform() < pb:
          self.flip(s)
        if integrate_excitations:
          self.time_integrated_excitations += self.lattice.sum()
  
  def bw_run(self,nsweeps):
    for i in range(nsweeps):
      for p in range(self.N):
        #pick a site
        s = np.random.randint(self.N)
        pb = self.bw_probabilitiy(s)
        print(s,pb, self.lattice[s])
        if np.random.uniform() < pb:
          self.flip(s)

  def status(self,constraints=False):
    print ("sites ")
    print(self.lattice.astype(int))
    if constraints:
      print(self.constraint.astype(int))
    print ("\n")

  def write(self, fhd):
    for p in self.lattice:
      fhd.write("%d "%p)
    fhd.write("\n")

  def set_density(self, value):
    nflips =int(value*self.N)
    self.lattice[:nflips]=1
    np.random.shuffle(self.lattice)

  def density(self):
    return np.sum(self.lattice)/self.N
  def theoretical_density(self):
    return 1./(1+1./self.boltzmann)
  def compare_density(self):
    print("Observation %.2f Theory %.2f"%(self.density(), 1./(1+1./self.boltzmann)))

#model = FA1d(180,1.0)
#model.set_density(model.theoretical_density())
#fout = open("kymo.txt", 'w')
#for i in range(int(sys.argv[1])):
  #model.status()
  #model.compare_density()
  #model.fw_run(1)

  #model.write(fout)

