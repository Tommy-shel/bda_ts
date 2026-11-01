"""
Appends real disaster news rows (label=0) and matching fake/misinfo rows
(label=1) to high_accuracy_news_200k.csv.

Run once:  python apps/add_disaster_data.py
"""
import os
import csv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "raw", "high_accuracy_news_200k.csv")

# ── Real disaster articles  (label = 0) ──────────────────────────────────────
REAL_ROWS = [

    # ── Cyclone Arnab (Oct 28-29 2026) ───────────────────────────────────────
    {
        "title": "Cyclone Arnab makes landfall on Andhra Pradesh coast, nine killed and 180,000 evacuated",
        "text": (
            "Very Severe Cyclonic Storm Arnab crossed the Andhra Pradesh coastline between Yanam and Kakinada "
            "over a six-hour period from 2 am to 8 am on October 29, 2026, the India Meteorological Department "
            "confirmed. The storm brought sustained winds of up to 100 kmph and heavy rainfall across coastal "
            "Andhra Pradesh and southern Odisha. Authorities evacuated more than 180,000 people to cyclone "
            "shelters before landfall. Nine fatalities were recorded across the state, caused by falling trees, "
            "electrocution, wall collapses and cyclone-related incidents. Andhra Pradesh Chief Minister "
            "N. Chandrababu Naidu wrote to Union Home Minister Amit Shah stating that at least 180 houses were "
            "destroyed, 220 trees uprooted and power supply disrupted across West Godavari, Konaseema and "
            "Kakinada districts. The state government estimated total losses at Rs 4,600 crore, with 325,000 "
            "hectares of standing crops inundated. South Central Railway cancelled more than 50 trains. "
            "Odisha announced it would airlift relief supplies to residents of 300 cyclone-hit villages cut off "
            "by floodwaters. The National Disaster Response Force deployed 30 teams across both states."
        ),
        "subject": "world",
        "date": "October 29, 2026",
        "label": 0,
    },
    {
        "title": "Odisha to airlift residents of 300 cyclone-hit villages after Arnab batters coast",
        "text": (
            "Odisha authorities announced emergency airlifts for residents stranded in 300 villages cut off "
            "by floodwaters in the aftermath of Cyclone Arnab. The state government said rising water levels "
            "in the Mahanadi delta system had isolated numerous low-lying communities. The Indian Air Force "
            "deployed Mi-17 helicopters to carry food, drinking water and medicines to affected areas. "
            "Heavy rainfall was forecast to continue for at least three more days, according to the India "
            "Meteorological Department. Odisha's Special Relief Commissioner said all district collectors "
            "had been placed on maximum alert and rescue boats were pre-positioned along major river systems. "
            "The cyclone also caused nine train cancellations on the East Coast Railway zone. Schools and "
            "colleges across six districts remained shut as a precautionary measure."
        ),
        "subject": "world",
        "date": "October 30, 2026",
        "label": 0,
    },
    {
        "title": "Cyclone Arnab leaves Rs 4,600 crore damage in Andhra Pradesh; crops across 325,000 hectares inundated",
        "text": (
            "A damage assessment submitted to the Union government by Andhra Pradesh Chief Minister "
            "N. Chandrababu Naidu put total losses from Cyclone Arnab at Rs 4,600 crore. Agriculture "
            "officials reported that standing crops across 325,000 hectares had been submerged, with "
            "paddy, cotton and chilli plantations in West Godavari and Konaseema districts among the "
            "worst affected. An auxiliary nurse midwife went missing while attempting to cross a swollen "
            "canal in East Godavari. Twelve thousand five hundred trees were uprooted and more than "
            "180 residences damaged across the three worst-hit districts. The state sought central "
            "assistance under the National Disaster Response Fund to fund relief and rehabilitation. "
            "Power restoration teams from APEPDCL were working to repair damaged transmission lines "
            "and restore electricity to the approximately 400,000 households that remained without power."
        ),
        "subject": "world",
        "date": "October 30, 2026",
        "label": 0,
    },

    # ── Hurricane Isaias (Oct 9-10 2026, Florida/Alabama) ────────────────────
    {
        "title": "Hurricane Isaias makes landfall in Destin, Florida as Category 2 storm; nine killed across three states",
        "text": (
            "Hurricane Isaias made landfall near Destin in the Florida Panhandle as a Category 2 storm on "
            "the evening of October 9, 2026, bringing sustained winds of 100 mph and gusts exceeding "
            "117 mph, the National Hurricane Center reported. The storm rapidly intensified to Category 3 "
            "strength in the Gulf of Mexico before weakening slightly before landfall. Florida Governor "
            "Ron DeSantis confirmed six deaths in the state, attributing fatalities to falling trees, "
            "storm surge and carbon monoxide poisoning from generator use. Two people were killed in "
            "Alabama and one in South Carolina as the storm moved inland. At its peak, nearly 930,000 "
            "customers across the Florida Panhandle and Alabama were without electricity. Insured losses "
            "in the United States were projected to surpass two billion dollars. Emergency teams conducted "
            "hundreds of water rescues in low-lying coastal communities."
        ),
        "subject": "world",
        "date": "October 10, 2026",
        "label": 0,
    },
    {
        "title": "Hurricane Isaias recovery: 17,000 still without power in Florida Panhandle days after landfall",
        "text": (
            "Recovery efforts continued across the Florida Panhandle several days after Hurricane Isaias "
            "made landfall near Destin as a Category 2 storm. While utility crews restored electricity "
            "to most of the 930,000 customers who lost power during the storm, approximately 17,000 "
            "households in the hardest-hit areas of Escambia and Okaloosa counties remained without "
            "power. Debris-clearing operations were under way on major highways, with the Florida "
            "Department of Transportation estimating it would take several weeks to fully reopen all "
            "impacted roads. FEMA opened disaster assistance registration centres in five Panhandle "
            "counties. The death toll from the storm rose to nine across Florida, Alabama and South "
            "Carolina, with insured losses expected to exceed two billion dollars."
        ),
        "subject": "world",
        "date": "October 12, 2026",
        "label": 0,
    },

    # ── Panama Earthquake (Oct 9 2026) ────────────────────────────────────────
    {
        "title": "Magnitude 7.5 earthquake strikes Panama, killing three and damaging 3,390 homes across ten provinces",
        "text": (
            "A powerful magnitude 7.5 earthquake struck the Azuero Peninsula in central Panama on "
            "October 9, 2026, at 12:56 pm local time, the United States Geological Survey reported. "
            "The quake was felt across all ten of Panama's provinces and two indigenous territories. "
            "Panamanian authorities confirmed three deaths and 27 injuries. The government declared a "
            "state of emergency as assessments revealed approximately 3,390 homes had been affected, "
            "including 727 classified as total losses. Schools, health centres and water systems were "
            "damaged in at least four central and west-central provinces. More than 200 aftershocks "
            "followed the main event over the weekend, hampering rescue and assessment efforts. UNICEF "
            "reported that children's access to education and safe drinking water was severely disrupted "
            "in Los Santos and Veraguas provinces. The Inter-American Development Bank offered emergency "
            "financing to support recovery operations."
        ),
        "subject": "world",
        "date": "October 9, 2026",
        "label": 0,
    },
    {
        "title": "Panama declares state of emergency as earthquake aftershocks isolate rural communities",
        "text": (
            "Panama's government declared a national state of emergency on October 10, 2026, one day "
            "after a magnitude 7.5 earthquake damaged homes, bridges and roads across the country's "
            "central provinces. The Panamanian Civil Protection System reported that collapsed bridges "
            "and landslides had cut off several rural communities, preventing rescue teams from reaching "
            "them by road. Military helicopters were deployed to deliver emergency supplies. Officials "
            "said the published injury tally of 27 might rise as field teams gained access to isolated "
            "areas. PAHO and WHO activated emergency health response protocols and pre-positioned "
            "medical supplies at regional distribution points. Schools in six provinces were closed "
            "pending structural safety assessments."
        ),
        "subject": "world",
        "date": "October 10, 2026",
        "label": 0,
    },

    # ── Tibet Earthquake (Oct 22 2026) ────────────────────────────────────────
    {
        "title": "Magnitude 7.0 earthquake kills 16 and injures 76 in China's Tibet, hundreds of homes collapse in Nagqu",
        "text": (
            "A magnitude 7.0 earthquake struck the Nagqu city area of the Tibet Autonomous Region on "
            "the evening of October 22, 2026, killing at least 16 people and injuring 76, Chinese state "
            "media reported citing official government sources. The disaster struck at an elevation of "
            "approximately 4,800 metres above sea level, complicating rescue operations due to the "
            "remote terrain and altitude. At least 339 homes and 20 livestock sheds collapsed in the "
            "initial quake. Eleven of the injured were in serious condition. The China Earthquake "
            "Administration described it as the strongest earthquake to hit the region in five years. "
            "Rescue teams from the People's Liberation Army and local fire departments were deployed "
            "within hours. Officials warned of ongoing risks from aftershocks and potential rockslides. "
            "Temperatures in the high-altitude area were expected to drop sharply overnight, adding "
            "urgency to efforts to shelter displaced residents."
        ),
        "subject": "world",
        "date": "October 22, 2026",
        "label": 0,
    },
    {
        "title": "Rescuers search for survivors after Tibet earthquake; cold temperatures hamper relief operations",
        "text": (
            "Search-and-rescue teams continued sifting through rubble in Nagqu, Tibet, on October 23, "
            "2026, one day after a magnitude 7.0 earthquake killed at least 16 people and caused "
            "widespread structural damage. The disaster philanthropy monitoring network noted that the "
            "quake was the strongest to hit Tibet in five years. Freezing overnight temperatures at "
            "the 4,800-metre elevation added urgency to the relief effort, as hundreds of displaced "
            "residents required emergency shelter. Chinese authorities confirmed the collapse of 339 "
            "homes and 20 livestock sheds, while officials warned that ongoing aftershocks posed a "
            "continued risk of further building collapses and rockslides. The central government "
            "released emergency relief funds and dispatched additional rescue personnel to the region."
        ),
        "subject": "world",
        "date": "October 23, 2026",
        "label": 0,
    },

    # ── Kilauea Eruption (Oct-Nov 2026) ───────────────────────────────────────
    {
        "title": "Kilauea volcano paused after episode 55; USGS forecasts episode 56 eruption between November 2 and 9",
        "text": (
            "The Halemaʻumaʻu eruption of Kilauea volcano on Hawaii's Big Island remained paused "
            "following the end of episode 55 fountaining on October 17, 2026, the United States "
            "Geological Survey Hawaiian Volcano Observatory reported. Ground deformation instruments "
            "recorded continued summit reinflation, indicating magma was accumulating beneath the "
            "crater. The observatory forecast that episode 56 fountaining was most likely to begin "
            "between November 2 and November 9, 2026, though it cautioned that the timing could "
            "shift based on the rate of inflation. The ongoing eruption cycle, which began earlier "
            "in the year, had produced dozens of eruptive episodes characterised by lava fountaining "
            "within the summit caldera. Hawaii Volcanoes National Park remained open, with park "
            "officials advising visitors to monitor conditions closely and avoid restricted zones "
            "near active vents."
        ),
        "subject": "science",
        "date": "October 31, 2026",
        "label": 0,
    },

    # ── Post-tropical Cyclone Rachel (Oct 12 2026, California) ───────────────
    {
        "title": "Post-tropical cyclone Rachel batters California coast; beachfront homes damaged in Long Beach",
        "text": (
            "Post-tropical cyclone Rachel made an unusual landfall along the Southern California "
            "coastline on October 12, 2026, generating large waves and strong winds that damaged "
            "beachfront properties in Long Beach and surrounding communities. The National Hurricane "
            "Center noted that the system had transitioned from a tropical cyclone in the Pacific "
            "and retained significant moisture and wind energy as it moved ashore. Associated Press "
            "photographs showed waves crashing into oceanfront homes. Local emergency managers issued "
            "evacuation advisories for low-lying coastal areas. The Los Angeles County Office of "
            "Emergency Management activated its emergency operations centre. Coastal erosion and "
            "flooding were reported along a stretch of beach communities from Seal Beach to Malibu. "
            "No fatalities were immediately confirmed, but officials warned residents to stay away "
            "from beaches and seawalls until conditions improved."
        ),
        "subject": "world",
        "date": "October 12, 2026",
        "label": 0,
    },
]

# ── Fake / misinfo disaster articles  (label = 1) ────────────────────────────
FAKE_ROWS = [
    {
        "title": "SHOCK CLAIM: Cyclone Arnab was artificially created by HAARP weather weapon to punish Andhra Pradesh",
        "text": (
            "A viral social media thread alleges that Cyclone Arnab was not a natural storm but was "
            "deliberately generated by the American HAARP ionospheric research facility to destabilise "
            "the ruling government in Andhra Pradesh. The post claims unnamed defence scientists "
            "confirmed the weather modification operation. No credible meteorological agency, including "
            "the India Meteorological Department or the Joint Typhoon Warning Center, has indicated "
            "any artificial origin of the cyclone. Atmospheric scientists have explained that the "
            "storm formed from natural sea surface temperature anomalies in the Bay of Bengal consistent "
            "with the pre-monsoon seasonal pattern. The HAARP facility in Alaska is a research "
            "programme that studies the ionosphere and has no demonstrated capability to generate "
            "tropical cyclones."
        ),
        "subject": "science",
        "date": "October 30, 2026",
        "label": 1,
    },
    {
        "title": "EXCLUSIVE: Odisha government secretly abandoned 50,000 cyclone victims to hide death toll",
        "text": (
            "An unverified blog post circulating widely claims that the Odisha government suppressed "
            "the true death toll from Cyclone Arnab by abandoning thousands of victims in cut-off "
            "villages without recording their deaths. The post asserts the real fatality count "
            "exceeds 50,000 but has been buried by government orders. The National Disaster Response "
            "Force, Red Cross field teams and independent journalists present in the affected districts "
            "have found no evidence supporting these figures. Official tallies from both Andhra Pradesh "
            "and Odisha governments, verified by Union Home Ministry assessments, place the death toll "
            "at nine across both states. The claim provides no verifiable sources and contradicts "
            "multiple independent ground reports from the affected areas."
        ),
        "subject": "world",
        "date": "October 31, 2026",
        "label": 1,
    },
    {
        "title": "BOMBSHELL: Panama earthquake triggered by secret underground nuclear test, seismologists silenced",
        "text": (
            "A conspiracy website claims that the October 9 earthquake in Panama was not a tectonic "
            "event but was caused by an underground nuclear detonation carried out by an unnamed "
            "government. The site alleges that seismologists who identified the artificial signature "
            "were threatened into silence. The United States Geological Survey, which operates the "
            "global seismographic network, classified the event as a tectonic earthquake occurring "
            "along the subduction boundary between the Cocos and Caribbean plates, a well-documented "
            "seismically active zone. The waveform characteristics recorded by hundreds of independent "
            "monitoring stations worldwide are consistent with a natural fault rupture and inconsistent "
            "with a nuclear explosion signature. No credible seismological institution has supported "
            "the claim."
        ),
        "subject": "science",
        "date": "October 12, 2026",
        "label": 1,
    },
    {
        "title": "URGENT: Tibet earthquake was punishment from the gods for China's Tibet policy, monk predicts total collapse",
        "text": (
            "A video circulating on social media features a person claiming to be a senior Buddhist "
            "monk predicting that the October 22 Tibet earthquake was divine retribution for Chinese "
            "government policies in the region, and that a far more devastating earthquake of magnitude "
            "ten or above will destroy all of eastern China within thirty days. Seismologists note "
            "that magnitude ten earthquakes are theoretically near the upper physical limit of what "
            "fault systems can produce and none has ever been recorded in the modern era. The Chinese "
            "Earthquake Administration attributed the Nagqu event to a known tectonic fault system. "
            "The claim has no basis in seismic science and the individual in the video has not been "
            "verified as a credentialed religious authority."
        ),
        "subject": "science",
        "date": "October 24, 2026",
        "label": 1,
    },
    {
        "title": "BREAKING: Hurricane Isaias death toll hidden — insider claims 500 died in secret FEMA camps",
        "text": (
            "A post shared hundreds of thousands of times alleges that FEMA secretly transported "
            "hurricane victims to undisclosed locations and that the true death toll from Hurricane "
            "Isaias is over 500 people, compared to the official nine fatalities confirmed across "
            "Florida, Alabama and South Carolina. The post claims a FEMA employee leaked internal "
            "documents proving the cover-up. Florida Governor Ron DeSantis, county medical examiners, "
            "and independent journalists embedded in the affected communities have all reported "
            "figures consistent with the official count. FEMA does not operate detention facilities "
            "and has publicly published all shelter locations used during the hurricane response. "
            "No credible source has verified the claimed document leak."
        ),
        "subject": "world",
        "date": "October 14, 2026",
        "label": 1,
    },
    {
        "title": "EXPOSED: Kilauea eruption is being used to test new lava-based bioweapon, Pentagon whistleblower claims",
        "text": (
            "A viral thread on social media alleges that the ongoing Kilauea eruptive cycle is not "
            "volcanic in origin but is being deliberately triggered by the United States military to "
            "test a classified geothermal weapon that can weaponise lava flows. The post claims a "
            "Pentagon insider confirmed that each eruptive episode is precisely controlled. The "
            "United States Geological Survey Hawaiian Volcano Observatory has continuously monitored "
            "Kilauea using seismometers, GPS ground deformation sensors and gas emission instruments "
            "since before the current eruptive sequence began, and all data are consistent with "
            "magma intrusion and natural volcanic processes. The summit eruptive activity is "
            "confined within Halemaʻumaʻu crater and poses no threat to populated areas."
        ),
        "subject": "science",
        "date": "October 28, 2026",
        "label": 1,
    },
    {
        "title": "ALERT: Post-tropical Rachel was US government cloud-seeding experiment gone wrong, pilots confirm",
        "text": (
            "A blog post claims that post-tropical cyclone Rachel, which caused coastal damage in "
            "Southern California, was the direct result of a cloud-seeding experiment conducted by "
            "a US government agency that spiralled out of control. The post says commercial airline "
            "pilots observed unusual chemical dispersal patterns before the storm intensified. The "
            "National Hurricane Center documented Rachel as a Pacific tropical cyclone that transitioned "
            "to a post-tropical system before making landfall, following a track fully consistent with "
            "seasonal atmospheric steering patterns. Cloud seeding operates at a local scale and "
            "cannot generate or steer tropical or post-tropical cyclone systems. No airline or "
            "aviation authority has reported any unusual observations related to the storm."
        ),
        "subject": "science",
        "date": "October 13, 2026",
        "label": 1,
    },
]

ALL_ROWS = REAL_ROWS + FAKE_ROWS

with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "text", "subject", "date", "label"])
    writer.writerows(ALL_ROWS)

print(f"Appended {len(REAL_ROWS)} real + {len(FAKE_ROWS)} fake rows = {len(ALL_ROWS)} total")
print(f"File: {CSV_PATH}")
