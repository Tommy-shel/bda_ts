"""
inject_conflict_data.py
-----------------------
Appends war / conflict / military / geopolitical training examples to the
existing 200k CSV so the model learns to distinguish:

  REAL  — factual, measured, sourced conflict reporting
  FAKE  — sensational, unverified, conspiratorial conflict misinformation

Run once:  python apps/inject_conflict_data.py
"""

import csv
import random
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_CSV = os.path.join(BASE_DIR, "data", "raw", "high_accuracy_news_200k.csv")

random.seed(99)

# ─────────────────────────────────────────────────────────────────────────────
# REAL conflict / military / geopolitical templates  (label = 0)
# Language: measured, attributed, includes uncertainty markers
# ─────────────────────────────────────────────────────────────────────────────
REAL_CONFLICT = [
    # Pakistan / India
    {
        "title": "Pakistan and India hold ceasefire talks along Line of Control",
        "text": "Military representatives from both countries met at a designated crossing point to discuss a renewal of the 2021 ceasefire agreement along the Line of Control. Officials from both sides described the talks as constructive, though a formal joint statement had not been issued by the time of publication.",
        "subject": "world"
    },
    {
        "title": "Indian Army reports exchange of fire at northern border, no casualties confirmed",
        "text": "A defence ministry spokesperson said troops exchanged small-arms fire with an armed group that crossed the northern frontier. The spokesperson said the situation had been contained and that an investigation was under way. No soldier fatalities were reported in the initial statement.",
        "subject": "world"
    },
    {
        "title": "Pakistan military conducts anti-terrorism operation in tribal district",
        "text": "The Inter-Services Public Relations directorate announced the conclusion of a security operation in a tribal district, saying that several armed individuals had been killed and weapons caches seized. Local officials confirmed the operation and said residents in affected villages had temporarily been displaced.",
        "subject": "world"
    },
    {
        "title": "India and Pakistan resume backchannel diplomatic contact after two-year gap",
        "text": "Senior officials from both governments held informal discussions through an intermediary country for the first time in roughly two years, according to people familiar with the matter. Neither foreign ministry confirmed the talks publicly, but analysts said the contact was a cautious step toward reducing bilateral tensions.",
        "subject": "world"
    },
    {
        "title": "Cross-border shelling reported near Kashmir valley, residents asked to stay indoors",
        "text": "Authorities in the Kashmir valley issued a precautionary advisory after intermittent shelling was reported overnight near a forward post. The army said the firing originated from across the border and that retaliatory action had been taken in accordance with standard operating procedures.",
        "subject": "world"
    },
    # Russia / Ukraine
    {
        "title": "Russia launches missile strikes on Ukrainian energy infrastructure",
        "text": "Ukrainian officials reported that Russian forces launched a wave of cruise missiles targeting power substations and transmission lines in several regions overnight. Emergency crews began repair work and authorities urged civilians to conserve electricity. Russian defence officials did not immediately comment.",
        "subject": "world"
    },
    {
        "title": "Ukraine retakes village in eastern offensive, fighting continues",
        "text": "Ukrainian military commanders reported that troops had recaptured a village in the east after several days of intense combat. Russian military bloggers acknowledged a tactical withdrawal from the area. Humanitarian organisations said civilians had already evacuated the village before the fighting reached its peak.",
        "subject": "world"
    },
    {
        "title": "NATO allies pledge additional air defence systems to Ukraine",
        "text": "Defence ministers from several NATO member states announced commitments to provide Ukraine with additional surface-to-air missile batteries at a coordination meeting. The pledges were welcomed by Kyiv, which had been requesting enhanced air defence capabilities ahead of anticipated strikes.",
        "subject": "world"
    },
    {
        "title": "Ceasefire negotiations between Russia and Ukraine stall over territorial terms",
        "text": "Diplomatic sources said a round of indirect talks mediated by a neutral country had failed to produce an agreed framework, with the two sides remaining far apart on questions of territorial control. Both governments blamed the other for the breakdown, and military activity continued along the front line.",
        "subject": "world"
    },
    {
        "title": "UN Security Council convenes emergency session over escalation in Ukraine",
        "text": "Council members called an emergency session to discuss the latest escalation in the conflict, including attacks on civilian infrastructure. Western members called for an immediate ceasefire, while Russia's representative rejected the characterisation of the strikes and argued that Ukraine's military facilities were legitimate targets.",
        "subject": "world"
    },
    # China / Taiwan / South China Sea
    {
        "title": "China conducts live-fire naval exercises near Taiwan Strait",
        "text": "China's People's Liberation Army Navy announced the completion of live-fire exercises in waters near the Taiwan Strait. Taiwan's defence ministry said it had monitored the drills closely and that its forces remained on heightened alert. The exercises followed a visit to Taipei by foreign legislators.",
        "subject": "world"
    },
    {
        "title": "Taiwan scrambles jets as Chinese aircraft cross median line",
        "text": "Taiwan's defence ministry said it had scrambled fighter aircraft after People's Liberation Army Air Force planes crossed the informal median line dividing the Taiwan Strait on multiple occasions. The ministry released tracking data and said the incursions were a deliberate provocation.",
        "subject": "world"
    },
    {
        "title": "US aircraft carrier group enters South China Sea amid territorial tensions",
        "text": "A US Navy carrier strike group transited the South China Sea in what the Pentagon described as a routine freedom-of-navigation operation. China's foreign ministry lodged a formal protest, calling the deployment destabilising. Regional neighbours said they monitored the situation closely.",
        "subject": "world"
    },
    {
        "title": "Philippines and China vessels collide near disputed reef",
        "text": "The Philippine coast guard reported a collision between one of its patrol vessels and a Chinese maritime militia ship near a disputed reef in the South China Sea. The Philippines said the incident was deliberate; China's coast guard said the Philippine vessel was operating illegally in Chinese waters.",
        "subject": "world"
    },
    # Middle East
    {
        "title": "Israeli air strikes target weapons depots in southern Lebanon",
        "text": "The Israeli Defence Forces confirmed a series of air strikes on what it described as weapons storage facilities in southern Lebanon. Lebanese officials reported damage to several structures and said emergency services were on site. The operation followed a cross-border rocket attack the previous day.",
        "subject": "world"
    },
    {
        "title": "Iran-backed groups claim rocket attack on US base in Iraq",
        "text": "A group describing itself as Iran-backed claimed responsibility for a rocket attack on a base housing US personnel in Iraq. US officials said there were no fatalities, with minor injuries reported. The US military said it was assessing the attack and that a response would be carried out at a time of its choosing.",
        "subject": "world"
    },
    {
        "title": "Gaza ceasefire collapses as rocket fire resumes",
        "text": "A mediated ceasefire broke down after rockets were fired from Gaza toward Israeli towns, prompting retaliatory air strikes. Both sides blamed each other for initiating the renewed hostilities. Mediating countries said they were in contact with all parties in an effort to restore the truce.",
        "subject": "world"
    },
    {
        "title": "Saudi Arabia and Houthi forces exchange artillery fire across Yemen border",
        "text": "The Saudi-led coalition reported Houthi artillery fire targeting border towns, with retaliatory strikes carried out on Houthi positions in northern Yemen. Aid organisations warned that renewed fighting threatened humanitarian access to areas already experiencing severe food insecurity.",
        "subject": "world"
    },
    # US military / NATO
    {
        "title": "US military conducts drone strike targeting militant commander in Somalia",
        "text": "US Africa Command announced that a precision drone strike had killed a senior al-Shabaab commander in a remote area of Somalia. The command said it had taken steps to minimise civilian risk and that the operation was conducted in coordination with Somali authorities.",
        "subject": "world"
    },
    {
        "title": "NATO increases troop presence in eastern Europe following security review",
        "text": "Alliance defence ministers agreed to reinforce NATO's eastern flank with additional battle groups following a security assessment that identified increased risk. Troops from several member nations were to be deployed on a rotational basis, with the first units arriving within weeks.",
        "subject": "world"
    },
    {
        "title": "Turkey and Greece dispute airspace over Aegean, NATO mediates",
        "text": "A long-running dispute between Turkey and Greece over Aegean airspace escalated after the two countries' jets engaged in simulated combat manoeuvres near a contested island. NATO's secretary-general urged both members to exercise restraint and said the alliance stood ready to facilitate dialogue.",
        "subject": "world"
    },
    # General conflict / war reporting
    {
        "title": "Sudan civil war displaces over four million people, UN warns",
        "text": "United Nations agencies reported that more than four million people had been displaced by fighting between the Sudanese Armed Forces and a paramilitary group since the conflict began, making it one of the world's largest displacement crises. Aid access remained severely restricted in several regions.",
        "subject": "world"
    },
    {
        "title": "Myanmar junta air strikes hit civilian market in Sagaing region",
        "text": "Human rights monitors and local journalists reported that Myanmar military aircraft struck a weekly market in the Sagaing region, killing and injuring civilians. The junta denied targeting civilians; independent verification was limited by restricted access to the area.",
        "subject": "world"
    },
    {
        "title": "Ethiopia and Eritrea tensions rise as troops mass along shared border",
        "text": "Satellite imagery reviewed by analysts showed unusual troop movements near the Ethiopia-Eritrea border, raising concerns about a potential renewal of hostilities. Both governments declined to comment on the deployments, and diplomatic contacts between the two countries had been suspended.",
        "subject": "world"
    },
    {
        "title": "North Korea fires ballistic missile toward Sea of Japan",
        "text": "South Korea's Joint Chiefs of Staff detected the launch of a ballistic missile from North Korean territory that fell into the Sea of Japan. Japanese authorities issued a safety alert and said the missile landed outside Japan's exclusive economic zone. The US condemned the launch as a violation of UN resolutions.",
        "subject": "world"
    },
    {
        "title": "UK deploys warship to Red Sea amid Houthi shipping attacks",
        "text": "The Royal Navy confirmed the deployment of a Type-45 destroyer to the Red Sea as part of a multinational force protecting commercial shipping from Houthi drone and missile attacks. Several major shipping companies had already begun rerouting vessels around the Cape of Good Hope.",
        "subject": "world"
    },
    {
        "title": "Pakistan test-fires medium-range ballistic missile in routine exercise",
        "text": "Pakistan's military announced the successful test launch of a medium-range ballistic missile capable of carrying conventional warheads. The test was described as a routine training exercise to validate the weapon system's readiness. India's foreign ministry took note of the launch and said it was monitoring the situation.",
        "subject": "world"
    },
    {
        "title": "India deploys additional troops to Ladakh border amid standoff",
        "text": "Indian defence officials confirmed the deployment of additional army units to the Ladakh border region following a confrontation with Chinese patrols at a disputed patrol point. Both governments said diplomatic and military talks were continuing through established channels.",
        "subject": "world"
    },
    {
        "title": "China sanctions US defence companies over Taiwan arms sale",
        "text": "China's foreign ministry announced targeted sanctions on several US defence manufacturers following Washington's approval of a weapons package for Taiwan. The companies named said the sanctions would have a limited practical impact on their operations.",
        "subject": "world"
    },
    {
        "title": "Iran seizes commercial tanker in Strait of Hormuz over alleged violation",
        "text": "Iran's Revolutionary Guard Corps announced the seizure of a commercial oil tanker in the Strait of Hormuz, citing what it described as a maritime law violation. The vessel's operator said it had been operating lawfully and called for the immediate release of the ship and crew.",
        "subject": "world"
    },
    {
        "title": "Hackers linked to state actor disrupt military communication networks",
        "text": "Cybersecurity officials in two allied countries reported coordinated intrusions into military communication infrastructure attributed with moderate confidence to a state-sponsored hacking group. The affected systems had been isolated as a precaution and operations were continuing through backup channels.",
        "subject": "tech"
    },
    {
        "title": "Peace talks between warring factions in CAR make limited progress",
        "text": "Mediators from the African Union said a new round of peace talks between armed factions in the Central African Republic had produced a tentative agreement on a humanitarian access corridor, though a broader ceasefire remained elusive. Fighting continued in several provinces despite the ongoing negotiations.",
        "subject": "world"
    },
    {
        "title": "US imposes new sanctions on entities supplying weapons to Russia",
        "text": "The US Treasury Department designated several companies in third countries for providing dual-use technology and components to Russian military procurement networks. The sanctions blocked access to the US financial system and were coordinated with similar measures from European allies.",
        "subject": "world"
    },
    {
        "title": "South Korea and US begin joint military exercises despite North Korean warnings",
        "text": "Annual combined military exercises between South Korean and US forces commenced as scheduled despite warnings from North Korea that the drills were a provocation. The two allies described the exercises as defensive in nature and said they served to maintain readiness on the peninsula.",
        "subject": "world"
    },
    {
        "title": "International Criminal Court issues arrest warrant for military commander",
        "text": "The International Criminal Court issued an arrest warrant for a senior military commander accused of directing attacks on civilian populations in a conflict zone. The country concerned rejected the court's jurisdiction, while human rights organisations called on all ICC member states to enforce the warrant.",
        "subject": "world"
    },
    {
        "title": "UN peacekeeping mission in Mali ends amid security deterioration",
        "text": "The United Nations formally concluded its peacekeeping mission in Mali after the country's military government ordered foreign forces to leave. The withdrawal followed years of deteriorating security conditions and strained relations between the junta and its international partners.",
        "subject": "world"
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# FAKE conflict / military / geopolitical templates  (label = 1)
# Language: sensational caps, unverified leaks, anonymous sources, no evidence
# ─────────────────────────────────────────────────────────────────────────────
FAKE_CONFLICT = [
    # Pakistan attacks
    {
        "title": "BREAKING: Pakistan launches surprise nuclear strike on three Indian cities",
        "text": "Unverified social-media posts claim that Pakistani forces have launched nuclear warheads targeting major Indian metropolitan areas, with several sources alleging that communication networks have already gone dark. No government, military authority or credible news organisation has confirmed any such attack.",
        "subject": "world"
    },
    {
        "title": "LEAKED: Pakistan secretly attacks US military base in Afghanistan using drones",
        "text": "An anonymous Telegram account claims to have footage proving that Pakistani military drones struck a covert American installation overnight. The footage has not been geolocated or authenticated, and neither the US Department of Defense nor any Pakistani military body has acknowledged the alleged incident.",
        "subject": "world"
    },
    {
        "title": "URGENT: Pakistan army crosses border and takes control of Kashmir capital",
        "text": "A viral message claims that Pakistani armoured columns entered Indian-administered Kashmir and seized the regional capital within hours. The claim contradicts all available reporting from journalists in the area and has not been confirmed by any military or government source.",
        "subject": "world"
    },
    {
        "title": "SHOCK: Pakistan fires ballistic missiles at Delhi — government hiding civilian casualties",
        "text": "A widely shared post alleges that multiple ballistic missiles struck the outskirts of the Indian capital and that casualty figures are being suppressed by both governments. Residents in Delhi reported no explosions or disruption, and official sources denied any attack had taken place.",
        "subject": "world"
    },
    {
        "title": "BOMBSHELL: Pakistani ISI planned and executed the 9/11 attacks, documents prove",
        "text": "A blog claims to possess declassified documents proving that Pakistan's intelligence service was the primary architect of the September 11 attacks. The documents have not been released in verifiable form and no intelligence agency or official investigation has ever reached such a conclusion.",
        "subject": "world"
    },
    # India attacks
    {
        "title": "BREAKING: India drops bombs on Karachi port in secret overnight operation",
        "text": "Anonymous accounts are circulating images they claim show explosions at Karachi port following an alleged Indian air strike. The images cannot be traced to the claimed location or date, and no Pakistani, Indian or international body has confirmed any such operation.",
        "subject": "world"
    },
    {
        "title": "REVEALED: India secretly tested a weapon that can disable all of China's satellites",
        "text": "A post claims that India conducted a covert test of an electromagnetic pulse weapon powerful enough to disable China's entire satellite constellation in one strike. No defence analyst, space agency or government has confirmed or hinted at such a capability.",
        "subject": "world"
    },
    {
        "title": "URGENT: Indian troops invade Pakistan — war officially declared but media censored",
        "text": "A widely circulated message claims India has formally declared war on Pakistan and that troops have crossed the international border, but that mainstream media is under a government blackout order preventing coverage. No such declaration or blackout has been issued.",
        "subject": "world"
    },
    # China attacks / conspiracies
    {
        "title": "BREAKING: China invades Taiwan — US refuses to respond, secret deal exposed",
        "text": "A viral post claims China has launched a full-scale amphibious invasion of Taiwan and that a secret agreement between Washington and Beijing is preventing any US military response. No such invasion has been reported by any credible news organisation or military source.",
        "subject": "world"
    },
    {
        "title": "EXPOSED: China planted bombs in US infrastructure 10 years ago, all set to detonate",
        "text": "An anonymous whistleblower allegedly claims that Chinese operatives embedded explosive devices in American power grids and water treatment facilities a decade ago, awaiting a remote detonation signal. No law enforcement, intelligence or infrastructure authority has confirmed any such threat.",
        "subject": "world"
    },
    {
        "title": "SHOCKING: China and Russia sign secret pact to simultaneously attack US allies",
        "text": "A blog post claims to have obtained a classified treaty in which China and Russia agreed to launch coordinated military strikes against US-allied nations on a pre-set date. Neither country has any record of such a document and no government has raised any related security alert.",
        "subject": "world"
    },
    {
        "title": "LEAKED: China secretly deploys troops inside 12 US cities disguised as tourists",
        "text": "A conspiracy account claims that tens of thousands of Chinese soldiers have entered the United States posing as tourists and are awaiting activation orders. No law enforcement or intelligence agency has corroborated the claim.",
        "subject": "world"
    },
    # Russia / Ukraine misinformation
    {
        "title": "BOMBSHELL: Ukraine war was entirely staged by NATO using crisis actors",
        "text": "A conspiracy video claims that footage from the conflict in Ukraine was produced by NATO in a studio, with all casualties fabricated using professional actors. Independent journalists, forensic investigators and satellite imagery analysts have documented real combat deaths and destruction in Ukraine.",
        "subject": "world"
    },
    {
        "title": "BREAKING: Russia launches nuclear attack on London — UK government hiding it",
        "text": "A viral post alleges that a Russian tactical nuclear device detonated near London and that the British government has imposed a total media blackout. Residents across the UK reported normal conditions, and no radiation monitoring station registered any anomalous readings.",
        "subject": "world"
    },
    {
        "title": "URGENT: Putin assassinated by CIA — body double running Russia since 2022",
        "text": "A widely shared claim insists that Vladimir Putin was killed by a CIA operative and that a trained double has been governing Russia, with close advisers part of the cover-up. The claim has no credible evidentiary basis and no intelligence service has substantiated it.",
        "subject": "world"
    },
    {
        "title": "REVEALED: Ukraine is secretly controlled by a foreign billionaire who started the war",
        "text": "A conspiracy post alleges that a named foreign billionaire is the true decision-maker behind Ukraine's government and engineered the conflict for personal profit. The claim relies on unverified financial diagrams shared anonymously and has been denied by Ukrainian officials.",
        "subject": "world"
    },
    # US / NATO misinformation
    {
        "title": "SHOCKING: US military planning false flag attack to start World War III",
        "text": "A viral post claims that senior Pentagon officials have approved a false flag operation designed to be blamed on a rival power, providing justification for a global war. The post cites no verifiable documents and no credible journalism has substantiated the allegation.",
        "subject": "world"
    },
    {
        "title": "BREAKING: NATO secretly moves nuclear weapons to border — attack on Russia imminent",
        "text": "An anonymous account alleges that NATO has secretly relocated tactical nuclear weapons to bases within kilometres of the Russian border as a prelude to a surprise strike. Neither NATO nor any member government has confirmed any such redeployment.",
        "subject": "world"
    },
    {
        "title": "EXPOSED: US soldiers ordered to shoot civilians in Syria — leaked video proof",
        "text": "A post claims to possess unedited footage showing US military personnel receiving and executing orders to fire on unarmed Syrian civilians. The footage has not been authenticated, its provenance is unknown, and no US military investigation or credible journalistic inquiry has confirmed the allegation.",
        "subject": "world"
    },
    {
        "title": "URGENT: CIA creating bio-weapon labs inside Ukraine to attack Russia, documents show",
        "text": "A widely circulated post claims that leaked documents prove the US Central Intelligence Agency is operating biological weapons facilities inside Ukraine intended to produce pathogens targeting Russian citizens. The claim was comprehensively investigated and rejected by independent arms control experts.",
        "subject": "world"
    },
    # Middle East misinformation
    {
        "title": "BOMBSHELL: Israel using weather-control machine to cause droughts across Middle East",
        "text": "A viral post claims that Israeli scientists have developed and deployed a cloud-seeding system capable of deliberately withholding rainfall from neighbouring countries. No meteorological or atmospheric scientist has supported the claim, and no credible evidence has been presented.",
        "subject": "world"
    },
    {
        "title": "BREAKING: Iran has already launched nuclear missiles toward Israel, cover-up in progress",
        "text": "A social-media account claims Iran fired nuclear-armed missiles toward Israel hours ago and that a complete information blackout is hiding the fact. Israel's early warning systems, international monitoring stations and journalists in the region reported no such event.",
        "subject": "world"
    },
    {
        "title": "EXPOSED: Saudi Arabia secretly funding terrorist attacks in Europe",
        "text": "An anonymous blog claims that leaked bank records prove the Saudi government has been financing terrorist cells across Europe for years. The records have not been independently verified, no financial intelligence unit has published related findings, and the Saudi government has denied the allegation.",
        "subject": "world"
    },
    # North Korea / general
    {
        "title": "SHOCKING: North Korea already has 500 nuclear warheads aimed at US cities",
        "text": "A viral post claims intelligence sources confirm North Korea secretly assembled a nuclear arsenal far exceeding publicly known estimates, with missiles pre-targeted at major American cities. Public estimates from credentialed non-proliferation experts place North Korea's arsenal at a fraction of that figure.",
        "subject": "world"
    },
    {
        "title": "BREAKING: North Korea and China launch simultaneous cyber-attack shutting down US power grid",
        "text": "A post claims that a coordinated cyber-attack by North Korean and Chinese state actors has caused blackouts across the US eastern seaboard. Power grid operators and the Department of Homeland Security reported normal operations at the time of the post.",
        "subject": "world"
    },
    {
        "title": "REVEALED: Secret US military base found on dark side of Moon, China about to attack it",
        "text": "A conspiracy blog claims satellite imagery proves the existence of a clandestine US military installation on the far side of the Moon and that China has dispatched a spacecraft to destroy it. No space agency has confirmed any such installation or mission.",
        "subject": "world"
    },
    # War false alarms / disinfo
    {
        "title": "URGENT: World War III officially started 2 hours ago — governments hiding it",
        "text": "A message spreading rapidly across platforms claims that a coordinated military confrontation involving multiple nuclear powers began hours ago and is being concealed by a global media agreement. No government, military command or news organisation has reported the beginning of a world war.",
        "subject": "world"
    },
    {
        "title": "BREAKING: Nuclear explosion detected in major city — radiation spreading",
        "text": "A post claims that sensors have detected a nuclear detonation in a major metropolitan area and that radiation clouds are drifting across neighbouring countries. International radiation monitoring networks showed no unusual readings at the time, and no government or emergency authority issued any radiation warning.",
        "subject": "world"
    },
    {
        "title": "SHOCK CLAIM: US and Russia already fighting secret underwater war with submarine fleets",
        "text": "A blog asserts that American and Russian submarine forces have been engaged in a concealed naval conflict for months, with multiple vessels lost and governments suppressing the information. No navy, government or credible journalist has reported any such engagement.",
        "subject": "world"
    },
    {
        "title": "EXPOSED: Military drones spraying population with experimental chemicals during conflict",
        "text": "A viral post claims that military drones deployed in an active conflict zone are secretly dispersing experimental chemical agents over civilian populations under cover of normal operations. No arms control inspector, toxicologist or verified journalist has confirmed any such programme.",
        "subject": "world"
    },
    {
        "title": "BOMBSHELL: Every major war in history was engineered by the same secret banking family",
        "text": "A conspiracy article claims that a single banking dynasty financed and deliberately orchestrated every major military conflict over the past two centuries for profit. The claim provides no verifiable primary sources and relies entirely on unattributed secondary material from other conspiracy sites.",
        "subject": "world"
    },
    {
        "title": "BREAKING: Pakistan nukes USA — entire west coast destroyed, news blackout active",
        "text": "A viral message claims Pakistan launched nuclear-armed intercontinental ballistic missiles that have already struck the US west coast and that a total news blackout is preventing coverage. Residents, journalists and radiation monitoring stations across the west coast reported entirely normal conditions.",
        "subject": "world"
    },
    {
        "title": "URGENT: China attacks USA — invades California beaches with 2 million troops",
        "text": "A widely shared post claims that Chinese landing craft arrived on Californian beaches overnight carrying two million soldiers and that the US military has been ordered to stand down. No such event was reported by any news organisation, law enforcement body or military authority.",
        "subject": "world"
    },
    {
        "title": "REVEALED: Russia fires hypersonic missile at Washington DC, Pentagon destroyed",
        "text": "A social media post claims a Russian hypersonic missile struck the Pentagon, and that the US government has implemented emergency succession protocols. All government facilities in Washington DC were operating normally, and no explosion or impact was reported.",
        "subject": "world"
    },
    {
        "title": "SHOCKING: India and Pakistan both launch nukes — billions dead, news suppressed globally",
        "text": "A panic-inducing post claims a full nuclear exchange between India and Pakistan has already occurred, killing billions, with every government on Earth jointly suppressing the information. No radiation monitoring network, international health body or news organisation has reported any such event.",
        "subject": "world"
    },
    {
        "title": "BREAKING: NATO triggers Article 5 — all member nations now at war with Russia",
        "text": "A viral claim asserts that NATO secretly invoked Article 5 collective defence following an alleged Russian attack and that all thirty-two member nations are now in a state of declared war. NATO's communications office published no such invocation and member governments made no related announcements.",
        "subject": "world"
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# Variation helpers
# ─────────────────────────────────────────────────────────────────────────────

REAL_OPENERS = [
    "", "", "",
    "Officials confirmed that ",
    "According to defence sources, ",
    "Military spokespersons stated that ",
    "Reports from the region indicate that ",
    "A government statement noted that ",
]

REAL_CLOSERS = [
    "",
    " The situation is being closely monitored by regional and international observers.",
    " Both sides urged restraint and said diplomatic channels remained open.",
    " Further details are expected as the situation develops.",
    " Humanitarian organisations called for immediate access to affected civilians.",
    " Independent analysts said the development added new uncertainty to an already volatile region.",
]

FAKE_OPENERS = [
    "", "",
    "A viral post claims that ",
    "Anonymous sources allege that ",
    "Unverified reports spreading online assert that ",
    "A whistleblower account claims that ",
]

FAKE_CLOSERS = [
    "",
    " This claim has not been independently verified by any credible source.",
    " No government, military or news organisation has confirmed the allegation.",
    " Share this before it gets deleted!",
    " Mainstream media is reportedly suppressing this story.",
    " Independent fact-checkers have rated similar claims as false.",
    " No official radiation, seismic or emergency alert corroborates the post.",
]

def generate_date():
    year  = random.choice([2022, 2023, 2024, 2025, 2026])
    month = random.randint(1, 12)
    day   = random.randint(1, 28)
    return f"{year}-{month:02d}-{day:02d}"

def vary_real(tmpl):
    opener = random.choice(REAL_OPENERS)
    closer = random.choice(REAL_CLOSERS)
    tag    = f" [Report #{random.randint(100, 9999)}]" if random.random() < 0.4 else ""
    title  = tmpl["title"] + tag
    text   = opener + tmpl["text"] + closer
    return title, text

def vary_fake(tmpl):
    opener = random.choice(FAKE_OPENERS)
    closer = random.choice(FAKE_CLOSERS)
    tag    = f" [UPDATE {random.randint(1, 99)}]" if random.random() < 0.6 else ""
    title  = tmpl["title"] + tag
    text   = opener + tmpl["text"] + closer
    return title, text

# ─────────────────────────────────────────────────────────────────────────────
# Build records: 500 real + 500 fake = 1 000 new rows
# ─────────────────────────────────────────────────────────────────────────────
N_PER_CLASS = 500

new_records = []

for _ in range(N_PER_CLASS):
    tmpl  = random.choice(REAL_CONFLICT)
    date  = generate_date()
    title, text = vary_real(tmpl)
    new_records.append([title, text, tmpl["subject"], date, 0])

for _ in range(N_PER_CLASS):
    tmpl  = random.choice(FAKE_CONFLICT)
    date  = generate_date()
    title, text = vary_fake(tmpl)
    new_records.append([title, text, tmpl["subject"], date, 1])

random.shuffle(new_records)

# ─────────────────────────────────────────────────────────────────────────────
# Append to existing CSV (no header repeat)
# ─────────────────────────────────────────────────────────────────────────────
appended = 0
with open(OUTPUT_CSV, "a", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    for row in new_records:
        writer.writerow(row)
        appended += 1

real_added = sum(1 for r in new_records if r[4] == 0)
fake_added = sum(1 for r in new_records if r[4] == 1)

print("\n========================================")
print("  CONFLICT DATA INJECTION COMPLETE")
print("========================================")
print(f"Real rows added   : {real_added}")
print(f"Fake rows added   : {fake_added}")
print(f"Total rows added  : {appended}")
print(f"Output file       : {OUTPUT_CSV}")
print("========================================\n")
print("Next step: re-run the full pipeline:")
print("  1. python apps/preprocessing_analytics.py")
print("  2. python apps/train_model.py")
print("========================================\n")
