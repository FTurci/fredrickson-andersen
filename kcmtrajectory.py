from FredricksonAndersen import FA1d
import pickle
import tqdm
import numpy as np
import copy
#from joblib import Parallel, delayed


class KCMtrajectory(object):
  """docstring for KCMtrajectory"""
  def __init__(self, model,tobs):
    super(KCMtrajectory, self).__init__()
    self.model = model
    self.tobs = tobs
    self.kymograph = np.zeros((tobs,len(model.get())))

  def spawn(self):
    for i in range(tobs):
      self.kymograph[i]=self.model.get()
      model.fw_run(1)
    self.excitations = self.kymograph.sum()

  def excitation_density(self):
    return self.excitations/np.prod(self.kymograph.shape) 
    

class KCMtps(object):
  """docstring for KCMtps"""
  def __init__(self, trajectory,mcsteps):
    super(KCMtps, self).__init__()
    self.trajectory = trajectory
    self.mcsteps = mcsteps
    self.length = trajectory.kymograph.shape[1]
    self.tobs = trajectory.kymograph.shape[0]


  def fw_shoot(self):
    r = np.random.randint(self.tobs)
    #new trajectory
    trajcopy = copy.copy(self.trajectory)
    trajcopy.model.set(trajcopy.kymograph[r])
    for i in range(r+1,self.tobs):
      trajcopy[i] = trajcopy.model.fw_run(1) 
    self.trajectory = trajcopy

  def bw_shoot(self):
    r = np.random.randint(self.tobs)
    #new trajectory
    trajcopy = copy.copy(self.trajectory)
    trajcopy.model.set(trajcopy.kymograph[r])
    for i in range(r-1,0, -1):
      trajcopy[i] = trajcopy.model.bw_run(1) 
    self.trajectory = trajcopy

  def fw_shift(self):
    pass
  def bw_shift(self):
    pass

  

N = 10
L = N
tobs=320
ntrajectories = 1000
model = FA1d(N,1.0)
model.set_density(model.theoretical_density())
# #fout = open("kymo.txt", 'w')
# # equilibrate
model.fw_run(10*tobs)
X =KCMtrajectory(model, tobs)
X.spawn()
# model.load("equilibrated.txt")
# values= []
# for i in tqdm.tqdm(range(ntrajectories)):
#   model.fw_run(tobs, integrate_excitations=True)
#   values.append(model.time_integrated_excitations/float(N*L*tobs))


# pickle.dump(values,open("values.p",'w'))

# import pylab as pl

# pl.hist(values,bins=30)
# pl.show()
  #model.fw_run(1)
  #model.write(fout)
