#def min_cost(N, K, A, B):
#    # Step 1: Precompute costs for all intervals
#    cost = [[0] * (N + 1) for _ in range(N + 1)]
#    
#    for l in range(1, N + 1):
#        sumA = 0
#        sumB = 0
#        for r in range(l, N + 1):
#            sumA += A[r - 1]
#            sumB += B[r - 1]
#            cost[l][r] = min(sumA, sumB)
#    
#    # Step 2: Initialize the DP table
#    dp = [[float('inf')] * (N + 1) for _ in range(K + 1)]
#    
#    # Base case: when k = 1
#    for j in range(1, N + 1):
#        dp[1][j] = cost[1][j]
#    
#    # Step 3: Fill the DP table
#    for k in range(2, K + 1):
#        for j in range(k, N + 1):  # j should be at least k
#            for i in range(k - 1, j):  # i must be at least k-1
#                dp[k][j] = min(dp[k][j], dp[k - 1][i] + cost[i + 1][j])
#    
#    # Step 4: The result is in dp[K][N]
#    return dp[K][N]
#
## Input reading
#N,K = input().split()
#A = [int(i) for i in input().split()]
#B = [int(j) for j in input().split()]
#
## Function call
#result = min_cost(int(N), int(K), A, B)
#print(result)


import os

import random

import sqlite3 as s
db = s.connect('TESTING.db')
c = db.cursor()


def setup():

 role=''
# try:
# c.execute('CREATE DATABASE YATRA')
# db.commit()
# except:
# print('Using existing database...')
# c.execute('USE YATRA')
# db.commit()
 try:
  c.execute('CREATE TABLE ADM_PLANE (FCODE INT(3) PRIMARY KEY, COMPANY CHAR(15), TYPE CHAR(10) NOT NULL, STARTDEST CHAR(15) NOT NULL, TIME INT(4) NOT NULL, GATENO CHAR(3) UNIQUE, STATUS CHAR(10), BASEPRICE FLOAT(10,2), PILOT CHAR(15) NOT NULL, PASSENGERS INT(2) NOT NULL, RUNWAY INT(2) UNIQUE)')
  db.commit()
  c.execute('CREATE TABLE TICKETS_PLANE (TICKETNO CHAR(6) PRIMARY KEY, COST FLOAT(10,2), FCODE INT(3), COMPANY CHAR(15), TYPE CHAR(10) NOT NULL, STARTDEST CHAR(15) NOT NULL, TIME INT(4) NOT NULL, GATENO CHAR(3) UNIQUE, STATUS CHAR(10))')
  c.execute('CREATE TABLE ADM_TRAIN (TCODE CHAR(3) PRIMARY KEY, COMPANY CHAR(23),NAME CHAR(20), STARTDEST CHAR(15), TIME INT(4), PLATFORM CHAR(2), STATUS CHAR(10), BASEPRICE FLOAT(10,2), PASSENGERS INT(2) ,CONFIRMED INT(3))')
  c.execute('CREATE TABLE TICKETS_TRAIN (PNR CHAR(6) PRIMARY KEY,COMPANY CHAR(15), NAME CHAR(20), TCODE INT(3), STARTDEST CHAR(20), TIME INT(4), STATUS CHAR(10) ,PLATFORM CHAR(2)),FOREIGN KEY (TCODE) REFERENCES ADM_TRAIN(TCODE)')
  db.commit()
  print('Creating Tables...')
 except:
  print('Using existing TABLES AND DATA...')

 global login_info
 login_info = {}
 try:
  with open('login.txt', 'r') as f:
   for i in f.read().split('\n'):
    login_info[i.split(' - ')[0]] = i.split(' - ')[1]

 except:
  print('Creating login info...')
  with open('login.txt', 'w') as f:
   f.write('plane_admin - _\nplane_user - _\ntrain_admin - _\ntrain_user - _')
  login_info = {'plane_admin' : '_', 'plane_user' : '_', 'train_admin' : '_', 'train_user' : '_'}

 print('Ready!')


def SelectMode():

 role=''
 print('\nWelcome to Yatra app (Delhi Server)')
 while True:
  ta = input('Select Mode of Transport(Rail/Air): ')
  if ta.lower() == 'air':
   role += 'plane_'
   break

  elif ta.lower() == 'rail':
   role += 'train_'
   break

  else:
   print('This mode of transport is not available')
 return role


def login(role):


  print('\nPlease login to continue(admin/user)')
  print("Default Password is '_'\n")
  while True:
   U = input('Enter Role/Username: ')
   r = role + U
   if r in login_info.keys():
    P = input('Enter Password: ')
    if login_info[r] == P:
     role = r
     print(f'You are logged in as {role}')
     change = input('Do you want to change your password(Y/N)? ')
     if change.lower() == 'y':
      p = input('Enter new password: ')
      with open('login.txt','r') as f:
       info = f.readlines()
       for i in range(len(info)):
        if r + ' - ' + P in info[i]:
         index1 = info[i].find(' - '+P)+3
         j = i
       f.seek(0)
      with open('login.txt', 'w') as f:
       for i in range(len(info)):
        if i == j:
         data = info[i][:index1]+p+'\n'
         f.write(data)
        else:
         f.write(info[i])

       print('New password saved! Restarting...')
       setup()
       SelectMode()
     else:
      break
    else:
     print('Wrong Password')
   else:
    print('Username not recognised')

def logout(rolename):

    print("You have been logged out.")
    choice = input("Do you want to log in again with the same role (y/n)? ").lower()

    if choice == 'y':
        login(rolename)
        return rolename
    else:
        rolename = SelectMode()
        login(rolename)
        return rolename

def printSelect(table):
    global rows
    D = {
    'admin_plane': '| FCODE |     COMPANY     |    TYPE    |    STARTDEST    | TIME | GATENO |   STATUS   | BASE-PRICE |      PILOT      | PASSENGERS | RUNWAY |',
    'user_plane': '| FCODE |     COMPANY     |    TYPE    |    STARTDEST    | TIME | BASE-PRICE |',
    'tickets_plane': '| TICKETNO |    COST    | FCODE |     COMPANY     |    TYPE    |    STARTDEST    | TIME | GATENO |   STATUS   |',
    'admin_train': '| TCODE |        COMPANY        |          NAME          |   STARTDEST   |   TIME   |  PLATFORM |   STATUS   | BASEPRICE |  PASSENGERS  |  CONFIRMED |',
    'user_train': '| TCODE |        COMPANY        |          NAME          |   STARTDEST   |   TIME   |  PLATFORM |   STATUS   | BASEPRICE |',
    'tickets_train': '| PNR | TCODE |        COMPANY        |          NAME          |   STARTDEST   |   TIME   |  PLATFORM |   STATUS   | '
    }

    spacesplane = {0: ' %8s |', 1: ' %10s |', 2: ' %5s |', 3: ' %15s |', 4: ' %10s |', 5: ' %15s |', 6: ' %4s |', 7: ' %6s |', 8: ' %10s |', 9: ' %10s |', 10: ' %15s |', 11: ' %10s |', 12: ' %6s |'}
    spacestrain = {
      0: ' %3s |',  1: ' %5s |', 2: ' %21s |', 3: ' %22s |', 4: ' %13s |', 5: ' %8s |',
        6: ' %9s |', 7: ' %10s |', 8: ' %9s |', 9: ' %12s |', 10: ' %10s |'
    }
    rows = c.fetchall()
    col = []
    char = len(D[table])
    if len(rows) != 0:
        print()
        print('='*char)
        print(D[table])
        print('='*char)
        if 'plane' in table.lower():
          if table.lower() == 'tickets_plane':
              col = list(range(9))
          else:
              for i in range(2,13):
                if ('user' in table.lower()) and (i <= 6 or i==9):
                  col.append(i)
                elif 'admin' in table.lower():
                  col.append(i)
          for a in rows:
            if 'plane' in table.lower():
                print('|',end='')
                for b in range(len(a)):
                  print(spacesplane[col[b]]%(a[b]),end='')
                else:
                  print()
                  print('-'*char)

            elif 'train' in table.lower():
             if table.lower() == 'tickets_train':
                col = list(range(8))
             elif table.lower() == 'user_train':
                col = list(range(1, 9))
             elif table.lower() == 'admin_train':
                col = list(range(1, 11))
             else:
              pass


          for row in rows:
                  print('|', end='')
                  for i in range(len(col)):
                      print(spacestrain[col[i]] % (row[col[i]]), end='')
                  print("\n" + '-' * char)

    else:
        print('No data available')


def ViewAll(role):

 if role == 'plane_admin':
  c.execute('SELECT * FROM ADM_PLANE ORDER BY TIME ASC')
  print('FLIGHT LOGS OF DELHI:')
  printSelect('admin_plane')

 elif role == 'plane_user':
  c.execute("SELECT FCODE, COMPANY, TYPE, STARTDEST, TIME, BASEPRICE FROM ADM_PLANE WHERE STATUS != 'CANCELLED' ORDER BY TIME ASC")
  print('FLIGHT LOGS OF DELHI:')
  printSelect('user_plane')

 elif role == 'train_admin':
  c.execute('SELECT * FROM ADM_TRAIN ORDER BY TIME ASC')
  printSelect('admin_train')

 elif role == 'train_user':
  c.execute("SELECT TCODE, COMPANY,NAME, STARTDEST, TIME, PLATFORM, STATUS FROM ADM_TRAIN WHERE STATUS != 'CANCELLED' ORDER BY TIME ASC")
  printSelect('user_train')


E = ['FCODE', 'TIME', 'BASEPRICE', 'PASSENGERS', 'RUNWAY']
def Find(role):
    if role == 'plane_admin':
      parameter = input('Enter Column: ').upper()
      value = input('Enter Value: ').upper()
      if parameter not in E:
        c.execute('SELECT * FROM ADM_PLANE WHERE ' + parameter + ' = ' + "'"+value+"'")
      else:
        c.execute('SELECT * FROM ADM_PLANE WHERE ' + parameter + ' = ' + value)
      print('FLIGHT LOGS OF DELHI:')
      printSelect('admin_plane')

    elif role == 'plane_user':
      parameter = input('Enter Column: ').upper()
      value = input('Enter Value: ').upper()
      if parameter not in E:
        c.execute("SELECT FCODE, COMPANY, TYPE, STARTDEST, TIME, BASEPRICE FROM ADM_PLANE WHERE STATUS != 'CANCELLED' AND "+parameter + ' = ' + "'"+value+"'")
      else:
        c.execute("SELECT FCODE, COMPANY, TYPE, STARTDEST, TIME, BASEPRICE FROM ADM_PLANE WHERE STATUS != 'CANCELLED' AND " + parameter + ' = ' + value)
      print('FLIGHT LOGS OF DELHI:')
      printSelect('user_plane')

    elif role == 'train_admin':
      parameter = input('Enter Column: ').upper()
      value = input('Enter Value: ').upper()
      c.execute('SELECT TCODE, COMPANY, NAME, STARTDEST, TIME, PLATFORM, STATUS, BASEPRICE, PASSENGERS, CONFIRMED FROM ADM_TRAIN WHERE '  +parameter+  " = '" + value + "'")
      printSelect('admin_train')

    elif role == 'train_user':
      parameter = input('Enter Column: ').upper()
      value = input('Enter Value: ').upper()
      c.execute('SELECT TCODE, COMPANY, NAME, STARTDEST, TIME, PLATFORM, STATUS, BASEPRICE FROM ADM_TRAIN WHERE ' +parameter+ " = '" + value + "'")
      printSelect('user_train')


seating='     01A 01B 01C\n     02A 02B 02C\n     03A 03B 03C\n     04A 04B 04C\n     05A 05B 05C\n\n06A 06B 06C 06D 06E 06F\n07A 07B 07C 07D 07E 07F\n08A 08B 08C 08D 08E 08F\n09A 09B 09C 09D 09E 09F\n10A 10B 10C 10D 10E 10F\n11A 11B 11C 11D 11E 11F\n12A 12B 12C 12D 12E 12F\n13A 13B 13C 13D 13E 13F\n14A 14B 14C 14D 14E 14F\n15A 15B 15C 15D 15E 15F'
def RandomPassengers():# for each plane
 passengers = random.randint(0,75)
 return passengers


def RandomSeats(fcode,psgr):
 filename = str(fcode) + '.txt'
 for k in range(int(psgr)):
  L =[]
  with open(filename) as f:
   for i in f.read().split('\n'):
    for j in i.split():
     if j != '---':
      L.append(j)
  s = random.choice(L)
  f = open(filename)
  data = f.read()
  index = data.find(s)
  f.close()
  with open(filename, 'w') as f:
   f.write(data[:index]+'---'+data[index+3:])


def AddData(role):
  try:
    if role == 'plane_admin':
      while True:
        i = input('FLIGHT CODE: ').upper()
        j = "'" + input('COMPANY: ').upper() + "'"
        a1 = int(input('TYPE(1-ARRIVAL, 2-DEPARTURE): '))
        if a1 == 1:
          k = "'" + 'ARRIVAL' + "'"
        elif a1 == 2:
          k = "'" + 'DEPARTURE' + "'"
        l = "'" + input('ORIGIN/DESTINATION: ').upper() + "'"
        m = input('TIME(2400 format): ')
        n= "'" + "G" + input('GATE NO(1-20): ') + "'"
        a2 = int(input('STATUS(1-DELAYED, 2-ONTIME, 3-EARLY): '))
        if a2 == 1:
          o = "'" + 'DELAYED' + "'"
        elif a2 == 2:
          o = "'" + 'ONTIME' + "'"
        elif a2 == 3:
          o = "'" + 'EARLY' + "'"
        b = input('BASE-PRICE: ')
        p = "'" + input('PILOT NAME: ').upper() + "'"
        q = input('PASSENGERS(0-75): ')
        r = input('RUNWAY(1-20): ')
        c.execute("INSERT INTO ADM_PLANE VALUES("+i+','+j+','+k+','+l+','+m+','+n+','+o+','+b+','+p+','+q+','+r+")")
        db.commit()
        filename = i + '.txt'
        f = open(filename, 'w')
        f.write(seating)
        f.close()
        RandomSeats(i,q)
        more = input('More Data(y/n)? ').lower()
        if more == 'n':
            break
    elif role =='train_admin':
      while True:
        a=int(input('Enter train code'))
        b=input('Enter company name: ')
        tname=input('Enter train name: ')
        d=int(input('Enter time: '))
        e=int(input('Enter platform'))
        f=(input('Enter starting point'))
        g=int(input('Enter total number of passengers: '))
        j=int(input('Enter confirmed: '))
        h=int(input('Enter baseprice: '))
        i=input('Enter status: ')
        statement1='INSERT INTO ADM_TRAIN VALUES(?,?,?,?,?,?,?,?,?,?)'
        values=(str(a),b,tname,f,str(d),str(e),i,str(h),str(g),str(j))
        c.execute(statement1,values)
        db.commit()
        more=input('Do you want to add more? ')
        if more in 'Nn':
          break
    else:
      print('You are not authorised for this action')
  except:
    print('Some error occurred! Check the entered values')


def Update(role):
  try:
    if role == 'plane_admin':
      parameter = input('Enter Column to be updated: ').upper()
      value = str(input('Enter updated Value: ')).upper()
      condition = input('Enter Conditional Column: ')
      c_value = str(input('Enter Conditional value: ')).upper()
      if parameter not in E and condition not in E:
        c.execute('UPDATE ADM_PLANE SET ' + parameter + ' = ' + "'"+value+"'" + ' WHERE ' + condition + ' = ' + "'"+c_value+"'")
        db.commit()
      elif parameter in E and condition not in E:
        c.execute('UPDATE ADM_PLANE SET ' + parameter + ' = ' +value+ ' WHERE ' + condition + ' = ' + "'"+c_value+"'")
        db.commit()
      elif parameter not in E and condition in E:
        c.execute('UPDATE ADM_PLANE SET ' + parameter + ' = ' + "'"+value+"'"+ ' WHERE ' + condition + ' = ' +c_value)
        db.commit()
      else:
        c.execute('UPDATE ADM_PLANE SET ' + parameter + ' = ' + value+ ' WHERE ' + condition + ' = ' +c_value)
        db.commit()
      if parameter == 'STATUS' and value == 'CANCELLED':
        c.execute('DELETE FROM TICKETS_PLANE WHERE STATUS = CANCELLED')
        db.commit()
    elif role == 'train_admin':
      column = input('Enter Column to be updated: ').upper()
      update = str(input('Enter updated Value: ')).upper()
      condition = input('Enter Conditional Column: ').upper()
      value = str(input('Enter Conditional value: ')).upper()
      c.execute('UPDATE ADM_TRAIN SET ' + column + " = '" + update + "' WHERE " + condition + " = '" + value + "'")
      db.commit()
  except:
    print('Some error occurred! Check the entered values')


def Delete(role):
  try:
    if role == 'plane_admin':
      condition = input('Enter Conditional Column: ').upper()
      c_value = str(input('Enter Conditional value: ')).upper()
      if condition not in E:
        c.execute('SELECT FCODE FROM ADM_PLANE WHERE ' + condition + ' = ' + "'"+c_value+"'")
        r = c.fetchall()
        c.execute('DELETE FROM ADM_PLANE WHERE ' + condition + ' = ' + "'"+c_value+"'")
        c.execute('DELETE FROM TICKETS_PLANE WHERE ' + condition + ' = ' + "'"+c_value+"'")
        db.commit()
      else:
        c.execute('SELECT FCODE FROM ADM_PLANE WHERE ' + condition + ' = ' +c_value)
        r = c.fetchall()
        c.execute('DELETE FROM ADM_PLANE WHERE ' + condition + ' = ' + c_value)
        c.execute('DELETE FROM TICKETS_PLANE WHERE ' + condition + ' = ' + c_value)
        db.commit()
        os.remove(str(r[0][0]) + '.txt')

    elif role == 'train_admin':
      condition = input('Enter Conditional Column: ')
      value = str(input('Enter Conditional value: ')).upper()
      c.execute('DELETE FROM ADM_TRAIN WHERE '+ condition + " = '" + value + "'")
      db.commit()
  except:
    print('Some error occurred! Check the entered values')


def BookingPlane(role,code,base,ticketno):

 if role == 'plane_user':
  ViewAll()
  while True:
   Find()
   cont = input('\nContinue Booking? ')
   if cont.lower() == 'y':
    break

  try:
   code = input('Enter FCODE of flight you want to book: ')
   c.execute('SELECT FCODE, COMPANY, TYPE, STARTDEST, TIME, BASEPRICE FROM ADM_PLANE WHERE FCODE = ' + code)
   print('THIS IS THE FLIGHT YOU WANT TO BOOK:')
   printSelect('user_plane')
   base = rows[0][5]
   tprice,seat = AvlSeatsPlane(code,base)
   print(f'Total Cost = {tprice}')
   confirm = input('Confirm booking? ').lower()
   if confirm == 'y':
    ticketno = "'" +str(code) + str(seat) + "'"
    print(f'Transaction successful! Your ticket number is {ticketno}')
    SeatBookedPlane(ticketno,code, seat, tprice)
   else:
    print('Transaction terminated!')
  except:
   print('Error! Transaction terminated!')
 else:
  print('You need to login as user for this action')


spcost = ['01','02','03','04','05','C','D']

def AvlSeatsPlane(fcode, baseprice):

 filename = str(fcode) + '.txt'
 L = []
 with open(filename) as f:
  print('\n Available Seats in th plane:')
  print(f.read())
  f.seek(0)
  for i in f.read().split('\n'):
   for j in i.split():
    if j != '---':
     L.append(j)

 while True:
  seat = input('Enter the seat you want to book: ').upper()
  if seat in L:
   print('Booking...')
   break
  else:
   print('Seat not Available')
 extra = 0.00
 no = seat[:2]
 alpha = seat [-1]
 if no in spcost:
  extra += 5000.00
 elif no not in spcost and alpha in spcost:
  extra += 2000.00
 tprice = float(baseprice) + float(extra)
 return (tprice,seat)


def SeatBookedPlane(tno,fcode,bseat,tprice):
 filename = str(fcode) + '.txt'
 f = open(filename)
 data = f.read()
 index = data.find(bseat)
 f.close()

 with open(filename, 'w') as f:
  f.write(data[:index]+'---'+data[index+3:])
 c.execute('UPDATE ADM_PLANE SET PASSENGERS = PASSENGERS + 1 WHERE FCODE = ' + fcode)
 c.execute('SELECT * FROM ADM_PLANE WHERE FCODE = '+ fcode)
 r = c.fetchall()
 c.execute('INSERT INTO TICKETS_PLANE VALUES('+ str(tno)+','+str(tprice)+','+fcode+','+"'"+str(r[0][1])+"'"+','+"'"+str(r[0][2])+"'" +','+"'"+str(r[0][3])+"'"+','+str(r[0][4])+','+"'"+str(r[0][5])+"'"+','+"'"+str(r[0][6])+"'"+ ')')
 db.commit()


def ViewAllTick(role):

 print()
 if role=='plane_user':
    c.execute('SELECT * FROM TICKETS_PLANE')
    print('THESE ARE THE TICKETS YOU PURCHASED:')
    printSelect('tickets_plane')
 elif role=='train_user':
    c.execute('SELECT * FROM TICKETS_TRAIN')
    print('THESE ARE THE TICKETS YOU PURCHASED')
    printSelect('tickets_train')
 else:
    print('You need to login as user for this action')


def CancellingPlane(role):
 if role=='plane_user':
  ViewAllTick()
  cont = input('\nContinue Cancellation? ')
  if cont.lower() == 'y':
   try:
    tcode = input('Enter TICKETNO of ticket you want to cancel: ').upper()
    c.execute('SELECT * FROM TICKETS_PLANE WHERE TICKETNO = ' + "'" + tcode + "'")
    printSelect('tickets_plane')
    confirm = input('\nConfirm Cancellation? ').lower()
    if confirm == 'y':
     DelTick(tcode)
     print('Ticket Succesfully Cancelled! Your money will be refunded shortly.')
    else:
     print('Cancellation stopped!')
   except:
    print('Error! Cancellation Stopped!')
 else:
  print('You need to login as user for this action')


def DelTick(tickno):
  c.execute('DELETE FROM TICKETS_PLANE WHERE TICKETNO = ' + "'" + tickno+ "'")
  c.execute('UPDATE ADM_PLANE SET PASSENGERS = PASSENGERS-1 WHERE FCODE = '+ "'" + tickno[:3]+ "'")
  db.commit()


def DeleteAllData(role):
 if role == 'plane_admin':
  print('Deleting all Tables and Data...')
  c.execute('SELECT * FROM ADM_PLANE')
  r = c.fetchall()
  for i in range(len(r)):
   os.remove(str(r[i][0]) + '.txt')
  os.remove('login.txt')
  c.execute('DROP TABLE ADM_PLANE')
  c.execute('DROP TABLE TICKETS_PLANE')
  db.commit()
 elif role=='train_admin':
  print('DELETING EVERYTHING IN DATABASE...')
  c.execute('DROP TABLE ADM_TRAIN')
  c.execute('DROP TABLE TICKETS_TRAIN')
 else:
  print('You are not authorised to perform this action.')


def RandomDataPlane(no,role):
 if role == 'plane_admin':
  print('Calling random data function')
  z =1
  while z <=no:
   try:
    i = str(random.randint(100,999))
    j = "'" + random.choice(['AIR INDIA', 'KINGFISHER', 'INDIGO', 'SPICE JET', 'QATAR AIRWAYS', 'JET AIRWAYS', 'VISTARA']) + "'"
    k = "'" + random.choice(['ARRIVAL', 'DEPARTURE']) + "'"
    l = "'" + random.choice(['MUMBAI', 'HYDERABAD', 'KOLKATA', 'CHENNAI', 'BENGALURU', 'KOCHIN', 'BHOPAL', 'AMRITSAR', 'CHANDIGARH','LUCKHNOW', 'KANPUR']) + "'"
    m = str(random.randrange(0,2400,100))
    n= "'" + 'G' + str(random.randint(1,20)) + "'"
    o = "'" +random.choice(['ON TIME', 'EARLY', 'DELAYED', 'CANCELLED'])+ "'"
    b = str(random.randrange(5000,25100,100))
    p = "'" + random.choice(['YASH ','NITIN ','ANSH ','KARAN ','VIJAY ','ISHAAN ','PIYUSH ','RAGHAV ','SARTHAK ','ANURAG ']) +random.choice(['SHARMA', 'SINGH', 'GOEL', 'KASHYAP','RAHEJA', 'JAIN', 'AGARWAL']) + "'"
    q = str(RandomPassengers())
    r = str(random.randint(1,25))
    c.execute("INSERT INTO ADM_PLANE VALUES("+i+','+j+','+k+','+l+','+m+','+n+','+o+','+b+','+p+','+q+','+r+")")
    db.commit()
    filename =i + '.txt'
    f = open(filename, 'w')
    f.write(seating)
    f.close()
    RandomSeats(i,q)
    z +=1
   except:
    pass










def RandomSeatsTrain(traincode):
 coaches={'1A':40,'2A':40,'3A':40,'EC':20}#maximum capacity for each coach
 seats={'traincode':traincode,'seating':{}}
 for coach,capacity in coaches.items():
  confirmed_seats=random.randint(0,capacity)
  seats['seating'][coach]=confirmed_seats

 return seats


def Waitlist(traincode,seats,booking):

  WL={'traincode':traincode,'seatingWL':{}}
  RandomSeatsTrain(traincode)
  if rolename=='train_admin':
   for coach, capacity in seats['seating'].items():
            if seats['seating'][coach] == 0 and booking[traincode] >= 140:
                if coach not in WL['seatingWL']:
                    WL['seatingWL'][coach] = 0
                WL['seatingWL'][coach] += 1
  return WL


def GeneratePNR():
  pnr=random.randrange(10000,100000)
  return pnr


def CheckPNRStatus():
  pnr=int(input('Enter pnr'))
  c.execute('SELECT STATUS,PLATFORM,TIME FROM TICKETS_TRAIN WHERE PNR=?',(pnr,))
  r=c.fetchall()
  print('The train status is: ',r)


def Randomdatatrain():
    print("Randomdatatrain function called")
    while True:
        used_platforms = set(row[0] for row in c.execute("SELECT PLATFORM FROM ADM_TRAIN").fetchall())
        available_platforms = set(range(1, 11)) - used_platforms
        if not available_platforms:
         print("No available platforms. Cannot insert more data.")
         break
        platform = random.choice(list(available_platforms))
        a = random.choice(['INDIAN RAILWAYS', 'IRCTC', 'KONKAN RAILWAY', 'SOUTHERN RAILWAY', 'EASTERN RAILWAY', 'WESTERN RAILWAY', 'NORTHERN RAILWAY', 'CENTRAL RAILWAY', 'NORTH EASTERN RAILWAY', 'SOUTH CENTRAL RAILWAY'])
        b = random.choice(['SHATABDI EXPRESS', 'RAJDHANI EXPRESS', 'VANDE BHARAT EXPRESS', 'PUROSHOTTAM EXPRESS', 'TEJAS EXPRESS', 'TAMILNADU EXPRESS', 'ANDAMAN EXPRESS', 'GARIB RATH EXPRESS', 'SAMPOORAN EXPRESS', 'MAGADH EXPRESS'])
        platform = random.randint(1, 100)
        d = random.randint(100, 999)
        e = random.choice(['CANCELLED', 'ON TIME', 'DELAYED', 'EARLY'])
        f = random.choice(['DELHI', 'KANPUR', 'LUCKHNOW', 'PATNA', 'CHENNAI', 'BHOPAL', 'INDORE', 'UJJAIN', 'CALCUTTA', 'CHANDIGARH'])
        hour = random.randint(0, 23)
        minute = random.choice([0, 15, 30, 45])
        g = f"{hour:02}:{minute:02}"
        h = random.choice([100, 200, 300, 400, 500])
        i = random.randint(1, 100)
        j = random.randint(1, i)
        pnr = GeneratePNR()

        statement = ('INSERT INTO ADM_TRAIN VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?,?)')
        val = (str(d),a,b,f,str(g),str(platform),e,str(h),str(i),str(j))


        print("Executing SQL:", statement)
        print("Values:", val)

        try:
            c.execute(statement, val)
            db.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print("Error during insertion:", e)

        choice = input('Enter more (Y/N): ')
        if choice in 'Nn':
            break


spcost = ['01','02','03','04','05','C','D']
def BookingTrain(role):
    if role == 'train_user':
     ViewAll()
     while True:
          Find()
          choice = input("Do you want to continue booking? ")
          if choice.upper() == 'N':
              break
          option = input('Enter TCODE of train you want to book: ')
          booking = {'traincode': option, 'bookings': 0}
          sa = RandomSeatsTrain(option)
          wl = Waitlist(option, sa, booking)

          for coach, capacity in sa['seating'].items():
              if capacity <= 40:
                  TYPE = 'CONFIRMED'
                  print(coach, capacity)
              else:
                  TYPE = 'WAITLISTING'
                  print(coach, capacity)

          c.execute('SELECT TCODE, COMPANY, STARTDEST, TIME, BASEPRICE, CONFIRMED FROM ADM_TRAIN WHERE TCODE = ?', (option,))

          contin = input('Do you want to continue booking: ')
          baseprice = random.choice([100, 200, 300, 400, 500])
          if contin in 'Yy':
              try:
                  ch = input('Enter choice of coach: ')
                  if ch.upper() == '1A':
                      price = baseprice + random.randint(2500, 5000)
                  elif ch.upper() == '2A':
                      price = baseprice + random.randint(1200, 3500)
                  elif ch.upper() == '3A':
                      price = baseprice + random.randint(800, 2500)
                  elif ch.upper() == 'EC':
                      price = baseprice + random.randint(1500, 3500)
                  else:
                      print('Enter right choice of coach')
                      continue

                  print('The total cost is', price)
                  confirm = input('Confirm booking: ')
                  if confirm.upper() == 'Y':
                      booking['bookings'] += 1  # Increment bookings count
                      sa['seating'][ch.upper()] += 1  # Update seats count for the coach
                      pnr = GeneratePNR()
                      if TYPE == 'CONFIRMED':
                          c.execute('INSERT INTO TICKETS_TRAIN (TCODE, COMPANY, NAME, STARTDEST, TIME, PLATFORM, STATUS) SELECT TCODE, COMPANY, NAME, STARTDEST, TIME, PLATFORM, STATUS FROM ADM_TRAIN WHERE TCODE = ?', (option,))
                          c.execute('UPDATE ADM_TRAIN SET CONFIRMED = CONFIRMED + 1 WHERE TCODE = ?', (option,))
                          c.execute('UPDATE TICKETS_TRAIN SET PNR = ? WHERE TCODE = ? AND PNR IS NULL', (pnr, option))

                      print('Your transaction was successfully made! Here is your PNR: ', pnr)

              except Exception as e:
                  print('Error! Transaction terminated. Error details: ', e)
                  more = input('Do you want to book more tickets? ')
                  if more in 'Nn':
                      break
          else:
              print('Transaction terminated')


def CancellingTrain(role,traincode):
 global WL
 global seats
 if role=='train_user':
  ViewAllTick(role)
  cancellation={'traincode':traincode}
  traincode=input('Enter train code: ')
  pnr=input('Enter pnr on ticket')
  coach=input('Enter coach: ')
  proceed=input('Proceed with cancellation(Y/N)? ')
  try:
   if proceed.upper()=='Y':
    c.execute('SELECT * FROM TICKETS_TRAIN WHERE PNR='+pnr+'AND TCODE='+traincode)
    printSelect('tickets_train')
    confirm = input('\nConfirm Cancellation? ').lower()
    if confirm == 'y':
      cancellation[traincode]+=1
      if WL['traincode']==traincode and WL['seatingWL'][coach]!=0:
       WL['seatingWL'][coach]-=1
       c.execute('UPDATE ADM_TRAIN CONFIRMED=CONFIRMED+1 WHERE TCODE=?',(traincode,))
       c.execute('DELETE FROM TICKETS_TRAIN WHERE PNR=?',(pnr,))
       print('Cancellation successful! ')
       db.commit()
      else:
       seats['seating'][coach]+=1
   else:
     print('Cancellation stopped!')
  except:
   print('Error! Cancellation Stopped!')



#MENU DRIVEN PROGRAM

setup()
rolename=SelectMode()
login(rolename)

while True:
 try:
  print('\ntype 0 to view the list of commands!')
  if rolename[:5] == 'plane':
    com = int(input('What would you like to do: '))
    if com == 0:
      print('''List of commands...
      1 : To see all the flight data
      2 : To find specific data
      3 : To add data to the flight table
      4 : To update data in the flight table
      5 : To delete particular flight data
      6 : To enter random data to the flight log
      7 : To book a ticket
      8 : To see all purchased tickets
      9 : To cancel tickets
      10: To logout
      11: To delete all Tables and Data
      12: To stop the program and exit''')

    elif com == 1:
      ViewAll('plane_admin')

    elif com == 2:
      Find(rolename)

    elif com == 3:
      AddData(rolename)

    elif com == 4:
      Update(rolename)

    elif com == 5:
      Delete(rolename)

    elif com == 6:
      n = int(input('Enter number of rows: '))
      RandomDataPlane(n,'admin_plane')

    elif com == 7:
      BookingPlane(rolename)

    elif com == 8:
      ViewAllTick(rolename)

    elif com == 9:
      CancellingPlane(rolename)

    elif com == 10:
      logout(rolename)

    elif com == 11:
      sure = input('Confirm deletion of all Tables and Data: ').lower()
      if sure == 'y':
        DeleteAllData()
        break

    elif com == 12:
      break

    else:
      print('Request Cancelled.')


  elif rolename[:5] == 'train':
    task= int(input('Enter the task we can perform for you: '))
    if task == 0:
      print('''These are the list of tasks:
    1 . Manually add data to table
    2 . Add Random data to table)
    3 . See all data
    4 . Find something specific
    5 . Update information
    6 . Book a ticket
    7 . Cancel a ticket
    8 . Check PNR Status
    9 . See purchase history
    10. Delete information
    11. Delete everything
    12. Logout
    13. Exit''')

    elif task==1:
      AddData(rolename)

    elif task==2:
      Randomdatatrain(rolename)
      print('random data function')

    elif task==3:
      ViewAll(rolename)

    elif task==4:
      Find(rolename)

    elif task==5:
      Update(rolename)

    elif task==6:
      BookingTrain(rolename)

    elif task==7:
      tc=int(input('Enter traincode: '))
      CancellingTrain(rolename,tc)

    elif task==8:
      CheckPNRStatus()

    elif task==9:
      ViewAllTick(rolename)

    elif task==10:
      Delete(rolename)

    elif task==11:
      confirm=input('Are you sure? Do you want to delete everything? ')
      if confirm in 'Yy':
        print('Deleting everything')
        DeleteAllData(rolename)

    elif task==12:
      logout(rolename)

    elif task==13:
      break

    else:
      print('Request Cancelled')
 except:
    print('Something went wrong! Try again...')


