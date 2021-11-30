# import necessary libraries
import sys
import pandas as pd
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression

engine = create_engine("postgresql://postgres:password@localhost:5432/data_quality_demo")

# create instance of Flask app
app = Flask(__name__)


def acre_to_sq_ft(acres):
    return acres * 43560


# create route that renders index.html template
@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/data_entry")
def data_entry():
    return render_template("data_entry.html")
    
@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form.to_dict()
      print(result, file=sys.stderr) 

      #if not result['lot_size'].replace(".","1").isdigit():
      #  result['lot_size'] = result['lot_size'].replace('acres','').replace('ft','')
      #  print("Not a number, replacing string elements", file=sys.stderr) 
       
      
      #Area Conversion
      if float(result['lot_size']) < 100:
        result['lot_size'] = acre_to_sq_ft(float(result['lot_size']))
      
      engine.execute(f"""INSERT INTO housing_data (address, city, state, zip, sq_feet, lot_size, year_built, bedrooms, bathrooms, sale_price)
                        VALUES ('{result["address"]}','{result["city"]}','{result["state"]}','{result["zip"]}','{result["sq_feet"]}','{result["lot_size"]}','{result["year_built"]}','{result["bedrooms"]}','{result["bathrooms"]}','{result["sale_price"]}');
                       """)
      return render_template("result.html",result = result)

@app.route("/predict_data_entry")
def predict_data_entry():
    return render_template("predict_data_entry.html")
    
@app.route("/predict_price",methods = ['POST', 'GET'])
def predict_price():
    df = pd.read_sql('SELECT * FROM housing_data',engine)
    X_df = df[['zip','sq_feet','lot_size','year_built','bedrooms','bathrooms']]
    y_df = df['sale_price']
    X_df = pd.get_dummies(X_df,columns=['zip'])
    empty_df = X_df[X_df['sq_feet']<-99999]
    model = LinearRegression()
    model.fit(X_df,y_df)
    
    if request.method == 'POST':
      result = request.form.to_dict()
      print(result, file=sys.stderr)  
      
      #if not result['lot_size'].replace(".","1").isdigit():
      #  result['lot_size'] = result['lot_size'].replace('acres','').replace('ft','')
      #  print("Not a number, replacing string elements", file=sys.stderr)  
      
      this_zip = result["zip"]
      
      new_df = pd.DataFrame(result,index=[0])
      new_df = pd.get_dummies(new_df,columns=['zip'])
      new_df = pd.concat([empty_df,new_df]).fillna(0)
      
      prediction = model.predict(new_df[X_df.columns])
      prediction = round(prediction[0],2)
      
      weights = dict(zip(X_df.columns,model.coef_))
      intercept = model.intercept_
      
      equation = "Price = "
      for k,v in weights.items():
          if "zip" not in k or k.replace("zip_","") == this_zip:
              equation += f"({round(v,2)} * {k}) + "
      equation += str(round(intercept,2))
      
      print(prediction, file=sys.stderr)
      print(model.coef_, file=sys.stderr)
      print(model.intercept_, file=sys.stderr)
    return render_template("prediction.html",predicted_price = prediction, formula = equation)
    
    
    

      


if __name__ == "__main__":
    app.run(debug=True)
