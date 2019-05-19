from __future__ import print_function
import numpy as np
#from numba import jit
import sys
import copy
np.random.seed(0)

class FA1d(object):
  """Fredrickson-Andersen 1d kinetically constrained model."""
  def __init__(self,N,T):
    """Initialise the lattice. Parameters:
    N : number of sites
    T : temperature
    """
    super(FA1d, self).__init__()
    self.N = N
    self.T = T
    self.beta = 1./T
    self.lattice = np.zeros(N)
    self.lattice[0]=1
    self.boltzmann = np.exp(-self.beta)
    self.time_integrated_excitations = 0.0
    self.facilitation()
    
  def set(self,conf):
    """Assign a configuration to the lattice."""
    self.lattice = np.copy(conf)
    self.facilitation()

  def get(self):
    """Obtain a lattice configuration."""
    return self.lattice

  def load(self,filename, snapshot= -1):
    """Load system's state from file"""
    print ("Loading",filename)
    table = np.loadtxt(filename)
    assert table.shape[1] == self.N
    self.lattice= table[snapshot] 
    self.facilitation()

  def at(self,value):
    """Consider periodic boundary conditions when computing the lattice site."""
    return value%self.N
  
  def fw_probabilitiy(self,site):
    """Compute the jump probability forward in time."""
    if self.lattice[site]==0:
      """If the spin is 0 and the constraint is satisifed it flips with a Boltzmann probability"""
      return self.constraint[site]*self.boltzmann
    else:
      """If the spin is 1 it flips if the constraint is satisfied"""
      return self.constraint[site]
  
  def bw_probabilitiy(self,site):
    if self.lattice[site]==0:
      return self.constraint[site]*self.boltzmann
    else:
      return self.constraint[site]
  
  @jit(nopython=True)
  def flip(self, site):
    #self.lattice[site] =0 if self.lattice[site]==1 else 1
    #self.facilitation()

    if self.lattice[site]==0:
      self.lattice[site]=1 #flip
      self.constraint[self.at(site+1)]=1
      self.constraint[self.at(site-1)]=1
    else:
      self.lattice[site]=0 #flip
      for i in [-1,0,1]:
        idx = self.at(site+i)
        idm1 = self.lattice[self.at(idx-1)]
        idp1 = self.lattice[self.at(idx+1)]
        self.constraint[idx] =idp1+idm1-idm1*idp1

  def facilitation(self): 
    np1=np.roll(self.lattice,-1)
    nm1=np.roll(self.lattice,1)
    self.constraint = np1+nm1-np1*nm1
  

  @jit(nopython=True)
  def fw_run(self,nsweeps, integrate_excitations=False):
    # print("Forward")
    for i in range(nsweeps):
      for p in range(self.N):
        #pick a site
        s = np.random.randint(self.N)
        pb = self.fw_probabilitiy(s)
        # print(s,pb,self.lattice,self.constraint)
        #print(s,pb, self.lattice[s])
        if np.random.uniform() < pb:
          self.flip(s)
        if integrate_excitations:
          self.time_integrated_excitations += self.lattice.sum()
  
  @jit(nopython=True) 
  def bw_run(self,nsweeps):
    for i in range(nsweeps):
      for p in range(self.N):
        #pick a site
        s = np.random.randint(self.N)
        pb = self.bw_probabilitiy(s)
        # print(s,pb, self.lattice[s])
        if np.random.uniform() < pb:
          self.flip(s)

  @jit(nopython=True)
  def continous_fw():


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
    self.facilitation()

  def density(self):
    return np.sum(self.lattice)/self.N
  def theoretical_density(self):
    return 1./(1+1./self.boltzmann)
  def compare_density(self):
    print("Observation %.2f Theory %.2f"%(self.density(), 1./(1+1./self.boltzmann)))

model = FA1d(10,1.0)

model.set_density(model.theoretical_density())
print (model.lattice)
print (model.constraint)
#fout = open("kymo.txt", 'w')
#for i in range(int(sys.argv[1])):
  #model.status()
  #model.compare_density()
  #model.fw_run(1)

  #model.write(fout)

