import MySQLdb

conn = MySQLdb.connect(host="localhost", user="silgy", passwd="silgy", autocommit="true")

cursor = conn.cursor()

cursor.execute("use iss;")

def db_insert(sim_id):
  print("Trying INSERT INTO results...")
  cursor.execute("insert into results values (%s,%s,%s);", (sim_id,0.1,0.5))
#  conn.commit()
  print("after execute")

#cursor.close()
#conn.close()