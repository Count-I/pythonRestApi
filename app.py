from flask import Flask, jsonify, request, json
from products import products
import os
import urllib.request
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def ping():
    return jsonify({"message":"Welcome Home"})

@app.route('/products/')
def getProducts():
    return jsonify({"products": products})

@app.route('/products/a/')
def getProducta():
    return jsonify({"product": products[0]})

@app.route('/products/<string:product_name>/')
def getProduct(product_name):
    productsFound = [product for product in products if product['name']==product_name]
    if (len(productsFound)>0):
        return jsonify({"product": productsFound[0]})
    return jsonify({"message": "product not found"})

@app.route('/products/', methods=['POST'])
def addProduct():
    new_product = {
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(new_product)
    return jsonify({"message": "product added successfully", "products": products})



#MULTIPART POST -----------------------------------------------
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['txt','pdf','png','jpg','jpeg','gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods=["POST"])
def upload_file():
    #if 'files[]' not in request.files:
    #    resp = jsonify({"message": "no file part in the request"})
    #    resp.status_code = 400
    #    return resp

    files = request.files.getlist('')

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True
        else:
            errors[file.filename] = 'File type is not allowed'

    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({"message": "File(s) successfully uploaded"})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

#------------------------------------------------------------------------
@app.route('/products/<string:product_name>/', methods=['PUT'])
def editProduct(product_name):
    productFound= [product for product in products if product['name']== product_name]
    if(len(productFound)>0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            "message": "product updated",
            "product": productFound[0]
        })
    return jsonify({"message": "Product not found"})

@app.route('/products/<string:product_name>/', methods=['DELETE'])
def deleteProduct(product_name):
    productFound = [product for product in products if product['name'] == product_name]
    if len(productFound)>0:
        products.remove(productFound[0])
        return jsonify({
            "message": "product deleted",
            "products" : products
        })  
    return jsonify({"message": "product not found"})

if  __name__ == '__main__':
    app.run(debug=True, port= 4000)