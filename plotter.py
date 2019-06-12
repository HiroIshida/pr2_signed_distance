#!/usr/bin/env python
from numpy.random import *
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

        Nxyz = np.array(map(lambda str: int(str), re.sub('\n', '', lines[0]).split()))
        bmin = np.array(map(lambda str: float(str), re.sub('\n', '', lines[1]).split()))

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
        self.bmax = bmin + (Nxyz-1)*dx
        self.Nxyz = Nxyz
        self.dx = dx
        self.itp = itp

    def compute_sd(self, p):
        if self.isInsideDefBox(p):
            return self.itp(p)
        else:
            return float('inf')

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

    def isInsideDefBox(self, p):
        for i in range(3):
            if p[i] < self.bmin[i]:
                return False
            if p[i] > self.bmax[i]:
                return False
        return True

class SignedDistanceFieldComposite:
    def __init__(self, sdf_lst, origin_lst):
        self.sdf_lst = sdf_lst
        self.origin_lst = origin_lst

    def compute_sd(self, pts):
        sd_lst = []
        for i in range(len(self.sdf_lst)):
            sdf = self.sdf_lst[i]
            self.sdf_lst[i].compute_sd(map(lambda x: x + self.origin_lst[i], pts))






sdf_palm = SignedDistanceField("./sdffiles/gripper_palm.sdf")
sdf_lfinger = SignedDistanceField("./sdffiles/l_finger.sdf")
#sdfc = SignedDistanceFieldComposite([sdf_palm, sdf_lfinger], [[0, 0, 0], [0.07691, 0.01, 0]])
pts = [np.array([0.03, randn()*0.001, randn()*0.001]) for i in range(1000000)]
print sdf_palm.compute_sd([0, 0, 0])


#sdf.compute_sd(pts)

