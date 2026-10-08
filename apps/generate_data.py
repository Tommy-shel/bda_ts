import csv
import random

# ============================================================
# REAL NEWS TEMPLATES
# label = 0
# Covers: politics, world, tech, health, science, business,
#         environment, sports, education, economy
# ============================================================

real_templates = [
    # --- Politics ---
    {
        "title": "Parliament approves landmark pension reform bill",
        "text": "Lawmakers voted to pass a sweeping pension reform package after months of debate. The bill adjusts retirement age thresholds and increases contribution rates for high-income earners. Analysts say the changes are designed to stabilise long-term public finances.",
        "subject": "politics"
    },
    {
        "title": "Prime minister outlines new anti-corruption measures",
        "text": "The head of government announced a package of legislative reforms aimed at improving transparency in public procurement. Independent watchdog groups cautiously welcomed the announcement while calling for stronger enforcement mechanisms.",
        "subject": "politics"
    },
    {
        "title": "Opposition party calls for independent inquiry into budget leaks",
        "text": "The main opposition bloc has formally requested a parliamentary inquiry after financial projections were reportedly shared outside official channels ahead of the budget announcement. The ruling party denied wrongdoing and said all processes followed established procedures.",
        "subject": "politics"
    },
    {
        "title": "Senate committee approves judicial appointments after lengthy review",
        "text": "A Senate committee voted to approve the nomination of three appellate judges following hearings that examined their judicial records. Legal observers noted that the appointments could influence the interpretation of constitutional law for the next decade.",
        "subject": "politics"
    },
    {
        "title": "Local elections produce fragmented results across three key states",
        "text": "Preliminary results from regional elections indicate that no single party secured a majority in any of the three contested states. Coalition talks are expected to begin in the coming days, with analysts predicting extended negotiations.",
        "subject": "politics"
    },
    {
        "title": "Government tables new data privacy bill for public consultation",
        "text": "Officials published a draft bill that would impose stricter requirements on companies handling personal data, including mandatory breach notifications and expanded rights for citizens to access or delete their information. Public comments are open for thirty days.",
        "subject": "politics"
    },
    # --- World ---
    {
        "title": "Ceasefire agreement reached in prolonged regional conflict",
        "text": "Diplomatic negotiators announced that the warring parties had agreed to a ceasefire after talks mediated by international representatives. The truce is set to take effect at midnight local time and will be monitored by a joint observer team.",
        "subject": "world"
    },
    {
        "title": "United Nations calls for urgent humanitarian access to affected region",
        "text": "Senior UN officials urged all parties to allow unimpeded access for relief workers after reports of food and medicine shortages in the conflict zone. Aid agencies estimated that more than two million people require immediate assistance.",
        "subject": "world"
    },
    {
        "title": "Earthquake strikes coastal region, rescue teams deployed",
        "text": "A moderate earthquake struck a coastal area, prompting authorities to deploy search-and-rescue teams to affected districts. Preliminary assessments indicated structural damage to hundreds of buildings, and officials asked residents in vulnerable areas to remain cautious.",
        "subject": "world"
    },
    {
        "title": "Trade ministers meet to resolve long-running tariff dispute",
        "text": "Representatives from both countries convened for two days of talks aimed at resolving a tariff disagreement that has disrupted bilateral trade for nearly two years. Officials said progress was made on several items but that a final agreement had not yet been reached.",
        "subject": "world"
    },
    {
        "title": "Refugee organisations report record displacement in sub-Saharan region",
        "text": "International humanitarian organisations published data showing that displacement in the sub-Saharan region had reached its highest level in fifteen years. Conflict, drought and economic hardship were identified as the primary drivers of movement.",
        "subject": "world"
    },
    {
        "title": "G20 finance ministers agree on framework for debt relief",
        "text": "Finance ministers from the world's major economies reached a preliminary agreement on a framework to restructure the debt of heavily indebted lower-income countries. Details of the timeline and conditions are expected to be finalised at the next summit.",
        "subject": "world"
    },
    # --- Technology ---
    {
        "title": "Semiconductor firm announces next-generation chip architecture",
        "text": "A major semiconductor manufacturer unveiled a new processor architecture that promises significant improvements in performance per watt compared with current designs. The company said volume production was scheduled to begin later in the year.",
        "subject": "tech"
    },
    {
        "title": "Regulators open antitrust investigation into cloud computing market",
        "text": "Competition authorities launched a formal investigation into whether a small number of large providers have engaged in practices that limit competition in the cloud services market. The companies under review declined to comment in detail but said they would cooperate fully.",
        "subject": "tech"
    },
    {
        "title": "Researchers achieve new milestone in quantum error correction",
        "text": "A research team published results demonstrating a significant reduction in error rates for quantum computations using a novel error-correction protocol. Experts described the findings as an encouraging step toward practical quantum computing, while cautioning that many engineering challenges remain.",
        "subject": "tech"
    },
    {
        "title": "Open-source AI framework gains traction among enterprise developers",
        "text": "An open-source machine learning framework released by a research consortium has seen rapid adoption among enterprise software teams over the past quarter. Developers cited lower infrastructure costs and greater transparency compared with proprietary alternatives.",
        "subject": "tech"
    },
    {
        "title": "Cybersecurity agency warns of vulnerability in widely used networking software",
        "text": "A national cybersecurity authority issued an advisory urging organisations to apply patches for a critical vulnerability discovered in a widely deployed networking product. Researchers noted that the flaw could allow remote code execution if left unpatched.",
        "subject": "tech"
    },
    {
        "title": "Electric vehicle maker reports steady growth in delivery numbers",
        "text": "An electric vehicle manufacturer disclosed quarterly delivery figures that met analyst expectations, supported by increased production capacity at its newer facilities. The company reiterated its full-year delivery guidance while noting that supply chain conditions remained a variable.",
        "subject": "tech"
    },
    # --- Health ---
    {
        "title": "WHO releases updated guidelines on antibiotic prescribing",
        "text": "The World Health Organization published revised recommendations on antibiotic prescribing practices, emphasising the need to preserve the effectiveness of last-resort drugs by restricting their use to cases where alternative treatments are ineffective.",
        "subject": "health"
    },
    {
        "title": "Clinical trial shows promise for new treatment of drug-resistant tuberculosis",
        "text": "Preliminary results from a clinical trial involving a novel drug combination showed a significant improvement in outcomes for patients with drug-resistant tuberculosis compared with the standard treatment regimen. Researchers said a larger phase-three trial would be required to confirm the findings.",
        "subject": "health"
    },
    {
        "title": "National health authority recommends updated vaccine schedule for adults",
        "text": "Public health officials revised the recommended vaccination schedule for adults to include updated boosters for several respiratory illnesses. The changes reflected new evidence about waning immunity and changes in circulating strains.",
        "subject": "health"
    },
    {
        "title": "Study links ultra-processed food consumption to elevated cardiovascular risk",
        "text": "A large observational study found that higher consumption of ultra-processed foods was associated with elevated risks of cardiovascular events over a ten-year follow-up period. Authors noted that the study design could not establish causation and called for further research.",
        "subject": "health"
    },
    {
        "title": "Hospitals report improvements in patient outcomes after surgical checklist adoption",
        "text": "A multi-hospital review found measurable reductions in post-surgical complications at facilities that had adopted standardised pre-operative checklists over the preceding three years. The findings supported broader implementation of the protocol.",
        "subject": "health"
    },
    {
        "title": "Mental health researchers call for expanded access to talking therapies",
        "text": "A review of mental health provision in several countries found that access to evidence-based psychological therapies remained limited, particularly in rural areas. Researchers recommended increased funding for community-based services and digital-delivery platforms.",
        "subject": "health"
    },
    # --- Science ---
    {
        "title": "Astronomers detect water vapour in atmosphere of distant exoplanet",
        "text": "An international team of astronomers reported the detection of water vapour in the atmosphere of a rocky exoplanet located in the habitable zone of its star. The discovery is considered an important step in the search for potentially habitable worlds, though researchers cautioned that many other conditions must be met for life to be possible.",
        "subject": "science"
    },
    {
        "title": "Paleontologists uncover fossilised remains of previously unknown dinosaur species",
        "text": "A team of paleontologists announced the discovery of fossilised skeletal remains belonging to a previously undescribed dinosaur species from the Late Cretaceous period. The specimen revealed distinctive anatomical features that had not been observed in related species.",
        "subject": "science"
    },
    {
        "title": "Marine biologists document decline in coral reef biodiversity",
        "text": "A long-term study of reef ecosystems in multiple ocean regions found a measurable decline in the diversity of coral species over a fifteen-year monitoring period. Rising sea temperatures and ocean acidification were identified as the principal contributing factors.",
        "subject": "science"
    },
    {
        "title": "Physicists confirm existence of rare particle predicted by theoretical model",
        "text": "Researchers at a particle physics facility announced the experimental confirmation of a rare subatomic particle that had been predicted by theoretical models decades earlier. The finding was described as a significant validation of the standard model of particle physics.",
        "subject": "science"
    },
    {
        "title": "Climate scientists publish revised sea-level rise projections for coastal regions",
        "text": "A group of climate researchers released updated projections indicating that sea-level rise along certain coastlines could be higher by mid-century than previously estimated, depending on greenhouse gas emission trajectories. The authors recommended that coastal planning authorities incorporate the new data into long-term infrastructure decisions.",
        "subject": "science"
    },
    {
        "title": "Geneticists map previously uncharted regions of the human genome",
        "text": "A consortium of genomic researchers published the results of a project that mapped previously sequenced regions of the human genome with greater accuracy. The improved reference sequence is expected to facilitate the identification of genetic variants associated with rare diseases.",
        "subject": "science"
    },
    # --- Business / Economy ---
    {
        "title": "Central bank raises interest rates by quarter-point to curb inflation",
        "text": "The country's central bank raised its benchmark interest rate by twenty-five basis points at its latest policy meeting, citing persistent inflation pressures. The decision was in line with market expectations, and officials signalled that future adjustments would depend on incoming economic data.",
        "subject": "business"
    },
    {
        "title": "Manufacturing output grows for third consecutive quarter",
        "text": "Official statistics showed that manufacturing output expanded for the third quarter in a row, driven by increased demand from export markets. Economists said the trend suggested a gradual broadening of economic activity beyond the services sector.",
        "subject": "business"
    },
    {
        "title": "Retail sector reports mixed results as consumer spending patterns shift",
        "text": "Several major retailers disclosed quarterly earnings that showed divergent performance between physical stores and online channels. Analysts noted that shifts in consumer behaviour since the pandemic had created lasting structural changes in the retail landscape.",
        "subject": "business"
    },
    {
        "title": "Government launches infrastructure investment fund for rural connectivity",
        "text": "Officials announced the establishment of a dedicated fund to finance broadband and transport infrastructure in underserved rural areas. The programme is expected to be implemented over a five-year period through a combination of public grants and private co-investment.",
        "subject": "business"
    },
    # --- Environment ---
    {
        "title": "Reforestation project restores thousands of hectares of degraded land",
        "text": "A partnership between government agencies and conservation organisations has replanted trees across a significant area of previously deforested land over the past two years. Project monitors reported that native species were re-establishing themselves in restored areas.",
        "subject": "world"
    },
    {
        "title": "Cities commit to expanding urban green spaces under climate adaptation plan",
        "text": "Forty-seven cities across five continents signed a commitment to increase the share of urban land dedicated to parks, wetlands and other green infrastructure as part of a climate adaptation initiative. Studies have linked urban green space to reductions in heat island effects and improved air quality.",
        "subject": "world"
    },
    # --- Education ---
    {
        "title": "Universities report rising enrolment in science and engineering programmes",
        "text": "Higher education data showed an increase in the number of students enrolling in science, technology, engineering and mathematics degree programmes over the past three academic years. Institutions attributed the trend partly to government scholarship initiatives and growing demand for STEM skills in the labour market.",
        "subject": "tech"
    },
    {
        "title": "Schools pilot new curriculum designed to improve critical thinking skills",
        "text": "A group of state schools began piloting an updated curriculum framework emphasising critical analysis, evidence evaluation and structured argumentation across multiple subject areas. Early assessments showed improvements in students' ability to identify unsupported claims in written texts.",
        "subject": "politics"
    },
]

# ============================================================
# FAKE / MISLEADING NEWS TEMPLATES
# label = 1
# Covers: conspiracy theories, pseudoscience, sensationalism,
#         misattributed claims, health misinformation, political hoaxes
# ============================================================

fake_templates = [
    # --- Conspiracy / Government ---
    {
        "title": "LEAKED: Government secretly microchipping citizens through flu vaccines",
        "text": "An anonymous whistleblower has allegedly published internal documents claiming that microscopic tracking chips are embedded in seasonal flu vaccine doses. The documents have not been independently verified and no credible scientific body has endorsed the claim.",
        "subject": "health"
    },
    {
        "title": "BOMBSHELL: World governments planning secret currency replacement by next year",
        "text": "A viral post claims that a secretive group of central banks is coordinating a surprise elimination of paper currency to be replaced by a trackable digital token. The post relies on unnamed insiders and unverified documents, and no central bank has confirmed any such plan.",
        "subject": "politics"
    },
    {
        "title": "EXPOSED: Chemtrails confirmed as mass mind-control programme",
        "text": "A widely shared article alleges that aircraft contrails contain chemical agents designed to make populations more compliant and easier to manipulate. No peer-reviewed scientific study supports the claim, and aviation and atmospheric scientists have repeatedly explained that contrails consist of water vapour.",
        "subject": "science"
    },
    {
        "title": "BREAKING: Secret underground tunnels discovered beneath major world capitals",
        "text": "A conspiracy blog asserts that satellite imagery proves the existence of a vast network of underground tunnels linking the governmental centres of several countries. Independent geospatial analysts found no evidence to support the claim in publicly available imagery.",
        "subject": "world"
    },
    {
        "title": "URGENT: Authorities planning surprise internet shutdown in 48 hours",
        "text": "A message circulating on social media claims that governments have secretly agreed to impose a total internet blackout to prevent the release of damaging information. No official government or telecom body has announced any such action, and the claim provides no verifiable source.",
        "subject": "tech"
    },
    {
        "title": "SHOCK CLAIM: Global elite held secret meeting to plan population reduction",
        "text": "A viral post alleges that billionaires and heads of state convened in a private location to discuss a coordinated plan to reduce the world population through engineered food shortages and engineered pandemics. The post provides no authenticated evidence for this sweeping claim.",
        "subject": "world"
    },
    # --- Health Misinformation ---
    {
        "title": "DOCTORS HIDE THIS: Common spice cures cancer in three days",
        "text": "An online article claims that a popular kitchen spice has been proven to eliminate all forms of cancer within seventy-two hours of daily consumption, and that pharmaceutical companies have suppressed the discovery. No clinical evidence supports the claim, and oncologists have described it as dangerous misinformation.",
        "subject": "health"
    },
    {
        "title": "WARNING: Tap water secretly laced with fertility-reducing chemical",
        "text": "A widely shared social media post asserts that authorities have been deliberately adding a chemical compound to municipal water supplies that reduces human fertility. No independent laboratory analysis or health authority has confirmed the presence of any such compound.",
        "subject": "health"
    },
    {
        "title": "ALERT: New vaccine causes DNA alteration in 90% of recipients",
        "text": "A viral article claims that a newly approved vaccine permanently alters human DNA in the vast majority of recipients, based on anonymous laboratory reports. Molecular biologists and regulatory agencies have stated that the claim is scientifically inaccurate and lacks any credible evidence.",
        "subject": "health"
    },
    {
        "title": "EXPOSED: Hospitals paid to falsify death certificates as COVID",
        "text": "A widely circulated post claims that medical facilities receive financial incentives to list unrelated deaths as caused by a specific illness, inflating official statistics. No credible audit or investigation has substantiated the claim, and health authorities have described the allegation as unfounded.",
        "subject": "health"
    },
    # --- Technology Misinformation ---
    {
        "title": "SHOCKING: 5G towers confirmed to transmit mind-altering frequencies",
        "text": "A viral message asserts that fifth-generation mobile networks emit specific electromagnetic frequencies designed to alter human cognitive function and increase susceptibility to suggestion. No credible scientific or engineering study has supported the allegation.",
        "subject": "tech"
    },
    {
        "title": "BREAKING: Tech giant secretly records all home conversations 24 hours a day",
        "text": "An anonymous post claims that a major consumer electronics company continuously records audio from all devices in every household and shares the recordings with intelligence agencies. The company denied the allegation and no independent technical analysis has confirmed the claim.",
        "subject": "tech"
    },
    {
        "title": "REVEALED: Artificial intelligence already secretly running all world governments",
        "text": "A sensational article claims that a secret AI system developed by a private consortium has already assumed de facto control of decision-making in the governments of multiple major countries, with elected officials serving only as figureheads. No credible source or evidence is provided.",
        "subject": "tech"
    },
    # --- Science Misinformation ---
    {
        "title": "PROOF: The Earth is expanding by one kilometre per year, scientists admit",
        "text": "A viral post claims that geologists have quietly admitted to evidence showing the planet's radius increasing at a rate of one kilometre annually, and that this fact is being concealed from the public. No peer-reviewed geological study supports the claim.",
        "subject": "science"
    },
    {
        "title": "EXPOSED: Moon landing footage was filmed in an Arizona desert studio",
        "text": "A long-circulating conspiracy claim re-emerged, alleging that behind-the-scenes photographs prove that footage from a historic lunar mission was produced in a secret terrestrial studio. The photographic evidence presented has been repeatedly debunked by independent analysts and former space agency employees.",
        "subject": "science"
    },
    {
        "title": "STUDY SUPPRESSED: Scientists prove that humans lived alongside dinosaurs",
        "text": "A blog post claims that a scientific study demonstrating coexistence of humans and non-avian dinosaurs was retracted from journals due to pressure from establishment scientists. No such peer-reviewed study exists, and the geological record places human ancestors millions of years after the mass extinction.",
        "subject": "science"
    },
    # --- Political Misinformation ---
    {
        "title": "EXPLOSIVE: Ballot-counting machines pre-programmed to switch votes",
        "text": "A viral post alleges that electronic voting machines used in multiple districts were pre-programmed by a foreign entity to alter results automatically. Election authorities and independent auditors found no evidence of any such programming in post-election machine inspections.",
        "subject": "politics"
    },
    {
        "title": "SECRET MEMO: Government to declare martial law and seize private assets",
        "text": "An allegedly leaked internal memo supposedly shows plans for an imminent declaration of martial law and mass confiscation of private property. Neither the document's origin nor its authenticity has been established, and government officials have denied any such plan exists.",
        "subject": "politics"
    },
    {
        "title": "BOMBSHELL: Senior official secretly working for foreign intelligence service",
        "text": "An anonymous online account claims to have evidence that a named senior government official is a long-running covert agent for a foreign power. The claim rests entirely on unverified screenshots and anonymous testimony, and no law enforcement body has opened a related investigation.",
        "subject": "politics"
    },
    # --- Economic Misinformation ---
    {
        "title": "ALERT: Banks to freeze all accounts simultaneously next month",
        "text": "A post circulating widely on messaging platforms claims that a coordinated banking freeze will lock customers out of their accounts as part of a planned financial reset. No central bank or regulatory authority has announced or confirmed any such action.",
        "subject": "business"
    },
    {
        "title": "SHOCKING: Gold secretly removed from all national reserves years ago",
        "text": "A conspiracy article asserts that the gold held in major national reserves was secretly replaced with gold-plated tungsten bars decades ago and that the true reserves are now empty. Independent audits conducted at multiple reserve facilities have not confirmed this claim.",
        "subject": "business"
    },
    # --- Environment Misinformation ---
    {
        "title": "EXPOSED: Wildfires deliberately started by government using secret laser weapons",
        "text": "A viral video claims that visible light patterns during recent wildfires prove the fires were ignited by directed-energy weapons deployed by government forces. Fire scientists and investigators have attributed the fires to natural and accidental causes following standard forensic analysis.",
        "subject": "world"
    },
    {
        "title": "BREAKING: Climate change data entirely fabricated by UN scientists",
        "text": "A blog post claims that leaked emails prove that United Nations climate researchers invented temperature records to support a predetermined political agenda. The emails referenced were investigated and found to have been misrepresented, and multiple independent analyses have reproduced the warming trends using raw data.",
        "subject": "science"
    },
    # --- Current Event Misinformation (CJP, Epstein, Nepal) ---
    {
        "title": "SHOCKING: CJP protest exposes secret government shutdown plan",
        "text": "A viral post claims the CJP protest uncovered a hidden government directive to shut down the country's legal system within 72 hours. The post provides no verifiable evidence and asks users to share immediately before it is supposedly removed by authorities.",
        "subject": "politics"
    },
    {
        "title": "BREAKING: CJP protesters reportedly seize control of Supreme Court building",
        "text": "A social media message claims CJP protesters physically took control of the Supreme Court premises. No credible news agency or official authority confirmed the claim, and footage presented as evidence could not be independently geolocated.",
        "subject": "politics"
    },
    {
        "title": "NEW EPSTEIN FILES: Secret list names every living world leader",
        "text": "A viral post claims that a newly released batch of Epstein-related documents contains a verified list implicating every current world leader. Screenshots circulating online have not been authenticated, and no court has released documents matching the description.",
        "subject": "world"
    },
    {
        "title": "Nepal floods were secretly caused by a weather-control machine",
        "text": "A widely shared message asserts that cloud-seeding technology was deliberately weaponised to trigger the devastating floods in Nepal. No meteorological or governmental body has presented evidence for the claim, and atmospheric scientists described it as without scientific basis.",
        "subject": "world"
    },
    {
        "title": "URGENT: Government knew Nepal disaster was coming and deliberately withheld warning",
        "text": "An online post claims government authorities possessed advance satellite data predicting the exact timing and severity of the Nepal floods but chose to suppress the information. The allegation provides no authenticated documentary evidence.",
        "subject": "world"
    },
]

# ============================================================
# DATE GENERATOR
# ============================================================

def generate_date():
    year = random.choice([2022, 2023, 2024, 2025, 2026])
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"


# ============================================================
# TEXT VARIATION HELPERS
# ============================================================

# Sentence openers that add surface variety without changing meaning
REAL_OPENERS = [
    "", "", "",  # most of the time no prefix
    "Officials confirmed that ",
    "Reports indicate that ",
    "According to authorities, ",
    "Data released on {date} shows that ",
    "In a statement issued recently, officials noted that ",
]

FAKE_OPENERS = [
    "", "",  # sometimes no prefix
    "A viral post claims that ",
    "An anonymous source alleges that ",
    "Widely shared messages assert that ",
    "Unverified reports suggest that ",
    "According to an unnamed whistleblower, ",
]

REAL_CLOSERS = [
    "",
    " Officials said the situation would continue to be monitored.",
    " Further details are expected in the coming days.",
    " Independent analysts broadly confirmed the findings.",
    " Relevant authorities said the process would proceed according to established procedures.",
    " Stakeholders were invited to submit comments before the consultation deadline.",
]

FAKE_CLOSERS = [
    "",
    " This claim has not been independently verified.",
    " No credible evidence has been provided to support the allegation.",
    " Mainstream media has not reported on this story.",
    " Share this before it gets deleted!",
    " Authorities have refused to comment, fuelling speculation.",
    " Independent fact-checkers have rated the claim as false.",
]

NUMERIC_TAGS = [
    "", "",  # often no tag
    f" [Report #{random.randint(100, 9999)}]",
    f" (Update {random.randint(1, 50)})",
    f" — Source #{random.randint(10, 999)}",
]


def vary_real(template, date):
    opener = random.choice(REAL_OPENERS).replace("{date}", date)
    closer = random.choice(REAL_CLOSERS)
    tag = random.choice(NUMERIC_TAGS)
    title = template["title"] + tag
    text = opener + template["text"] + closer
    return title, text


def vary_fake(template):
    closer = random.choice(FAKE_CLOSERS)
    tag = f" [UPDATE {random.randint(1, 99)}]"
    title = template["title"] + tag
    text = template["text"] + closer
    return title, text


# ============================================================
# DATASET GENERATOR
# ============================================================

def generate_dataset(output_file="../data/raw/sample_news.csv", n_real=500, n_fake=500):
    records = []

    # --- REAL articles ---
    for _ in range(n_real):
        tmpl = random.choice(real_templates)
        date = generate_date()
        title, text = vary_real(tmpl, date)
        records.append([title, text, tmpl["subject"], date, 0])

    # --- FAKE articles ---
    for _ in range(n_fake):
        tmpl = random.choice(fake_templates)
        date = generate_date()
        title, text = vary_fake(tmpl)
        records.append([title, text, tmpl["subject"], date, 1])

    random.shuffle(records)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "text", "subject", "date", "label"])
        writer.writerows(records)

    real_count = sum(1 for r in records if r[4] == 0)
    fake_count = sum(1 for r in records if r[4] == 1)

    print("\n========================================")
    print("      FAKE NEWS DATASET GENERATED")
    print("========================================")
    print(f"Total records     : {len(records)}")
    print(f"Real records      : {real_count}")
    print(f"Fake records      : {fake_count}")
    print(f"Real templates    : {len(real_templates)}")
    print(f"Fake templates    : {len(fake_templates)}")
    print(f"Output file       : {output_file}")
    print("========================================\n")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    generate_dataset()
