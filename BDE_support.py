#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Betriebsdatenerfassung by D. Junkherr @ 7/18
# v0.1 : Erstversion

import sys
import time
import os
import mysql.connector as mc
from datetime import datetime
from datetime import timedelta
from uuid import getnode
from platform import system as system_name  # Returns the system/OS name
from subprocess import call as system_call  # Execute a shell command
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
py3 = True
Debug=False
try:
	import RPi.GPIO as GPIO
except:
	Debug=True

if not Debug:
	import BDE_ReadCard
	
################## Variabeln und Konstanten #####################
Fehler=False
Connected=False
continue_reading = True
ap=""
version="v0.1"
sql_user='Daniel'
sql_pass='mitarbeiter01'
sql_host='192.168.188.21'
sql_db='MF-Test'

def set_Tk_var():
    global lblTest_var
    lblTest_var = StringVar()

def exitButton():
	destroy_window()
	root.quit()

def Login_AP():
	global Fehler, Connected, ap, version, myMAC
	w.lblOutput.configure(text="verbinde mit Server...")
	result=connect_DB()
	if result:
		w.lblOutput.configure(text="Taste bitte...")
		Fehler=False
		lblTest_var.set("online")
	else:
		w.lblOutput.configure(text="verbinde mit Server...Fehler")
		Fehler=True
		w.lblAP.configure(text="Station: ???")
		lblTest_var.set("offline")
	if not Fehler:
		Connected=True
		ap=get_AP()
		if type(ap) != bool:
			w.lblAP.configure(text="Station: " + ap)
		else:
			w.lblAP.configure(text="Station: "+myMAC)
			Fehler=True

def init(top, gui, *args, **kwargs):
	global w, top_level, root
	w = gui
	top_level = top
	root = top
	w.lblOutput.configure(text="Login bitte...")
	w.lblVersion.configure(text=version)
	print(system_name())
	print("ping Server...")
	if ping(sql_host):		#wenn Server online automatisch verbinden
		Login_AP()
	
def ping(host):
    # Ping command count option as function of OS
    param = '-n' if system_name().lower()=='windows' else '-c'
    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]
    # Pinging
    return system_call(command) == 0

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

###################### Start Custom #########################

print('---+-+-+-+-+-+-+-+- build -+-++-+-+-+-+-+-+-+-++\n',time.asctime(),'\n')

###################### FUNKTIONEN #########################
#Datenbank verbinden
def connect_DB():
	global sql_db, sql_host, sql_pass, sql_user
	try:
		connection = mc.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_db)
		cur = connection.cursor()
		connection.close()
		print('-> Datenbank OK')
		return True
	except mc.Error as e:
		print("Error %s" % (e.args[1]))
		return False

#MAC Adresse auslesen
def get_mac():
	if system_name().lower() == 'linux':
		strMAC = open('/sys/class/net/eth0/address').readline().replace(':','')
	elif  system_name().lower() == 'windows':
		strMAC = hex(getnode())[-12:]	#lan-mac z.B. e47fb21d9c54
	return strMAC

#Ausweis einlesen
def get_Card():
	#CardID = '5F4870D4'   # z.B. Daniel Junkherr
	#CardID = '5F4870D'   # z.B. zu kurz
	#CardID = 'C73C2DB1'	# z.B. Sobenin
	return CardID

#ESD Check aus Tabelle 'esd' 
def get_ESD(CardID):
	global sql_db, sql_host, sql_pass, sql_user
	connection = mc.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_db)
	cur = connection.cursor()
	sql_command="SELECT * FROM esd WHERE uid= '" + CardID + "'"
	cur.execute(sql_command)
	row=cur.fetchone()
	if cur.rowcount < 1:
		cur.close()
		connection.close()
		return "error"
	cur.close()
	connection.close()
	lastCheck=row[1]
	time_diff_hours=(datetime.now()-lastCheck) / timedelta(hours=1)
	if time_diff_hours < 12:		#kleiner 12 Stunden ist OK
		status=True
	else:
		status=False
	return status
	
#Sicherheitsunterweisung Check aus Tabelle 'su'
def get_SU(GID,Bereich):
	global sql_db, sql_host, sql_pass, sql_user
	connection = mc.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_db)
	cur = connection.cursor()
	sql_command="SELECT * FROM su WHERE gid= '" + GID + "'"
	cur.execute(sql_command)
	row=cur.fetchone()
	if cur.rowcount < 1:
		cur.close()
		connection.close()
		return "error"
	cur.close()
	connection.close()
	
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
	if dateCheck != None:		#wenn Datumseintrag vorhanden ist
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
	global sql_db, sql_host, sql_pass, sql_user
	connection = mc.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_db)
	cur = connection.cursor()
	sql_command="SELECT * FROM ap WHERE ap_name= '" + AP + "'"
	cur.execute(sql_command)
	row=cur.fetchone()
	if cur.rowcount < 1:
		cur.close()
		connection.close()
		return "error"
	cur.close()
	connection.close()
	return row[2]

# Arbeitsplatz holen aus Tabelle 'mac_address'
def get_AP():
	global myMAC
	myMAC=get_mac()
	print("-> MAC Adresse = " + myMAC)
	sql_command ="SELECT * FROM devices WHERE mac_address='" + myMAC + "'"
	global sql_db, sql_host, sql_pass, sql_user
	connection = mc.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_db)
	cur = connection.cursor()
	cur.execute(sql_command)
	row = cur.fetchone()
	if cur.rowcount < 1:
		print("Fehler: Gerät nicht in der Datenbank vorhanden")
		cur.close()
		return False
	if cur.rowcount > 1:
		print("Fehler: Gerät hat doppelten Datenbank Eintrag")
		cur.close()
		return False
	ap=row[1]
	print("-> Arbeitsplatz = " + ap)
	cur.close()
	connection.close()
	return ap


def Buchung(ereignis):
########################## MAIN ##########################
	global Fehler, Connected, w
	starttime=time.time()
	print("Ereignis: " + ereignis)
	
	if Connected:
		#Karte einlesen
		Fehler=False
		w.lblOutput.configure(text="Karte bitte...")
		if messagebox.askokcancel("Karte einlesen","Karte: 5F4870D4"):
			karte=get_Card()
		else:
			karte=""
		print("-> CardID = " + karte)
		if karte=="":
			print("Fehler: keine Kartennr. erhalten")
			messagebox.showwarning("Warnung","keine Kartennr. erhalten")
			Fehler=True

		if not Fehler:
			# Mitarbeiter Daten holen aus Tabelle 'mitarbeiter'
			starttime=time.time()
			Fehler=False
			global sql_db, sql_host, sql_pass, sql_user
			connection = mc.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_db)
			cur = connection.cursor()
			sql_command ="SELECT * FROM mitarbeiter WHERE uid='" + karte + "'"
			cur.execute(sql_command)
			ergebnis = cur.fetchone()
			if cur.rowcount < 1:
				print("Fehler: Karte nicht in der Datenbank vorhanden")
				messagebox.showwarning("Warnung","Karte nicht in der Datenbank vorhanden")
				Fehler=True
			if cur.rowcount > 1:
				print("Fehler: Karte hat doppelten Datenbank Eintrag")
				messagebox.showwarning("Warnung","Karte hat doppelten Datenbank Eintrag")
				Fehler=True
			cur.close()

			if not Fehler:
				print('-> Karte OK')
				print(ergebnis)
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

				if ereignis=="kommen":
					# ESD Messung holen
					esd = get_ESD(karte)
					if type(esd) != bool:
						print("Fehler: Karte hat keinen ESD Datenbank Eintrag")
						messagebox.showwarning("Warnung","Karte hat keinen ESD Datenbank Eintrag")
						esd=None
					if not esd and esd!=None:
						messagebox.showwarning("Warnung","Keine gültige ESD Messung vorhanden!!!")
					print("-> ESD = " + str(esd))

					# Allgemeine Sicherheitsunterweisung holen
					su = get_SU(gid,"Allgemein")
					if type(su) != bool:
						print("Fehler: Karte hat keinen Sicherheitsunterweisung Datenbank Eintrag")
						messagebox.showwarning("Warnung","Karte hat keinen Sicherheitsunterweisung Datenbank Eintrag")
						su=None
					if not su and su!=None:
						messagebox.showwarning("Warnung","Keine gültige Allgemeine Sicherheitsunterweisung vorhanden!!!")
					print("-> SU (Allgemein) = " + str(su))
						
					# Bereich spezifische Sicherheitsunterweisung holen
					if su!=None:
						bereich=get_Area(ap)
						if bereich == "error":
							print("Fehler: Arbeitsplatz nicht vorhanden")
							su=False
						su = get_SU(gid,bereich)
						if not su:
							messagebox.showwarning("Warnung","Keine gültige Arbeitsplatz spezifische Sicherheitsunterweisung vorhanden!!!")
						print("-> SU (" + bereich + ") = " + str(su))
					else:
						print("-> SU (Bereich) = skip")

				if ereignis=="gehen":		#bei 'gehen' Buchung wird esd & su Abfrage übersprungen
					esd=None
					su=None
					
				#Datensatz an Tabelle 'buchungen' einfügen
				cur = connection.cursor()
				sql_command="INSERT INTO buchungen (vname,nname,ereignis,esd,su,ap,uid,gid) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
				cur.execute(sql_command,(vname,nname,ereignis,esd,su,ap,uid,gid))
				cur.close()
				connection.commit()
				print("-> " + ereignis + " Buchung eingetragen")
				# w.lblOutput.configure(text="Buchung erfolgreich")
				# time.sleep(2)
				w.lblOutput.configure(text="Taste bitte...")
	else:
		messagebox.showwarning("Warnung","Server nicht verbunden")

	print("%.4f sek."% (time.time()-starttime))


if __name__ == '__main__':
    import BDE
    BDE.vp_start_gui()


