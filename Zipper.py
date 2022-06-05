from functions import *
import configparser
import sys
import os

#load config file
config = configparser.ConfigParser()
config.read('config.ini')

if (os.path.exists('Units') == False):
	os.mkdir('Units')
if (os.path.exists('Tmp') == False):
	os.mkdir('Tmp')
if (os.path.exists('Zips') == False):
	os.mkdir('Zips')

#enter menu() at start
decision = 8

#main loop
while True:
	#add unit - 1
	if decision == 1:
		addUnit(config)
		decision = menu()

	#edit unit - 2
	elif decision == 2:
		editUnit(config)
		decision = menu()

	#delete unit - 3
	elif decision == 3:
		deleteUnit(config)
		decision = menu()	

	#list units and codes - 4
	elif decision == 4:
		listUnits(config)
		decision = menu()

	#zip files - 5 
	elif decision == 5:
		zipFiles(config)
		decision = menu()
	
	#settings - 7
	elif decision == 7:
		settings(config)
		decision = menu()

	#menu - 8
	elif decision == 8:
		decision = menu()

	#about - 9
	elif decision == 9:
		about()
		decision = menu()

	#exit - 0
	elif decision == 0:
		sys.exit(0)
