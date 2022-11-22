from flask import Flask,jsonify, request
from werkzeug.utils import secure_filename
import os
import urllib.request
from main import DataBase
import uuid

app = Flask(__name__)
mysql = DataBase()

@app.route('/')
def main():

    return "main"

UPLOAD_FOLDER = "/opt/lampp/htdocs/imageUploader/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png','jpeg','jpg'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads', methods  =['GET', 'POST'])
def imageUpload():
    if request.method == 'POST':
        errors = {}
        success = False
        print(request.files)
        #if request.args.get['description'] not in request.files:
        #    response = jsonify({"msg" : "description is required"})
        #    response.status_code = 400
        #    return response
        if 'image' not in request.files:
            response = jsonify({"msg" : "file part is required"})
            response.status_code = 400
            return response
        #if file.filename == '':
        #    response = jsonify({"msg": "No selected file"})
        #    return response

        files = request.files.getlist('image')
        #for file in files:
        #    print("x")
        #    print(file.filename)
        #    print(allowed_file(file.filename))

        for file in files:
            if file.filename and allowed_file(file.filename):
                print("Si entra")
                file_extension = "."+ file.filename.rsplit('.',1)[1].lower()
                filename = str(uuid.uuid4()) + file_extension
                #description = request.args.get[]
                path = UPLOAD_FOLDER + filename 
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                mysql.uploadImage(path)
                success = True
            else:
                errors[file.filename] = 'File type is not allowed'
        if success and errors:
            errors['msg'] = 'File(s) succesfully uploaded, but with issues'
            response = jsonify(errors)
            response.status_code = 206
            return response
        if success:
            response = jsonify({"msg":"File(s) sucessfully uploaded with no errors"})
            response.status_code = 201
            return response
        else:
            response = jsonify(errors)
            response.status_code = 500
            return response
    else:
        return "u.u"

if __name__ == "__main__":
    app.run(debug=True, port= 5000)