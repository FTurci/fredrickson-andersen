from FredricksonAndersen import FA1d
import pickle
import tqdm
#from joblib import Parallel, delayed


N = 180
L = N
tobs=320
ntrajectories = 1000
model = FA1d(N,1.0)
#model.set_density(model.theoretical_density())
#fout = open("kymo.txt", 'w')
# equilibrate
#model.fw_run(10*tobs)
model.load("equilibrated.txt")


values= []
for i in tqdm.tqdm(range(ntrajectories)):
  model.fw_run(tobs, integrate_excitations=True)
  values.append(model.time_integrated_excitations/float(N*L*tobs))


pickle.dump(values,open("values.p",'w'))

import pylab as pl

pl.hist(values,bins=30)
  #model.fw_run(1)
  #model.write(fout)
