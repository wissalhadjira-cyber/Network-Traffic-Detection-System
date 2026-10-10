import pandas as pd
import numpy as np
import joblib
import glob
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier  
from sklearn.metrics import accuracy_score
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("   NETWORK Traffic DETECTION - TRAINING")
print("=" * 60)

# ==============================================
# ⚙️ الإعدادات
# ==============================================
NROWS = 150000
NUM_FEATURES = 15
# ==============================================

# 1. البحث عن الملفات
print("\n[1] Finding CSV files...")
path = "data/MachineLearningCVE/*.csv"
all_files = glob.glob(path)

if not all_files:
    print("❌ No CSV files found!")
    exit()

print(f"✅ Found {len(all_files)} files")

# 2. قراءة البيانات
print(f"\n[2] Loading {NROWS:,} rows per file...")
all_data = []
total_rows = 0

for filename in all_files:
    try:
        df = pd.read_csv(filename, nrows=NROWS, low_memory=False)
        df.columns = df.columns.str.strip()
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        
        if len(df) > 0:
            all_data.append(df)
            total_rows += len(df)
            print(f"   ✅ {os.path.basename(filename)}: {len(df):,} rows")
    except Exception as e:
        print(f"   ⚠️ Skipped: {e}")

if not all_data:
    print("❌ No data loaded!")
    exit()

data = pd.concat(all_data, axis=0, ignore_index=True)
print(f"\n✅ Total: {len(data):,} rows")

# 3. تنظيف
print("\n[3] Cleaning data...")
non_numeric = data.select_dtypes(exclude=[np.number]).columns
non_numeric = [col for col in non_numeric if col != 'Label']
if len(non_numeric) > 0:
    data.drop(columns=non_numeric, inplace=True)
    print(f"   ✅ Dropped {len(non_numeric)} non-numeric columns")

# 4. ترميز
print("\n[4] Encoding labels...")
label_encoder = LabelEncoder()
data['Label_Encoded'] = label_encoder.fit_transform(data['Label'])
print(f"   ✅ {len(label_encoder.classes_)} classes")

# 5. فصل الخصائص
print(f"\n[5] Preparing features...")
X = data.drop(columns=['Label', 'Label_Encoded'])
y = data['Label_Encoded']
if X.shape[1] > NUM_FEATURES:
    X = X.iloc[:, :NUM_FEATURES]
print(f"   ✅ Using {X.shape[1]} features")

# 6. تطبيع
print("\n[6] Normalizing...")
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 7. تقسيم
print("\n[7] Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)
print(f"   ✅ Train: {len(X_train):,}, Test: {len(X_test):,}")

# 8. تدريب النموذج (RandomForest)
print("\n[8] Training RandomForest model...")

model = RandomForestClassifier(
    n_estimators=50,          
    max_depth=15,            
    min_samples_split=10,
    min_samples_leaf=4,
    class_weight='balanced',  
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)
print(f"   ✅ Training completed")

# 9. تقييم
print("\n[9] Evaluating...")
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"   ✅ Accuracy: {acc * 100:.2f}%")

# 10. حفظ
print("\n[10] Saving model...")
joblib.dump(model, "random_forest_model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")
joblib.dump(scaler, "scaler.pkl")
print("   ✅ Saved!")
print("\n" + "=" * 60)
print("   ✅ TRAINING COMPLETED")
print("=" * 60)
print(f"\n📊 Summary:")
print(f"   - Files: {len(all_files)}")
print(f"   - Samples: {len(data):,}")
print(f"   - Features: {X.shape[1]}")
print(f"   - Accuracy: {acc * 100:.2f}%")
print(f"   - Model: {type(model).__name__}")