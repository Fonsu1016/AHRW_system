"""
XGBoost 心臟風險因子分析模組
用於分析使用者健康資料並預測各項危險因子的風險機率
"""

import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
import pickle
from datetime import datetime

class XGBoostRiskAnalyzer:
    """XGBoost 風險分析器"""

    def __init__(self, csv_path=None, model_path=None):
        """
        初始化分析器

        Args:
            csv_path: 訓練資料 CSV 檔案路徑
            model_path: 已訓練模型的路徑（若存在則載入）
        """
        self.csv_path = csv_path or r"C:\Users\USER\Desktop\csmu\實驗室\因子預測\IHCAdata01.csv"
        self.model_path = model_path or os.path.join(
            os.path.dirname(__file__), 'xgboost_model.pkl'
        )
        self.model = None
        self.feature_names = [
            'age', 'sex', 'smoke', 'drink', 'BMI',
            'CPR', 'ROSC', 'temperature1', 'heartbeat1', 'b',
            'sblood pressure1', 'dblood pressure1'
        ]
        self.feature_importances = None
        self.training_accuracy = None
        self.test_accuracy = None

    def load_training_data(self):
        """載入訓練資料"""
        try:
            print(f"📂 正在載入訓練資料: {self.csv_path}")
            csv_data = pd.read_csv(self.csv_path, index_col=0)
            csv_data = pd.DataFrame(csv_data)

            # 提取特徵和標籤
            features = csv_data[self.feature_names]
            labels = csv_data[['target']]

            print(f"✅ 訓練資料載入成功: {len(csv_data)} 筆記錄")
            return features, labels

        except Exception as e:
            print(f"❌ 載入訓練資料失敗: {e}")
            return None, None

    def train_model(self, test_size=0.33, random_state=0, n_estimators=100, learning_rate=0.3):
        """
        訓練 XGBoost 模型

        Args:
            test_size: 測試集比例
            random_state: 隨機種子
            n_estimators: 決策樹數量
            learning_rate: 學習率

        Returns:
            bool: 訓練是否成功
        """
        try:
            # 載入資料
            features, labels = self.load_training_data()
            if features is None:
                return False

            # 分割訓練集和測試集
            train_features, test_features, train_labels, test_labels = train_test_split(
                features, labels, test_size=test_size, random_state=random_state
            )

            print(f"🔄 開始訓練 XGBoost 模型...")
            print(f"   訓練集: {len(train_features)} 筆")
            print(f"   測試集: {len(test_features)} 筆")

            # 構造 XGBoost 模型
            self.model = XGBClassifier(n_estimators=n_estimators, learning_rate=learning_rate)

            # 訓練模型
            self.model.fit(train_features, train_labels)

            # 評估模型
            train_predictions = self.model.predict(train_features)
            test_predictions = self.model.predict(test_features)

            self.training_accuracy = accuracy_score(train_labels, train_predictions)
            self.test_accuracy = accuracy_score(test_labels, test_predictions)

            print(f"✅ 模型訓練完成")
            print(f"   訓練集準確度: {self.training_accuracy:.4f}")
            print(f"   測試集準確度: {self.test_accuracy:.4f}")

            # 取得特徵重要性
            self.feature_importances = self.model.feature_importances_

            # 儲存模型
            self.save_model()

            return True

        except Exception as e:
            print(f"❌ 模型訓練失敗: {e}")
            return False

    def save_model(self):
        """儲存訓練好的模型"""
        try:
            # 確保目錄存在
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

            # 儲存模型和相關資訊
            model_data = {
                'model': self.model,
                'feature_names': self.feature_names,
                'feature_importances': self.feature_importances,
                'training_accuracy': self.training_accuracy,
                'test_accuracy': self.test_accuracy,
                'trained_at': datetime.now().isoformat()
            }

            with open(self.model_path, 'wb') as f:
                pickle.dump(model_data, f)

            print(f"💾 模型已儲存至: {self.model_path}")
            return True

        except Exception as e:
            print(f"❌ 模型儲存失敗: {e}")
            return False

    def load_model(self):
        """載入已訓練的模型"""
        try:
            if not os.path.exists(self.model_path):
                print(f"⚠️  模型檔案不存在: {self.model_path}")
                return False

            with open(self.model_path, 'rb') as f:
                model_data = pickle.load(f)

            self.model = model_data['model']
            self.feature_names = model_data['feature_names']
            self.feature_importances = model_data.get('feature_importances')
            self.training_accuracy = model_data.get('training_accuracy')
            self.test_accuracy = model_data.get('test_accuracy')

            print(f"✅ 模型載入成功")
            print(f"   訓練時間: {model_data.get('trained_at', 'Unknown')}")
            print(f"   測試集準確度: {self.test_accuracy:.4f}")

            return True

        except Exception as e:
            print(f"❌ 模型載入失敗: {e}")
            return False

    def prepare_user_data(self, health_data, user_profile=None):
        """
        準備使用者資料以進行預測

        Args:
            health_data: 從 health_data 表取得的健康資料 (dict)
            user_profile: 從 user_profiles 表取得的使用者資料 (dict, optional)

        Returns:
            pd.DataFrame: 準備好的特徵資料
        """
        try:
            # 計算 BMI
            height_m = float(health_data.get('height', 170)) / 100
            weight_kg = float(health_data.get('weight', 70))
            bmi = weight_kg / (height_m * height_m) if height_m > 0 else 23

            # 從 user_profile 或 health_data 取得年齡和性別
            if user_profile:
                age = int(user_profile.get('age', 50))
                sex = 1 if user_profile.get('gender', 'male') == 'male' else 0
            else:
                # 如果沒有 user_profile，使用預設值
                age = 50
                sex = 1

            # 準備特徵資料（對應訓練資料的12個特徵）
            user_features = {
                'age': age,
                'sex': sex,
                'smoke': 1 if health_data.get('smoking', False) else 0,
                'drink': 1 if health_data.get('drinking', False) else 0,
                'BMI': round(bmi, 1),
                'CPR': 1 if health_data.get('hypertension', False) else 0,  # 使用高血壓作為 CPR 代理
                'ROSC': 1 if health_data.get('diabetes', False) else 0,  # 使用糖尿病作為 ROSC 代理
                'temperature1': float(health_data.get('temperature', 36.5)),
                'heartbeat1': float(health_data.get('pulse', 75)),
                'b': 20,  # 預設值（原始資料中的 b 欄位意義不明確）
                'sblood pressure1': float(health_data.get('systolic_pressure', 120)),
                'dblood pressure1': float(health_data.get('diastolic_pressure', 80))
            }

            # 轉換為 DataFrame
            df = pd.DataFrame([user_features])
            df = df[self.feature_names]  # 確保欄位順序正確

            return df

        except Exception as e:
            print(f"❌ 準備使用者資料失敗: {e}")
            return None

    def analyze_risk(self, health_data, user_profile=None):
        """
        分析使用者的健康風險

        Args:
            health_data: 健康資料 (dict)
            user_profile: 使用者個人資料 (dict, optional)

        Returns:
            dict: 風險分析結果
        """
        try:
            # 確保模型已載入
            if self.model is None:
                if not self.load_model():
                    print("⚠️  模型未載入，嘗試訓練新模型...")
                    if not self.train_model():
                        return None

            # 準備使用者資料
            user_df = self.prepare_user_data(health_data, user_profile)
            if user_df is None:
                return None

            # 預測風險
            prediction = self.model.predict(user_df)[0]
            prediction_proba = self.model.predict_proba(user_df)[0]

            # 計算整體風險分數
            risk_score = float(prediction_proba[1])  # 高風險的機率

            # 取得各特徵的重要性作為風險因子分析
            feature_importance_dict = {}
            if self.feature_importances is not None:
                for feature_name, importance in zip(self.feature_names, self.feature_importances):
                    feature_importance_dict[feature_name] = float(importance)

            # 判斷風險等級
            if risk_score < 0.3:
                risk_level = 'low'
            elif risk_score < 0.6:
                risk_level = 'medium'
            elif risk_score < 0.8:
                risk_level = 'high'
            else:
                risk_level = 'critical'

            # 組織分析結果
            analysis_result = {
                'prediction': int(prediction),  # 0: 低風險, 1: 高風險
                'overall_risk_score': round(risk_score, 4),
                'risk_level': risk_level,
                'risk_probability': {
                    'low_risk': round(float(prediction_proba[0]), 4),
                    'high_risk': round(float(prediction_proba[1]), 4)
                },
                # 特徵重要性作為風險因子分析（存入資料庫的欄位）
                'systolic_pressure': feature_importance_dict.get('sblood pressure1', 0.0),
                'diastolic_pressure': feature_importance_dict.get('dblood pressure1', 0.0),
                'pulse': feature_importance_dict.get('heartbeat1', 0.0),
                'temperature': feature_importance_dict.get('temperature1', 0.0),
                'blood_sugar': 0.0,  # CSV 中沒有血糖，設為 0
                'cholesterol': 0.0,  # CSV 中沒有膽固醇，設為 0
                'smoking': feature_importance_dict.get('smoke', 0.0),
                'drinking': feature_importance_dict.get('drink', 0.0),
                'exercise': 0.0,  # CSV 中沒有運動，設為 0
                'diabetes': feature_importance_dict.get('ROSC', 0.0),
                'sleep_disorder': 0.0,  # CSV 中沒有睡眠障礙，設為 0
                'hypertension': feature_importance_dict.get('CPR', 0.0),
                'analyzed_at': datetime.now().isoformat()
            }

            print(f"✅ 風險分析完成")
            print(f"   整體風險分數: {risk_score:.4f}")
            print(f"   風險等級: {risk_level}")

            return analysis_result

        except Exception as e:
            print(f"❌ 風險分析失敗: {e}")
            import traceback
            traceback.print_exc()
            return None

    def get_feature_importance_report(self):
        """取得特徵重要性報告"""
        if self.feature_importances is None:
            return None

        importance_list = []
        for feature_name, importance in zip(self.feature_names, self.feature_importances):
            importance_list.append({
                'feature': feature_name,
                'importance': float(importance)
            })

        # 依重要性排序
        importance_list.sort(key=lambda x: x['importance'], reverse=True)

        return importance_list


# 全域分析器實例（單例模式）
_global_analyzer = None

def get_analyzer():
    """取得全域分析器實例"""
    global _global_analyzer
    if _global_analyzer is None:
        _global_analyzer = XGBoostRiskAnalyzer()
        # 嘗試載入已訓練的模型，若不存在則訓練新模型
        if not _global_analyzer.load_model():
            print("⚠️  未找到已訓練的模型，開始訓練新模型...")
            _global_analyzer.train_model()
    return _global_analyzer


def analyze_health_risk(health_data, user_profile=None):
    """
    便捷函數：分析健康風險

    Args:
        health_data: 健康資料 (dict)
        user_profile: 使用者個人資料 (dict, optional)

    Returns:
        dict: 風險分析結果
    """
    analyzer = get_analyzer()
    return analyzer.analyze_risk(health_data, user_profile)


# 測試函數
if __name__ == '__main__':
    print("=== XGBoost 風險分析器測試 ===\n")

    # 創建分析器
    analyzer = XGBoostRiskAnalyzer()

    # 訓練模型
    print("1. 訓練模型...")
    if analyzer.train_model():
        print("\n2. 特徵重要性報告:")
        importance_report = analyzer.get_feature_importance_report()
        if importance_report:
            for item in importance_report:
                print(f"   {item['feature']}: {item['importance']:.4f}")

        # 測試預測
        print("\n3. 測試預測...")
        test_health_data = {
            'systolic_pressure': 140,
            'diastolic_pressure': 90,
            'pulse': 85,
            'temperature': 36.8,
            'height': 170,
            'weight': 75,
            'smoking': True,
            'drinking': False,
            'exercise': True,
            'diabetes': False,
            'sleep_disorder': False,
            'hypertension': True
        }

        result = analyzer.analyze_risk(test_health_data)
        if result:
            print(f"\n   分析結果:")
            print(f"   - 整體風險分數: {result['overall_risk_score']:.4f}")
            print(f"   - 風險等級: {result['risk_level']}")
            print(f"   - 低風險機率: {result['risk_probability']['low_risk']:.4f}")
            print(f"   - 高風險機率: {result['risk_probability']['high_risk']:.4f}")

        print("\n✅ 測試完成！")
    else:
        print("\n❌ 模型訓練失敗")
