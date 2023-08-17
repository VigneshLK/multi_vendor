import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "Vicky@2552",database ="multivendor_marketplace" )
mycursor = mydb.cursor()
#mycursor.execute("create database multivendor_marketplace")

class vendor:
    
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def create_table(self): # create a table
        mycursor.execute("create table vendors(id int not null auto_increment, name varchar(100) not null,email varchar(100) not null, password varchar(50) not null, primary key(id))")
        pass

     def insert_value(self): # insert value
        sql = "insert into vendors (name, email, password) VALUES (%s, %s, %s)"
        val = [("vicky","vky@gmail.com", 123456), ("arun", "arun@gmail.com", 456789),("mani", "mani@gmail.com", 789456), ("ravi", "ravi@gmail.com",963258)]
        mycursor.executemany(sql,val)
        mydb.commit()
        print("values inserted successfully")

    def register(self):
        self.name = input("Enter your name: ")
        while not self.name.isalpha() or len(self.name) > 50:
            print("Enter a valid name")
            self.name = input("Enter your name: ")
        self.email = input("Enter your email: ")
        while not self.email.endswith("@gmail.com"):
            print("Enter a valid email")
            self.email = input("Enter your email: ")
        self.password = input("Enter your password: ")
        while len(self.password) != 6:
            print("Enter a valid password")
            self.password = input("Enter your password: ")
        sql = "INSERT INTO vendors (name, email, password) VALUES (%s, %s, %s)"
        val = (self.name, self.email, self.password)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Registration successfully")

    def login(self):
        self.email = input("Enter your email: ")
        while not self.email.endswith("@gmail.com"):
            print("Enter a valid email")
            self.email = input("Enter your email: ")
        self.password = input("Enter your password: ")
        while len(self.password) != 6:
            print("Enter a valid password")
            self.password = input("Enter your password: ")
        sql = "SELECT * FROM vendors WHERE email = %s AND password = %s"
        val = (self.email, self.password)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if result:
            print("Login successfully")
        else:
            print("Invalid login")
            vendor.login()

class product:

    def __init__(self,vendor_key, name, price, quantity, description):
        self.vendor_key = vendor_key
        self.name = name
        self.price = price
        self.quantity = quantity
        self.description = description
        
    def create_table(self):
        mycursor.execute("CREATE TABLE products (id INT NOT NULL AUTO_INCREMENT, vendor_key INT NOT NULL, name VARCHAR(100) NOT NULL, price DECIMAL(10,2) NOT NULL, quantity INT NOT NULL, description TEXT, PRIMARY KEY(id), UNIQUE KEY unique_name(name), FOREIGN KEY(vendor_key) REFERENCES vendors(id))")
        pass
    def insert_product(self):
         products = [
            (1, "Product A", 9.99, 100, "This is a great product"),
            (2, "Product B", 19.99, 50, "This is another great product"),
            (3, "Product C", 14.99, 75, "This is a cool product"),
            (4, "Product E", 4.99, 200, "This is a cheap product")
         ]
         sql = "INSERT INTO products (vendor_key, name, price, quantity, description) VALUES (%s, %s, %s, %s, %s)"
         mycursor.executemany(sql, products)
         mydb.commit()
         print("Product values inserted successfully")
         
    def add_product(self):
        vendor_key_input = input("Enter vendor key: ")
        if vendor_key_input.isdigit():
            self.vendor_key = int(vendor_key_input)
            sql = "SELECT * FROM vendors WHERE id = %s"
            val = (self.vendor_key,)
            mycursor.execute(sql, val)
            result = mycursor.fetchall()
            if not result:
                print("Vendor with the given ID does not exist. Please enter a valid vendor ID.")
                return
        else:
           print("Invalid input. Please enter an integer value for vendor key.")
           return

        self.name = input("Enter product name: ")
        sql = "SELECT * FROM products WHERE name = %s"
        val = (self.name,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if result:
            print("Product with the same name already exists. Please enter a different name.")
            return

        price_input = input("Enter product price: ")
        if  float(price_input) < 0:
            print("Invalid input. Please enter a numerical value for price.")
            return
        else:
            self.price = float(price_input)

        quantity_input = input("Enter product quantity: ")
        if int(quantity_input) < 1:
            print("Invalid input. Please enter a positive integer value for quantity.")
            return
        else:
            self.quantity = int(quantity_input)

        description_input = input("Enter product description: ")
        if len(description_input) > 100:
             print("Invalid input. Please enter a description with less than 100 characters.")
             return
        else:
             self.description = description_input

        sql = "INSERT INTO products (vendor_key, name, price, quantity, description) VALUES (%s, %s, %s, %s, %s)"
        val = (self.vendor_key, self.name, self.price, self.quantity, self.description)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Product added successfully")
        
    def update_product(self):
        vendor_key_input = input("Enter vendor key: ")
        while not vendor_key_input.isdigit():
            print("Invalid input. Please enter an integer value for vendor key.")
            vendor_key_input = input("Enter vendor key: ")
        self.vendor_key = int(vendor_key_input)

        sql = "SELECT * FROM vendors WHERE id = %s"
        val = (self.vendor_key,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        while not result:
            print("Vendor with the given ID does not exist. Please enter a valid vendor ID.")
            vendor_key_input = input("Enter vendor key: ")
            while not vendor_key_input.isdigit():
                print("Invalid input. Please enter an integer value for vendor key.")
                vendor_key_input = input("Enter vendor key: ")
            self.vendor_key = int(vendor_key_input)
            val = (self.vendor_key,)
            mycursor.execute(sql, val)
            result = mycursor.fetchall()
    
        self.name = input("Enter product name: ")
        sql = "SELECT * FROM products WHERE name = %s AND vendor_key = %s"
        val = (self.name, self.vendor_key)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        while not result:
            print("Product with the given name and vendor key does not exist. Please enter a valid product name and vendor key.")
            self.name = input("Enter product name: ")
            val = (self.name, self.vendor_key)
            mycursor.execute(sql, val)
            result = mycursor.fetchall()

        price_input = input("Enter new product price: ")
        while not price_input.isdigit():
             print("Invalid input. Please enter a numerical value for price.")
             price_input = input("Enter new product price: ")
        self.price = float(price_input)

    
        quantity_input = input("Enter new product quantity: ")
        while not quantity_input.isdigit():
              print("Invalid input. Please enter an integer value for quantity.")
              quantity_input = input("Enter new product quantity: ")
        self.quantity = int(quantity_input)

        self.description = input("Enter new product description: ")
        while len(self.description) > 100:
            print("Invalid input. Please enter a description with less than 100 characters.")
            self.description = input("Enter new product description: ")

        sql = "UPDATE products SET price = %s, quantity = %s, description = %s WHERE name = %s AND vendor_key = %s"
        val = (self.price, self.quantity, self.description, self.name, self.vendor_key)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Product updated successfully.")

    def delete_product(self):
        self.vendor_key = input("Enter vendor key: ")
        if not self.vendor_key.isdigit():
            print("Invalid input. Please enter an integer value for vendor key.")
            return
        self.vendor_key = int(self.vendor_key)
        sql = "SELECT * FROM vendors WHERE id = %s"
        val = (self.vendor_key,)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if not result:
            print("Vendor with the given ID does not exist. Please enter a valid vendor ID.")
            return
        self.name = input("Enter product name: ")
        sql = "SELECT * FROM products WHERE name = %s AND vendor_key = %s"
        val = (self.name, self.vendor_key)
        mycursor.execute(sql, val)
        result = mycursor.fetchall()
        if not result:
            print("Product with the given name and vendor key does not exist. Please enter a valid product name.")
            return
        sql = "DELETE FROM products WHERE name = %s AND vendor_key = %s"
        val = (self.name, self.vendor_key)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Product deleted successfully.")
        
    def compare_price(self):
        valid_name = False
        while not valid_name:
            self.name = input("Enter the product name: ")
            if len(self.name) > 0:
                 valid_name = True
            else:
                 print("Invalid input. Please enter a non-empty product name.")
        
        valid_price = False
        while not valid_price:
            self.price = input("Enter the product price: ")
            if self.price.isnumeric() or (self.price.count(".") == 1 and self.price.replace(".", "").isnumeric()):
                
                self.price = float(self.price)
                valid_price = True
            else:
                print("Invalid input. Please enter a numerical value for price.")
        
        sql = "SELECT AVG(price) FROM products WHERE name = %s"
        val = (self.name,)
        mycursor.execute(sql, val)
        result = mycursor.fetchone()
        if result[0] is None:
            print("The product is not available in the table")
        else:
            avg_price = result[0]
            if self.price > avg_price:
                print("Your product price is higher than the average market price.")
            elif self.price < avg_price:
                print("Your product price is lower than the average market price.")
            else:
                print("Your product price is the same as the average market price.")
            
    def sell_product(self, alert_threshold):
        id = input("Enter product ID: ")
        while not id.isdigit() or int(id) <= 0:
            print("Invalid input. Please enter a positive integer for product ID.")
            id = input("Enter product ID: ")
        self.id = int(id)

        quantity = input("Enter product quantity: ")
        while not quantity.isdigit():
            print("Invalid input. Please enter an integer value for quantity.")
            quantity = input("Enter product quantity: ")
        self.quantity = int(quantity)

        quantity_sold = input("Enter quantity sold: ")
        while not quantity_sold.isdigit() or int(quantity_sold) <= 0:
            print("Invalid input. Please enter a positive integer for quantity sold.")
            quantity_sold = input("Enter quantity sold: ")
        quantity_sold = int(quantity_sold)

        #alert_threshold = input("Enter alert threshold: ")
        #while not alert_threshold.isdigit() or int(alert_threshold) <= 0:
          #  print("Invalid input. Please enter a positive integer for alert threshold.")
           # alert_threshold = input("Enter alert threshold: ")
       # alert_threshold = int(alert_threshold)

        if quantity_sold > self.quantity:
            print("There is not enough stock to sell that quantity.")
            return

        self.quantity -= quantity_sold
        sql = "UPDATE products SET quantity = %s WHERE id = %s"
        val = (self.quantity, self.id)
        mycursor.execute(sql, val)
        mydb.commit()
        print("Product quantity updated successfully.")

        if self.quantity < alert_threshold:
            #self.handle_alert()
            print("ALERT: The quantity of product {} is below the alert threshold.".format(self.id))

vendor = vendor("", "", "")               
product = product("", "", "", "", "")
i = 1
while i < 2:
    choose = input("1. Press 1 to register\n2. Press 2 to login\n")
    if choose == "1":
        vendor.register()
        i = 1
    elif choose == "2":
        vendor.login()
            
        i = 0

        while i < 2:
            choose = input("1. Add product\n2. Update product\n3. Delete product\n4. Compare product\n5. Sell product\n")
            if choose == "1":
                product.add_product()
            elif choose == "2":
                product.update_product()
            elif choose == "3":
                product.delete_product()
            elif choose == "4":
                product.compare_price()
            elif choose == "5":
                product.sell_product(40)
                i = 2
