import csv
from flask import Flask, redirect, render_template, request, send_file
import transfer

app = Flask(__name__,)

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method =="GET":
        rows=[]
        with open('allotment.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                rows.append(row)
        return render_template('p1.html',rows=rows)
        
    elif request.method=='POST':
        transfer.teacher_transfer()
        path='teacher_time_tables.xlsx'
        return send_file(path, as_attachment=True)
    


@app.route("/<action>/<id>", methods=['GET', 'POST'])
def view_update_delete(action, id):
    if request.method =="GET":
        sections=[]

        days=[]
        with open('days.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                days.append(row[0])
        with open('sections.csv', 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    sections.append(row[0])
        if action=='add':
            temp=[id,"","","","","",""]
        elif action=='view':
            temp=[]
            with open('allotment.csv', 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    if row[0]==id:
                        temp=row
                        temp[3]=int(temp[3])
                        temp[5]=int(temp[5])
                        break
        return render_template('p2.html', row=temp, action=action, sections=sections, days=days)
    
    elif request.method == "POST" :
        if action=='save':
            fname=request.form.get("fname")
            cname=request.form.get("cname")
            sem=request.form.get("sem")
            sec=request.form.get("sec")
            period=request.form.get("period")
            day=request.form.get("day")

            rows=[]
            with open('allotment.csv', 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    rows.append(row)
            f = open("allotment.csv", "w")
            f.close()
            for row in rows:
                if row[0]!=id:
                    with open('allotment.csv', 'a') as csvfile:
                        csvwriter = csv.writer(csvfile) 
                        csvwriter.writerow(row)
                    
            with open('allotment.csv', 'a') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow([id,fname,cname,sem,sec,period,day])

        else: 
            rows=[]
            with open('allotment.csv', 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    rows.append(row)
            f = open("allotment.csv", "w")
            f.close()
            for row in rows:
                if row[0]!=id:
                    with open('allotment.csv', 'a') as csvfile:
                        csvwriter = csv.writer(csvfile) 
                        csvwriter.writerow(row)
        return redirect('/')
        

@app.route("/add")
def add_course():
    ids=[]
    with open('allotment.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            ids.append(row[0])
    ids.sort()
    id=0
    for i in ids:
        if int(i)!=id:
            break
        id+=1
    return redirect('/add/'+str(id))