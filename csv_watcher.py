import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from insert_csv_to_mysql import insert_csv_to_mysql

class CSVHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)

        # ✅ 只處理非 raw 的 decoded_health_report 檔案
        if filename.startswith("decoded_health_report_") and "raw" not in filename:
            print(f"📄 偵測到新檔案: {filename}")
            try:
                insert_csv_to_mysql(event.src_path)
            except Exception as e:
                print(f"❌ 匯入失敗: {e}")
        else:
            print(f"⚠️ 忽略檔案：{filename}")

if __name__ == "__main__":
    folder_to_watch = r"C:\Users\user\Downloads\decode\result"  # ← 改成你的CSV資料夾
    print(f"🚀 正在監控資料夾: {folder_to_watch}")

    event_handler = CSVHandler()
    observer = Observer()
    observer.schedule(event_handler, folder_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
