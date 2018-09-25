import mysql.connector as mc

sql_user='Daniel'
sql_pass='mitarbeiter01'
sql_host='192.168.188.21'
sql_db='MF-Test'
ap="PRF"
strMAC = open('/sys/class/net/eth0/address').readline().replace(':','')

connection = mc.connect(user=sql_user, password=sql_pass, host=sql_host, database=sql_db)
cur = connection.cursor()
sql_command="INSERT INTO devices VALUES (%s,%s)"
cur.execute(sql_command,(strMAC,ap))
cur.close()
connection.commit()
connection.close()

