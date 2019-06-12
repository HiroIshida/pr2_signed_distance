#!/usr/bin/env python
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
import re
# execfile("plotter.py")

"""
filename = "./tmp.json"
f = open(filename, 'r')
chunk_json = json.load(f)
data = np.array(chunk_json["data"])
Nxyz = data.shape
"""
class SignedDistanceField:

    def __init__(self, sdffile):

        with open(sdffile) as f:
            lines = f.readlines()

        Nxyz = map(lambda str: int(str), re.sub('\n', '', lines[0]).split())
        bmin = map(lambda str: float(str), re.sub('\n', '', lines[1]).split())
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
        self.data = np.array(data_)
        self.Nxyz = Nxyz
        self.dx = dx

    def show(self):
        xlin = [bmin[0]+dx*i for i in range(Nx)]
        ylin = [bmin[1]+dx*i for i in range(Ny)]
        zlin = [bmin[2]+dx*i for i in range(Nz)]
        A, B = np.meshgrid(zlin, ylin) 
        plt.pcolor(A, B, data[10, :, :])
        plt.show()

sdf = SignedDistanceField("./sdffiles/l_finger.sdf")




