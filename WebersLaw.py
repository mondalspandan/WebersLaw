#!/usr/bin/env python

#    Weber's Law
#
#    A python-based software to test Weber's Law of just noticeable
#    difference in the context of speeds of objects on a computer screen.
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
import sys
try:
    import progressbar,datetime, numpy as np
    from time import sleep
    from random import randint
except ImportError:
    print("One or more required Python modules could not be imported. Please follow the Installation Notes in README.md to install the required modules before running this program.")
    sys.exit()

DevMode=False
GameMode=False

testrounds=[2,1.5,1,.5]

def rand():
	return randint(0,1)

def starttrial(t1,t2):	
	t1=float(t1)
	t2=float(t2)
	length=100
	ans="r"
	
	while ans.lower()=="r":
		print("Run 1:")
		sleep(0.3)
		bar = progressbar.ProgressBar(maxval=length, \
			widgets=[progressbar.Bar('=', '[', ']'), ' '])
		bar.start()
		for i in xrange(length):
			bar.update(i)
			sleep(t1/length)
		bar.finish()
	
		sleep(0.3)
		print("Run 2:")
		sleep(0.3)
		bar2 = progressbar.ProgressBar(maxval=length, \
			widgets=[progressbar.Bar('=', '[', ']'), ' '])
		bar2.start()
		for i in xrange(length):
			bar.update(i)
			sleep(t2/length)
		bar2.finish()
		
		ans=""
		while ans.lower() not in ["1","2","r"]:
			ans=raw_input("Which run was faster? (1/2/r=repeat): ")
			if ans not in ["1","2","r"]:
				print ("Unrecognized input. ",end='')
	
	return ans
	
def changetest(standard,test,isCorr,step):
	std=float(standard)
	tst=float(test)
	if isCorr:
		if tst>=1.6*std:
			step=.2
		elif tst>=1.3*std:
			step=.1
		elif tst>=1.2*std:
			step=.05
		elif tst>=1.03*std:
			step=.01
		else:
			step=.005
		return test-step*std, step
	else:
		if tst>=1.15*std:
			bias=1
		elif tst>=1.03*std:
			bias=2
		else:
			bias=4
		return test+step*bias*std, step
		
print("\n==============================================================\nWeber's Law  Copyright (C) 2017 Spandan Mondal\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; see LICENSE file for details.\n==============================================================\n")

sleep(.5)

print("\nHello there! This programme is designed to carry out an experiment to test \"Weber's law of just noticeable difference\" in the context of the following task. Your relevant inputs to the programme will be saved in an output file which will be later analyzed as one of the input samples in the study. No personal information is collected over the course of this experiment, and all collected data will be treated as anonymous during analysis.\n\nBy continuing with the programme, you are consenting to the usage the programme's output for the aforementioned study.\n\n- Spandan Mondal\n  IISc, Bangalore\n")
reply=""
while reply.lower() not in ["yes","no"]:
	reply=raw_input("Do you wish to continue? (yes/no): ")
	if reply.lower() not in ["yes","no"]:
		print ("Unrecognized input. ",end='')
	elif reply.lower()=="no":
		print("\nThank you for your interest. Have a nice day! :)\n")
		sys.exit()

if DevMode and GameMode:
	print("\nWarning: Both Developer and Game modes are on. Turning off Game mode.")
	GameMode=False
step=.2
nrounds=len(testrounds)

print("\n=============\nInstructions:\n=============\nThe experiment consists of",nrounds,"rounds. In each round, you will be presented with a number of trials, in each of which you will be sequentially shown two progressing ASCII progressbars. For each trial, you will have to say which one of the two bars progressed faster. You can enter your answer using the numeric 1 and 2 keys on your keyboard, followed by the Enter/Return key. To repeat a trial, press the R key followed by the Enter key.")

filename='Result_{:%Y%m%d-%H%M%S}.txt'.format(datetime.datetime.now())
out=open(filename,"w")

out.write("Round# Standard dI_min dI_max dI_avg dI_std k_mean dI_Active_Inputs dI_All_Inputs\n\n")

score = 0
for num in range(nrounds):
	standard=testrounds[num]
	test=standard*1.8
	alltrials=[]

	print("\nBeginning Round ",num+1," of ",nrounds,". Press enter to begin.",sep="",end="")
	raw_input("")
	print()
	
	while test>standard:
		if GameMode:
			print("Level ",end="")
		else:
			print("Trial ",end="")
		print(str(len(alltrials)+1)+":")
		rndm=rand()
		if rndm:
			order=[standard,test]
			corr=1
		else:
			order=[test,standard]
			corr=2
		
		isCorr=starttrial(order[0],order[1])==str(corr)
		dI=round(test-standard,3)
		alltrials.append(dI)
		if DevMode:
			print(isCorr,"; This trial was: Standard =",standard,"; Test =",test,"; k =",dI/standard)
			print(alltrials)
		if GameMode:
			if isCorr:
				score+=1
				print("Correct! +1 score. Total score:",score)
			else:
				score-=1
				print("Oops, wrong! -1 score. Total score:",score)
				
		test,step=changetest(standard,test,isCorr,step)
		print()
		if len(alltrials)>=15:
			least=min(alltrials[:-9])
			acttrials=alltrials[-10:]
			if least<=min(acttrials):
				dImin=min(acttrials)
				dImax=max(acttrials)
				dIavg=round(np.mean(acttrials),3)
				dIstd=round(np.std(acttrials,ddof=1),3)
				kmean=round(dIavg/standard,3)
				
				out.write(str(num+1)+" "+str(standard)+" "+str(dImin)+" "+str(dImax)+" "+str(dIavg)+" "+str(dIstd)+" "+str(kmean)+" ["+''.join(str(i)+',' for i in acttrials)[:-1]+"] ["+''.join(str(i)+',' for i in alltrials)[:-1]+"]\n")
				if DevMode:
					print("Standard =",standard,"; dImean =",dIavg,"; dIstd =",dIstd,"; kmean =",kmean)
				if GameMode:
					print("Total score after round ",num+1,": ",score,sep="")
				
				print("End of Round ",num+1," of ",nrounds,". Press enter to continue.",sep="",end="")
				raw_input("")
				break
				
print("\nThank you very much for participating in the study. Have a nice day! :)\n")
out.close()
