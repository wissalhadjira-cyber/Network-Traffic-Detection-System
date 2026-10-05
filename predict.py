import joblib
import numpy as np
import pandas as pd
import glob
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("   NETWORK TRAFFIC DETECTION - PREDICTION")
print("=" * 60)

# ==============================================
# 1. تحميل النموذج والمحولات
# ==============================================
print("\n[1] Loading model and encoders...")

try:
    model = joblib.load("random_forest_model.pkl")
    label_encoder = joblib.load("label_encoder.pkl")
    scaler = joblib.load("scaler.pkl")
    print("✅ All files loaded successfully!")
    print(f"   - Model: {type(model).__name__}")
    print(f"   - Classes: {len(label_encoder.classes_)}")
except FileNotFoundError as e:
    print(f"❌ Error: {e}")
    print("   Please run main.py first.")
    exit()

# ==============================================
# 2. اختيار الملفات للتحليل
# ==============================================
print("\n[2] Select files to analyze...")

path = "data/MachineLearningCVE/*.csv"
all_files = glob.glob(path)

if not all_files:
    print("❌ No CSV files found!")
    exit()

print(f"\n📁 Found {len(all_files)} CSV files:")
for i, f in enumerate(all_files):
    size_mb = os.path.getsize(f) / (1024 * 1024)
    print(f"   {i+1}. {os.path.basename(f)} ({size_mb:.1f} MB)")

print("\nOptions:")
print("  a. Analyze ALL files")
print("  b. Analyze a specific file (enter number)")

choice = input("\nEnter your choice (a or number): ").strip()

if choice.lower() == 'a':
    files_to_analyze = all_files
    print("\n📊 Analyzing ALL files...")
elif choice.isdigit() and 1 <= int(choice) <= len(all_files):
    files_to_analyze = [all_files[int(choice) - 1]]
    print(f"\n📊 Analyzing: {os.path.basename(files_to_analyze[0])}")
else:
    print("❌ Invalid choice! Analyzing all files...")
    files_to_analyze = all_files

# ==============================================
# 3. قراءة وتحليل كل ملف
# ==============================================
print("\n[3] Processing files...")
print("-" * 50)

all_predictions = []
total_rows = 0

for file_idx, file_path in enumerate(files_to_analyze):
    print(f"\n📁 File {file_idx+1}/{len(files_to_analyze)}: {os.path.basename(file_path)}")
    
    try:
        # قراءة الملف
        data = pd.read_csv(file_path, low_memory=False)
        print(f"   ✅ Loaded {len(data):,} rows")
        
        # تنظيف البيانات
        data.columns = data.columns.str.strip()
        data.replace([np.inf, -np.inf], np.nan, inplace=True)
        data.fillna(0, inplace=True)
        
        # ==============================================
        # 4. استخدام أول 15 خاصية (مثل التدريب)
        # ==============================================
        X = data.iloc[:, :15]  # ← 15 خاصية
        print(f"   ✅ Using {X.shape[1]} features")
        
        # ==============================================
        # 5. تطبيع البيانات
        # ==============================================
        X_scaled = scaler.transform(X)
        
        # ==============================================
        # 6. التنبؤ
        # ==============================================
        predictions = model.predict(X_scaled)
        predicted_labels = label_encoder.inverse_transform(predictions)
        
        all_predictions.extend(predicted_labels)
        total_rows += len(data)
        
        # إحصائيات هذا الملف
        malicious = np.sum(predicted_labels != "BENIGN")
        print(f"   ✅ Detected: {malicious:,} malicious flows")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        continue

if not all_predictions:
    print("❌ No data processed!")
    exit()

# ==============================================
# 7. النتائج النهائية
# ==============================================
print("\n" + "=" * 60)
print("   FINAL DETECTION SUMMARY")
print("=" * 60)

total_count = len(all_predictions)
malware_count = np.sum(np.array(all_predictions) != "BENIGN")
benign_count = total_count - malware_count

print(f"Total flows analyzed:   {total_count:,}")
print(f"Benign traffic:         {benign_count:,}")
print(f"MALICIOUS/SUSPICIOUS:   {malware_count:,}")
print("-" * 60)

if malware_count == 0:
    print("🟢 STATUS: ALL CLEAR - No threats detected")
else:
    percentage = (malware_count / total_count) * 100
    if percentage > 50:
        status = "🔴 CRITICAL - High threat level!"
    elif percentage > 20:
        status = "🟠 WARNING - Medium threat level"
    else:
        status = "🟡 CAUTION - Low threat level"
    
    print(f"🚨 {status}")
    print(f"   {malware_count:,} malicious flows detected ({percentage:.2f}%)")

print("=" * 60)

# ==============================================
# 8. توزيع الهجمات
# ==============================================
print("\n📊 Detailed Traffic Distribution:")
print("-" * 60)

traffic_dist = pd.Series(all_predictions).value_counts()
for label, count in traffic_dist.items():
    percentage = (count / total_count) * 100
    bar = "█" * int(percentage / 2)
    print(f"{label:25} {count:8,} ({percentage:5.2f}%) {bar}")

print("\n" + "=" * 60)
print("   ✅ ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)