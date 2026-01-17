from flask import Flask,render_template, request, redirect, url_for, flash,session #request接收使用者提交的表單資料（如帳號密碼）
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash #加密 / 驗證密碼
from flask_socketio import SocketIO
from datetime import datetime

app = Flask(__name__)#建立一個 Flask 應用實例，__name__ 代表目前這個 Python 檔案的名稱。
app.secret_key = '13579'  # 用於 flash 提示訊息
socketio = SocketIO(app)

# 設定資料庫參數
app.config['MYSQL_HOST'] = 'localhost'#指定 MySQL 伺服器主機位置為本機
app.config['MYSQL_USER'] = 'root'#登入資料庫使用的帳號，通常是 root（可自行修改）
app.config['MYSQL_PASSWORD'] = ''  # 如果你有設密碼，請填入
app.config['MYSQL_DB'] = 'ahrw-sts'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'#指定游標類型為 DictCursor，代表查詢資料會以字典格式回傳（key 是欄位名稱）

# 初始化 MySQL
mysql = MySQL(app)

@app.route('/test-db')
def test_db():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        return str(users)
    except Exception as e:
        return f"資料庫錯誤：{e}"
    
@app.route('/')#顯示登入畫面
def login_page():
    return render_template('login.html',msg='')

@app.route('/login', methods=['POST'])#處理登入驗證資料
def login():
    
    if request.method =='POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()#建立一個資料庫游標，用來執行 SQL 指令。
        # cur.execute('SELECT * FROM users WHERE username=%s', (username,))#只比對帳號
        cur.execute('SELECT * FROM users WHERE username=%s AND password = %s', (username, password))#去 users 資料表找出符合帳號和密碼的那一筆資料。
        isuser=cur.fetchone()#fetchone() 會把那筆資料取出來，變成一個字典
        cur.close()#關閉游標，釋放資源。

        # if isuser and check_password_hash(isuser['password'], password):#用來比較 加密後的密碼 和 使用者輸入的原始密碼
        if isuser:  
            session['doctor_id'] = isuser['id'] 
            return redirect(url_for('index_page'))
        
        else:
            flash('帳號或密碼錯誤，請重新輸入')
            return redirect(url_for('login_page'))#將使用者導回登入頁面（login_page() 函式所對應的 / 頁面）



@app.route('/index', methods=['GET'])
def index_page():
    doctor_id = session['doctor_id']#從使用者的 session（登入後儲存的資訊）中抓取目前登入醫生的 ID。
    user_id = request.args.get('user_id')  # 如果有輸入病患 ID 就會抓到
    cur = mysql.connection.cursor()

    if user_id:
        # 只查詢這位醫生的這位病患
        cur.execute("SELECT * FROM patients WHERE doctor_id = %s AND patient_id = %s", (doctor_id, user_id))
    else:
        # 查詢這位醫生的所有病患
        cur.execute("SELECT * FROM patients WHERE doctor_id = %s", (doctor_id,))
    patients = cur.fetchall()
    # 統計風險等級數量

    cur.execute("""
        SELECT 
            risk_level, COUNT(*) AS count
        FROM patients
        WHERE doctor_id = %s
        GROUP BY risk_level
    """, (doctor_id,))#是要傳入的參數，%s 就會被替換成這位醫生的 ID。
    risk_counts_raw = cur.fetchall()
    cur.close()

    # 整理統計資料為 dict，例如：{'高': 3, '中': 5, '低': 2}
    risk_counts = {'高風險': 0, '中風險': 0, '低風險': 0}# 先建一個字典，預設所有風險等級數量都設為 0，避免資料庫查不到某個等級時出錯。
    for row in risk_counts_raw:#把查詢回來的結果逐一塞入 risk_counts 字典中。
        risk_counts[row['risk_level']] = row['count'] #ex：risk_counts['高'] = 3

    return render_template('index.html', patients=patients, risk_counts=risk_counts)



@app.route('/diagnose/<int:user_id>')
def diagnose_patient(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM patients WHERE user_id = %s", (user_id,))
    patient = cur.fetchone()
    cur.close()
    # return redirect(url_for('diagnose_patient',patient=patient)) 
    return render_template('diagnose.html', patient=patient)

@app.route('/save_diagnosis/<int:user_id>', methods=['POST'])
def save_diagnosis(user_id):
    diagnosis = request.form["diagnosis"]
    diagnosis_time = datetime.now()

    cur = mysql.connection.cursor()
    # 用 UPDATE，而不是 INSERT
    cur.execute("""
        UPDATE patients
        SET diagnose_result = %s, diagnosis_time = %s
        WHERE user_id = %s
    """, (diagnosis, diagnosis_time, user_id))

    mysql.connection.commit()
    cur.close()

    return '', 204

    # # 重新撈病患資料回診斷頁面
    # cur = mysql.connection.cursor()
    # cur.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
    # patient = cur.fetchone()
    # cur.close()

    # return render_template('diagnose.html', patient=patient)



# def save_diagnosis():
#     diagnosis = request.form["diagnosis"]
#     diagnosis_time = datetime.now()

#     cur = mysql.connection.cursor()

#     cur.execute("""
#         INSERT INTO patients (diagnose_result, diagnosis_time)
#         VALUES (%s, %s)""",(diagnosis, diagnosis_time)
#     )
#     cur.commit()

#     cur.close()
#     return render_template('diagnose.html', patient=patient)



# @app.route('/search', methods=['GET'])
# def search_patient():
#     doctor_id = session['doctor_id']#從使用者的 session（登入後儲存的資訊）中抓取目前登入醫生的 ID。
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM patients WHERE doctor_id = %s", (doctor_id,))#用 %s 搭配 tuple (doctor_id,) 是為了防止 SQL injection（SQL 注入攻擊）。
#     patients = cur.fetchall()
#     cur.close()
#     return render_template('index.html',patients=patients)




@app.route('/update_profile', methods=['POST'])
def update_profile():
    # 從表單取得資料
    name = request.form['name']
    title = request.form['title']
    specialty = request.form['specialty']
    experience = request.form['experience']
    gender = request.form['gender']
    age = request.form['age']
    history = request.form['history']
    phone = request.form['phone']
    email = request.form['email']
    address = request.form['address']

    # 資料庫連線與更新
    conn = mysql.connection
    try:
        with conn.cursor() as cursor:
            sql = """
                UPDATE users
                SET name=%s, title=%s, specialty=%s, experience=%s,
                    gender=%s, age=%s, history=%s,
                    phone=%s, email=%s, address=%s
                WHERE doctor_id = %s
            """
            cursor.execute(sql, (name, title, specialty, experience, gender, age, history, phone, email, address, session['doctor_id']))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for('profile_page'))

@app.route('/profile')
def profile_page():
    conn = mysql.connection
    doctor_data = {}
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE doctor_id = %s", (session['doctor_id'],))
    doctor_data = cur.fetchone()
    conn.close()
    return render_template('profile.html', doctor=doctor_data)


@app.route('/setting')
def setting_page():
    return render_template('setting.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)# 清除使用者登入狀態
    return redirect(url_for('login_page'))# 導回登入畫面



# @app.route('/upload_data', methods=['POST'])
# def upload_data():
#     data = request.get_json()
#     patient_id = data.get('patient_id')
#     raw_data = data.get('raw_data')

#     # 解碼處理（你自訂的邏輯）
#     decoded_data = decode_algorithm(raw_data)

#     # 儲存至資料庫
#     cur = mysql.connection.cursor()
#     cur.execute("INSERT INTO records (patient_id, decoded_data) VALUES (%s, %s)",
#                 (patient_id, decoded_data))
#     mysql.connection.commit()
#     cur.close()

#     return {"status": "success"}, 200

# def decode_algorithm(raw_data):
#     # 假設只是回傳原始資料（你可改成你實際的演算法）
#     return raw_data





if __name__ == '__main__':
    app.run(debug=True)
