from flask import Flask,render_template,request
from components.popularProducts import popular_recommend
from components.ContentBasedRec import content_based_recommend
from components.imageRec import image_recommend
from api.products_api import getMultiple,getOneProduct
import shutil


app=Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    popular_products=popular_recommend(51)
    popular_products_data=getMultiple(popular_products)
    return render_template('home.html',popular_products=popular_products_data)



@app.route('/product',methods=['GET','POST'])
def product():
    if request.method=='POST':
        product_id=request.form['product_id']
        product_details=getOneProduct(product_id)
        product_id=int(product_id)
        content_rec=content_based_recommend(product_id, 40)
        if content_rec =='No Data':
            content_based_products='No Data'
        else:
            content_based_products=getMultiple(content_rec)
    return render_template('product.html', product_details= product_details,content_based_products=content_based_products)


@app.route('/predict-style-upload',methods=['GET','POST'])
def predictStyleUpload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            uploaded_file.save('static/predictImage.jpg')
            image_pred=image_recommend(6)
            image_pred_data=getMultiple(image_pred)
            print(image_pred_data)
        else:
            return 'Upload A Valid File'
    return render_template('imageRec.html',image_pred_data=image_pred_data,images=image_pred)

@app.route('/predict-style',methods=['GET','POST'])
def predictStyle():
    pro_id=str(request.form['product'])
    source_loc=f'static\images\{pro_id}.jpg'
    shutil.copy(source_loc,'static/predictImage.jpg')
    image_pred=image_recommend(6)
    image_pred_data=getMultiple(image_pred)
    print(image_pred_data)
    return render_template('imageRec.html',image_pred_data=image_pred_data,images=image_pred)


@app.route('/upload-file',methods=['GET'])
def uploadFile():
       return render_template('upload-file.html')
            
@app.route('/login',methods=['GET'])
def login():
       return render_template('login.html')

if __name__=='__main__':
    app.run(debug=True)