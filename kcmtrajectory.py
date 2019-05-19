from __future__ import print_function
from FredricksonAndersen import FA1d
import pickle
import tqdm
import numpy as np
import copy
import pylab as pl
#from joblib import Parallel, delayed


class KCMtrajectory(object):
  """docstring for KCMtrajectory"""
  def __init__(self, model,tobs):
    super(KCMtrajectory, self).__init__()
    self.model = model
    self.tobs = tobs
    self.kymograph = np.zeros((tobs,len(model.get())))
    self.constraints = np.zeros((tobs,len(model.get())))

  def spawn(self):
    for i in range(tobs):
      self.kymograph[i]=self.model.get()
      self.constraints[i] = self.model.constraint
      model.fw_run(1)
    

  def excitation_density(self):
    return self.excitations()/np.prod(self.kymograph.shape) 
  def excitations(self): 
    return self.kymograph.sum()

class KCMtps(object):
  """docstring for KCMtps"""
  def __init__(self, trajectory, field,log=False):
    super(KCMtps, self).__init__()
    self.trajectory = trajectory
    self.field=field    
    #self.mcsteps = mcsteps
    self.length = trajectory.kymograph.shape[1]
    self.tobs = trajectory.kymograph.shape[0]
    self.log = log

  def fw_shoot(self,margin=2):
    r = np.random.randint(margin,self.tobs-margin)
    if self.log:
      print ("forward",r) 
    #new trajectory
    trajcopy = copy.deepcopy(self.trajectory)
    trajcopy.model.set(trajcopy.kymograph[r])

    for i in range(r+1,self.tobs):
      trajcopy.model.fw_run(1)
      # print (i)
      trajcopy.kymograph[i] =  trajcopy.model.get()

    #self.trajectory = trajcopy
    return trajcopy

  def bw_shoot(self,margin=2):
    r = np.random.randint(margin,self.tobs-margin)
    if self.log:
      print ("backward",r)
    #new trajectory
    trajcopy = copy.deepcopy(self.trajectory)
    trajcopy.model.set(trajcopy.kymograph[r])
    for i in range(r-1,0, -1):
      trajcopy.model.bw_run(1) 
      trajcopy.kymograph[i] = trajcopy.model.get()
    
    return trajcopy
    #self.trajectory = trajcopy

  def fw_shift(self):
    pass
  def bw_shift(self):
    pass

  def metropolis(self):
    if np.random.uniform()<0.5:
      attempt = self.fw_shoot()
    else:
      attempt = self.bw_shoot()
    r = np.random.uniform()
    
   
    if r <np.exp(-self.field*attempt.excitations()):
      self.trajectory = attempt
      
      

N = 30
L = N
tobs=320
ntrajectories = 1000
mcsteps = 100000
model = FA1d(N,1.0)
model.set_density(model.theoretical_density())
# #fout = open("kymo.txt", 'w')
# # equilibrate
# model.fw_run(10*tobs)
# create the first trajectory
X =KCMtrajectory(model, tobs)
X.spawn()

# pl.imshow(X.kymograph)
# pl.figure()
# pl.imshow(X.constraints, cmap=pl.cm.Paired)
# pl.show()
TPS = KCMtps(X, 0.0001,log= False)

values=[]
#for i in tqdm.tqdm(range(mcsteps)):
for i in range(mcsteps):
  TPS.metropolis()
  values.append(TPS.trajectory.excitation_density())
  print (i, np.mean(values))
#pl.imshow(TPS.trajectory.kymograph)

#TPS.bw_shoot()
#pl.figure()
#pl.imshow(TPS.trajectory.kymograph)#cmap=pl.cm.Paired)
#pl.show()


