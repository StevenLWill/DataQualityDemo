# DataQualityDemo

This flask app was created to demonstrate why data quality is important for machine learning models. 

This app has two components, a data entry tool and a prediction tool. Users are invited to enter in housing data via the data entry tool which stores the data in a relational database. The prediction tool pulls in the data from the database and uses a simple linear regression model to predict the price of an individual house.

There are pieces of the code that are commented out so that I was able to demonstrate what happens if "bad" data is entered into a field and how an engineer might try to standardize the data types and units of measurement.

