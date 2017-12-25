# -*- coding: utf-8 -*-
import sqlite3
import re

chk_id = int(raw_input('Enter the ID : '))
print "start to verify about ID", chk_id

conn = sqlite3.connect('taxdata2.sqlite')
cur = conn.cursor()

#collect data
cur.execute("SELECT * FROM emp WHERE ID = ? ;", (chk_id, ))
empdata = cur.fetchone()
print "Employee information :", empdata

cur.execute("SELECT * FROM emp_deduct WHERE emp_ID = ? ;", (chk_id, ))
empset = cur.fetchone()
print "Employee set option :", empset

cur.execute("SELECT * FROM fml WHERE emp_ID = ? ;", (chk_id, ))
fmlst = cur.fetchall()
print "Family information :", fmlst

fmlset = list() ; b = 0
for z in fmlst :
    fmlset.append(z[0])
for z in fmlset :
    cur.execute("SELECT * FROM fml_deduct WHERE fml_ID = ? ;", (z, ))
    a = cur.fetchone()
    fmlset[b] = a
    b += 1
print "Family set option :", fmlset

#initialize values
cur.execute("UPDATE final SET Person = 0 WHERE emp_ID = ? ;", (chk_id, ))
cur.execute("UPDATE final SET Special = 0 WHERE emp_ID = ? ;", (chk_id, ))
cur.execute("UPDATE final SET Etc = 0 WHERE emp_ID = ? ;", (chk_id, ))
cur.execute("UPDATE emp SET After_Tax = 0 WHERE ID = ? ;", (chk_id, ))
print "Value is initialized"

#varify data - personal
cur.execute("UPDATE final SET Person = 1500000 WHERE emp_ID = ? ;", (chk_id, ))
print "Employee is reflected"
if len(fmlst) > 0 :
    startnum = fmlst[0][0]
perlst = list()
for z in fmlset :
    if z[1] == 1 :
        perlst.append(z)
print "Test target :", perlst
ytest = [1,2,5,6] ; stest = [1,3,5,7]
percount = 0 ; kidcount = 0
for z in perlst :
    if z[0] == fmlst[z[0]-startnum][0] :
        if fmlst[z[0]-startnum][3] == 1 :
            cur.execute("UPDATE final SET Person = Person + 1500000 WHERE emp_ID = ? ;", (chk_id, ))
            percount += 1
            print "Family ID", z[0], "wife reflected"

        elif fmlst[z[0]-startnum][3] == 2 :
            c = int(fmlst[z[0]-startnum][2][7])
            d = str(fmlst[z[0]-startnum][2][:2])
            if c in ytest :
                ydump=['19']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            else :
                ydump=['20']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            if ydump >= 1997 :
                cur.execute("UPDATE final SET Person = Person + 1500000 WHERE emp_ID = ? ;", (chk_id, ))
                percount += 1
                kidcount += 1
                print "Family ID", z[0], "is reflected"
            else :
                print "Family ID", z[0], "is rejected"

        elif fmlst[z[0]-startnum][3] == 3 :
            c = int(fmlst[z[0]-startnum][2][7])
            d = str(fmlst[z[0]-startnum][2][:2])
            if c in ytest :
                ydump=['19']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            else :
                ydump=['20']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            if ydump <= 1957 :
                cur.execute("UPDATE final SET Person = Person + 1500000 WHERE emp_ID = ? ;", (chk_id, ))
                percount += 1
                print "Family ID", z[0], "is reflected"
            else :
                print "Family ID", z[0], "is rejected"

        elif fmlst[z[0]-startnum][3] == 4 :
            c = int(fmlst[z[0]-startnum][2][7])
            d = str(fmlst[z[0]-startnum][2][:2])
            if c in ytest :
                ydump=['19']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            else :
                ydump=['20']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            if ydump >= 1997 or ydump <= 1957 :
                cur.execute("UPDATE final SET Person = Person + 1500000 WHERE emp_ID = ? ;", (chk_id, ))
                percount += 1
                print "Family ID", z[0], "is reflected"
            else :
                print "Family ID", z[0], "is rejected"

        elif fmlst[z[0]-startnum][3] == 5 :
            cur.execute("UPDATE final SET Person = Person + 1500000 WHERE emp_ID = ? ;", (chk_id, ))
            percount += 1
            print "Family ID", z[0], "basic reflected"

        elif fmlst[z[0]-startnum][3] == 6 :
            c = int(fmlst[z[0]-startnum][2][7])
            d = str(fmlst[z[0]-startnum][2][:2])
            if c in ytest :
                ydump=['19']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            else :
                ydump=['20']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            if ydump >= 2000 :
                cur.execute("UPDATE final SET Person = Person + 1500000 WHERE emp_ID = ? ;", (chk_id, ))
                percount += 1
                print "Family ID", z[0], "is reflected"
            else :
                print "Family ID", z[0], "is rejected"

        else :
            print "Relation is wrong"

print percount, "person,", kidcount, "kid is reflected"

if kidcount >= 2 :
    kidadd = 1000000 + (2000000 * (kidcount - 2))
    cur.execute("UPDATE final SET Person = Person + ? WHERE emp_ID = ? ;", (kidadd, chk_id))
    print "Additional deduct is reflected by two more kids", kidadd
else :
    print "No Additional deduct is reflected by two more kids"

if empset[1] is not None :
    e = str(empset[1])
    delimiter = ','
    e = e.split(delimiter)
    print e
    if 'P1' in e :
        c = int(empdata[1][7])
        d = str(empdata[1][:2])
        if c in ytest :
            ydump=['19']
            ydump.append(d)
            delimiter = ''
            ydump = int(delimiter.join(ydump))
            print ydump, type(ydump)
        else :
            ydump=['20']
            ydump.append(d)
            delimiter = ''
            ydump = int(delimiter.join(ydump))
            print ydump, type(ydump)
        if ydump <= 1947 :
            cur.execute("UPDATE final SET Person = Person + 1000000 WHERE emp_ID = ? ;", (chk_id, ))
            print "Employee is reflected P1"
        else :
            print "Employee is rejected P1"

    if 'P2' in e :
        cur.execute("UPDATE final SET Person = Person + 2000000 WHERE emp_ID = ? ;", (chk_id, ))
        print "Employee is reflected P2"

    if 'P3' in e :
        c = int(empdata[1][7])
        if c in stest :
            print "P3 is only for woman"
        else :
            d = empdata[2]
            if d == 1 :
                cur.execute("UPDATE final SET Person = Person + 500000 WHERE emp_ID = ? ;", (chk_id, ))
                P3test = 1
                print "Employee is reflected P3"
            elif percount > 0 :
                cur.execute("UPDATE final SET Person = Person + 500000 WHERE emp_ID = ? ;", (chk_id, ))
                P3test = 1
                print "Employee is reflected P3"
            else :
                print "Employee is rejected P3"

    if 'P4' in e :
        print "Employee can't P4"

    if 'P5' in e :
        print "Employee can't P5"

    if 'P6' in e :
        d = empdata[2]
        if d == 1 :
            print "P3 is only for single"
        elif kidcount > 0 and P3test == 0 :
            cur.execute("UPDATE final SET Person = Person + 1000000 WHERE emp_ID = ? ;", (chk_id, ))
            print "Employee is reflected P6"
        elif kidcount > 0 and P3test == 1 :
            cur.execute("UPDATE final SET Person = Person + 500000 WHERE emp_ID = ? ;", (chk_id, ))
            print "Employee is reflected P6 and is rejected P3"
        else :
            print "Employee is rejected P6"
else :
    print "Employee did not set"

perlst = []
for z in fmlset :
    if z[2] is not None :
        perlst.append(z)
print "Test target :", perlst

for z in perlst :
    if z[0] == fmlst[z[0]-startnum][0] :
        perdump = [z[0]]
        e = str(z[2])
        delimiter = ','
        e = e.split(delimiter)
        perdump = perdump + e
        print perdump
        if 'P1' in perdump :
            c = int(fmlst[z[0]-startnum][2][7])
            d = str(fmlst[z[0]-startnum][2][:2])
            if c in ytest :
                ydump=['19']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            else :
                ydump=['20']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            if ydump <= 1947 :
                cur.execute("UPDATE final SET Person = Person + 1000000 WHERE emp_ID = ? ;", (chk_id, ))
                print "Family ID", z[0], "is reflected P1"
            else :
                print "Family ID", z[0], "is rejected P1"

        if 'P2' in perdump :
            cur.execute("UPDATE final SET Person = Person + 2000000 WHERE emp_ID = ? ;", (chk_id, ))
            print "Family ID", z[0], "is reflected P2"

        if 'P3' in perdump :
            print "Family can't P3"

        if 'P4' in perdump :
            c = int(fmlst[z[0]-startnum][2][7])
            d = str(fmlst[z[0]-startnum][2][:2])
            if c in ytest :
                ydump=['19']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            else :
                ydump=['20']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            if ydump >= 2011 :
                cur.execute("UPDATE final SET Person = Person + 1000000 WHERE emp_ID = ? ;", (chk_id, ))
                print "Family ID", z[0], "is reflected P4"
            else :
                print "Family ID", z[0], "is rejected P4"

        if 'P5' in perdump :
            c = int(fmlst[z[0]-startnum][2][7])
            d = str(fmlst[z[0]-startnum][2][:2])
            if c in ytest :
                ydump=['19']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            else :
                ydump=['20']
                ydump.append(d)
                delimiter = ''
                ydump = int(delimiter.join(ydump))
                print ydump
            if ydump == 2017 :
                cur.execute("UPDATE final SET Person = Person + 2000000 WHERE emp_ID = ? ;", (chk_id, ))
                print "Family ID", z[0], "is reflected P5"
            else :
                print "Family ID", z[0], "is rejected P5"

        if 'P6' in perdump :
            print "Family can't P6"

    else :
        print "Family did not set"

#varify data - Special
pens = [4000000, empset[2]]
mpen = min(pens)
cur.execute("UPDATE final SET Special = Special + ? WHERE emp_ID = ? ;", (mpen, chk_id))
print "Pension is reflected", mpen

#Insurence
perlst = []
perlst.append(empset)
for z in fmlset :
    if z[1] == 1 and z[3] is not None :
        perlst.append(z)
print "Test target :", perlst

for z in perlst :
    inslst = [1000000, z[3]]
    mins = min(inslst)
    cur.execute("UPDATE final SET Special = Special + ? WHERE emp_ID = ? ;", (mins, chk_id))
    print "Insure is reflected", mins

#Medical
mainmedi = 0 ; etcmedi = 0 ; tmedi = 0 ; fmedi = 0
if empset[4] is not None :
    mainmedi = empset[4]
for z in fmlset :
    if z[4] is not None :
        e = str(z[2])
        delimiter = ','
        e = e.split(delimiter)
        if 'P1' in e or 'P2' in e :
            mainmedi += z[4]
        else :
            etcmedi += z[4]
print "Main :", mainmedi, "etc :", etcmedi
tmedi = mainmedi + etcmedi
cmedi = empdata[4] * 0.03

if tmedi > cmedi :
    if etcmedi >= cmedi :
        fmedi += mainmedi
        f = etcmedi - cmedi
        mdump = [7000000]
        mdump.append(f)
        fmedi += min(mdump)
    else :
        fmedi += mainmedi -(cmedi - etcmedi)
cur.execute("UPDATE final SET Special = Special + ? WHERE emp_ID = ? ;", (fmedi, chk_id))
print "Medical is reflected", fmedi

#Education 5
if empset[5] is not None :
    cur.execute("UPDATE final SET Special = Special + ? WHERE emp_ID = ? ;", (empset[5], chk_id))
    print "Employee's Education is reflected", empset[5]
perlst = []
for z in fmlset :
    if z[5] is not None :
        perlst.append(z)
print "Test target ", perlst
for z in perlst :
    if z[0] == fmlst[z[0]-startnum][0] :
        if fmlst[z[0]-startnum][3] == 3 :
            if fmlst[z[0]-startnum][4] == 'E5' :
                cur.execute("UPDATE final SET Special = Special + ? WHERE emp_ID = ? ;", (z[5], chk_id))
                print "Dis-edu is reflected", z[5]
            else :
                print "Ancestor can not edu"
        else :
            if fmlst[z[0]-startnum][4] == 'E1' or fmlst[z[0]-startnum][4] == 'E2' :
                edump = [3000000]
                edump.append(z[5])
                medu = min(edump)
                cur.execute("UPDATE final SET Special = Special + ? WHERE emp_ID = ? ;", (medu, chk_id))
                print z[0], "Education is reflected", medu
            elif fmlst[z[0]-startnum][4] == 'E3' :
                edump = [9000000]
                edump.append(z[5])
                medu = min(edump)
                cur.execute("UPDATE final SET Special = Special + ? WHERE emp_ID = ? ;", (medu, chk_id))
                print z[0], "Education is reflected", medu
            elif fmlst[z[0]-startnum][4] == 'E4' :
                print "Graduate school is only for Employee"
            elif fmlst[z[0]-startnum][4] == 'E5' :
                cur.execute("UPDATE final SET Special = Special + ? WHERE emp_ID = ? ;", (z[5], chk_id))
                print "Dis-edu is reflected", z[5]

#varify data - Etc
#Epension
if empset[7] is not None :
    epen = [720000, empset[7] * 0.4]
    mpen = min(epen)
    cur.execute("UPDATE final SET Etc = Etc + ? WHERE emp_ID = ? ;", (mpen, chk_id))
    print "EPension is reflected", mpen

#credit
tcredit = empset[6] ; ccredit = empdata[4] * 0.25 ; fcredit = 0
crelst = [empset[6]*0.2, 3000000]
perlst = []
for z in fmlset :
    if z[6] is not None :
        perlst.append(z)
print "Test target :", perlst
for z in perlst :
    if z[0] == fmlst[z[0]-startnum][1] :
        if fmlst[z[0]-startnum][3] in [1,2,3] :
            if z[1] == 1 :
                tcredit += z[6]
                print "Credit is reflected", z[6]
            else :
                print "income not yet"
        else :
            print z[0], "is rejected"

fcredit = tcredit - ccredit
crelst.append(fcredit)
mcre = min(crelst)
cur.execute("UPDATE final SET Etc = Etc + ? WHERE emp_ID = ? ;", (mcre, chk_id))
print "Credit is reflected", mcre

#show data
cur.execute("SELECT * FROM final WHERE emp_ID = ? ;", (chk_id, ))
dedval = cur.fetchone()
print "Reflected data :", dedval

#compute tax value
tincome = empdata[4]
for z in dedval[1:] :
    tincome += - z
if dedval[2] > 25000000 :
    tincome += dedval[2] - 25000000

if tincome < 0 :
    ftax = tincome
    tincome = 0
else :
    if tincome <= 12000000 :
        ftax = tincome * 0.06
    elif tincome <= 46000000 :
        ftax = tincome * 0.15 - 1080000
    elif tincome <= 88000000 :
        ftax = tincome * 0.24 - 5220000
    elif tincome <= 300000000 :
        ftax = tincome * 0.35 - 14900000
    else :
        ftax = tincome * 0.38 - 23900000
    tincome += -ftax
print tincome, ftax
cur.execute("UPDATE emp SET After_Tax = ? WHERE ID = ? ;", (tincome, chk_id))



conn.commit()
cur.close()
