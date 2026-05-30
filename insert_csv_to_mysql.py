import mysql.connector
import pandas as pd
from datetime import datetime
import chardet
import matplotlib.pyplot as plt

def insert_csv_to_mysql(file_path):
    print(f"📥 開始匯入資料：{file_path}")

    # 🔍 自動偵測檔案編碼
    with open(file_path, "rb") as f:
        encoding = chardet.detect(f.read())["encoding"]

    # ✅ 自動判斷分隔符號（, 或 \t）
    with open(file_path, "r", encoding=encoding) as f:
        first_line = f.readline()
        delimiter = "\t" if "\t" in first_line else ","

    # ✅ 正確讀取 CSV
    df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding)

    # 🔄 若偵測到是「縱向格式」
    if df.shape[1] == 2 and df.columns[0].strip().lower() in ["user_id", "項目", "欄位"]:
        df.columns = [c.strip() for c in df.columns]  # 去掉空白
        df = df.set_index(df.columns[0]).T
        df.reset_index(drop=True, inplace=True)
        print("🔄 已自動轉換縱向 CSV 為橫向格式")

    # 將 1/0 轉換為 ENUM 對應值
    mapping_dict = {
        'sex': {1: '男', 0: '女'},
        'smoking': {1: '有', 0: '無'},
        'drinking': {1: '有', 0: '無'},
        'exercise': {1: '有', 0: '無'},
        'diabetes': {1: '有', 0: '無'},
        'sleep_disorder': {1: '有', 0: '無'},
        'hypertension': {1: '有', 0: '無'}
    }

    for col, mapping in mapping_dict.items():
        if col in df.columns:
            df[col] = df[col].map(mapping).fillna(df[col])

    # 定義風險等級轉換函數
    def risk_level(score):
        if score < 0:
            return "未知"  # 防呆：避免負數
        elif score <= 30:
            return "低風險"
        elif score <= 60:
            return "中等風險"
        elif score <= 100:
            return "高風險"
    
    # ✅ 檢查並補上缺少的欄位
    expected_columns = [
        "user_id", "systolic_pressure", "diastolic_pressure", "pulse", "temperature",
        "height", "weight", "cholesterol", "blood_sugar", "smoking", "drinking",
        "exercise", "diabetes", "sleep_disorder", "hypertension",
        "overall_risk_score", "systolic_pressure_p", "diastolic_pressure_p",
        "pulse_p", "temperature_p", "blood_sugar_p", "cholesterol_p",
        "smoking_p", "drinking_p", "exercise_p", "diabetes_p", "sleep_disorder_p"
    ]

    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0
            print(f"⚠️ 欄位 '{col}' 缺失，已補上預設值 0")



    # ✅ 固定欄位內容
    df["name"] = "王小美"
    df["sex"] = "女"
    df["birth_date"] = "2000-01-01"
    df["phone"] = "0912-345-678"
    df["email"] = "wang.xiaomei@example.com"
    df["doctor_id"] = 1
    df["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df["risk_level"] = df["overall_risk_score"].apply(risk_level)
    df["age"] = 20
    df["diagnose_result"] = "無"
    df["diagnosis_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df["BMI"] = round(df["weight"] / ((df["height"]/100)**2), 2)

    # ✅ 連線到 MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # ← 改成你自己的 MySQL 密碼
        database="ahrw-sts"     # ← 改成你的資料庫名稱
    )
    cursor = conn.cursor()

    # ✅ 準備 INSERT 指令
    sql = """
    INSERT INTO patients (
        user_id, name, sex, birth_date, phone, email, doctor_id, created_at,
        risk_level, age, height, weight, BMI, systolic_pressure, diastolic_pressure,
        pulse, temperature, cholesterol, blood_sugar,  smoking, drinking, exercise,
        diagnose_result, diabetes, sleep_disorder, diagnosis_time, overall_risk_score,
        systolic_pressure_p, diastolic_pressure_p, pulse_p, temperature_p,
        blood_sugar_p, cholesterol_p, smoking_p, drinking_p, exercise_p,
        diabetes_p, sleep_disorder_p, hypertension
    )
    VALUES (
        %(user_id)s, %(name)s, %(sex)s, %(birth_date)s, %(phone)s, %(email)s, %(doctor_id)s, %(created_at)s,
        %(risk_level)s, %(age)s, %(height)s, %(weight)s, %(BMI)s, %(systolic_pressure)s, %(diastolic_pressure)s, %(pulse)s,
        %(temperature)s, %(cholesterol)s, %(blood_sugar)s, %(smoking)s, %(drinking)s, %(exercise)s,
        %(diagnose_result)s, %(diabetes)s, %(sleep_disorder)s, %(diagnosis_time)s, %(overall_risk_score)s ,
        %(systolic_pressure_p)s, %(diastolic_pressure_p)s, %(pulse_p)s, %(temperature_p)s,
        %(blood_sugar_p)s, %(cholesterol_p)s, %(smoking_p)s, %(drinking_p)s, %(exercise_p)s,
        %(diabetes_p)s, %(sleep_disorder_p)s, %(hypertension)s
    )
    """


    # ✅ 將每一列插入 MySQL
    for _, row in df.iterrows():
        cursor.execute(sql, row.to_dict())

    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ 匯入成功，共 {len(df)} 筆資料！")

    
    columns_of_interest = [ "systolic_pressure_p", "diastolic_pressure_p", "pulse_p", "temperature_p", "blood_sugar_p", "cholesterol_p", "smoking_p", "drinking_p", "exercise_p", "diabetes_p", "sleep_disorder_p" ]
     # 取第一筆資料 
    data = df.loc[0, columns_of_interest] 
    # 轉成 Series 並排序 
    data_sorted = data.sort_values(ascending=True) 
    # 小到大，如果想大到小改成 False 
    # 畫橫向長條圖 
    plt.figure(figsize=(8,6)) 
    plt.barh(data_sorted.index, data_sorted.values, color='skyblue')
    plt.xlabel("Value", fontsize=18)
    plt.title("Health Indicator Ranking Bar Chart", fontsize=18)
    plt.tight_layout()

    save_path = r"C:\Users\user\Desktop\ahrw-system\static\img\health_chart.png"
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"📊 圖表已儲存至：{save_path}")
    # plt.show() 
        
