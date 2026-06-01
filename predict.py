"""Classify new documents using the trained model."""
import joblib
import sys

MODEL_PATH = "/home/claude/doc_classifier/outputs/best_model.pkl"

def classify(texts):
    model = joblib.load(MODEL_PATH)
    predictions = model.predict(texts)
    # Get probabilities if available
    try:
        probs = model.predict_proba(texts)
        classes = model.classes_
        for text, pred, prob in zip(texts, predictions, probs):
            print(f"\nText: {text[:80]}...")
            print(f"→ Predicted: {pred.upper()}")
            for cls, p in sorted(zip(classes, prob), key=lambda x: -x[1]):
                bar = "█" * int(p * 20)
                print(f"   {cls:<12} {p:.3f}  {bar}")
    except AttributeError:
        for text, pred in zip(texts, predictions):
            print(f"\nText: {text[:80]}...")
            print(f"→ Predicted: {pred.upper()}")
    return predictions

# Demo with sample texts
SAMPLES = [
    "Invoice #INV-4521 | Bill To: Acme Corp | Date: 15/03/2024 | "
    "Item: Software License x5 @ $200.00 | Total Due: $1180.00 | Tax: $180.00",

    "SERVICE AGREEMENT between TechNova Ltd and John Smith. Effective Date: 01/01/2024. "
    "Term: 12 months. Scope: IT consulting. Fees: $10,000/month. Governing Law: Karnataka.",

    "From: john.smith@company.com | To: hr@acme.com | Subject: Meeting Follow-up | "
    "Hi Sarah, I wanted to follow up on our last discussion regarding the project timeline. "
    "Best regards, John Smith",

    "QUARTERLY REPORT - Q2 2024 | Acme Corp | Revenue: $45.2M (+12.5% YoY). "
    "Key Highlights: Launched three new product lines. Outlook: Strong pipeline for next quarter.",
]

if __name__ == "__main__":
    print("=" * 60)
    print("DOCUMENT CLASSIFIER — Inference Demo")
    print("=" * 60)
    classify(SAMPLES)
