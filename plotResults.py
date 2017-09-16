#!/usr/bin/env python

#    This file is a part of the package "Weber's Law".
#
#    Copyright (C) 2017 Spandan Mondal
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
#    Contact: mondalspandan@gmail.com, spandanm@ug.iisc.in, spandanm.webs.com


from __future__ import print_function
import sys, os
try:
    import matplotlib.pyplot as plt
except ImportError:
    print("A required Python module, Matplotlib, could not be imported. Please follow the Installation Notes in README.md and install Matplotlib before running this program.")
    sys.exit()
    
filelist = [i for i in os.listdir('.') if i.startswith("Result_")]
    
for ind in range(len(filelist)):
    print(str(ind+1)+". "+filelist[ind])

ans=""
while ans.lower() not in [str(i+1) for i in range(len(filelist))]:
	ans=raw_input("Which file? ("+''.join(str(i+1)+"/" for i in range(len(filelist)))[:-1]+"): ")
	if ans not in [str(i+1) for i in range(len(filelist))]:
		print ("Unrecognized input. ",end='')

inpfile=filelist[int(ans)-1]

print("\nReading file",inpfile)
inp=open(inpfile,"r")
y=[]
t=[]
I=[]
delI=[]
delIerr=[]
for line in inp:
    if not line.startswith("Round") and line!='\n':
        y.append([float(i) for i in line.split()[-1][1:-1].split(',')])  
        t.append(float(line.split()[1]))
        delI.append(float(line.split()[4]))
        delIerr.append(float(line.split()[5]))
        
inp.close()

cols=['red','blue','green','black']

def plotk():
    x=[]
    for ind in range(len(y)):
        y[ind]=[i/t[ind] for i in y[ind]]
        x.append([i+1 for i in range(len(y[ind]))])
        plt.plot(x[ind],y[ind],cols[ind],label=str(round(t[ind],1))+" sec")
        plt.legend()
        
def plotdelI():
    plt.errorbar(t,delI,fmt='o',yerr=delIerr)
    plt.xlim([0,2.5])

print("\n1. Plot of del(I)/I as a function of number of trials\n2. Plot of del(I) as a function of I")
ans=""
while ans not in ["1","2"]:
	ans=raw_input("Which plot? (1/2): ")
	if ans not in ["1","2"]:
		print ("Unrecognized input. ",end='')
		
if ans=="1":
    plotk()
else:
    plotdelI()

print("\nDisplaying plot...")
plt.show()
