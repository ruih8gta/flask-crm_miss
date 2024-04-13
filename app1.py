from flask import render_template,request
from models import app,db,Customer
import sqlalchemy

#ページ遷移
@app.route("/")
def index():
    customers = Customer.query.all()
    return render_template("1_index.html",customers=customers)

@app.route("/item")
def item():
    return render_template("2_item.html")

#機能
@app.route("/add_customer",methods=["POST"])
def add_customer():
    customer_id = request.form["input-customer-id"]
    customer_name = request.form["input-customer-name"]
    age = request.form["input-age"]
    gender = request.form["input-gender"]

    customer = Customer(customer_id,customer_name,age,gender)
    try:
        db.session.add(customer)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return render_template("error.html")    
    return render_template("1-1_confirm_added_customer.html",customer=customer)

@app.route("/select_gender",methods=["POST"])
def select_gender():
    gender = request.form["input-gender2"]
    customers = Customer.query.filter(Customer.gender==gender).all()
    return render_template("1-2_result_select_gender.html",customers=customers)



if __name__ =="__main__":
    app.run(debug=True)