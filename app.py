import MySQLdb
from flask import Flask,render_template, redirect,url_for,request
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'poasMn11@'
app.config['MYSQL_DB'] = 'petty_kadai'

mysql = MySQL(app)

@app.route('/',methods=['GET','POST'])
def welcome():
    return render_template('welcome.html')

@app.route('/wel',methods=['POST','GET'])
def wel():
    if request.method=='POST':
      cash_balance=request.form['cash_balance']
      company_name=request.form['company_name']
      cur=mysql.connection.cursor()
      cur.execute("Insert into company(cash_balance,company_name) VALUES(%s,%s)",[cash_balance,company_name])
      mysql.connection.commit()
      cur.close()
    return render_template('secon.html')
    

@app.route('/second',methods=['GET','POST'])
def second():
    if request.method=='POST':
     return render_template('secon.html')
    
@app.route('/add_item',methods=['POST','GET'])
def add_item():
   return render_template('additem.html')

@app.route('/submitadd',methods=['GET','POST'])
def submitadd():
   if request.method=='POST':
      item_id=request.form.get('item_id')
      item_name=request.form.get('item_name')
      qty=request.form.get('qty')
      cur=mysql.connection.cursor()
      cur.execute("insert into ite(item_id,item_name,qty) VALUES(%s,%s,%s)",(item_id,item_name,qty))
      mysql.connection.commit()
      mysql.connection.close()
   return render_template('sucess.html') 
      
   
@app.route('/purchase',methods=['GET','POST'])
def purchase():
      return render_template('purchase.html')
   
@app.route('/submitpur',methods=['POST','GET']) 
def submitpur():
      if request.method=='POST':
         purchase_id=request.form.get('purchase_id')
         timestam=request.form.get('timestam')
         item_id=request.form.get('item_id')
         qty=request.form.get('qty')
         rate=request.form.get('rate')
         amount=float(request.form.get('amount'))

         cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)

         cur.execute('SELECT item_id FROM ite where item_id=%s',(item_id))
         result=cur.fetchone()
         if result:
           cur.execute("Insert into purcha(purchase_id,timestam,item_id,qty,rate,amount) VALUES(%s,%s,%s,%s,%s,%s)",[purchase_id,timestam,item_id,qty,rate,amount])
           mysql.connection.commit()
           cur.execute("""UPDATE ite SET ite.qty=ite.qty+(%s) where ite.item_id=%s""",(qty,item_id,))
           mysql.connection.commit()
           return "Done"
         else:
           cur.execute('INSERT INTO ite(item_id,quantity) VALUES(%s,%s)',[item_id,qty])
           mysql.connection.commit()
           cur.execute('INSERT INTO purcha(purchase_id,timestam,item_id,qty,rate,amount) VALUES (%s,%s,%s,%s,%s,%s,%s)',(purchase_id,timestam,item_id,qty,rate,amount))
           mysql.connection.commit()
           return "Done"
      cur.execute("""UPDATE company SET cash_balance=cash_balance+%s""",(amount,))
      mysql.connection.commit()
      mysql.connection.close()
      return "updated"
         
   
@app.route('/sales',methods=['GET','POST'])
def sales():
   return render_template('sales.html')

@app.route('/submitsal',methods=['POST','GET'])
def submitsal():
   if request.method=='POST':
      sales_id=request.form.get('sales_id')
      timestamp=request.form.get('timestamp')
      item_id=request.form.get('item_id')
      qty=request.form.get('qty')
      rate=request.form.get('rate')
      amount=float(request.form.get('amount'))

      
      cur=mysql.connection.cursor(MySQLdb.cursors.DictCursor)

      cur.execute('SELECT item_id FROM ite where item_id=%s',(item_id))
      result=cur.fetchone()
      if result:
         cur.execute("Insert into sales(sales_id,timestamp,item_id,qty,rate,amount) values(%s,%s,%s,%s,%s)",[sales_id,timestamp,item_id,qty,rate,amount])
         mysql.connection.commit()
         cur.execute("""UPDATE ite SET ite.qty=ite.qty+(%s) where ite.item_id=%s""",(qty,item_id,))
         mysql.connection.commit()
         return "Done"
      else:
         cur.execute('INSERT INTO ite(item_id,quantity) VALUES(%s,%s)',[item_id,qty])
         mysql.connection.commit()
         cur.execute("insert into sales(sales_id,timestamp,item_id,qty,rate,amount) values(%s,%s,%s,%s,%s)",[sales_id,timestamp,item_id,qty,rate,amount])
         mysql.connection.commit()
         return "Done"
      
   cur.execute("""UPDATE company SET cash_balance=cash_balance-%s""",(amount))
   mysql.connection.commit()
   mysql.connection.close()
   return "updated"
         

if __name__==('__main__'):
    app.run(debug=True)