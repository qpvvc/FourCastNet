#BSD 3-Clause License
#
#Copyright (c) 2022, FourCastNet authors
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
#3. Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
#FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The code was authored by the following people:
#
#Jaideep Pathak - NVIDIA Corporation
#Shashank Subramanian - NERSC, Lawrence Berkeley National Laboratory
#Peter Harrington - NERSC, Lawrence Berkeley National Laboratory
#Sanjeev Raja - NERSC, Lawrence Berkeley National Laboratory 
#Ashesh Chattopadhyay - Rice University 
#Morteza Mardani - NVIDIA Corporation 
#Thorsten Kurth - NVIDIA Corporation 
#David Hall - NVIDIA Corporation 
#Zongyi Li - California Institute of Technology, NVIDIA Corporation 
#Kamyar Azizzadenesheli - Purdue University 
#Pedram Hassanzadeh - Rice University 
#Karthik Kashinath - NVIDIA Corporation 
#Animashree Anandkumar - California Institute of Technology, NVIDIA Corporation


# Instructions: 
# Set Nimgtot correctly

import h5py
from mpi4py import MPI
import numpy as np
import time
from netCDF4 import Dataset as DS
import os

def writetofile(src, dest, channel_idx, varslist, src_idx=0, frmt='nc'):
    if os.path.isfile(src):
        batch = 2**4
        rank = MPI.COMM_WORLD.rank
        Nproc = MPI.COMM_WORLD.size
        Nimgtot = 1460#src_shape[0]

        Nimg = Nimgtot//Nproc
        base = rank*Nimg
        end = (rank+1)*Nimg if rank<Nproc - 1 else Nimgtot
        idx = base

        for variable_name in varslist:

            if frmt == 'nc':
                fsrc = DS(src, 'r', format="NETCDF4").variables[variable_name]
            elif frmt == 'h5':
                fsrc = h5py.File(src, 'r')[varslist[0]]
            print("fsrc shape", fsrc.shape)
            fdest = h5py.File(dest, 'a', driver='mpio', comm=MPI.COMM_WORLD)
            
            #cdj 检查并创建 'fields' 数据集
            if 'fields' not in fdest:
                if len(fsrc.shape) == 4:
                    maxshape = (None, fsrc.shape[1], fsrc.shape[2], fsrc.shape[3])
                else:
                    maxshape = (None, fsrc.shape[1], fsrc.shape[2])
                fdest.create_dataset('fields', shape=(0,) + fsrc.shape[1:], maxshape=maxshape, dtype=fsrc.dtype)
            
            start = time.time()
            while idx<end:
                if end - idx < batch:
                    if len(fsrc.shape) == 4:
                        ims = fsrc[idx:end,src_idx]
                    else:
                        ims = fsrc[idx:end]
                    print(ims.shape)
                    fdest['fields'].resize((end,) + fsrc.shape[1:]) #cdj
                    fdest['fields'][idx:end, channel_idx, :, :] = ims
                    break
                else:
                    if len(fsrc.shape) == 4:
                        ims = fsrc[idx:idx+batch,src_idx]
                    else:
                        ims = fsrc[idx:idx+batch]
                    #ims = fsrc[idx:idx+batch]
                    print("ims shape", ims.shape)
                    fdest['fields'].resize((idx+batch,) + fsrc.shape[1:])       #cdj             
                    fdest['fields'][idx:idx+batch, channel_idx, :, :] = ims
                    idx+=batch
                    ttot = time.time() - start
                    eta = (end - base)/((idx - base)/ttot)
                    hrs = eta//3600
                    mins = (eta - 3600*hrs)//60
                    secs = (eta - 3600*hrs - 60*mins)

            ttot = time.time() - start
            hrs = ttot//3600
            mins = (ttot - 3600*hrs)//60
            secs = (ttot - 3600*hrs - 60*mins)
            channel_idx += 1 
            
filestr = '2015'
dest = f'/datasets/FourCastNet/wave_5var_6h/{filestr}.h5'
src = f'/datasets/FourCastNet/wave_5var_6h/{filestr}.nc'
#
writetofile(src, dest, 0, ['u10n'])
writetofile(src, dest, 1, ['v10n'])
writetofile(src, dest, 2, ['msl'])
writetofile(src, dest, 3, ['swh'])
writetofile(src, dest, 4, ['pp1d'])




