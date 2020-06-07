
from flask import Flask, render_template, request, redirect, url_for
import datetime
from database import Database

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/addEntry')
def addEntry():
    return render_template('addEntry.html')

@app.route('/addEntryDB')
def addEntryDB(): 
    name = request.form['name']
    contact = request.form['contact']
    therapy = request.form.getlist('therapy')
    staff = request.form['staff']
    total = request.form['total']
    entry = {
        'name': name,
        'contact': contact,
        'therapy': therapy,
        'staff': staff,
        'transaction_details' : {
            'subtotal': request.form['subtotal'],
            'tax': request.form['tax'],
            'discount': request.form['discount'],
            'total': request.form['total']
        },
        'pay_method': request.form['pay_method'],
        'date': datetime.datetime.utcnow()
    }
    Database.insert(collection='entry', query = entry)
    return redirect(url_for('dashboard'))

@app.route('/search', methods=['GET'])
def search():
    sdate = datetime.datetime(2019, 1, 1)
    edate = datetime.datetime.now()
    if request.args.get('date1') is not None or request.args.get('date1')=="":
        sdate = datetime.datetime.strptime(request.args.get('date1'),'%Y-%m-%d')
        edate = datetime.datetime.strptime(request.args.get('date2'),'%Y-%m-%d') + datetime.timedelta(days=1)

    entries = Database.find(collection='entry', query =  {
        'date': { '$gte': sdate, '$lt': edate }
    })
    return render_template("search.html", Entries= entries)

@app.route('/addEnquiry')
def enquiry():
    return render_template("addEnquiry.html")

@app.route('/addEnquiryDB', methods=['POST'])
def addenquiry():
    name = request.form['name']
    contact = request.form['contact']
    source = request.form['source']

    enquiry = {
        'name': name,
        'contact': contact,
        'source': source,
        'date': datetime.datetime.utcnow()
    }
    Database.insert(collection='enquiry', data=enquiry)
    return redirect(url_for('dashboard'))

@app.route('/view', methods=['GET'])
def view():
    sdate = datetime.datetime(2019, 1, 1)
    edate = datetime.datetime.now()
    if request.args.get('date1') is not None or request.args.get('date1')=="":
        sdate = datetime.datetime.strptime(request.args.get('date1'),'%Y-%m-%d')
        edate = datetime.datetime.strptime(request.args.get('date2'),'%Y-%m-%d') + datetime.timedelta(days=1)

    enquiries = Database.find(collection='enquiry', query = {
        'date': { '$gte': sdate, '$lt': edate }
    })
    return render_template("view.html", Enquiries= enquiries)


if __name__ == '__main__':
	app.run()
