# AHRW-STS 系統操作說明

## 環境需求

- Python 3.13+
- MySQL
- MATLAB（用於解碼加密文件）

---

## 首次安裝套件

在虛擬環境中執行一次即可：

```cmd
cd C:\Users\user\Desktop\ahrw-system
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 每次啟動步驟

### 1. 開啟以下程式

- MySQL（確認資料庫服務已啟動）
- MATLAB
- 開啟兩個 cmd 視窗

---

### 2. 啟動網站（cmd 視窗 1）

依照自己電腦路徑進入專案資料夾，啟動虛擬環境後執行：

```cmd
cd C:\Users\user\Desktop\ahrw-system
venv\Scripts\activate
python app.py
```

---

### 3. 啟動 CSV 監控程式（cmd 視窗 2）

同樣進入專案資料夾並啟動虛擬環境，再執行：

```cmd
cd C:\Users\user\Desktop\ahrw-system
venv\Scripts\activate
python csv_watcher.py
```

---

## 解碼與資料上傳流程

1. 將加密文件放入：
   ```
   C:\Users\user\Downloads\decode\read
   ```

2. 開啟 MATLAB，執行 `auto_extract_main`

3. 解碼成功後，`result` 資料夾內會自動產生 5 個檔案

4. `csv_watcher.py` 偵測到新檔案後，自動寫入資料庫

5. 重新整理網站頁面，即可看到解碼後的病患資料

---

## 資料夾結構說明

```
C:\Users\user\Downloads\decode\
├── read\      ← 放入加密文件
└── result\    ← 解碼後的 CSV 自動產生於此
```
