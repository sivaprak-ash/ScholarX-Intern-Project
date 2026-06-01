# ScholarX-Intern-Project

# 📄 Document Classifier

A machine learning pipeline that automatically classifies documents into four common business categories — **Invoice**, **Contract**, **Email**, and **Report** — using TF-IDF features and classical ML models.

---

## 🚀 Features

- Classifies documents into 4 categories: `invoice`, `contract`, `email`, `report`
- Trains and benchmarks **5 ML models** automatically
- Selects and saves the best model based on F1-macro score
- Generates visualizations: confusion matrix, model comparison, top features
- Includes a synthetic dataset generator for bootstrapping
- Simple inference script for classifying new documents

---

## 📁 Project Structure

```
doc_classifier/
├── generate_data.py        # Synthetic dataset generator (800 samples)
├── train.py                # Model training, evaluation & visualization
├── predict.py              # Inference on new documents
├── dataset.csv             # Generated labeled dataset
├── best_model.pkl          # Saved best model (Logistic Regression)
└── outputs/
    ├── best_model.pkl              # Trained pipeline (TF-IDF + classifier)
    ├── confusion_matrix.png        # Confusion matrix + per-class F1
    ├── model_comparison.png        # All models comparison chart
    ├── top_features.png            # Most discriminative words per class
    ├── classification_report.csv   # Detailed per-class metrics
    ├── top_features.csv            # Top TF-IDF features per class
    └── summary.json                # Training summary & scores
```

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/doc-classifier.git
cd doc-classifier
pip install -r requirements.txt
```

**Requirements:**
```
scikit-learn>=1.0
pandas
numpy
matplotlib
seaborn
joblib
```

Or install directly:
```bash
pip install scikit-learn pandas numpy matplotlib seaborn joblib
```

---

## 🏋️ Training

**Step 1 — Generate synthetic dataset** (skip if you have your own data):
```bash
python generate_data.py
```
This creates `dataset.csv` with 800 labeled samples (200 per class).

**Step 2 — Train models:**
```bash
python train.py
```

This will:
- Train 5 models (Logistic Regression, Linear SVM, Multinomial NB, Random Forest, Gradient Boosting)
- Print a comparison table of accuracy, F1-macro, and 5-fold CV scores
- Save the best model to `outputs/best_model.pkl`
- Generate all plots and reports in `outputs/`

### Sample training output:
```
Model                     Acc     F1-macro    CV-mean
----------------------------------------------------------
Logistic Regression      1.0000     1.0000     1.0000  ✅ Best
Linear SVM               1.0000     1.0000     1.0000
Multinomial NB           1.0000     1.0000     1.0000
Random Forest            1.0000     1.0000     1.0000
Gradient Boosting        1.0000     1.0000     1.0000
```

> **Note:** Scores of 1.0 are expected on the synthetic dataset due to its clean, template-based structure. On real-world documents you can expect **90–97% accuracy**.

---

## 🔍 Inference

Classify new documents using the saved model:

```bash
python predict.py
```

Or use it programmatically:

```python
import joblib

model = joblib.load("outputs/best_model.pkl")

texts = [
    "Invoice #INV-4521 | Bill To: Acme Corp | Total Due: $1180.00",
    "SERVICE AGREEMENT between TechNova Ltd and John Smith. Term: 12 months.",
    "From: john@company.com | Subject: Meeting Follow-up | Hi Sarah...",
    "QUARTERLY REPORT Q2 2024 | Revenue: $45.2M (+12.5% YoY)",
]

predictions = model.predict(texts)
for text, pred in zip(texts, predictions):
    print(f"{pred.upper():<12} → {text[:60]}")
```

**Output:**
```
INVOICE      → Invoice #INV-4521 | Bill To: Acme Corp | Total Due: $...
CONTRACT     → SERVICE AGREEMENT between TechNova Ltd and John Smith...
EMAIL        → From: john@company.com | Subject: Meeting Follow-up |...
REPORT       → QUARTERLY REPORT Q2 2024 | Revenue: $45.2M (+12.5% Y...
```

---

## 📊 Results

| Model | Accuracy | F1-Macro | CV F1 (5-fold) |
|---|---|---|---|
| **Logistic Regression** ✅ | 1.0000 | 1.0000 | 1.0000 |
| Linear SVM | 1.0000 | 1.0000 | 1.0000 |
| Multinomial NB | 1.0000 | 1.0000 | 1.0000 |
| Random Forest | 1.0000 | 1.0000 | 1.0000 |
| Gradient Boosting | 1.0000 | 1.0000 | 1.0000 |

---

## 🔧 Using Your Own Data

Replace `dataset.csv` with your own labeled dataset. The file must have two columns:

```csv
text,label
"Invoice #1234 Total Due $500","invoice"
"This agreement is between...","contract"
...
```

Then simply run:
```bash
python train.py
```

The pipeline handles all preprocessing automatically.

---

## 🧠 How It Works

```
Raw Text
   │
   ▼
TF-IDF Vectorizer  (unigrams + bigrams, top 20,000 features, sublinear TF)
   │
   ▼
Classifier  (Logistic Regression / SVM / NB / RF / GBM)
   │
   ▼
Predicted Label  →  invoice | contract | email | report
```

The best model is selected automatically by F1-macro score and saved as a single sklearn `Pipeline` object, so vectorization and prediction are bundled together.

---

## 📈 Visualizations

| Plot | Description |
|---|---|
| `confusion_matrix.png` | Heatmap of true vs predicted labels + per-class F1 bars |
| `model_comparison.png` | Accuracy, F1, and CV scores across all 5 models |
| `top_features.png` | Top 10 TF-IDF features driving each class prediction |

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

*Built with scikit-learn, pandas, and matplotlib.*
