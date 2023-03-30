import random as rd
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.ticker as tick

mn=0.05 #mutation rate
ms=0.2 #mutation strenght
n=2
L=100
global maxL
maxL=40000

def make_pop(L,n):
	pop = []
	for i in range(0,L):
		os=[]
		for j in range(0,n):
			os.append(rd.normalvariate(0,1))
			#print('os',os)
		pop.append(os)
		#print('pop',pop)
	print(pop[0],pop[10])
	return pop


def mutacje(pop,n,ms,mn):
	new_pop=[]
	for os in pop:
		if rd.uniform(0,1)<mn:
			#print('mutacja',os)
			wyb=rd.randrange(0,n)
			#print(rd.normalvariate(0,ms))
			os[wyb]=os[wyb]+rd.normalvariate(0,ms)
			#print(wyb,os)
		new_pop.append(os)
	return new_pop
	#print(new_pop)

def fitness(os,opt):
	fn=np.linalg.norm(np.array(os)-np.array(opt))
	#f=1/(1+fn) #prawdopodobieństwo przeżycia i wydania potomstwa wersja 1
	fs=1.2
	f=np.exp(-fn/(2*fs**2))
	#print(f)
	return float(f)

def selekcja(pop,opt):
	alive=[]
	#print('Mamy ',len(pop),' osobników...')
	for os in pop:
		f=fitness(os,opt) #prawdopodobieństwo przeżycia i wydania potomstwa
		#print(f)
		if rd.uniform(0,1)<f:
			#print('p=',p,'fz=',fz)
			alive.append(os)
			#print('przeżył')
		if len(alive)>maxL:
			zgon_id=rd.sample(range(0,len(alive)-1),len(alive)-maxL)
			zgon_id.sort(reverse=True)
			#print(zgon_id)
			for d in zgon_id:
				#print(d)
				alive.remove(alive[d])
	print('Żyje ',len(alive),' osobników!')
	return alive

def rozmnażanie(pop,n,opt):
	new_os=[]
	for os in pop:
			#dzieci=int(rd.randrange(1,5)*fitness(os,opt)) #ile dzieci ma osobnik
			#dzieci=int(fitness(os,opt)*3)
			dzieci=int(fitness(os,opt)*2.5)
			#print('ile dzieci ',dzieci)
			if dzieci>0:
				for i in range(0, int(dzieci)):
					new_os.append(os) #kopia rodzica
	return new_os

def ruch_opt(opt):
	new_opt=[]
	#globalne ocieplenie
	zmiana1=0.1
	zmiana2=0
	new_opt.append(opt[0]+zmiana1)
	new_opt.append(opt[1]+zmiana2)
	#if rd.normalvariate(0,1)>0.5:
	#	wyb=rd.randrange(0,n)
	#	opt[wyb]=opt[wyb]+rd.normalvariate(0,1)
	return new_opt

def pokolenie(pop,opt,n,ms,mn):
	pop=mutacje(pop,n,ms,mn) #wstawia mutacje nie zmienia liczby osobnikó
	pop=selekcja(pop,opt) #daje osobniki które przeżyły
	#pop=pop+rozmnażanie(pop,n,opt) #lista z nowymi i starymi osobnikami
	pop=rozmnażanie(pop,n,opt) #lista nowych osobników
	opt1=ruch_opt(opt)
	return pop,opt1

def i_pokolenia(pop,opt,n,ms,mn,i):
	historia=[]
	optima=[]
	historia.append(pop)
	opt1=opt
	for j in range(0,i):
		pop,opt1=pokolenie(pop,opt1,n,ms,mn)
		historia.append(pop)
		optima.append(opt1)
	return historia,optima

def średnia_cechy(historia,n):
	średnie=[]
	for i in range(0,n):
		średnia_pok=[]
		for pok in historia:
			suma=0
			for os in pok:
				suma=suma+os[i]
			if len(pok)>0:
				średnia_pok.append(suma/len(pok))
			else:
				średnia_pok.append(0)
		średnie.append(średnia_pok)
	return średnie


pop=make_pop(L,n)
print('START',len(pop), 'osobników')

i=50
opt=[0,0]
historia,optimum = i_pokolenia(pop,opt,n,ms,mn,i)
#print(optimum)
średnie=średnia_cechy(historia,n)

global pop_list
pop_list=[]
pop_list.append(pop)

fig = plt.figure(figsize=(8,6))

axes = fig.add_subplot()
axes.set_ylim(-10,10)
axes.set_xlim(-10,10)

populacja, = axes.plot([], [], 'o', color = 'black', markersize=2)
optimum_plot, = axes.plot([], [], 'o', color='green', markersize=5)
text = axes.text(0.5, 0.9, '', transform=axes.transAxes, va='top', ha='center')

print(populacja)

def animate_pop(i):
	#print(i)
	populacja.set_data([os[0] for os in historia[i]], [os[1] for os in historia[i]])
	optimum_plot.set_data([optimum[i][0]], [optimum[i][1]])
	text.set_text(f'Pokolenie {i}')
	
	return populacja, optimum_plot

anim = FuncAnimation(fig, animate_pop, frames = i, repeat=True, interval=50)
#anim.save(r'C:\Users\zosai\Desktop\BS\15_anim.gif', writer="imagemagick")
plt.show()

plt.plot(średnie[0],label='cecha 1')
plt.plot(średnie[1],label='cecha 2')
plt.plot(optimum,label=['optimum cecha 1','optimum cecha 2'])
plt.legend()
plt.xlabel('Pokolenie')
plt.ylabel('Średnia wartość cechy')
#plt.savefig(r'C:\Users\zosai\Desktop\BS\3.png')
plt.show()

liczebność=[]
for pok in historia:
	liczebność.append(len(pok))
plt.plot(liczebność,label='liczebność')
plt.legend()
plt.xlabel('Pokolenie')
plt.ylabel('Liczba osobników')
#plt.savefig(r'C:\Users\zosai\Desktop\BS\3.png')
plt.show()