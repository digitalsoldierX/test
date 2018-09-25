#! usr/bin/env/python3
# -*- coding: utf-8 -*-

#
# Betriebsdatenerfassung für die Benutzung auf dem Raspberry PI.
#
# 17.07.2018 Junkherr

import time
import sys
import os
import mysql.connector as mc
from datetime import datetime
from datetime import timedelta
import platform
from uuid import getnode

print('---+-+-+-+-+-+-+-+- build -+-++-+-+-+-+-+-+-+-++\n',time.asctime(),'\n')

################## Variabeln und Konstanten #####################
Fehler=False

###################### FUNKTIONEN #########################
#MAC Adresse auslesen
def get_mac():
	if  platform.system() == 'Linux':
		strMAC = ""
	elif  platform.system() == 'Windows':
		strMAC = hex(getnode())[-12:]	#mac z.B. e47fb21d9c54
	return strMAC

#Ausweis einlesen
def get_Card():
	CardID = '5F4870D4'   # z.B. Daniel Junkherr
	#CardID = '5F4870D'   # z.B. zu kurz
	#CardID = 'C73C2DB1'	# z.B. Sobenin
	return CardID

#ESD Check aus Tabelle 'esd' 
def get_ESD(CardID):
	cur = connection.cursor()
	sql_command="SELECT * FROM esd WHERE uid= '" + CardID + "'"
	cur.execute(sql_command)
	row=cur.fetchone()
	if cur.rowcount < 1:
		cur.close()
		return "error"
	cur.close()
	lastCheck=row[1]
	time_diff_hours=(datetime.now()-lastCheck) / timedelta(hours=1)
	if time_diff_hours < 12:		#kleiner 12 Stunden ist OK
		status=True
	else:
		status=False
	return status
	
#Sicherheitsunterweisung Check aus Tabelle 'su'
def get_SU(GID,Bereich):
	cur = connection.cursor()
	sql_command="SELECT * FROM su WHERE gid= '" + GID + "'"
	cur.execute(sql_command)
	row=cur.fetchone()
	if cur.rowcount < 1:
		cur.close()
		return "error"
	cur.close()
	
	if Bereich=="Allgemein":
		dateCheck=row[1]
	elif Bereich=="SMT":
		dateCheck=row[2]
	elif Bereich=="THT":
		dateCheck=row[3]
	elif Bereich=="PRF":
		dateCheck=row[4]
	elif Bereich=="AS2":
		dateCheck=row[5]
	elif Bereich=="XRAY":
		dateCheck=row[6]
	else:
		return "error"
	if dateCheck != None:		#wenn kein Datumseintrag vorhanden ist
		time_diff_hours=(datetime.now()-dateCheck) / timedelta(days=1)
		if time_diff_hours < 365:		#kleiner 365 Tage ist OK
			status=True
		else:
			status=False
		return status
	else:
		return False

#Arbeitsbereich holen aus Tabelle 'ap_name'
def get_Area(AP):
	cur = connection.cursor()
	sql_command="SELECT * FROM ap WHERE ap_name= '" + AP + "'"
	cur.execute(sql_command)
	row=cur.fetchone()
	if cur.rowcount < 1:
		cur.close()
		return "error"
	cur.close()
	return row[2]
	
########################## MAIN ##########################

starttime=time.time()
ereignis="kommen"

#Datenbank verbinden
try:
	connection = mc.connect(user='Daniel', password='mitarbeiter01', host='192.168.188.21', database='MF-Test')
	cur = connection.cursor()
	print('-> Datenbank geöffnet')
except mc.Error as e:
	print("Error %s" % (e.args[1]))
	sys.exit(1)

# Arbeitsplatz holen aus Tabelle 'mac_address'
Fehler=False
myMAC=get_mac()
print("-> MAC Adresse = " + myMAC)
sql_command ="SELECT * FROM devices WHERE mac_address='" + myMAC + "'"
cur.execute(sql_command)
row = cur.fetchone()
if cur.rowcount < 1:
	print("Fehler: Gerät nicht in der Datenbank vorhanden")
	Fehler=True
if cur.rowcount > 1:
	print("Fehler: Gerät hat doppelten Datenbank Eintrag")
	Fehler=True
cur.close()

if not Fehler:
	ap=row[1]
	print("-> Arbeitsplatz = " + ap)
	
	#Karte einlesen
	karte=get_Card()
	print("-> CardID = " + karte)

	# Mitarbeiter Daten holen aus Tabelle 'mitarbeiter'
	Fehler=False
	cur = connection.cursor()
	sql_command ="SELECT * FROM mitarbeiter WHERE uid='" + karte + "'"
	cur.execute(sql_command)
	ergebnis = cur.fetchone()
	if cur.rowcount < 1:
		print("Fehler: Karte nicht in der Datenbank vorhanden")
		Fehler=True
	if cur.rowcount > 1:
		print("Fehler: Karte hat doppelten Datenbank Eintrag")
		Fehler=True
	cur.close()

	if not Fehler:
		print('-> Karte OK')

		maid=ergebnis[0]
		vname=ergebnis[1]
		nname=ergebnis[2]
		gender=ergebnis[3]
		valid=ergebnis[4]
		uid=ergebnis[5]
		manr=ergebnis[6]
		pnr=ergebnis[7]
		gid=ergebnis[8]
		email=ergebnis[9]

		esd = get_ESD(karte)
		if type(esd) != bool:
			print("Fehler: Karte hat keinen ESD Datenbank Eintrag")
			Fehler=True

		if not Fehler:
			print("-> ESD = " + str(esd))

			su = get_SU(gid,"Allgemein")
			if type(su) != bool:
				print("Fehler: Karte hat keinen Sicherheitsunterweisung Datenbank Eintrag")
				Fehler=True

			if not Fehler:
				print("-> SU (Allgemein) = " + str(su))
				bereich=get_Area(ap)
				if bereich == "error":
					print("Fehler: Arbeitsplatz nicht vorhanden")
					Fehler=True

				if not Fehler:
					su = get_SU(gid,bereich)
					print("-> SU (" + bereich + ") = " + str(su))
				
					#Datensatz an Tabelle 'buchungen' einfügen
					cur = connection.cursor()
					sql_command="INSERT INTO buchungen (vname,nname,ereignis,esd,su,ap,uid,gid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
					cur.execute(sql_command,(vname,nname,ereignis,esd,su,ap,uid,gid))
					cur.close()
					connection.commit()
					print("-> " + ereignis + " Buchung eingetragen")

connection.close()                               # DB schliessen
print("-> Datenbank geschlossen")
print()
print("%.4f sek."% (time.time()-starttime))