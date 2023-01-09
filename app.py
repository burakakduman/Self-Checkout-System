from itertools import product
from operator import methodcaller
import os
from queue import Empty
from tkinter.messagebox import YES
from typing import Type
from xml.dom.minidom import TypeInfo
from xml.etree.ElementTree import tostring
from flask import Flask, request, jsonify, render_template, url_for
from firebase_admin import credentials, firestore, initialize_app
import json

# Initialize Flask app
app = Flask(__name__)
xlist=[]
# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
todo_ref = db.collection('Urunler')
document=db.collection("Urunler").document("1")


# SPECIAL GET
@app.route('/',methods=["GET","POST"])
def working():
    
    
    if request.method=="POST":
        product_name = request.form 
        if(product_name["action"]=="sepet"):
            total=0
            for item in xlist:
                total+=int(item["urun_ucret"])
            return render_template("urun.html",xlist=xlist,listlen=len(xlist),total=total)
        else:
            s=product_name["name"]
            datas=todo_ref.stream()
            for data in datas:
                if s == data.id:
                    products=data.to_dict()
                    xlist.append(products)
                    
                   
                    
                    return render_template("index.html",xlist=xlist)
          
        #toplam=sum(xlist)
    return render_template("index.html")

#TEMİZLEME
@app.route('/temiz', methods=["GET","POST"])
def temiz():
    xlist.clear()
    return render_template("urun.html", xlist=xlist)

@app.route("/teksil", methods=["GET","POST"])
def sil():
    if request.method == "POST":
        c=0
        for x in xlist:
            if request.form["action"] == "silme"+str(c):
                del xlist[c]
                return render_template("urun.html",xlist=xlist)
            c=c+1
    return render_template("urun.html",xlist=xlist)

#Ürünleri Kart Sayfasıne Gönderme
@app.route("/gonder", methods =['GET','POST'])
def gönder():
    if request.method == "POST":
        return render_template("cardeme.html",xlist=xlist)

#Ürün Ekleme
@app.route("/users", methods =['GET','POST'])
def users():
    if request.method == "POST":
        data = request.form
        todo_ref.document(data["stok_no"]).set(data)
        
    return render_template("add.html")

# GET ALL
@app.route('/list', methods=['GET'])
def read():
    try:
        todo_id = request.form
        if todo_id:
            todo = todo_ref.document(todo_id).get()
            return jsonify(todo.to_dict()), 200
        else:
            all_todos = [doc.to_dict() for doc in todo_ref.stream()]
            return jsonify(all_todos), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

# UPDATE
@app.route('/update', methods=['POST', 'PUT'])
def update():
    try:
        id = request.json['id']
        todo_ref.document(id).update(request.json)
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

# DELETE
@app.route('/delete', methods=['GET', 'DELETE'])
def delete():
    try:
        todo_id = request.args.get('id')
        todo_ref.document(todo_id).delete()
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An Error Occurred: {e}"

# CONNECTION IP CONFIG
port = int(os.environ.get('PORT', 8080))
if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=port)