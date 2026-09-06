import csv
import random

# Templates for generating realistic Real and Fake news
real_titles = [
    "Senate passes bipartisan infrastructure bill",
    "Global climate summit reaches historic agreement",
    "Federal Reserve holds interest rates steady",
    "New study shows benefits of Mediterranean diet on heart health",
    "Local council approves new public park construction",
    "Tech company announces breakthrough in quantum computing",
    "Mars rover discovers signs of ancient water",
    "World health officials monitor new flu strain",
    "National library archives historic letters from the 18th century",
    "Mayor announces new initiatives for urban housing"
]

real_texts = [
    "The Senate today voted in favor of a major infrastructure package, marking a rare moment of bipartisan cooperation. Spokespersons from both parties stated that this bill will fund critical upgrades to roads, bridges, and public transit systems over the next decade. Economists suggest this will create thousands of jobs across the nation.",
    "Delegates at the climate summit have officially signed an agreement pledging to reduce carbon emissions by thirty percent by the end of the decade. The agreement comes after weeks of intense negotiations. Environmental advocates called the treaty a step in the right direction, though some warn that stricter enforcement is necessary.",
    "In its monthly meeting, the Federal Reserve decided to keep current interest rates unchanged. The chairman noted that while inflation shows signs of slowing, the labor market remains exceptionally strong. Market analysts predict that rate cuts may not occur until the next fiscal quarter.",
    "A comprehensive study published in the Journal of Medicine reveals that individuals following a Mediterranean diet experience a significant reduction in cardiovascular risks. Researchers monitored over five thousand participants over five years, confirming that olive oil, nuts, and fresh vegetables contribute to arterial longevity.",
    "The city council voted unanimously to approve the development of a new fifty-acre public park in the downtown district. The project will feature walking paths, community gardens, and solar-powered lighting. Construction is scheduled to begin early next spring, with completion expected within eighteen months."
]

fake_titles = [
    "SHOCKING: Aliens landed in Washington DC last night!",
    "ALERT: This common kitchen ingredient is slowly poisoning you!",
    "Secret government document leaks online proving election fraud",
    "Miracle pill cures all diseases in under 24 hours!",
    "BREAKING: World leaders secretly meeting to plan global shutdown",
    "You won't believe what this celebrity did at the private island!",
    "Scientists confirm the Earth is actually expanding every day",
    "This simple trick can generate infinite electricity at home",
    "Leaked video shows secret underground city beneath the pyramids",
    "Government is using cellular towers to control minds"
]

fake_texts = [
    "A shocking new video circulating online shows what conspiracy theorists claim is an alien spacecraft hovering directly over the Capitol building. Eyewitnesses reported bright green flashing lights and unusual static on their mobile devices. Officials have refused to comment, fueling rumors of a massive government cover-up.",
    "A secret whistleblower from a major pharmaceutical company has leaked files detailing a secret ingredient in everyday foods that is designed to make people sick. According to the document, the FDA has known about this for years but is being paid off by large corporations. Share this warning before it is deleted!",
    "An anonymous hacker group has released what they claim is an unredacted video proving that the election was completely rigged by an advanced AI algorithm. The video, which has already been banned on major social networks, shows simulated voting statistics being altered in real time. Absolute proof inside!",
    "A brilliant independent researcher has bypassed mainstream medical institutions to create an all-natural herbal pill that cures cancer, diabetes, and heart disease overnight. Big Pharma is currently trying to arrest the scientist to keep their multi-billion dollar treatment business alive. Click here to buy now!",
    "High-ranking sources report that world elites are currently meeting in an undisclosed bunker in Switzerland to execute a global lockdown protocol. The plan involves turning off the internet and replacing paper money with a trackable digital currency. Prepare your family immediately!"
]

def generate_dataset():
    # Generate 550 rows of news
    records = []
    subjects = ["politics", "world", "tech", "health", "science"]
    
    # 275 Real articles
    for i in range(275):
        title = random.choice(real_titles) + f" (Report #{random.randint(100, 999)})"
        text = random.choice(real_texts) + f" Statistics from official census indicate a {random.randint(1, 10)}% margin of error."
        subject = random.choice(subjects)
        date = f"2023-0{random.randint(1,9)}-{random.randint(10,28)}"
        records.append([title, text, subject, date, 0]) # 0 = Real
        
    # 275 Fake articles
    for i in range(275):
        title = random.choice(fake_titles) + f"!!! MUST SEE [VIDEO {random.randint(1, 9)}]"
        text = random.choice(fake_texts) + f" This is a 100% real secret conspiracy that they do not want you to know about!!!"
        subject = random.choice(subjects)
        date = f"2023-0{random.randint(1,9)}-{random.randint(10,28)}"
        records.append([title, text, subject, date, 1]) # 1 = Fake

    # Shuffle the dataset so labels are mixed
    random.shuffle(records)

    # Save to local CSV path
    with open('../data/raw/sample_news.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["title", "text", "subject", "date", "label"])
        writer.writerows(records)

    print(f"🎉 Generated a realistic Big Data dataset with {len(records)} records!")

if __name__ == "__main__":
    generate_dataset()
