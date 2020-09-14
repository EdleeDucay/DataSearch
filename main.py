from bsddb3 import db
from datetime import datetime
import re
import math

def open_db(name):
    # Opens the inputted database
    database = db.DB()
    database.set_flags(db.DB_DUP)
    database.open(name)
    cursor = database.cursor()

    return database, cursor

def read_db(name):
    # Reads the values of a database
    database, cursor = open_db(name)
    data = []
    
    iter = cursor.first()
    while (iter):
        print(iter)
        data.append(iter)
        iter = cursor.next()

    return data

def main():
    reviews, r_cur = open_db('rw.idx')
    rterms, rt_cur = open_db('rt.idx')
    pterms, pt_cur = open_db('pt.idx')
    scores, sc_cur = open_db('sc.idx')
    outfull = False

    
    while True:
        badc = False
        modechange = False
        emptyterms = True
        termc = False

        datec = False
        hdate = math.inf
        ldate = 0

        pricec = False
        hprice = math.inf
        lprice = 0

        prices = []
        terms = set()

        c = " " + input("Enter commands: ").lower() + " "
        if c.strip() == "output=brief":
            modechange = True
            outfull = False
        elif c.strip() == "output=full":
            modechange = True
            outfull = True
        elif c.strip() == "exit()":
            break
        else:
            commands = re.findall('((?:date\s*(?:>|<){1}\s*\d{4}/\d{2}/\d{2})|(?:(?:pterm|rterm)\s*:\s*[a-zA-Z0-9]+%?)|(?:(?:score|price)\s*(?:>|<){1}\s*\d+))', c)
            line = re.sub('((?:date\s*(?:>|<){1}\s*\d{4}/\d{2}/\d{2})|(?:(?:pterm|rterm)\s*:\s*[a-zA-Z0-9]+%?)|(?:(?:score|price)\s*(?:>|<){1}\s*\d+))', '!', c)
            keys = line.split()
            for k in keys:
                if re.match('(^[a-zA-Z0-9]+%?$)|(^!$)', k):
                    if re.match('(^[a-zA-Z0-9]+%?$)', k):
                        commands.append(k.strip())
                else:
                    badc = True

              
        while (len(commands) > 0 and not badc and not modechange):
            term = commands.pop(0).replace(" ", "")
            if (term.find("date", 0, 4) != -1):
                datec = True
                h = True
                if (term.find(">") != -1):
                    i = term.split(">")
                else:
                    i = term.split("<")
                    h = False
                try:
                    time = datetime.strptime(i[1], '%Y/%m/%d').timestamp()
                except:
                    print("Invalid date format given")
                    badc = True
                    break

                if (h):
                    if (ldate != 0):
                        if (ldate < time):
                            ldate = time
                    else:
                        ldate = time
                else:
                    if (hdate != math.inf):
                        if (hdate > time):
                            hdate = time
                    else:
                        hdate = time
                if (hdate != math.inf and ldate != 0 and hdate < ldate):
                    print("Date range given is invalid")
                    badc = True
                    break

            # Querying for score:
            elif (term.find("score", 0, 5) != -1):
                termc = True
                score_val = re.findall('(>|<)', term)
                term = re.split('>|<', term)                
                sc = set()
                score = sc_cur.first()
                if emptyterms:
                    while score:
                        if score_val[0] == '>':
                            if (float(score[0].decode('utf-8')) > float(term[1])):
                                terms.add(score[1])
                        elif score_val[0] == '<':
                            if (float(score[0].decode('utf-8')) < float(term[1])):
                                terms.add(score[1])
                        score = sc_cur.next()
                    emptyterms = False
                else:
                    while score:
                        if score_val[0] == '>':
                            if (float(score[0].decode('utf-8')) > float(term[1])):
                                sc.add(score[1])
                        elif score_val[0] == '<':
                            if (float(score[0].decode('utf-8')) < float(term[1])):
                                sc.add(score[1])
                        score = sc_cur.next()
                    terms = terms.intersection(sc)
                
            # Quering for price:
            elif (term.find("price", 0, 5) != -1):
                pricec = True
                h = True
                if (term.find(">") != -1):
                    i = term.split(">")
                else:
                    i = term.split("<")
                    h = False
                price = float(i[1])
                if (h):
                    if (lprice != 0):
                        if (lprice < price):
                            lprice = price
                    else:
                        lprice = price
                else:
                    if (hprice != math.inf):
                        if (hprice > price):
                            hprice = price
                    else:
                        hprice = price
                if (hprice != math.inf and lprice != 0 and hprice < lprice):
                    print("Price range given is invalid")
                    badc = True
                    break


            # Quering for rterms:
            elif (term.find("rterm", 0, 5) != -1):
                termc = True                
                term = term.split(':')                
                r = set()
                startswith = False
                if term[1].endswith('%'):
                    term[1] = term[1].replace('%', '')
                    startswith = True
                    review = rt_cur.set_range(term[1].encode("utf-8"))
                else:
                    review = rt_cur.set(term[1].encode("utf-8"))
                if emptyterms: 
                    while review:
                        if startswith and review[0].decode('utf-8').startswith(term[1]):
                            terms.add(review[1])
                        elif review[0].decode('utf-8') == term[1]:
                            terms.add(review[1])
                        review = rt_cur.next_dup()
                    emptyterms = False
                else:
                    while review:
                        if startswith and review[0].decode('utf-8').startswith(term[1]):
                            r.add(review[1])
                        elif review[0].decode('utf-8') == term[1]:
                            r.add(review[1])
                        review = rt_cur.next_dup()
                    terms = terms.intersection(r)
                
            # Querying for pterm:
            elif (term.find("pterm", 0, 5) != -1):
                termc = True
                term = term.split(':')
                p = set()
                startswith = False
                if term[1].endswith('%'):
                    term[1] = term[1].replace('%', '')
                    startswith = True
                    product = pt_cur.set_range(term[1].encode("utf-8"))
                else:
                    product = pt_cur.set(term[1].encode("utf-8"))
                if emptyterms:
                    while product:
                        if startswith and product[0].decode('utf-8').startswith(term[1]):
                            terms.add(product[1])
                        elif product[0].decode('utf-8') == term[1]:
                            terms.add(product[1])                            
                        product = pt_cur.next_dup()
                    emptyterms = False       
                else:
                    while product:
                        if startswith and product[0].decode('utf-8').startswith(term[1]):
                            p.add(product[1])
                        elif product[0].decode('utf-8') == term[1]:
                            p.add(product[1])
                        product = pt_cur.next_dup()
                    terms = terms.intersection(p)
                    
                
            else:
                t = set()
                termc = True
                startswith = False
                if term.endswith('%'):
                    term = term.replace('%', '')
                    startswith = True
                    pt = pt_cur.set_range(term.encode("utf-8"))
                    rt = rt_cur.set_range(term.encode("utf-8"))
                else:
                    pt = pt_cur.set(term.encode("utf-8"))
                    rt = rt_cur.set(term.encode("utf-8"))

                if emptyterms:                    
                    while rt or pt:
                        if startswith and pt != None and pt[0].decode('utf-8').startswith(term):
                            terms.add(pt[1])
                        elif pt != None and pt[0].decode('utf-8') == term:
                            terms.add(pt[1])
                        if startswith and rt != None and rt[0].decode('utf-8').startswith(term):
                            terms.add(rt[1])
                        elif (rt != None and rt[0].decode('utf-8') == term):
                            terms.add(rt[1])
                        if pt != None:                            
                            pt = pt_cur.next_dup()
                        if rt != None:
                            rt = rt_cur.next_dup()
                    emptyterms = False
                else:
                    while rt or pt:
                        if startswith and pt != None and pt[0].decode('utf-8').startswith(term):
                            t.add(pt[1])
                        elif pt != None and pt[0].decode('utf-8') == term:
                            t.add(pt[1])
                        if startswith and rt != None and rt[0].decode('utf-8').startswith(term):
                            t.add(rt[1])
                        elif (rt != None and rt[0].decode('utf-8') == term):
                            t.add(rt[1])
                        if pt != None:
                            pt = pt_cur.next_dup()
                        if rt != None:
                            rt = rt_cur.next_dup()
                    terms = terms.intersection(t)
                
        
        if badc:
            print("Improperly formated command")
        elif modechange:
            print("Output mode changed")
        else:
            review = r_cur.first()
            r = set()
            while review:
                conditions = True                
                if review[0] in terms or not termc:
                    rdata = re.split(''',(?=(?:[^'"]|'[^']*'|"[^"]*")*$)''', review[1].decode('utf-8'))
                    if (datec and rdata[7] == "unknown"):
                        conditions = False
                    elif (datec and (float(rdata[7]) < ldate or float(rdata[7]) > hdate)):
                        conditions = False
                    if (pricec and rdata[2] == "unknown"):
                        conditions = False
                    elif (pricec and (float(rdata[2]) < lprice or float(rdata[2]) > hprice)):
                        conditions = False

                    if conditions:
                        print("Review ID:",review[0].decode('utf-8'))
                        print("Product Title:",rdata[1])
                        print("Review Score:",rdata[6])
                        if outfull:
                            print("Product ID:",rdata[0])
                            print("Product Price:",rdata[2])
                            print("User ID:",rdata[3])
                            print("Reviewer Name:",rdata[4])
                            print("Helpfulness:",rdata[5])
                            print("Review TimeStamp:",rdata[7])
                            print("Summary:",rdata[8])
                            print("Full text:",rdata[9])
                        print("==================================================")
                        r.add(review[0])
                review = r_cur.next()
            if len(r) == 0:
                print("No results found")        
       
    reviews.close()
    rterms.close()
    pterms.close()
    scores.close()

    return

if __name__ == '__main__':
    main()
