#!/usr/bin/env python
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import re
import inspect
from scipy.interpolate import RegularGridInterpolator

class SignedDistanceField:

    def __init__(self, sdffile):

        with open(sdffile) as f:
            lines = f.readlines()

        Nxyz = map(lambda str: int(str), re.sub('\n', '', lines[0]).split())
        bmin = map(lambda str: float(str), re.sub('\n', '', lines[1]).split())
        print Nxyz

        dx = float(re.sub('\n', '', lines[2]))

        data_raw = map(lambda str: float(re.sub('\n', '', str)), lines[3:])
        Nx = Nxyz[0]
        Ny = Nxyz[1]
        Nz = Nxyz[2]

        data_ = np.zeros([Nx, Ny, Nz], dtype=float)
        for k in range(Nz):
            for j in range(Ny):
                for i in range(Nx):
                    idx = i + j*Nx + k*Nx*Ny
                    data_[i, j, k] = data_raw[idx]
        data = np.array(data_)
        xlin = [bmin[0]+dx*i for i in range(Nx)]
        ylin = [bmin[1]+dx*i for i in range(Ny)]
        zlin = [bmin[2]+dx*i for i in range(Nz)]
        itp = RegularGridInterpolator((xlin, ylin, zlin), data)

        self.data = data
        self.bmin = bmin
        self.Nxyz = Nxyz
        self.dx = dx
        self.itp = itp

    def compute_sd(self, p):
        return self.itp(p)


    def show(self):
        Nxyz = self.Nxyz
        Nx = Nxyz[0]
        Ny = Nxyz[1]
        Nz = Nxyz[2]
        xlin = [self.bmin[0]+self.dx*i for i in range(Nx)]
        ylin = [self.bmin[1]+self.dx*i for i in range(Ny)]
        zlin = [self.bmin[2]+self.dx*i for i in range(Nz)]
        A, B = np.meshgrid(ylin, xlin) 
        plt.pcolor(A, B, self.data[:, :, 13])
        plt.colorbar()
        plt.show()

sdf = SignedDistanceField("./sdffiles/gripper_palm.sdf")

print sdf.compute_sd([0.03, -0.045, sdf.bmin[2]+sdf.dx*13])
sdf.show()





