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

title3 = "Nepal Flood: Death Toll Rises as Rescue Operations Continue"
text3 = "Devastating floods in Nepal have displaced thousands. Emergency teams are working around the clock to provide relief and food to affected regions. The government has declared a state of emergency in several districts."
label3, conf3 = predict_with_spark_weights(f"{title3} {text3}")

print("\n--- Test 3 (Real News - Nepal Flood) ---")
print(f"Prediction: {label3}")
print(f"Confidence: {conf3 * 100:.2f}%")

title4 = "CJP Protest Secretly Funded by Foreign Intelligence"
text4 = "Reports indicate that the recent protests against the Chief Justice were orchestrated by foreign agents looking to destabilize the nation. Evidence of secret payments has surfaced on the dark web."
label4, conf4 = predict_with_spark_weights(f"{title4} {text4}")

print("\n--- Test 4 (Fake News - CJP Protest) ---")
print(f"Prediction: {label4}")
print(f"Confidence: {conf4 * 100:.2f}%")

title5 = "CJP Protest: Lawyers and Activists Gather Outside Supreme Court"
text5 = "Massive protests erupted today as legal experts and activists gathered to demand judicial reforms. The Chief Justice of Pakistan's recent decisions have sparked a nationwide debate on constitutional powers."
label5, conf5 = predict_with_spark_weights(f"{title5} {text5}")

print("\n--- Test 5 (Real News - CJP Protest) ---")
print(f"Prediction: {label5}")
print(f"Confidence: {conf5 * 100:.2f}%")
