import re
import tkinter as tk
from tkinter import filedialog

def read_ris(file_path):

	with open(file_path) as f:
		lines = f.readlines()
	entries = dict()
	entries['authors'] = list()
	entries['authors'].append('')
	for TempLine in lines:
		if re.match('TY',TempLine):
			entries['Type'] = TempLine[6:-1]
		elif re.match('PB',TempLine):
			entries['publisher'] = TempLine[6:-1]
		elif re.match('J1',TempLine):	
			entries['journal nickname'] = TempLine[6:-1]
		elif re.match('ID',TempLine):
			entries['doi'] = TempLine[6:-1]
		elif re.match('TI',TempLine):
			entries['title'] = TempLine[6:-1]
		elif re.match('PY',TempLine):
			entries['year'] = TempLine[6:10]
			entries['month'] = TempLine[11:13]
		elif re.match('UR',TempLine):
			entries['url'] = TempLine[6:-1]
		elif re.match('JA',TempLine):
			entries['journal'] = TempLine[6:-1]
		elif re.match('A1',TempLine):
			entries['authors'][0] = TempLine[6:-1]	
		elif re.match("AU",TempLine):
			entries['authors'].append(TempLine[6:-1]) 
		elif re.match('VL',TempLine):
			entries['volume'] = TempLine[6:-1]		
		elif re.match('IS',TempLine):
			entries['issue'] = TempLine[6:-1]
		elif re.match('SP',TempLine):
			entries['startpage'] = TempLine[6:-1]
		elif re.match('EP',TempLine):
			entries['endpage'] = TempLine[6:-1]	
		elif re.match('AB',TempLine):
			entries['abstract'] = TempLine[6:-1]	
	if entries['authors'][0] == '':
		entries['authors'].pop(0)	
	if ('journal nickname' in entries) == False:
		entries['journal nickname'] = entries['journal'][0][0:6]		
	return entries

def Ris_To_bib(entries,Bib_FileName):
	bib = open(Bib_FileName,'w+')
	bib.write('@article{' + Bib_FileName[0:-4] + ',')
	bib.write('\n\ttitle = {'+ entries['title']+'}')
	bib.write('\n\tauthors = {'+ entries['authors'][0])
	for entry in entries['authors']:
		bib.write(' and ' + entry)
	bib.write('\n\tjournal = {'+ entries['journal']+'}')
	bib.write('\n\tvolume = {'+ entries['volume']+'}')
	if ('issue' in entries):
		bib.write('\n\tissue = {'+ entries['issue']+'}')
	bib.write('\n\tpages = {'+ entries['startpage'] +':'\
		+ entries['endpage'] +'}')
	bib.write('\n\tyear = {'+ entries['year']+'}')
	bib.write('\n\tmonth = {'+ entries['month']+'}')
	bib.write('\n\tpublisher = {'+ entries['publisher']+'}')
	if ('doi' in entries):
		bib.write('\n\tdoi = {'+ entries['doi']+'}')
	bib.write('\n\turl = {'+ entries['url']+'}')
	if ('abstract' in entries):
		bib.write('\n\tabstract = {' + entries['abstract'] + '}')
	bib.write('\n } \n')
	bib.close()

def NameMyBib(entries):
	start_pos = entries['authors'][0].index(',')+2
	if ('.' in entries['authors'][0][start_pos:len(entries['authors'][0])]):
		FirstAuthorLastName = entries['authors'][0][0:start_pos-2]
	else:
		end_pos = len(entries['authors'][0]) 
		FirstAuthorLastName = entries['authors'][0][start_pos:end_pos]
	return  FirstAuthorLastName + entries['journal nickname'] +\
		entries['year']+ '.bib'


root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
entries = read_ris(file_path)
Bib_FileName = NameMyBib(entries)
Ris_To_bib(entries,Bib_FileName)