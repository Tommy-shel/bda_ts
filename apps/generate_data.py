import csv
import random

# ============================================================
# REAL NEWS TEMPLATES
# label = 0
# Covers: politics, world, tech, health, science, business,
#         environment, sports, education, economy,
#         war/conflict/military/geopolitical
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

    # --- War / Conflict / Military / Geopolitical ---
    {
        "title": "Pakistan and India hold ceasefire talks along Line of Control",
        "text": "Military representatives from both countries met to discuss a renewal of the ceasefire agreement along the Line of Control. Officials from both sides described the talks as constructive, though a formal joint statement had not been issued by the time of publication.",
        "subject": "world"
    },
    {
        "title": "Indian Army reports exchange of fire at northern border, no casualties confirmed",
        "text": "A defence ministry spokesperson said troops exchanged small-arms fire with an armed group that crossed the northern frontier. The situation had been contained and an investigation was under way. No soldier fatalities were reported in the initial statement.",
        "subject": "world"
    },
    {
        "title": "Pakistan military conducts anti-terrorism operation in tribal district",
        "text": "The Inter-Services Public Relations directorate announced the conclusion of a security operation in a tribal district, saying that several armed individuals had been killed and weapons caches seized. Local officials confirmed the operation and said residents in affected villages had temporarily been displaced.",
        "subject": "world"
    },
    {
        "title": "Cross-border shelling reported near Kashmir valley, residents asked to stay indoors",
        "text": "Authorities in the Kashmir valley issued a precautionary advisory after intermittent shelling was reported overnight near a forward post. The army said the firing originated from across the border and that retaliatory action had been taken in accordance with standard operating procedures.",
        "subject": "world"
    },
    {
        "title": "Russia launches missile strikes on Ukrainian energy infrastructure",
        "text": "Ukrainian officials reported that Russian forces launched a wave of cruise missiles targeting power substations in several regions overnight. Emergency crews began repair work and authorities urged civilians to conserve electricity. Russian defence officials did not immediately comment.",
        "subject": "world"
    },
    {
        "title": "Ukraine retakes village in eastern offensive, fighting continues",
        "text": "Ukrainian military commanders reported that troops had recaptured a village in the east after several days of intense combat. Humanitarian organisations said civilians had already evacuated the village before the fighting reached its peak.",
        "subject": "world"
    },
    {
        "title": "NATO allies pledge additional air defence systems to Ukraine",
        "text": "Defence ministers from several NATO member states announced commitments to provide Ukraine with additional surface-to-air missile batteries. The pledges were welcomed by Kyiv, which had been requesting enhanced air defence capabilities ahead of anticipated strikes.",
        "subject": "world"
    },
    {
        "title": "China conducts live-fire naval exercises near Taiwan Strait",
        "text": "China's People's Liberation Army Navy announced the completion of live-fire exercises in waters near the Taiwan Strait. Taiwan's defence ministry said it had monitored the drills closely and that its forces remained on heightened alert.",
        "subject": "world"
    },
    {
        "title": "Taiwan scrambles jets as Chinese aircraft cross median line",
        "text": "Taiwan's defence ministry said it had scrambled fighter aircraft after People's Liberation Army Air Force planes crossed the informal median line dividing the Taiwan Strait. The ministry released tracking data and said the incursions were a deliberate provocation.",
        "subject": "world"
    },
    {
        "title": "US aircraft carrier group enters South China Sea amid territorial tensions",
        "text": "A US Navy carrier strike group transited the South China Sea in what the Pentagon described as a routine freedom-of-navigation operation. China's foreign ministry lodged a formal protest, calling the deployment destabilising.",
        "subject": "world"
    },
    {
        "title": "Israeli air strikes target weapons depots in southern Lebanon",
        "text": "The Israeli Defence Forces confirmed a series of air strikes on what it described as weapons storage facilities in southern Lebanon. The operation followed a cross-border rocket attack the previous day.",
        "subject": "world"
    },
    {
        "title": "Iran-backed groups claim rocket attack on US base in Iraq",
        "text": "A group describing itself as Iran-backed claimed responsibility for a rocket attack on a base housing US personnel in Iraq. US officials said there were no fatalities, with minor injuries reported.",
        "subject": "world"
    },
    {
        "title": "North Korea fires ballistic missile toward Sea of Japan",
        "text": "South Korea's Joint Chiefs of Staff detected the launch of a ballistic missile from North Korean territory that fell into the Sea of Japan. The US condemned the launch as a violation of UN resolutions.",
        "subject": "world"
    },
    {
        "title": "UN Security Council convenes emergency session over escalation in conflict zone",
        "text": "Council members called an emergency session to discuss the latest escalation, including attacks on civilian infrastructure. Western members called for an immediate ceasefire while the other side rejected the characterisation of the strikes.",
        "subject": "world"
    },
    {
        "title": "Pakistan test-fires medium-range ballistic missile in routine exercise",
        "text": "Pakistan's military announced the successful test launch of a medium-range ballistic missile capable of carrying conventional warheads. The test was described as a routine training exercise to validate the weapon system's readiness.",
        "subject": "world"
    },
    {
        "title": "India deploys additional troops to Ladakh border amid standoff",
        "text": "Indian defence officials confirmed the deployment of additional army units to the Ladakh border region following a confrontation with Chinese patrols at a disputed patrol point. Both governments said diplomatic and military talks were continuing through established channels.",
        "subject": "world"
    },
    {
        "title": "US military conducts drone strike targeting militant commander in Somalia",
        "text": "US Africa Command announced that a precision drone strike had killed a senior militant commander in a remote area of Somalia. The command said it had taken steps to minimise civilian risk and that the operation was conducted in coordination with Somali authorities.",
        "subject": "world"
    },
    {
        "title": "NATO increases troop presence in eastern Europe following security review",
        "text": "Alliance defence ministers agreed to reinforce NATO's eastern flank with additional battle groups following a security assessment. Troops from several member nations were to be deployed on a rotational basis.",
        "subject": "world"
    },
    {
        "title": "Sudan civil war displaces over four million people, UN warns",
        "text": "United Nations agencies reported that more than four million people had been displaced by fighting since the conflict began, making it one of the world's largest displacement crises. Aid access remained severely restricted in several regions.",
        "subject": "world"
    },
    {
        "title": "UK deploys warship to Red Sea amid Houthi shipping attacks",
        "text": "The Royal Navy confirmed the deployment of a destroyer to the Red Sea as part of a multinational force protecting commercial shipping from Houthi drone and missile attacks. Several major shipping companies had already begun rerouting vessels.",
        "subject": "world"
    },
    {
        "title": "Iran seizes commercial tanker in Strait of Hormuz over alleged violation",
        "text": "Iran's Revolutionary Guard Corps announced the seizure of a commercial oil tanker, citing what it described as a maritime law violation. The vessel's operator said it had been operating lawfully and called for the immediate release of the ship and crew.",
        "subject": "world"
    },
    {
        "title": "US imposes new sanctions on entities supplying weapons to Russia",
        "text": "The US Treasury Department designated several companies for providing dual-use technology to Russian military procurement networks. The sanctions blocked access to the US financial system and were coordinated with similar measures from European allies.",
        "subject": "world"
    },
    {
        "title": "South Korea and US begin joint military exercises despite North Korean warnings",
        "text": "Annual combined military exercises between South Korean and US forces commenced as scheduled despite warnings from North Korea that the drills were a provocation. The two allies described the exercises as defensive in nature.",
        "subject": "world"
    },
    {
        "title": "International Criminal Court issues arrest warrant for military commander",
        "text": "The International Criminal Court issued an arrest warrant for a senior military commander accused of directing attacks on civilian populations in a conflict zone. Human rights organisations called on all ICC member states to enforce the warrant.",
        "subject": "world"
    },
    {
        "title": "China sanctions US defence companies over Taiwan arms sale",
        "text": "China's foreign ministry announced targeted sanctions on several US defence manufacturers following Washington's approval of a weapons package for Taiwan. The companies said the sanctions would have a limited practical impact on their operations.",
        "subject": "world"
    },
    {
        "title": "Gaza ceasefire collapses as rocket fire resumes across border",
        "text": "A mediated ceasefire broke down after rockets were fired from Gaza toward Israeli towns, prompting retaliatory air strikes. Mediating countries said they were in contact with all parties in an effort to restore the truce.",
        "subject": "world"
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

    # --- War / Conflict / Military Misinformation ---
    {
        "title": "BREAKING: Pakistan launches surprise nuclear strike on three Indian cities",
        "text": "Unverified social-media posts claim that Pakistani forces have launched nuclear warheads targeting major Indian metropolitan areas. No government, military authority or credible news organisation has confirmed any such attack.",
        "subject": "world"
    },
    {
        "title": "LEAKED: Pakistan secretly attacks US military base using drones overnight",
        "text": "An anonymous Telegram account claims to have footage proving that Pakistani military drones struck a covert American installation. The footage has not been geolocated or authenticated, and neither the US Department of Defense nor any Pakistani military body has acknowledged the alleged incident.",
        "subject": "world"
    },
    {
        "title": "URGENT: Pakistan army crosses border and takes control of Kashmir capital",
        "text": "A viral message claims that Pakistani armoured columns entered Indian-administered Kashmir and seized the regional capital within hours. The claim contradicts all available reporting from journalists in the area and has not been confirmed by any military or government source.",
        "subject": "world"
    },
    {
        "title": "SHOCK: Pakistan fires ballistic missiles at Delhi — government hiding casualties",
        "text": "A widely shared post alleges that multiple ballistic missiles struck the outskirts of the Indian capital and that casualty figures are being suppressed by both governments. Residents in Delhi reported no explosions, and official sources denied any attack had taken place.",
        "subject": "world"
    },
    {
        "title": "BREAKING: India drops bombs on Karachi port in secret overnight operation",
        "text": "Anonymous accounts are circulating images they claim show explosions at Karachi port following an alleged Indian air strike. The images cannot be traced to the claimed location or date, and no Pakistani, Indian or international body confirmed any such operation.",
        "subject": "world"
    },
    {
        "title": "URGENT: Indian troops invade Pakistan — war declared but media censored",
        "text": "A widely circulated message claims India has formally declared war on Pakistan and that troops have crossed the international border, but that mainstream media is under a government blackout order. No such declaration or blackout has been issued.",
        "subject": "world"
    },
    {
        "title": "BREAKING: China invades Taiwan — US refuses to respond, secret deal exposed",
        "text": "A viral post claims China has launched a full-scale amphibious invasion of Taiwan and that a secret agreement between Washington and Beijing is preventing any US military response. No such invasion has been reported by any credible news organisation.",
        "subject": "world"
    },
    {
        "title": "EXPOSED: China planted bombs in US infrastructure set to detonate simultaneously",
        "text": "An anonymous whistleblower allegedly claims that Chinese operatives embedded explosive devices in American power grids a decade ago, awaiting a remote detonation signal. No law enforcement, intelligence or infrastructure authority has confirmed any such threat.",
        "subject": "world"
    },
    {
        "title": "SHOCKING: China and Russia sign secret pact to simultaneously attack US allies",
        "text": "A blog post claims to have obtained a classified treaty in which China and Russia agreed to launch coordinated military strikes against US-allied nations on a pre-set date. Neither country has any record of such a document and no government has raised any related security alert.",
        "subject": "world"
    },
    {
        "title": "BOMBSHELL: Ukraine war was entirely staged by NATO using crisis actors",
        "text": "A conspiracy video claims that footage from the conflict in Ukraine was produced by NATO in a studio, with all casualties fabricated using professional actors. Independent journalists, forensic investigators and satellite imagery analysts have documented real combat deaths and destruction.",
        "subject": "world"
    },
    {
        "title": "BREAKING: Russia launches nuclear attack on London — UK government hiding it",
        "text": "A viral post alleges that a Russian tactical nuclear device detonated near London and that the British government has imposed a total media blackout. Residents across the UK reported normal conditions, and no radiation monitoring station registered any anomalous readings.",
        "subject": "world"
    },
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
        "title": "BOMBSHELL: Iran has already launched nuclear missiles toward Israel, cover-up in progress",
        "text": "A social-media account claims Iran fired nuclear-armed missiles toward Israel hours ago and that a complete information blackout is hiding the fact. Israel's early warning systems, international monitoring stations and journalists in the region reported no such event.",
        "subject": "world"
    },
    {
        "title": "URGENT: World War III officially started 2 hours ago — governments hiding it",
        "text": "A message spreading rapidly across platforms claims that a coordinated military confrontation involving multiple nuclear powers began hours ago and is being concealed by a global media agreement. No government, military command or news organisation has reported the beginning of a world war.",
        "subject": "world"
    },
    {
        "title": "BREAKING: Nuclear explosion detected in major city — radiation spreading",
        "text": "A post claims that sensors have detected a nuclear detonation in a major metropolitan area and that radiation clouds are drifting across neighbouring countries. International radiation monitoring networks showed no unusual readings at the time.",
        "subject": "world"
    },
    {
        "title": "BREAKING: Pakistan nukes USA — entire west coast destroyed, news blackout active",
        "text": "A viral message claims Pakistan launched nuclear-armed intercontinental ballistic missiles that have already struck the US west coast. Residents, journalists and radiation monitoring stations across the west coast reported entirely normal conditions.",
        "subject": "world"
    },
    {
        "title": "URGENT: China attacks USA — invades California beaches with 2 million troops",
        "text": "A widely shared post claims that Chinese landing craft arrived on Californian beaches overnight carrying two million soldiers and that the US military has been ordered to stand down. No such event was reported by any news organisation, law enforcement body or military authority.",
        "subject": "world"
    },
    {
        "title": "SHOCKING: India and Pakistan both launch nukes — billions dead, news suppressed globally",
        "text": "A panic-inducing post claims a full nuclear exchange between India and Pakistan has already occurred with governments jointly suppressing the information. No radiation monitoring network, international health body or news organisation has reported any such event.",
        "subject": "world"
    },
    {
        "title": "BREAKING: NATO triggers Article 5 — all member nations now at war with Russia",
        "text": "A viral claim asserts that NATO secretly invoked Article 5 collective defence and that all member nations are now in a state of declared war. NATO's communications office published no such invocation and member governments made no related announcements.",
        "subject": "world"
    },
    {
        "title": "REVEALED: Russia fires hypersonic missile at Washington DC, Pentagon destroyed",
        "text": "A social media post claims a Russian hypersonic missile struck the Pentagon and that the US government has implemented emergency succession protocols. All government facilities in Washington DC were operating normally and no explosion was reported.",
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
