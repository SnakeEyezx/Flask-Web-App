from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from transliterate import slugify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(30), nullable=False)
    brand = db.Column(db.String(30), nullable=False)
    price = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    param_power = db.Column(db.Integer, nullable=False)
    param_type = db.Column(db.String(30), nullable=False)
    param_voltage = db.Column(db.String(30), nullable=False)
    param_accuracy = db.Column(db.String(30), nullable=False)
    param_warranty = db.Column(db.Integer, nullable=False)
    param_weight = db.Column(db.Integer, nullable=False)
    model_link = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.model


@app.route("/")
def hello_world():
    products = Product.query.all()
    return render_template('index.html', products=products)


@app.route("/add_product", methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        product_model_name = request.form['model']
        product_brand_name = request.form['brand']
        product_price = request.form['price']
        product_description = request.form['description']
        product_param_power = request.form['param_power']
        product_param_type = request.form['param_type']
        product_param_voltage = request.form['param_voltage']
        product_param_accuracy = request.form['param_accuracy']
        product_param_warranty = request.form['param_warranty']
        product_param_weight = request.form['param_weight']
        product_link = slugify(request.form['brand'] + " " + request.form['model'])
        new_product = Product(model=product_model_name, brand=product_brand_name, price=product_price,
                              description=product_description, param_power=product_param_power,
                              param_type=product_param_type, param_voltage=product_param_voltage,
                              param_accuracy=product_param_accuracy, param_warranty=product_param_warranty,
                              param_weight=product_param_weight, model_link=product_link)
        try:
            db.session.add(new_product)
            db.session.commit()
        finally:
            return "add done!"
    else:
        return render_template('add_product.html')


@app.route("/view_products/<single_model_link>")
def view_products(single_model_link):
    products = Product.query.filter_by(model_link=single_model_link)
    # result = db.session.execute(products)
    # for user_obj in result.scalars():
    #     link = "/".join([translit(user_obj.brand, reversed=True), user_obj.model, str(user_obj.id)])
    #     print(link)  # f"{user_obj.id} {user_obj.model} {user_obj.model}"
    #   translit_brand = translit(text, 'ru')
    return render_template('view_products.html', products=products)


@app.route("/create_all")
def create_tables():
    db.create_all()
    return "Create_all done!"


@app.route("/drop_all")
def drop_tables():
    db.drop_all()
    return "Drop_all done!"


if __name__ == "__main__":
    app.run(debug=True)
