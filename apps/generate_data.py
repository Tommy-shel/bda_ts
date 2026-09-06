import csv
import random

# ============================================================
# REAL-STYLE NEWS
# label = 0
# ============================================================

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
    "Mayor announces new initiatives for urban housing",
    "CJP protest draws attention from authorities",
    "Government discusses concerns raised during CJP demonstrations",
    "Authorities examine events following CJP demonstration",
    "Officials respond to developments surrounding CJP protest",
    "Authorities examine additional Epstein-related records",
    "Officials discuss access to Epstein-related documents",
    "Investigation into Epstein-related records continues",
    "Nepal continues flood recovery operations",
    "Flooding causes extensive damage across affected areas of Nepal",
    "Rescue teams work to reach remote flood-affected communities",
    "Authorities assess infrastructure damage following Nepal floods",
]

real_texts = [
    "The Senate today voted in favor of a major infrastructure package, marking a rare moment of bipartisan cooperation. Spokespersons from both parties stated that the bill will fund critical upgrades to roads, bridges, and public transit systems over the next decade. Economists said the investment could support employment and infrastructure development.",

    "Delegates at the climate summit signed an agreement pledging to reduce carbon emissions by the end of the decade. The agreement followed weeks of negotiations. Environmental advocates described the treaty as an important step while noting that implementation and enforcement would remain important.",

    "In its monthly meeting, the Federal Reserve decided to keep current interest rates unchanged. Officials said economic conditions and inflation would continue to be monitored before future policy decisions are made.",

    "A comprehensive research study examined dietary patterns and cardiovascular health. Researchers reported an association between Mediterranean-style diets and several positive health outcomes, while noting that additional research is required to understand the underlying causes.",

    "The city council voted to approve development of a new public park in the downtown district. The project is expected to include walking paths, community gardens, and public recreational areas. Construction is expected to begin after the required planning process.",

    "Demonstrators gathered during a CJP protest and called for action on issues raised by the organization. Authorities monitored the situation and officials issued statements about the demonstrations. Protest organizers also presented their position on the issues.",

    "Representatives of the government and protesters discussed several concerns following demonstrations. Participants gave different accounts of some events, while authorities said that the situation would continue to be monitored.",

    "Authorities examined events surrounding a demonstration involving CJP supporters. Officials and protest organizers provided separate accounts of the situation, and further developments were expected following discussions between the parties.",

    "Officials responded to developments surrounding a CJP demonstration and said that relevant authorities were assessing the situation. Protest organizers continued to communicate their demands and concerns.",

    # --------------------------------------------------------
    # Epstein files
    # --------------------------------------------------------

    "Officials continued examining records associated with Jeffrey Epstein. Legal requirements and privacy considerations affected access to some documents, while authorities continued reviewing material connected with previous investigations.",

    "Authorities continued reviewing Epstein-related material while some records remained subject to legal restrictions and protections for victims and other individuals.",

    "Investigators continued examining records connected to Jeffrey Epstein. Authorities said additional information could emerge as legal and investigative processes continue.",

    "Officials discussed the handling of records connected with the Epstein investigation. Some documents remained subject to legal procedures, privacy requirements, and decisions concerning public disclosure.",

    # --------------------------------------------------------
    # Nepal floods
    # --------------------------------------------------------

    "Rescue and recovery teams continued working in areas affected by severe flooding in Nepal. Infrastructure damage and displacement created significant challenges for local communities.",

    "Authorities reported deaths, displacement and damage to roads and other infrastructure following severe flooding. Emergency teams continued rescue and relief activities in affected areas.",

    "Emergency workers continued efforts to reach communities affected by flooding, while damaged infrastructure complicated transportation and communications.",

    "Authorities assessed damage to roads, homes, power infrastructure and other facilities following flooding in affected areas of Nepal. Relief organizations continued assisting displaced residents.",
]


# ============================================================
# FAKE / MISLEADING NEWS
# label = 1
# ============================================================

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
    "Government is using cellular towers to control minds",

    # New current-event misinformation themes
    "SHOCKING: CJP protest exposes SECRET government plan!!!",
    "BREAKING: CJP protesters have supposedly taken control of Parliament",
    "CJP protest proves India is entering an immediate nationwide shutdown!!!",
    "URGENT: CJP protest reveals hidden plan affecting every student",
    "NEW EPSTEIN FILES reveal a secret list of ALL politicians!!!",
    "Epstein files prove EVERY world leader was secretly involved!!!",
    "Anonymous hackers supposedly release final Epstein files",
    "SHOCKING Epstein document proves massive global conspiracy",
    "Nepal floods were secretly caused by a weather machine!!!",
    "URGENT: Government knew Nepal flood would destroy the entire country",
    "Nepal flood video supposedly shows an entire city disappearing",
    "BREAKING: Secret technology caused the Nepal floods",
]


fake_texts = [
    "A shocking new video circulating online shows what conspiracy theorists claim is an alien spacecraft hovering directly over the Capitol building. Eyewitnesses reportedly observed unusual lights. Officials have supposedly refused to comment, fueling rumors of a massive government cover-up.",

    "A secret whistleblower from a major pharmaceutical company has allegedly leaked files detailing a secret ingredient in everyday foods that is designed to make people sick. The post claims authorities have known about it for years and urges readers to share the warning immediately.",

    "An anonymous hacker group has released what they claim is an unredacted video proving that an election was completely rigged by an advanced AI algorithm. The post claims the video has been banned online and presents the material as absolute proof without independent verification.",

    "A supposedly independent researcher has created an all-natural pill that allegedly cures cancer, diabetes, and heart disease overnight. The article claims pharmaceutical companies are trying to suppress the discovery and encourages readers to purchase the treatment.",

    "High-ranking unnamed sources allegedly report that world leaders are meeting secretly to execute a global lockdown protocol. The post claims the plan involves shutting down the internet and replacing physical money with a trackable digital currency.",

    # --------------------------------------------------------
    # CJP protest misinformation
    # --------------------------------------------------------

    "A viral post claims the CJP protest uncovered a secret government plan affecting every student in the country. The post provides no independently verifiable evidence and asks users to share it immediately before it is supposedly removed.",

    "A social-media message claims CJP protesters secretly took control of Parliament during the demonstration. No credible evidence or official statement supports the claim, but the message presents the allegation as confirmed.",

    "An online post claims the CJP protest proves that India will enter a nationwide shutdown within hours. It cites unnamed insiders and provides no reliable evidence for the prediction.",

    "A viral thread claims CJP organizers discovered a hidden government program designed to control students through mobile phones. The thread relies on anonymous accounts and unverified screenshots.",

    # --------------------------------------------------------
    # Epstein misinformation
    # --------------------------------------------------------

    "A viral post claims newly released Epstein files prove that every major world leader participated in a global conspiracy. The post provides no authenticated evidence for the sweeping allegation.",

    "A social-media account claims that a complete secret list of politicians has been uncovered in newly released Epstein documents. Screenshots are presented without establishing the authenticity or origin of the alleged files.",

    "An anonymous account claims it has released a complete set of Epstein documents proving numerous allegations. The authenticity of the files has not been independently established.",

    "A sensational article claims that one newly discovered Epstein document proves the existence of a worldwide secret organization. The article relies on unnamed sources and unverified images.",

    # --------------------------------------------------------
    # Nepal flood misinformation
    # --------------------------------------------------------

    "A viral message claims that a secret weather-control machine deliberately caused the flooding in Nepal. No credible scientific or official evidence supports the allegation.",

    "An online post claims government officials knew the Nepal disaster would destroy the entire country and deliberately withheld the information. The claim provides no reliable evidence.",

    "A viral video is presented as proof that an entire Nepalese city disappeared underwater during the floods. The post does not establish when or where the footage was recorded.",

    "A social-media account claims that secret technology was used to create the Nepal floods. The allegation is presented as fact despite the absence of credible scientific or official evidence.",
]


# ============================================================
# SUBJECTS
# ============================================================

subjects = [
    "politics",
    "world",
    "tech",
    "health",
    "science"
]


# ============================================================
# DATE GENERATOR
# ============================================================

def generate_date():
    year = random.choice([2023, 2024, 2025, 2026])
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    return f"{year}-{month:02d}-{day:02d}"


# ============================================================
# DATASET GENERATOR
# ============================================================

def generate_dataset():

    records = []

    # --------------------------------------------------------
    # 500 REAL ARTICLES
    # --------------------------------------------------------

    for i in range(500):

        title = random.choice(real_titles)

        text = random.choice(real_texts)

        subject = random.choice(subjects)

        date = generate_date()

        # Add slight variation
        title = title + f" (Report #{random.randint(100, 9999)})"

        records.append([
            title,
            text,
            subject,
            date,
            0
        ])


    # --------------------------------------------------------
    # 500 FAKE ARTICLES
    # --------------------------------------------------------

    for i in range(500):

        title = random.choice(fake_titles)

        text = random.choice(fake_texts)

        subject = random.choice(subjects)

        date = generate_date()

        # Add variation
        title = title + f" [UPDATE {random.randint(1, 99)}]"

        text = (
            text
            + " This claim has not been independently verified."
        )

        records.append([
            title,
            text,
            subject,
            date,
            1
        ])


    # --------------------------------------------------------
    # SHUFFLE
    # --------------------------------------------------------

    random.shuffle(records)


    # --------------------------------------------------------
    # SAVE CSV
    # --------------------------------------------------------

    output_file = "../data/raw/sample_news.csv"

    with open(
        output_file,
        "w",
        newline="",
        encoding="utf-8"
    ) as f:

        writer = csv.writer(f)

        writer.writerow([
            "title",
            "text",
            "subject",
            "date",
            "label"
        ])

        writer.writerows(records)


    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    real_count = sum(1 for row in records if row[4] == 0)
    fake_count = sum(1 for row in records if row[4] == 1)

    print("\n========================================")
    print("      FAKE NEWS DATASET GENERATED")
    print("========================================")
    print(f"Total records : {len(records)}")
    print(f"Real records  : {real_count}")
    print(f"Fake records  : {fake_count}")
    print(f"Output file   : {output_file}")
    print("========================================\n")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    generate_dataset()
