#! /usr/bin/env python
# -*- coding: utf-8 -*-

from random import choice	#pour la méthode choice
ordinateur = choice(['O', 'X'])	#l'ordinateur est soit 'X', soit 'O'. 'X' commence toujours.
J = True # joueur initial
T = 3	# taille de grille, fonctionne aussi avec d'autres grilles
H = 60 # taille de cellule
M = [T * [False] for x in range(T)] # toutes cellules initialement libres

def joue(event) :	# handler lié à <Button-1>
	global J
	w = event.widget	# le widget actif
	if M[w.R][w.C] or gagnant(symbole(not J)) :	# cellule déjà occupée
		return
	dessine(w)	#fonction ancillaire
	s = symbole(J)	# joueur symbolique
	M[w.R][w.C] = s	#assigne valeur à la matrice
	J = not J
	if gagnant(s) : info['text'] = 'joueur %s gagne' % s
	else : possibilites()	#si l'humain ne joue pas un coup gagnant, alors l'ordinateur réplique


def dessine(ou) :	#nouvelle fonction qui n'était pas dans le code précédent. Ici on va beaucoup se servir de la création des polygones, donc j'en ai fait une fonction à part entière
	if J : fais_x(ou)	#dépendamment de J, car on ne sait pas si l'ordinateur est plutôt carré ou rond
	else : fais_o(ou)


#ici, on y va au hasard tant que la case n'est pas habité
def coup_aleatoire() : 
	global J
	if False in [x for y in range(len(M)) for x in M[y]] :	#tant qu'il reste des False dans la matrice car sinon la récursion aurait pu être infine car toutes les cases auraient toujours été pleines
		w = choice(choice(Cell))	#au hasard balthazard
		if M[w.R][w.C] : coup_aleatoire()	#on récurse si la case est habitée
		else : 
			dessine(w)	#on dessine sur le widget
			M[w.R][w.C] = symbole(J)	#on met dans la matrice
			J = not J	#on change de joueur

# On regarde aussi si l'ordi peut gagner
def ordinateur_peut_gagner() :
	global J
	s = symbole(J)
	for x in range(T): #on récurse sur toutes les cases de la matrice
		for y in range(T):
			if M[x][y] is False : #si la case est vide
				M[x][y] = s	#on y met le symbole de l'ordi
				if gagnant(s) :	#si c'est gagnant
					dessine(Cell[x][y])	#on le dessine
					info['text'] = 'joueur %s gagne' % s	#on affiche le message de victoire
					J = not J	#on change le joueur (nécessaire pour ne pas qu'on puisse continuer de jouer après le jeu, voir la condition dans joue())
					return True	#on sort avec une valeur vraie pour que possibilites() s'arrête.
				else : 
					M[x][y] = False	#sinon on remet la case de la matrice à faux
	return False	#si on est pas sorti avant de la fonction, celle-ci retourne faux pour que possibilites() continue

#on regarde si l'humain peut gagner

def empecher_humain_de_gagner() :
	global J
	s = symbole(J)
	for x in range(T):	#on récurse sur toutes les cases de la matrice
		for y in range(T):
			if M[x][y] is False : #si la case est vide
				M[x][y] = symbole(not J)	#on y met le symbole de l'humain
				if gagnant(symbole(not J)) :	#si c'est gagnant
					dessine(Cell[x][y])	#on le dessine
					M[x][y] = s	#on met la case de la matrice au symbole de l'ordi
					J = not J	#on change le joueur
					return True	#on sort avec une valeur vraie pour que possibilites() s'arrête.
				else : 
					M[x][y] = False	#sinon on remet la case de la matrice à faux
	return False	#si on est pas sorti avant de la fonction, celle-ci retourne faux pour que possibilites() continue


#fonction de contrôle qui agit en terme de priorité

def possibilites() :
	if ordinateur_peut_gagner() : return	#si je peux gagner, je gagne
	elif empecher_humain_de_gagner() : return	#si je peux t'empêcher de gagner, je t'empêche
	else : coup_aleatoire()	#sinon peu importe où j'atteris


def fais_x(w) :
	w.create_polygon(10, 10, 20, 10, 55, 45, 55, 55, 45, 55, 10, 20, fill = 'red')
	w.create_polygon(10, 55, 10, 45, 45, 10, 55, 10, 55, 20, 20, 55, fill = 'red')

def fais_o(w) : w.create_oval(10, 10, 55, 55, width = 10)

def symbole(j) : return ['O', 'X'][j]	# j ne peut valoir que 0 ou 1

def gagnant(s) :
	global info
	for x in range(T) :
		if [M[x][y] for y in range(T)].count(s) is T : return True	# ligne x
		if [M[y][x] for y in range(T)].count(s) is T : return True	# colonne x
		if [M[y][y] for y in range(T)].count(s) is T : return True	# diagonale \
		if [M[y][T-1-y] for y in range(T)].count(s) is T : return True	# diagonale /
	if False not in [x for y in range(len(M)) for x in M[y]] : info ['text'] = 'GAME OVER'



# ~~~~~~~~~~~~~~
from Tkinter import *
morpion = Tk()
morpion.title('MORPION 1.0')	# cosmétique
grille = Frame(morpion)
Cell=[]
for R in range(T) :
	Cell +=[[]]	#initialise la liste de listes 'Cell'
	for C in range(T) :
		Cell[R] += [Canvas(grille, bg = 'light grey', width = H, height = H)]	#on crée une matrice des instances du canvas dans cell pour que l'ordinateur puisse dessiner dans celle qu'il a choisi
		Cell[R][C].bind("<Button-1>", joue)
		Cell[R][C].grid(row = R, column = C)
		Cell[R][C].R, Cell[R][C].C = R, C	# localisation de chaque cellule


grille.pack()
stop = Button(morpion, text='ASSEZ', command = morpion.destroy)
stop.pack()
info = Label(morpion)
info.pack()
if ordinateur == 'X' : coup_aleatoire() #La machine commence seulement si l'ordinateur est 'X'

morpion.mainloop()


