import glob
import os
import shutil
import glob
import time
from zipfile import ZipFile

def clearConsole():
	command = 'clear'
	if os.name in ('nt', 'dos'):
	#if windows
		command = 'cls'
	os.system(command)

def about():
	clearConsole()
	print('''
Script for zipping invoices

Maintainer: X Y; x.y@z.com

More in the readme.md file

Version 0.24

Enter to continue
	''')
	input()

def menu():
	clearConsole()
	print('''
--------------Menu--------------
	1 - Add unit
	2 - Edit unit
	3 - Remove unit
	4 - List units
	5 - Zip files

	7 - Settings
	8 - Menu
	9 - About
	0 - Exit
--------------------------------
	''')
	return int(input('What do you want to do?\n'))

def wait():
	pass

def createFolders(unitName, config):
	os.mkdir('Units/' + unitName)
	i = 1
	while i <= len(config.items('types')):
		os.mkdir('Units/' + unitName + '/' + config['types'][str(i)].lower())
		os.mkdir('Units/' + unitName + '/' + config['types'][str(i)].lower() + '/paper')
		os.mkdir('Units/' + unitName + '/' + config['types'][str(i)].lower() + '/email')
		i += 1

def addUnit(config):
	clearConsole()
	while True:
		print('Adding new unit')
		print('You will be abble to change any value at the end of this process so any mistake can be easly overwritten')

		unitName = input('Type unit name: ')

		while True:
			unitCode = input('Type unit code: ')
			if (len(unitCode) == 4):
				break
			print('Unit code have to have 4 digits. Type it again')

		clearConsole()
		print('You have typed:')
		print('Unit name: ', unitName)
		print('Unit code: ', unitCode)
		answer = input('\nAre these informations correct? (Y)es / (N)o: ')[0].upper()
		if answer == 'Y':
			createFolders(unitName, config)
			break
		print('Ok, type it again:')	

	config[unitName]={
		"unitCode" : unitCode
	}

	with open('config.ini', 'w') as file_object:
		config.write(file_object)

def editUnit(config):
	clearConsole()
	i = 1
	units = []
	for c in config.sections():
		if config.has_option(c, 'unitCode'):
			units.append(c)
			print(i, ' - ', c)
			i += 1
	# answer = int(input('\nWhich unit do you want to edit?: '))
	answer = input('\nType number to edit corresponding unit or press Enter to return to menu: ')
	if answer == "":
		return 0
	answer = int(answer)
	while True:
		answerEdit = input('\nEditing: ' + units[answer - 1] + ' Proceed? (Y)es / (N)o: ')[0].upper()
		if answerEdit == 'Y':
			while True:	
				unitName = input('Type unit name: ')
				while True:
					unitCode = input('Type unit code: ')
					if (len(unitCode) == 4):
						break
					print('\nUnit code have to have 4 digits. Type it again')

				clearConsole()
				print('You have typed:')
				print('Unit name: ', unitName)
				print('Unit code: ', unitCode)
				confirm = input('\nAre these informations correct? (Y)es / (N)o: ')[0].upper()
				if confirm == 'Y':
					os.rename('Units/' + units[answer - 1], 'Units/' + unitName)	

					config[unitName]={
						"unitCode" : unitCode
					}

					with open('config.ini', 'w') as file_object:
						config.write(file_object)

					config.remove_section(units[answer - 1])
					with open('config.ini', 'w') as file_object:
						config.write(file_object)
					
					clearConsole()
					input('Unit edited. Enter to return to menu')
					return 0

				clearConsole()
				print('\nOk, type it again:')

		else:
			input('\nAborting, press Enter to return to menu')
			break

def deleteUnit(config):
	clearConsole()
	i = 1
	units = []
	for c in config.sections():
		if config.has_option(c, 'unitCode'):
			units.append(c)
			print(i, '- ' + c + '; ' + config[c]['unitCode'])
			i += 1
	answer = int(input('\nWhich unit do you want to remove?: '))
	while True:
		answerRemove = input('\n\nRemoving: ' + units[answer - 1] + '\nProceed? (Y)es / (N)o: ')[0].upper()
		if answerRemove == 'Y':
			config.remove_section(units[answer - 1])
			size = 0
			invoiceType = 1
			while invoiceType <= len(config.items('types')):
				for file in os.scandir('Units/' + units[answer - 1] + '/' + config['types'][str(invoiceType)].lower() + '/paper'):
					size += os.path.getsize(file)
				for file in os.scandir('Units/' + units[answer - 1] + '/' + config['types'][str(invoiceType)].lower() + '/email'):
					size += os.path.getsize(file)
				invoiceType += 1
			if (size != 0):
				clearConsole()
				print(units[answer - 1] + ' folders aren\'t empty! Check them and and try again')
				input('Enter to return to menu')
				break
			shutil.rmtree('Units/' + units[answer - 1])
			clearConsole()
			input('\nUnit removed\nEnter to return to menu')
			with open('config.ini', 'w') as file_object:
				config.write(file_object)
			break
		else:
			input('\nAborting, press Enter to return to menu')
			break

def listUnits(config):
	clearConsole()
	i = 1
	# units = []
	print('List of currently added units:\n')
	for c in config.sections():
		if config.has_option(c, 'unitCode'):
			# units.append(c)
			print(i, '- ' + c + '; ' + config[c]['unitCode'])
			i += 1
	input('\nPress Enter to return to menu')
	
def zipFiles(config):
	clearConsole()
	startNumber = int(input('Type start number: '))
	mailType = ['paper', 'email']
	for unit in config.sections():
		if config.has_option(unit, 'unitcode'):
			for invoiceType in list(config['types'].keys()):
				j = 0
				while j < len(mailType):
					mT = mailType[j]
					location = '**/' + unit + '/' + config['types'][invoiceType].lower() + '/' + mT + '/'
					fileList = sorted( filter( os.path.isfile, glob.glob(location + '*.pdf', recursive = True)))
					if len(glob.glob(location + '*.pdf', recursive = True)) > 0: #zobacz czy coś jest w email/paper
						sizeTmp = 0
						for file in os.scandir('Tmp/'):
							sizeTmp += os.path.getsize(file)

						if len(glob.glob(location + '*.pdf', recursive = True)) > 0 and (sizeTmp + os.path.getsize(sorted( filter( os.path.isfile, glob.glob(location + '*.pdf', recursive = True)))[0])) < int(config['settings']['zipSize']) and len(glob.glob('Tmp/*.pdf')) < int(config['settings']['maxInZip']):
							targetFile = 'Tmp/' + config[unit]['unitCode'] + '_' + str(int(time.time() * 1000))[2:] + '_' + time.strftime('%Y%m%d') + '_' + mT + '_XXXX.pdf'
							# targetFile = 'Tmp/' + config[unit]['unitCode'] + '_' + fileList[0][-7:]
							shutil.move(fileList[0], targetFile)
							if len(glob.glob(location + '*.pdf', recursive = True)) == 0: j += 1
						# elif len(glob.glob(location + '*.pdf', recursive = True)) == 0 or (sizeTmp + os.path.getsize(sorted( filter( os.path.isfile, glob.glob(location + '*.pdf', recursive = True)))[0])) > int(config['settings']['zipSize']):
						elif sizeTmp + os.path.getsize(sorted( filter( os.path.isfile, glob.glob(location + '*.pdf', recursive = True)))[0]) > int(config['settings']['zipSize']) or len(glob.glob('Tmp/*.pdf')) >= int(config['settings']['maxInZip']):
							startNumber = createZip(config, invoiceType, startNumber)
					else:
						j += 1
				startNumber = createZip(config, invoiceType, startNumber)
				
def createZip(config, invoiceType, startNumber):
	if len(glob.glob('Tmp/*.pdf')) > 0:
		invoicesCounter = 1
		invoiceList = sorted( filter( os.path.isfile, glob.glob('Tmp/*.pdf')))

		timeNewDelhi = time.strftime('%H%M%S', time.localtime(time.time() + 3 * 60 * 60 + 30 * 60))

		invoicesListTxt = open('Tmp/CONDUENT_invoices_' + time.strftime('%Y%m%d') + '_' + timeNewDelhi + '.txt', 'a')
		for pdfs in invoiceList:
			invoicesListTxt.write(str(invoicesCounter) + '.' + pdfs[4:] + '\n')
			invoicesCounter += 1
		invoicesListTxt.close()
		
		filesToZip = sorted( filter( os.path.isfile, glob.glob('Tmp/*')))
		zipFile = 'RRMTCONDUENT_' + config['types'][str(invoiceType)].upper() + 'INV.zip'
		with ZipFile(zipFile, 'a') as zip:
			for file in filesToZip:
				zip.write(file, arcname=file[4:])

		if startNumber < 10:
			startNumberStr = '0' + str(startNumber)
		else:
			startNumberStr = str(startNumber)

		shutil.move(zipFile, 'Zips/' + startNumberStr + '_' + zipFile)
		startNumber += 1

		deletelist = glob.glob('Tmp/*')
		for f in deletelist:
			os.remove(f)
	return startNumber

def settings(config):
	clearConsole()
	print('Current settings:\n')
	zipSize = float(config['settings']['zipSize'])/1000000
	print('1 - Max zip size: ' + str(zipSize) + ' MB')
	maxInZip = config['settings']['maxInZip']
	print('2 - Max files in zip: ' + maxInZip)
	answer = input('\nType section numer to edit or press Enter to return to menu: ')
	clearConsole()
	if answer == '1':
		while True:
			newZipSize = float(input('Type new size i megabytes: ').replace(',','.'))*1000000
			clearConsole()
			print('New max zip size: ' + str(newZipSize/1000000) + ' MB')
			answer = input('\nIs this information correct? (Y)es / (N)o: ')[0].upper()
			if answer == 'Y':
				config['settings']['zipSize'] = str(int(newZipSize))	
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				break
			clearConsole()
			print('Ok, type it again:\n')
	elif answer == '2':
		while True:
			newMaxInZip = int(input('Type new value: '))
			clearConsole()
			print('New value: ' + str(newMaxInZip))
			answer = input('\nIs this information correct? (Y)es / (N)o: ')[0].upper()
			if answer == 'Y':
				config['settings']['maxInZip'] = str(newMaxInZip)	
				with open('config.ini', 'w') as configfile:
					config.write(configfile)
				break
			clearConsole()
			print('Ok, type it again:\n')
