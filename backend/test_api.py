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

title6 = "NASA confirms an artificial structure has been detected beneath the far side of the Moon"
text6 = "NASA scientists have reportedly confirmed the discovery of a large artificial structure buried beneath the far side of the Moon after analyzing gravitational anomalies recorded by a lunar spacecraft."
label6, conf6 = predict_with_spark_weights(f"{title6} {text6}")

print("\n--- Test 6 (Fake News - Moon Structure) ---")
print(f"Prediction: {label6}")
print(f"Confidence: {conf6 * 100:.2f}%")

title7 = "India's retail inflation falls to a six-year low as food prices ease"
text7 = "India's annual retail inflation declined sharply in recent months as food prices moderated, providing relief to households and giving policymakers additional room to support economic activity."
label7, conf7 = predict_with_spark_weights(f"{title7} {text7}")

print("\n--- Test 7 (Real News - India Inflation) ---")
print(f"Prediction: {label7}")
print(f"Confidence: {conf7 * 100:.2f}%")

title8 = "India's central bank secretly introduces a mandatory AI-based credit score for every citizen"
text8 = "The Reserve Bank of India has introduced a nationwide artificial-intelligence credit scoring system that will automatically assign every Indian citizen a financial reliability score, according to documents allegedly circulated among commercial banks. The system reportedly combines bank transactions, mobile-phone location records, social-media activity and electricity consumption to determine an individual's eligibility for loans and government benefits. Officials have not publicly announced the programme, but several unnamed banking executives claimed that banks have already begun integrating the score into their lending systems."
label8, conf8 = predict_with_spark_weights(f"{title8} {text8}")
print("\n--- Prompt Test 2 (Fake News - AI Credit Score) ---")
print(f"Prediction: {label8}")
print(f"Confidence: {conf8 * 100:.2f}%")

title9 = "Scientists detect evidence of water ice in permanently shadowed lunar craters"
text9 = "Scientists have identified evidence consistent with water ice in permanently shadowed regions near the Moon's poles. Because sunlight does not directly reach these areas, temperatures can remain extremely low, allowing volatile substances such as water to survive for long periods. The discovery is significant for future lunar exploration because water could potentially be used for life support and, after processing, as a source of hydrogen and oxygen for fuel."
label9, conf9 = predict_with_spark_weights(f"{title9} {text9}")
print("\n--- Prompt Test 3 (Real News - Lunar Ice) ---")
print(f"Prediction: {label9}")
print(f"Confidence: {conf9 * 100:.2f}%")

title10 = "Researchers develop a battery that can charge an electric car completely in 47 seconds"
text10 = "A research consortium in Europe has announced a revolutionary battery capable of charging a passenger electric vehicle from zero to 100 percent in just 47 seconds. According to researchers, the battery uses a previously unknown crystalline material that allows lithium ions to move through the electrodes without generating significant heat. The team claims the technology has already completed more than 100,000 charging cycles without measurable degradation and will enter mass production next year. Independent researchers, however, have not yet been given access to the laboratory results."
label10, conf10 = predict_with_spark_weights(f"{title10} {text10}")
print("\n--- Prompt Test 4 (Fake News - Battery) ---")
print(f"Prediction: {label10}")
print(f"Confidence: {conf10 * 100:.2f}%")

title11 = "Astronomers discover an unusually massive black hole in the early universe"
text11 = "Astronomers using powerful space telescopes have observed a massive black hole that existed when the universe was still relatively young. The observation is helping researchers investigate how some black holes were able to grow to enormous sizes so early in cosmic history. The findings could challenge existing models of black-hole formation and growth, although scientists emphasized that additional observations are needed to determine the object's properties and evolutionary history."
label11, conf11 = predict_with_spark_weights(f"{title11} {text11}")
print("\n--- Prompt Test 5 (Real News - Black Hole) ---")
print(f"Prediction: {label11}")
print(f"Confidence: {conf11 * 100:.2f}%")

title12 = "Researchers demonstrate a new method for improving the efficiency of solar cells"
text12 = "Researchers have demonstrated a technique that can improve the performance of solar cells by reducing energy losses during the conversion of sunlight into electricity. The approach involves modifying the structure of the photovoltaic material and improving the movement of charge carriers through the device. Laboratory results suggest that the technique could increase efficiency, although researchers noted that further testing is required to determine whether the process can be economically scaled for commercial manufacturing."
label12, conf12 = predict_with_spark_weights(f"{title12} {text12}")
print("\n--- Prompt Test 7 (Real News - Solar Cells) ---")
print(f"Prediction: {label12}")
print(f"Confidence: {conf12 * 100:.2f}%")

title13 = "India announces nationwide satellite internet service providing free 1 Gbps connectivity to every household"
text13 = "The Indian government has reportedly approved a nationwide satellite-internet programme that will provide every household with a free 1 Gbps connection beginning in January 2027. Officials allegedly said the programme would use a newly launched constellation of more than 600 Indian satellites and would require no monthly subscription or installation fee. According to the announcement, the service will initially target rural districts before expanding to cities, with the government claiming that the project will eliminate India's digital divide within two years."
label13, conf13 = predict_with_spark_weights(f"{title13} {text13}")
print("\n--- Prompt Test 8 (Fake News - Satellite Internet) ---")
print(f"Prediction: {label13}")
print(f"Confidence: {conf13 * 100:.2f}%")
