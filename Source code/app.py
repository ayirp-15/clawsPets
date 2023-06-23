from flask import *
import ibm_db
import os
# import ibm_boto3                                  # pip install ibm_bot03
# from ibm_botocore.client import Config,ClientError   # pip install ibm_botocore


#conn = ibm_db.connect("DATABASE=bludb; HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud; PORT=31198; SECURITY=SSL;UID=gvp86200;PWD=rJapMOXJuQQlW1rp", '', '')

conn = ibm_db.connect("DATABASE=bludb; HOSTNAME=0c77d6f2-5da9-48a9-81f8-86b520b87518.bs2io90l08kqb1od8lcg.databases.appdomain.cloud; PORT=31198; SECURITY=SSL;UID=jvv22943;PWD=m310VAoD58zNAecY", '', '')
print(conn)

app=Flask(__name__)

# petsite index page routing

@app.route('/')
def index():
    return render_template('index.html')

# Paws & claws user home page routing

@app.route('/home')
def home():
    return render_template('home.html')

# PetFeed page routing

@app.route('/petfeed')
def petfeed():
    return render_template('petfeed.html')

# PetWear page routing

@app.route('/petwear')
def petwear():
    return render_template('pet_wear.html')

# pettoys page routing

@app.route('/pettoys')
def petToys():
    return render_template('pet_toys.html')

# Pet Medicine page routing

@app.route('/petmedi')
def petmedi():
    return render_template('pet_medi.html')

@app.route('/logout')
def logout():
    return render_template('User_login.html')

# My cart page routing

@app.route('/mycart')
def cart():
    return render_template('Mycart.html')

# User_Signup page routing

@app.route('/user_signup')
def User_signup():
    return render_template('User_signup.html')
    
@app.route('/register', methods=['POST'])
def register1():
    try:
        x = [x for x in request.form.values()]
        print(x)
        NAME = x[0]
        EMAIL = x[1]
        PASSWORD = x[2]
        sql = "SELECT * FROM USER_SIGNUP WHERE EMAIL =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, EMAIL)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            return render_template('User_login.html')
        else:
            insert_sql = "INSERT INTO USER_SIGNUP VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, NAME)
            ibm_db.bind_param(prep_stmt, 2, EMAIL)
            ibm_db.bind_param(prep_stmt, 3, PASSWORD)
            ibm_db.execute(prep_stmt)
            return render_template('User_login.html')
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        return render_template('error.html')

# User_login page routing

@app.route('/user_login')
def user_login():
    return render_template('User_login.html')

@app.route('/login1', methods=['POST'])
def login1():
    try:
        EMAIL = request.form['Email']
        PASSWORD = request.form['PASSWORD']
        sql = "SELECT * FROM USER_SIGNUP WHERE EMAIL=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, EMAIL)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            if str(PASSWORD) == str(account['PASSWORD'].strip()):
                return render_template('home.html')
            else:
                return render_template("User_signup.html", msg="Invalid E-Mail or Password")
        else:
            return render_template('User_signup.html', pred="Login unsuccessful. Incorrect username/password !")
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        return render_template('error.html')
    
# Merchant_login page routing
    
@app.route('/merchantlogin')
def merchantlogin():
    return render_template('Merchant_login.html')

@app.route('/merchlogin1', methods=['POST'])
def merchlogin1():
    try:
        MEMAIL = request.form['MEmail']
        MPASSWORD = request.form['MPASSWORD']
        sql = "SELECT * FROM MERCHANT_SIGNUP WHERE MEMAIL=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, MEMAIL)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            if str(MPASSWORD) == str(account['MPASSWORD'].strip()):
                return render_template('Merchant_home.html')
            else:
                return render_template("Merchant_signup.html", msg="Invalid E-Mail or Password")
        else:
            return render_template('Merchant_signup.html', pred="Login unsuccessful. Incorrect username/password !")
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        return render_template('error.html')

# Merchant_Signup page routing

@app.route('/merchantsignup')
def merchantsignup():
    return render_template('Merchant_signup.html')   

    
@app.route('/merchregister', methods=['POST'])
def merchregister():
    try:
        x = [x for x in request.form.values()]
        print(x)
        MNAME = x[0]
        MEMAIL = x[1]
        MPASSWORD = x[2]
        sql = "SELECT * FROM MERCHANT_SIGNUP WHERE MEMAIL =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt, 1, MEMAIL)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            return render_template('Merchant_login.html')
        else:
            insert_sql = "INSERT INTO MERCHANT_SIGNUP VALUES (?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, MNAME)
            ibm_db.bind_param(prep_stmt, 2, MEMAIL)
            ibm_db.bind_param(prep_stmt, 3, MPASSWORD)
            ibm_db.execute(prep_stmt)
            return render_template('Merchant_login.html')
    except Exception as e:
        # Handle the exception here
        print(f"An error occurred: {e}")
        return render_template('error.html')
    
# Merchant_home page routing
    
@app.route('/merchanthome')
def merchanthome():
    return render_template('Merchant_home.html') 



if __name__ == "__main__":
    app.run(debug=True)