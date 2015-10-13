#!usr/bin/env python
import os
import time
import subprocess
import getpass
import sys
import tkMessageBox
from Tkinter import *
Tk().withdraw()

root = Tk()
root.wm_title("Select Your Device")
listbox = Listbox(root)
global p
def scan():
	global name
	quality =0
	signal =0
	global spot
	global again
	global unlock
	os.system('sudo /home/randi/Desktop/wlanup.sh')
	pro = subprocess.Popen( ['sudo /home/randi/Desktop/wlan0.sh'], stdout=subprocess.PIPE,shell = True ).communicate()[0]
	#subprocess.Popen( ['xdotool key Return'], stdout=subprocess.PIPE,shell = True ).communicate()[0]
	#os.system('xdotool key Return')
	words = []
	words = pro.split()
	if len(words)==0:
		os.system('sudo /home/randi/Desktop/wlanup.sh')
		pro = subprocess.Popen( ['sudo /home/randi/Desktop/wlan0.sh'], stdout=subprocess.PIPE,shell = True ).communicate()[0]
		Lock = subprocess.Popen(['gnome-screensaver-command -q'], stdout = subprocess.PIPE, shell = True).communicate()[0]
		words = Lock.split()
		if words[3]=='inactive':
			if unlock==0:
				subprocess.Popen( ['xdotool search --name "~/Desktop/wifi" windowactivate %@ && xdotool key Return && xdotool search --name "/Desktop/wifi" windowminimize %@'], stdout=subprocess.PIPE,shell = True ).communicate()[0]
		words = []
		words = pro.split()
	for l in range(len(words)):
		if words[l] == name:
			spot = 1
			sig = words[l-4].split('=')
			signal =(-float(sig[1]))
			qua =words[l-6].split('=')
			qua = qua[1].split('/')
			quality = int(qua[0])
	return quality,signal
def Start_Tracking():
	global name
	global p
	o = 'gnome-screensaver-command -d && xdotool type password && xdotool key Return'
	open_lock=o.replace('password',p)
	#name = 'ESSID:"Batmen-1"'
	i = 0
	global spot
	spot = 0
	global again
	again = 0
	global unlock
	unlock =0
	os.system('sudo /home/randi/Desktop/wlanup.sh')
	

	pro = subprocess.Popen( ['sudo /home/randi/Desktop/wlan0.sh'], stdout=subprocess.PIPE,shell = True ).communicate()[0]
	Lock = subprocess.Popen(['gnome-screensaver-command -q'], stdout = subprocess.PIPE, shell = True).communicate()[0]
	words = Lock.split()
	if words[3]=='inactive':
		if unlock==0:
			subprocess.Popen( ['xdotool search --name "~/Desktop/wifi" windowactivate %@ && xdotool key Return && xdotool search --name "/Desktop/wifi" windowminimize %@'], stdout=subprocess.PIPE,shell = True ).communicate()[0]
	while i<1:
		qual, sig = scan()
		if (qual>0 and sig>0):
			tkMessageBox.showinfo('Batmen','Your phone has been spotted')
			spot = 1
		if spot ==0:
			tkMessageBox.showwarning('Batmen','Phone not spotted, start your hotspot and try again.')
			
			os.system("pkill -f pro2.py")
			break
		i = i + 1
	print 'Tracking your phone..'
	s = 0
	while 1:
		spot = 0
		quality, signal = scan()
		if spot == 0:
			if s ==0:
				print 'Phone signal lost, or out of coverage start your hotspot and try again.'
				again = again + 1

				s = 1

		else:
			s=0
			if again == 1:
				print"Phone spotted again.."
				again = 0

			if signal>=78 and quality<=32:
				os.system('sudo /home/randi/Desktop/wlanup.sh')
				quality2, sig2 = scan()
				if sig2>=80 and quality2<=30:
					quality3, sig3 = scan()
					if sig3>=80 and quality3<=30:
						os.system('sudo /home/randi/Desktop/wlanup.sh')
						subprocess.Popen(['gnome-screensaver-command -l'], stdout = subprocess.PIPE, shell = True).communicate()[0]
						if unlock == 0:
							print ('Locking your laptop..')
							unlock = 1
			if signal<=60 and quality>40:
				os.system('sudo /home/randi/Desktop/wlanup.sh')
				unlock = 0
				Lock = subprocess.Popen(['gnome-screensaver-command -q'], stdout = subprocess.PIPE, shell = True).communicate()[0]
				words = Lock.split()
				if words[3]=='active':
					print ('Unlocking your laptop..')
					subprocess.Popen([open_lock], stdout = subprocess.PIPE, shell = True).communicate()[0]
					unlock = 0
def endit():
	global name
	global p
	values = [listbox.get(idx) for idx in listbox.curselection()]
	name ='ESSID:' + ', '.join(values)
	print 'Selected device:', name
	p = widget.get()
	root.destroy()
	Start_Tracking()
def refresh():
	pro = subprocess.Popen( ['sudo /home/randi/Desktop/wlan0.sh'], stdout=subprocess.PIPE,shell = True ).communicate()[0]
	Wor2 = []
	Wor2 = pro.split()
	listbox.delete(0, END)
	for I in range(len(Wor2)):
		w = Wor2[I].split(':')
		if w[0]== 'ESSID':
			listbox.insert(END, w[1])

listbox.pack()
Label(root, text="Password: ").pack(side=LEFT)
widget = Entry(root, show="*", width=15)
widget.pack(side = LEFT)
b = Button(root, text="Confirm", command=endit)
b.pack(side = BOTTOM)
b = Button(root, text="Refresh", command=refresh)
b.pack(side = BOTTOM)


pro = subprocess.Popen( ['sudo /home/randi/Desktop/wlan0.sh'], stdout=subprocess.PIPE,shell = True ).communicate()[0]
Wor = []
Wor = pro.split()
for I in range(len(Wor)):
	w = Wor[I].split(':')
	if w[0]== 'ESSID':
		listbox.insert(END, w[1])

root.mainloop()

#p=getpass.getpass(prompt = 'Enter your lock-screen password: ')
