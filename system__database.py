#------------------------------------------#
# Store data to DB                         #
#------------------------------------------#
import pyodbc

class dbClass:

  # Constructor
  def __init__(self, param):
    self.param  = param

  # Function to stablish DB connection
  def dbConnection(self):
    connection  = pyodbc.connect(
      'Driver={SQL Server};'
      'Server=NZWR;'
      'Database=Web_Scraping;'
      'Trusted_Connection=yes;'
    )
    return connection

  # Get data from parameter
  def getData(self):
    return self.param['name'], self.param['email'], self.param['phone'], self.param['street'], self.param['town'], self.param['province'], self.param['range-min'], self.param['range-max'], self.param['leasetype'], self.param['property'], [self.param['s-source[0]'], self.param['s-source[1]'], self.param['s-source[2]']]
 
  # Store data into SQL
  def storeData(self):

    # Get data from get methods
    data        = self.getData()

    # Put values into varibles with more clear name
    name, email, phone, street, town , province, min, max, leasetype, property = data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9]

    # using list comprehension
    source      = ', '.join(map(str, data[10]))
    # check connection
    connection  = self.dbConnection()
    # initilize cursor
    cursor      = connection.cursor()
    # execute cursore and store data
    cursor.execute(
      """
      INSERT INTO Web_Scraping.dbo.Users 
      (User_Name, Email_Address, Phone_Number, Street, City, Province, Min_Rent,
      Max_Rent, Lease_Type, Type_Of_Property, Preferred_Website)
      VALUES (?, ?, ?,?, ?, ?,?, ?, ?, ?, ?)
      """,
      (name, email, phone, street, town, province, min, max, leasetype, property, source)
    )
    
    # commit connection 
    connection.commit()
    # Get data from database
    # cursor.execute('SELECT * FROM Web_Scraping.dbo.Users')
    # for row in cursor:
    #     print(row)