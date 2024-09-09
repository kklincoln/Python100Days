from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean
import random

app = Flask(__name__)

# CREATE DB
class Base(DeclarativeBase):
    pass
# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)

    #converting this to dictionary so that the data can easily be transmitted through an API call without needing to use
    #lengthy JSONIFY manual dictionary creation
    # Dictionary Comprehension to do this.
    def to_dict(self):
        # returns the "column.name : col_value for each column in this table
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}



with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


# HTTP GET - Read random cafe record
@app.route("/random", methods=["GET"])
def get_random_cafe():
    # count the number of entries in the cafe table
    num_cafes = db.session.query(Cafe).count()
    # create a random id from 1 to the maximum count
    rand_id = random.randint(1, num_cafes)
    # get the cafe by the random id
    random_cafe = db.session.query(Cafe).get(rand_id)
    # through a process called Serialization, we need to turn our random_cafe SQLAlchemy object into a JSON
    #Simply convert the random_cafe data record to a dictionary of key-value pairs.
    return jsonify(cafe=random_cafe.to_dict())

# HTTP GET - read ALL cafe records
@app.route("/all", methods=["GET"])
def get_all_cafes():
    # Hint: Combine the .execute() and .select() methods to make the query using flask-sqlalchemy.
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    # converting the result into a python list using scalars()
    all_cafes = result.scalars().all()
    # use list comprehension again to create a cafes list comprised of a dictionary for each cafe in all_cafes
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])

# HTTP GET - search for cafes at a particular location.
@app.route("/search")
def get_cafes_at_location():
    #using the argument "loc" that will be passed in within the template as argument: "loc", query db for those records
    query_location = request.args.get("location")
    if not query_location:
        # Return all cafes
        cafes = Cafe.query.all()
    else:
        # if the query_location was provided, filter by location
        cafes = Cafe.query.filter_by(location=query_location).all()

    if not cafes:
        #return error message
        return jsonify(error={
            "error": "No cafe found for location '{}'".format(query_location)}),404
    else:
        #return json
        return jsonify({"cafes": [cafe.to_dict() for cafe in cafes]})

#######################################################################################
# HTTP POST - Create Record for New Cafe
@app.route('/add', methods=["POST"])
def post_new_cafe():
    try:
        if request.method == "POST":
            #new cafe using the Cafe() class
            new_cafe= Cafe(
                #this form has not yet been created, but if there was a form, we would "get" the data inside with request.form.get("element")
                #one value to be populated for each of the fields created in the table above
                name=request.form.get("name"),
                map_url=request.form.get("map_url"),
                img_url=request.form.get("img_url"),
                location=request.form.get("location"),
                seats=request.form.get("seats"),
                #note, when testing in POSTman, you need to explicitly convert these boolean fields with bool() in the code
                #because postman sends these API calls as strings, not as boolean values
                #alternative; is setting data=request.form and then json.loads(data["toilets"].lower()) for these values
                has_toilet=bool(request.form.get("toilets")),
                has_wifi=bool(request.form.get("wifi")),
                has_sockets=bool(request.form.get("sockets")),
                can_take_calls=bool(request.form.get("calls")),
                coffee_price=request.form.get("price")
                )
            #within the db, create a session to add the new cafe
            db.session.add(new_cafe)
            db.session.commit()
            #return the json value of the new cafe to confirm the addition
            return jsonify(response={"Success": "Sucessfully added the new cafe."})
    except Exception as e:
        #return the error that is generated and stored as 'e', converted to string; error code 500
        return jsonify({"error":{"message": str(e)}}), 500

#######################################################################################
# HTTP PUT/PATCH - Update Record

#PATCH
#note, POSTman patch url: http://127.0.0.1:5000/update-price/22?new_price=$2.40
@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def patch(cafe_id):
    #the commented out cafe_to_update line below will actually automatically gen a standard 404 response, we are using a
    #custom one below, so replace with db.session.get(Cafe, cafe_id); change illustrated in POSTman
    # cafe_to_update = db.get_or_404(Cafe, cafe_id)
    cafe_to_update = db.session.get(Cafe, cafe_id)
    # new_price is a field from the form page
    # cafe_to_update = from db, table:"Cafe" get_or_404 using the id passed as an argument
    new_price = request.form.get("new_price")
    if request.method == "PATCH":
        if cafe_to_update:
            #set the table value of coffee_price = new price
            cafe_to_update.coffee_price = new_price
            db.session.commit()
            return jsonify(response = {"Success": "Successfully updated the price."})
        else:
            #404 = Resource not found
            return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."}), 404




#######################################################################################
# HTTP DELETE - Delete Record
#note: postman DELETE URL http://127.0.0.1:5000/report-closed/22?api-key=TopSecretAPIKey
# We can add a security feature by requiring an api-key . If they have the api-key "TopSecretAPIKey" then they're allowed
# to make the delete request, otherwise, we tell them they are not authorized to make that request. A 403 in HTTP speak.
@app.route("/report-closed/<cafe_id>" ,methods=["DELETE"])
def delete_cafe(cafe_id):
    #use request.args if the POSTman uses params, request.
    api_key = request.args.get("api-key")
    if api_key == "TopSecretAPIKey":
        #look through the Cafe table in the db for the cafe_id passed through an argument
        cafe_to_delete = db.session.get(Cafe, cafe_id)
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(response={"Success":"Successfully deleted the cafe from the database."}), 200
        else:
            # 404 = Resource not found; no matching cafe in db
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        # 403 = Method Not Allowed; permission error
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
