import sqlite3 as sq
import re
def getName():
    while True:
        pattern=r'[A-Za-z]+'
        first=input("First name:")
        if re.fullmatch(pattern,first,re.I):
            first=first.upper().strip()
            break
        else:
            print("Name must not include numbers or special characters")
    while True:
        pattern=r'[A-Za-z]+'
        last=input("Last name:")
        if re.fullmatch(pattern,last,re.I):
            last=last.upper().strip()
            break
        else:
            print("Name must not include numbers or special characters")
    return first,last

#==================

def getPhone():
    #Validates that phone number is an 11 digit number
    while True:
        pattern=r"[0-9]+"

        phone=input("Phone number:")
        if len(phone)==11:
            if re.fullmatch(pattern,phone):
                phone=phone.strip()
                break
            else:
                print("Phone number must be a number")
        else:
            print("Phone number must be an 11 digits long")
    return phone

#===================

def getEmail():
#checks that email is in the correct format to be returned
    while True:
        pattern=pattern = r'^(?!.*\.\.)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        email=input("Email Address:")
        if re.match(pattern,email):
            email=email.strip()
            break
        else:
            print("""Email must follow the following format:
\n Username-@-domain-top level domain\n e.g= 'John_doe@yahoo.com'""")

    return email

#==================

def getLocation():
#function to get email
    while True:
        pattern=r'[A-Za-z]+'
        location=input("Location:")
        if re.fullmatch(pattern,location,re.I):
            location.lower().strip()
            break
        else:
            print("location must not include numbers or special characters")
    return location

#================

def addContacts(cursor):
    while True:
        first,last=getName().lower().strip()#calls function to get first and last name, unpacks from a tuple
        #Add countries/ different formats in the future        
        phone=getPhone().strip().lower()#call phone number function
        email=getEmail().strip().lower()#Validates that email is in the correct format
        location=getLocation().lower().strip()#retrieves location
        #adds data to sql database- prevents error
        try:
            cursor.execute("SELECT id FROM contacts ORDER BY id DESC LIMIT 1;")
            cid=cursor.fetchone()[0]
            cid+=1
            cursor.execute("""INSERT INTO contacts
                        (id,firstname,lastname,email,phone,location)
                        VALUES(?,?,?,?,?,?)""",(cid,first,last,email,phone,location))

            break 
        except Exception as e:
                print("Phone number and email must be unique")

#=================
        
def displayContacts(cursor):
    #Selects all contact records from database
    cursor.execute("SELECT * FROM contacts")
    #saves all selected contacts as tuples in a list
    rows=cursor.fetchall()
    #checks if list-database- is empty
    if not rows:
        print("Database empty-No contact")
        return
    #iterates through each tuple
    for row in rows:
        #unpacks each tuple into variables
        cid,first,last,email,phone,location=row
        if cid != 0:
            print(f"======CONTACT {cid} ======")
            print(f"""\nName:{first} {last} \n \n Phone number:{phone}\n \n Email:{email}\n
\n Location:{location}\n\n

            ===========================""")
#================

def deleteContacts(cursor):
    cid=input("Enter ID of contact to remove")
    cursor.execute("SELECT id FROM contacts ORDER BY id DESC LIMIT 1;")
    maxim=int(cursor.fetchone()[0])
    if cid.strip() == "None":
        cursor.execute("DELETE FROM contacts WHERE id IS NULL")
    elif int(cid.strip()) >maxim:
        print("ID not stored")
    elif int(cid.strip())<0:
        print("ID not stored")
    elif cid.strip()== "":
        print("Please enter an ID to delete")
    else:
        cursor.execute("DELETE FROM contacts WHERE id = ?", (int(cid),))

#=================

def findContact(cursor):
    pattern=r"^[^0-9]+$"
    print("""====SEARCH=====\n
Enter a piece of information about a contatcs to search for!
\n E.g. Name,location etc""")
    info=input("Enter information to search for:")
    info=info.strip().lower()
    if re.fullmatch(pattern,info):
        term=f"%{info}%"
        
        query=(f"""SELECT * FROM contacts WHERE firstname LIKE ?
                OR lastname LIKE ?
                OR email LIKE ?
                OR phone LIKE ?
                OR location LIKE ?""")
        cursor.execute(query,(term,term,term,term,term))
        contacts=cursor.fetchall()
        if not contacts:
                print("No contacts match details provdided")
        for i in contacts:
            cid,first,last,email,phone,location=i
            if cid != 0:
                print(f"======CONTACT {cid} ======")
                print(f"""\nName:{first} {last} \n \n Phone number:{phone}\n \n Email:{email}\n
        \n Location:{location}\n\n=================""")
    else:
        print("Search info must only contain letters")


#================
def editContact(cursor):
    ##ADD INPUT VALIDATION FOR CID, must be num, maybe use regex, maybe exception catching?
    cursor.execute("SELECT id FROM contacts ORDER BY id DESC LIMIT 1;")
    maxim=int(cursor.fetchone()[0])
    while True:
        cid=input("Enter ID of contact to edit:")
        if int(cid.strip())>maxim:
            print("ID not stored")
        elif int(cid.strip())<0:
            print("ID not stored")
        else:
            detail=input("Enter detail of contact to edit:")
            detail=detail.lower().strip()
            if detail=="name":
                first,last=getName()
                cursor.execute("UPDATE contacts SET firstname=?,lastname=? WHERE id=?",(first,last,cid))
                break
            elif detail=="phone":
                phone=getPhone()
                cursor.execute("UPDATE contacts SET phone=? WHERE id=?",(phone,cid))
                break
            elif detail=="email":
                email=getEmail()
                cursor.execute("UPDATE contacts SET email=? WHERE id=?",(email,cid))
                break
            elif detail=="location":
                location=getLocation()
                cursor.execute("UPDATE contacts SET location=? WHERE id=?",(location,cid))
                break
            else:
                print("Detail must be a valid contact detail, such as:\nNAME\nPHONE\nEMAIL\nLOCATION")
        
    
###====MAIN PROGRAM=====

##INITIALISE DATABASE
#creates a connection to the database file
conn=sq.connect("miniCRM.db")
#creates a cursor- allows us to execute commands onto the database, in this case,
cursor=conn.cursor()
#creating the table
cursor.execute("""CREATE TABLE IF NOT EXISTS contacts(id INTEGER,
firstname TEXT NOT NULL,
lastname TEXT NOT NULL,
email TEXT UNIQUE NOT NULL,
phone TEXT UNIQUE NOT NULL,
location TEXT NOT NULL)""")
cursor.execute("SELECT * FROM contacts")
rows= cursor.fetchall()
if not rows:
    cursor.execute("INSERT INTO contacts(id,firstname,lastname,email,phone,location)VALUES(?,?,?,?,?,?)",(0,".",".",".",".","."))
#editContact(cursor)
#addContacts(cursor)
displayContacts(cursor)
findContact(cursor)
    
#saves and closes the file closes the file
conn.commit()
conn.close()

##====README=====


#Add edit function
#Add search function
