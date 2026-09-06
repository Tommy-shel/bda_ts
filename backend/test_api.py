import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, "backend"))

from main import predict_with_spark_weights

title1 = "SHOCKING: Aliens landed in Washington DC last night! Leaked video conspiracy"
text1 = "A shocking secret whistleblower from big pharma reports UFO spacecraft hovering over Capitol."
label1, conf1 = predict_with_spark_weights(f"{title1} {text1}")

print("\n--- Test 1 (Fake News) ---")
print(f"Prediction: {label1}")
print(f"Confidence: {conf1 * 100:.2f}%")

title2 = "Senate passes bipartisan infrastructure bill"
text2 = "The Senate today voted in favor of a major infrastructure package, funding critical upgrades to roads and bridges."
label2, conf2 = predict_with_spark_weights(f"{title2} {text2}")

print("\n--- Test 2 (Real News) ---")
print(f"Prediction: {label2}")
print(f"Confidence: {conf2 * 100:.2f}%")
