from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from transliterate import slugify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test1.db'
db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(30), nullable=False)
    brand = db.Column(db.String(30), nullable=False)
    power = db.Column(db.Integer, nullable=False)
    voltage_input_type = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    model_link = db.Column(db.String(150), nullable=False, unique=True)

    def __repr__(self):
        return '<Product %r>' % self.model


class Description(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(30), nullable=False)
    brand = db.Column(db.String(30), nullable=False)
    voltage_input_type = db.Column(db.String(30), nullable=False)
    description = db.Column(db.String(120))
    operating_mode = db.Column(db.String(30), nullable=False)
    stages_of_regulation = db.Column(db.Integer, nullable=False)
    deviation_of_output_voltages = db.Column(db.String(30), nullable=False)
    input_voltage_range = db.Column(db.String(30), nullable=False)
    output_voltage_range = db.Column(db.String(30), nullable=False)
    extreme_input_voltage_range = db.Column(db.String(30), nullable=False)
    reaction_time = db.Column(db.Integer, nullable=False)
    emergency_reaction_time = db.Column(db.Integer, nullable=False)
    thermal_protection = db.Column(db.Integer, nullable=False)
    warranty = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return '<Description %r>' % self.model


@app.route("/")
def index():
    energotech_onephase_optimum = Product.query.filter_by(brand="Энерготех",
                                                          voltage_input_type="Однофазный",
                                                          model='Optimum+').order_by(Product.power.asc())
    energotech_onephase_infinity = Product.query.filter_by(brand="Энерготех", voltage_input_type="Однофазный",
                                                           model='INFINITY').order_by(Product.power.asc())
    energotech_treephase_optimum = Product.query.filter_by(brand="Энерготех", voltage_input_type="Трехфазный",
                                                           model='Optimum+').order_by(Product.power.asc())
    energotech_treephase_infinity = Product.query.filter_by(brand="Энерготех", voltage_input_type="Трехфазный",
                                                            model='INFINITY').order_by(Product.power.asc())
    volt = Product.query.filter_by(brand="ВОЛЬТ")
    elim = Product.query.filter_by(brand="Элим")
    descr = Description.query.filter_by(brand="Энерготех")
    return render_template('index.html', energotech_onephase_optimum=energotech_onephase_optimum,
                           energotech_onephase_infinity=energotech_onephase_infinity,
                           energotech_treephase_optimum=energotech_treephase_optimum,
                           energotech_treephase_infinity=energotech_treephase_infinity,
                           volt=volt, elim=elim,
                           descr=descr)


@app.route("/add_product", methods=['POST', 'GET'])
def add_product():
    if request.method == 'POST':
        product_model_name = request.form['model']
        product_brand_name = request.form['brand']
        product_voltage_input_type = request.form['voltage_input_type']
        product_price = request.form['price']
        product_power = request.form['power']
        product_weight = request.form['weight']
        product_link = slugify(' '.join(str(item) for item in [product_brand_name, product_model_name,
                                                               product_power, product_voltage_input_type]))
        new_product = Product(model=product_model_name,
                              brand=product_brand_name,
                              voltage_input_type=product_voltage_input_type,
                              price=product_price,
                              power=product_power,
                              weight=product_weight,
                              model_link=product_link)
        try:
            db.session.add(new_product)
            db.session.commit()
        finally:
            return render_template('add_product.html')
    else:
        return render_template('add_product.html')


@app.route("/add_description", methods=['POST', 'GET'])
def add_description():
    if request.method == 'POST':
        description_model_name = request.form['model']
        description_brand_name = request.form['brand']
        description_voltage_input_type = request.form['voltage_input_type']
        description_description = request.form['description']
        description_operating_mode = request.form['operating_mode']
        description_stages_of_regulation = request.form['stages_of_regulation']
        description_deviation_of_output_voltages = request.form['deviation_of_output_voltages']
        description_input_voltage_range = request.form['input_voltage_range']
        description_output_voltage_range = request.form['output_voltage_range']
        description_extreme_input_voltage_range = request.form['extreme_input_voltage_range']
        description_reaction_time = request.form['reaction_time']
        description_emergency_reaction_time = request.form['emergency_reaction_time']
        description_thermal_protection = request.form['thermal_protection']
        description_warranty = request.form['description_warranty']
        new_description = Description(model=description_model_name,
                                      brand=description_brand_name,
                                      voltage_input_type=description_voltage_input_type,
                                      description=description_description,
                                      operating_mode=description_operating_mode,
                                      stages_of_regulation=description_stages_of_regulation,
                                      deviation_of_output_voltages=description_deviation_of_output_voltages,
                                      input_voltage_range=description_input_voltage_range,
                                      output_voltage_range=description_output_voltage_range,
                                      extreme_input_voltage_range=description_extreme_input_voltage_range,
                                      reaction_time=description_reaction_time,
                                      emergency_reaction_time=description_emergency_reaction_time,
                                      thermal_protection=description_thermal_protection,
                                      warranty=description_warranty)
        try:
            db.session.add(new_description)
            db.session.commit()
        except Exception as err:
            print('Query Failed: %s\nError: %s' % (new_description, str(err)))
        finally:
            return "Descr added!"
    else:
        return render_template('add_description.html')


@app.route("/view_products/<single_model_link>")
def view_products(single_model_link):
    product = Product.query.filter_by(model_link=single_model_link).first()
    description_query = Description.query.filter_by(voltage_input_type=product.voltage_input_type,
                                                    model=product.model)
    return render_template('view_products.html', product=product, model_descriptions=description_query)


# @app.route("/reset")
# def reset():
#     db.drop_all()
#     db.create_all()
#     return "Reset done!"


@app.route("/manage")
def manage():
    products = Product.query.order_by(Product.model.desc(),
                                      Product.voltage_input_type.asc(),
                                      Product.price.desc()).all()
    return render_template('manage.html', products=products)


@app.route("/delete", methods=['POST'])
def delete():
    product_model_link = request.form['model_link']
    try:
        Product.query.filter_by(model_link=product_model_link).delete()
        db.session.commit()
    except Exception as err:
        print('Query Failed: Error: %s' % (str(err)))
    finally:
        return redirect('/manage')


@app.route("/update", methods=['POST'])
def update():
    product_model_link = request.form['model_link']
    product_model_name = request.form['model']
    product_brand_name = request.form['brand']
    product_voltage_input_type = request.form['voltage_input_type']
    product_price = request.form['price']
    product_power = request.form['power']
    product_link = slugify(' '.join(str(item) for item in [product_brand_name, product_model_name,
                                                           product_power, product_voltage_input_type]))
    try:
        Product.query.filter_by(model_link=product_model_link).update(dict(model=product_model_name,
                                                                           brand=product_brand_name,
                                                                           voltage_input_type=product_voltage_input_type,
                                                                           price=product_price,
                                                                           power=product_power,
                                                                           model_link=product_link))
        db.session.commit()
    except Exception as err:
        print('Query Failed: Error: %s' % (str(err)))
    finally:
        return redirect('/manage')


if __name__ == "__main__":
    app.run(debug=True)
