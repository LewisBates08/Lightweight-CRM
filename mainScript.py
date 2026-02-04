import sqlite3 as sq
import re
def getTitle():
    while True:
        pattern=r'^[A-Za-z]+(?: [A-Za-z]+)*$'
        title=input("New Title:")
        if re.fullmatch(pattern,title,re.I):
            if len(title)<15 and len(title)>2:
                print("Valid title!")
                return title.lower().strip()
            else:
                print("Title must be more than 2 and less than 15 characters long")
        else:
            print("Title must not include numbers or special characters")
def getValue():
    while True:
        try:
            value=int(input("New Value:"))
            value=str(value)
            return value
        except ValueError:
            print("Value must be an integer")
def getContact_id():    
    while True:
        try:
            cid=int(input("New Contact ID:"))
            cid=str(cid)

            return cid
        except ValueError:
            print("ID must be an integer")
def getStage():
    while True:
            c=input("1.Lead\n2.Contacted\n3.Negotiation\n4.Won\n5.Lost\nSelect a stage of the deal:")
            if c=="1":
                stage="lead"
                break
            elif c=="2":
                stage="contacted"
                break
            elif c=="3":
                stage="negotiation"
                break
            elif c=="4":
                stage="won"
                break
            elif c=="5":
                stage="lost"
                break
            else:
                print("Please enter a number between 1-5")
    return stage
            

def getName():
    while True:
        pattern=r'[A-Za-z]+'
        first=input("First name:")
        first=first.strip()
        if re.fullmatch(pattern,first,re.I):
            first=first.upper().strip()
            break
        else:
            print("Name must not include numbers or special characters")
            
    while True:
        pattern=r'[A-Za-z]+'
        last=input("Last name:")
        last=last.strip()
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
        first,last=getName()
        first=first.strip().lower()
        last=last.strip().lower()
        #calls function to get first and last name, unpacks from a tuple
        #Add countries/ different formats in the future        
        phone=getPhone().strip().lower()#call phone number function
        email=getEmail().strip().lower()#Validates that email is in the correct format
        location=getLocation().lower().strip()#retrieves location
        #adds data to sql database- prevents error
        try:
            cursor.execute("""INSERT INTO contacts
                        (firstname,lastname,email,phone,location)
                        VALUES(?,?,?,?,?)""",(first,last,email,phone,location))
            print(f"Added contact: {first.upper()} {last.upper()}!")    
            break 
        except Exception as e:
                print("Email and phone must be unique")

#=================
def addDeal(cursor):
    #allows user to add deals to a contact, which will include deals title, value and status
    while True:
        cid=getContact_id()
        title=getTitle()
        value=getValue()
        stage=getStage()
        
        details=(cid,title,value,stage)
        try:
            query=("INSERT INTO deals(contact_id,title,value,stage)VALUES(?,?,?,?)")
            cursor.execute(query,(details))
            title=title.upper()
            stage=stage.upper()
            print(f"Added deal for contact {cid}!\nTitle:{title}\nValue:{value}\nStage:{stage}")
            break
        except:
            print("ID must correlate to a valid contact")
#================

def displayDeals(cursor):
    while True:
        pattern=r"^[0-9]+$"
        chosenid=input("Enter ID of contact to find deals for")
        if re.fullmatch(pattern,chosenid):
            try:
                cursor.execute("SELECT * FROM deals WHERE contact_id = ?",(chosenid))
                deals=cursor.fetchall()
                cursor.execute("SELECT firstname,lastname FROM contacts WHERE id = ?",(chosenid,))
                contact=cursor.fetchall()
                for i in contact:
                    first,last=i
                    print(f"Contact{chosenid}:{first} {last}")
            
                if not deals:
                    print('No deals assosiated with contact',chosenid)
                for i in deals:
                    #print(i)
                    did,cid,title,value,stage=i
                    print("===CONTACT ",chosenid,"'S DEALS====")
                    print(f"\nTitle:{title}\nValue:{value}\nStage:{stage}\n\n==========")
                break
            except:        
                print("ID must correlate to a valid contact")
                
        else:
            print("ID must be an integer")
                         
#====================
        
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
#Deletes contact based on ID provided by user
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
def deleteDeal(cursor):
    did=input("Enter ID of deal to remove")
    cursor.execute("SELECT id FROM deals ORDER BY id DESC LIMIT 1;")
    maxim=int(cursor.fetchone()[0])
    if did.strip() == "None":
        cursor.execute("DELETE FROM deals WHERE id IS NULL")
    elif int(did.strip()) >maxim:
        print("ID not stored")
    elif int(did.strip())<0:
        print("ID not stored")
    elif did.strip()== "":
        print("Please enter an ID to delete")
    else:
        try:
            int(did)
        except:
          print("Deal ID must be an integer")
        try:
            cursor.execute("DELETE FROM deals WHERE id = ?", (int(did),))
            print (f"Deleted deal {did}!")  
        except:
            print("No deal matches that ID")

def deleteall():
    confirm=input("Are you sure you want to delete all contacts and deals? This action cannot be undone. (Y/N):")
    if confirm.strip().lower()=="y":
        cursor.execute("DELETE FROM contacts WHERE id != 0")
        cursor.execute("DELETE FROM deals WHERE id != 0")
        print("All contacts and deals deleted")
    else:
        print("Action cancelled")
#=================

def findContact(cursor):
#Queries Database across all columns to find contatcs with details similar to the info provided
#Displays users
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
                OR phone = ?
                OR location LIKE ?""")
        cursor.execute(query,(term,term,term,term,term))
        contacts=cursor.fetchall()
        if not contacts:
                print("No contacts match details provdided")
        print("==RESULTS==")
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
#Allows user to change details in columns based on id inputted
    cursor.execute("SELECT id FROM contacts ORDER BY id DESC LIMIT 1;")
    maxim=int(cursor.fetchone()[0])
    pattern=r"[0-9]"
    while True:
        cid=input("Enter ID of contact to edit:")
        if re.fullmatch(pattern,cid):
            if int(cid.strip())>maxim:
                print("ID not stored-too high")
            elif int(cid.strip())<0:
                print("ID not stored-too low")
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
        else:
            print("ID must only contain numbers")
def editDeals(cursor):
    #ensures contact id is an integer, converts it back to string
    while True:
        while True:
            try:
                did=int(input("Enter ID of deal to edit:"))
                did=str(did)
                break
            except:
                print("deal id must be an integer")
        
        cursor.execute(" SELECT * FROM deals WHERE id=? ",(did))
        deal=cursor.fetchall()
        if not deal:
            print("No deal matches that ID")
        else:
            for i in deal:
                id,cid,title,val,stage=i
                print(f"DEAL {id} FOR CONTACT{cid}\nTITLE:{title}\nSTAGE:{stage}\nVALUE:{val}")
            break

    while True:
        details={"contact_id":getContact_id,"title":getTitle,"value":getValue,"stage":getStage}
        detail=input("enter the detail you would like to change: ").lower().strip()
        if not detail in details:
            print(" Detail must be a valid detail from :\n contact_id\n title\n value\n stage\n ")
        else:
            value=details[detail]()
            query= f"UPDATE deals SET {detail}=? WHERE id=?"
            try: 
                cursor.execute(query,(value,cid))
                print(f"Changed {detail} to {value}!")
                break
            except Exception as e:
                print("ID must relate to a contact")

def menu():
    while  True:
        print("""1. Create Contact 
            \n 2. View Contacts 
            \n 3.Edit contacts 
            \n 4. Delete Contacts
            \n 5. Add Deals
            \n 6. View deals
            \n 7. Edit Deals
            \n 8. Delete Deals
            \n9.  Delete all contacts
            \n10. Exit""")
        choice= int(input("Enter choice:"))
        if choice== 1:
            addContacts(cursor)
        elif choice==2:
            displayContacts(cursor)
        elif choice==3:
            editContact(cursor)
        elif choice==4:
            deleteContacts(cursor)
        elif choice==5:
            addDeal(cursor)
        elif choice==6:
            displayDeals(cursor)
        #PREMATURE FUNCTIONS - NEED TO CREATE
        elif choice==7:
            editDeals(cursor)
        elif choice==8:
            deleteDeal(cursor)
        elif choice==9:
            deleteall()
        #=============================
        elif choice==10:
            print("Goodbye. Thank for using this CRM")
            break 
    


    
###====MAIN PROGRAM=====

##INITIALISE DATABASE
#creates a connection to the database file
conn=sq.connect("miniCRM.db")
#creates a cursor- allows us to execute commands onto the database, in this case,
cursor=conn.cursor()
#creating the table
conn.execute("PRAGMA foreign_keys = ON")
cursor.execute("""CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY,
    firstname TEXT NOT NULL,
    lastname TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    location TEXT UNIQUE NOT NULL)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS deals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contact_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    value INTEGER NOT NULL,
    stage TEXT NOT NULL,
    FOREIGN KEY (contact_id) REFERENCES contacts(id)
);""")

#runs the menu function 
menu()

    
#saves and closes the file closes the file
conn.commit()
conn.close()    
