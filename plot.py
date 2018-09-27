import pylab as pl
import sys

A = pl.genfromtxt(sys.argv[1], invalid_raise=False, usecols=range(int(sys.argv[2])))

pl.imshow(A)

pl.show()
