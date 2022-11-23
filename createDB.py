import sqlite3

def createDB():
    con=sqlite3.connect(database=r"sms.db")
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(eid INTEGER PRIMARY KEY AUTOINCREMENT, name text, email text, gender text, contact text, dob text, pass text, utype text, address text, salary text);")
    con.commit()

    
    cur.execute(f"Insert or ignore into employee(eid,name,email,gender,contact,dob,pass,utype,address,salary) values(1,'','','','','','','password','Admin','','')")
    con.commit()

    
    cur.execute("CREATE TABLE IF NOT EXISTS supplier(invoice INTEGER PRIMARY KEY AUTOINCREMENT, name text, contact text, desc text);")
    con.commit()
    

    cur.execute("CREATE TABLE IF NOT EXISTS category(cid INTEGER PRIMARY KEY AUTOINCREMENT, name text);")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS product(pid INTEGER PRIMARY KEY AUTOINCREMENT, Category text, Supplier text, Name text, Price text, Quantity text, Status text);")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS cartList(pid INTEGER PRIMARY KEY AUTOINCREMENT, name text, price text, quantity text,priceperitem text);")
    con.commit()

