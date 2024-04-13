from flask import render_template,request
from models import app,db,Customer,Item,Purchase,Purchase_detail
import sqlalchemy
from sqlalchemy import func
from datetime import datetime

#ページ遷移
#1.トップページ
@app.route("/")
def index():
    customers = Customer.query.all()
    return render_template("1_index.html",customers=customers)
#2.商品管理ページ
@app.route("/item")
def item():
    items = Item.query.all()
    return render_template("2_item.html",items=items)
#3.商品管理ページ
@app.route("/purchase")
def purchase():
    customers = Customer.query.all()
    items = Item.query.all()
    return render_template("3_purchase.html",customers=customers,items=items)

#4.統計ページ
@app.route("/purchase_data_statistics")
def purchase_data_statistics():
    joined_purchase_details = db.session.query(Purchase,Purchase_detail).join(Purchase_detail,Purchase.purchase_id==Purchase_detail.purchase_id).all()
    joined_purchase_details = db.session.query(Purchase,Purchase_detail,Customer).join(Purchase_detail,Purchase.purchase_id==Purchase_detail.purchase_id).join(Customer,Purchase.customer_id==Customer.customer_id).all()
    joined_purchase_details = db.session.query(Purchase,Purchase_detail,Customer,Item).join(Purchase_detail,Purchase.purchase_id==Purchase_detail.purchase_id).join(Customer,Purchase.customer_id==Customer.customer_id).join(Item,Purchase_detail.item_id==Item.item_id).all()
    customers = Customer.query.all()
    return render_template("4_purchase_data_statistics.html",joined_purchase_details=joined_purchase_details,customers=customers)

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

#1-2 性別で抽出
@app.route("/select_gender",methods=["POST"])
def select_gender():
    gender = request.form["input-gender2"]
    customers = Customer.query.filter(Customer.gender==gender).all()
    return render_template("1-2_result_select_gender.html",customers=customers)

#2-1 商品登録
@app.route("/add_item",methods=["POST"])
def add_item():
    item_id = request.form["input-item-id"]
    item_name = request.form["input-item-name"]
    price = request.form["input-price"]

    item = Item(item_id,item_name,price)
    try:
        db.session.add(item)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return render_template("error.html")    
    return render_template("2-1_confirm_added_item.html",item=item)

#2-2 商品削除
@app.route("/delete_item",methods=["POST"])
def delete_item():
    item_id = request.form["input-item-id"]
    item = Item.query.filter_by(item_id=item_id).first()
    try:
        db.session.delete(item)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return render_template("error.html")    
    return render_template("2-2_confirm_deleted_item.html",item=item)

#2-3 商品更新
@app.route("/update_item",methods=["POST"])
def update_item():
    item_id = request.form["input-item-id"]
    update_item_name = request.form["input-item-name"]
    update_price = request.form["input-item-price"]

    item = Item.query.filter_by(item_id=item_id).first()
    try:
        item.item_name = update_item_name
        item.price = update_price
        db.session.add(item)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return render_template("error.html")    
    return render_template("2-3_confirm_updated_item.html",item=item)

#2-4 商品名で抽出
@app.route("/select_item_name",methods=["POST"])
def select_item_name():
    item_name = request.form["input-item-name"]
    select_target = "%{}%".format(item_name)

    result_type="抽出"

    items = Item.query.filter(Item.item_name.like(select_target)).all()
    return render_template("2-4_result_items.html",items=items,result_type=result_type)

#2-5　単価で並び替え
@app.route("/sorting_item",methods=["POST"])
def sorting_item():
    order_type = request.form["order-type"]
    if order_type =="ascending":
        items = Item.query.order_by(Item.price)
    else:
        items = Item.query.order_by(Item.price.desc())
    
    result_type="並び替え"

    return render_template("2-4_result_items.html",items=items,result_type=result_type)

#3 購入情報登録
@app.route("/add_purchase",methods=["POST"])
def add_purchase():
    customer_name = request.form["input-customer-name"]
    item_name1 = request.form["input-item-name1"]
    quantity1 = request.form["input-quantity1"]
    item_name2 = request.form["input-item-name2"]
    quantity2 = request.form["input-quantity2"]
    date = request.form["input-date"]
    date = datetime.strptime(date,"%Y-%m-%d")

    customer = Customer.query.filter_by(customer_name=customer_name).first()
    purchase = Purchase(customer.customer_id,date)
    try:
        db.session.add(purchase)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return render_template("error.html")
    
    item1 = Item.query.filter_by(item_name=item_name1).first()
    purchase_detail = Purchase_detail(purchase.purchase_id,item1.item_id,quantity1)
    try:
        db.session.add(purchase_detail)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return render_template("error.html")
    
    if item_name2:
        item2 = Item.query.filter_by(item_name=item_name2).first()
        purchase_detail = Purchase_detail(purchase.purchase_id,item2.item_id,quantity2)
        try:
            db.session.add(purchase_detail)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            return render_template("error.html")


    return render_template("3-1_confirm_purchase.html",purchase=purchase)

#3-2.購入情報削除
@app.route("/delete_purchase",methods=["POST"])
def delete_purchase():
    purchase_id = request.form["input-purchase-id"]
    purchase = Purchase.query.filter_by(purchase_id=purchase_id).first()
    try:
        db.session.delete(purchase)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        return render_template("error.html")    
    return render_template("3-2_confirm_deleted_purchase.html",purchase=purchase)

#4.1.購入情報検索
@app.route("/search_purchase",methods=["POST"])
def search_purchase():
    item_name = request.form["input-item-name"]
    customer_name = request.form["input-customer-name"]
    date = request.form["input-date"]

    if item_name:
        search_target = "%{}%".format(item_name)
        items = Item.query.filter(Item.item_name.like(search_target)).all()
        item_id_list = []
        for item in items:
            item_id_list.append(item.item_id)
    if customer_name:
        customer = Customer.query.filter_by(customer_name=customer_name).first()
        customer_id = customer.customer_id
    else:
        customer = None
    if date:
        date = datetime.strptime(date,"%Y-%m-%d")
    
    is_customer_or_date =True
    if customer and date:
        purchases = Purchase.query.filter(Purchase.customer_id==customer_id,Purchase.date==date).all()
    elif customer:
        purchases = Purchase.query.filter(Purchase.customer_id==customer_id).all()
    elif date:
        purchases = Purchase.query.filter(Purchase.date==date).all()
    else:
        is_customer_or_date = False

    if is_customer_or_date:
       
       purchase_id_list = []
       #for purchase in purchases:
       #    purchase_id_list.append(purchase.purchase_id)
       purchase_id_list = [purchase.purchase_id for purchase in purchases] 

    if is_customer_or_date and item_name:
        purchase_details = Purchase_detail.query.filter(Purchase_detail.item_id.in_(item_id_list),Purchase_detail.purchase_id.in_(purchase_id_list)).all()
        return render_template("4-1_result_search_purchase.html",purchase_details=purchase_details)
    elif is_customer_or_date:
        purchase_details = Purchase_detail.query.filter(Purchase_detail.purchase_id.in_(purchase_id_list)).all()
        return render_template("4-1_result_search_purchase.html",purchase_details=purchase_details)
    elif item_name:
        purchase_details = Purchase_detail.query.filter(Purchase_detail.item_id.in_(item_id_list)).all()
        return render_template("4-1_result_search_purchase.html",purchase_details=purchase_details)
    else:
        return render_template("error.html")
#4-2総顧客数算出
@app.route("/count_customers",methods=["POST"])
def count_customers():
    statistics_type ="総顧客数"
    number_of_customers = db.session.query(Customer).count()
    result = str(number_of_customers)+"人"
    return render_template("4-2_result_statistics.html",statistics_type=statistics_type,result=result)

#4-3総販売商品数量算出
@app.route("/count_quantity",methods=["POST"])
def count_quantity():
    statistics_type ="総販売商品数量"
    total_quantity = db.session.query(func.sum(Purchase_detail.quantity)).first()
    for row in total_quantity:
        result = row
    result = str(int(result))+"個"
    return render_template("4-2_result_statistics.html",statistics_type=statistics_type,result=result)

if __name__ =="__main__":
    app.run(debug=True)