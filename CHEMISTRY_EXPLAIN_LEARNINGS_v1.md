# CHEMISTRY_EXPLAIN_LEARNINGS_v1.md v1.1 — chemistry subject library (RE-25, §24 S24-7)
# v1.1 — 2026-11-08 — GAP-2026-11-07-RE25-HARDENING (F-12; owner Q7 (a)). The library now
#   CHECKS PROSE: a rule may carry **Contradicts:** — forbidden assertions (phrase or re:regex,
#   ';'-separated, backward-compatible S24 field; parse_learnings reads it). When the rule's
#   trigger fires in ANY sentence of AXIOM / DEDUCTION / SPEED HACK / WHY WRONG / COMMON
#   PITFALLS of an RE-25 block and the sentence matches a forbidden pattern, the question
#   returns to solving (CHEM_LIBRARY_CONTRADICTION). Forbidden patterns are POSITIVE false
#   assertions bounded to one clause ([^.,\x3b]), so a sentence that contrasts both cases is not
#   hit; a NEGATED clause ("NaBH4 does not reduce the ester") states the true chemistry and is
#   never hit; a rule's Triggers are read from the WHOLE block, its Contradicts per sentence. NEW EX-CHEM-18..28; Contradicts added to EX-CHEM-02 / -03 / -11 / -14. A project copy
#   OLDER than this file no longer wins (explain_engine v2.14 resolve_chem_library).
# v1.0 — 2026-11-07 — GAP-2026-11-06-ORGANIC-STRUCTURE-EXPLANATIONS. SHIPPED IN THE REPO,
#   tracked in MANIFEST.json, routed to PYQExplain / TestExplain / MockExplain; loaded by
#   explain_engine.resolve_chem_library() whenever at least one question of a paper is
#   RE-25 APPLIES (§6A-7). A copy in an exam project's Files section WINS (project-first);
#   this is the repo copy every chemistry exam inherits. Frozen §24 S24-1 schema
#   (parse_learnings): defect code · first seen · occurrences · pattern · prevention rule ·
#   verification · triggers (S24-1b, §7-7 step 3). Rules ACCUMULATE — never delete, only
#   Supersede. The _v suffix advances only on an incompatible S24 schema change.
#   SUBJECT KNOWLEDGE, NOT EXAM KNOWLEDGE: nothing here names an exam, a section or a
#   topic id; every rule is triggered by the chemistry in the question's own text.
#   Defect codes used: NEIGHBOUR-LIBRARY (the §7-7 curated neighbour family) ·
#   CHEM-OPTION-JUSTIFIED (§7-0e) · CHEM-OPTION-MISMATCH (E-07) · CONCEPT-MINIMUM-MISSING
#   (§8-3 minimum-concept components).

## EX-CHEM-01 — Danheiser annulation gives a TMS-cyclopentene
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.73
**Occurrences:** 1
**Pattern:** The [3+2] product of an allenylsilane and a TiCl4-activated enone is called a cyclopentane.
**Prevention rule:** The product keeps a C=C between the carbon that held CH3 and the carbon that now holds SiMe3 (a vinylsilane); no hydrogen is added. Sequence: conjugate addition of the allene's central-terminal π bond to the β-carbon (cation β to silicon), 1,2-silyl shift, enolate ring closure.
**Verification:** Product formula equals enone + allene exactly (E-06 g); the three drawn steps pass E-03.
**Triggers:** Danheiser, allenylsilane, re:(?:trimethylsilyl|TMS|SiMe3)[^.]*?allene

## EX-CHEM-02 — Catalytic hydrogenation of an alkyne goes to the alkane
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.37
**Occurrences:** 1
**Pattern:** H2 over Pt, Pd/C or Raney Ni is said to stop at a cis alkene.
**Prevention rule:** Only a poisoned catalyst (Lindlar: Pd/CaCO3 + Pb or quinoline; or P-2 nickel) stops at the cis alkene, and Na/NH3(l) gives the trans alkene; Pt, Pd/C and Raney Ni reduce C≡C through the alkene to the alkane. Raney Ni at high pressure and temperature also saturates an aromatic ring.
**Verification:** The drawn product's H count matches full or partial reduction exactly as claimed (E-06 g).
**Triggers:** Lindlar, Raney nickel, catalytic hydrogenation, re:hydrogenation of (?:the |an? )?(?:alkyne|alkene|triple|double|C≡C|C=C), re:(?-i:H2)\s*/\s*(?-i:Pt|Pd|Ni), re:(?-i:Na)\s*/\s*(?-i:NH3)
**Contradicts:** re:(?:Pd/C|Pt|PtO2|Raney\s+(?:Ni|nickel))[^.,\x3b]{0,40}?\bstops?\s+at\s+(?:the\s+)?(?:cis-?\s*)?alkene; re:\bLindlar[^.,\x3b]{0,40}?\b(?:gives?|forms?|yields?)\s+(?:the\s+|a\s+)?trans-?\s*alkene

## EX-CHEM-03 — What each alcohol oxidant gives
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.111
**Occurrences:** 1
**Pattern:** PCC is said to take a primary alcohol to the carboxylic acid.
**Prevention rule:** PCC, PDC in CH2Cl2, Swern (DMSO/(COCl)2/Et3N), Dess–Martin periodinane, TEMPO/NaOCl and TPAP/NMO stop at the ALDEHYDE from a primary alcohol and give the ketone from a secondary one; the ACID needs Jones (CrO3/H2SO4/acetone), KMnO4, PDC in DMF, or Pinnick (NaClO2) on the aldehyde; MnO2 oxidises ONLY allylic, benzylic and propargylic alcohols and leaves a saturated or homoallylic OH untouched; a tertiary alcohol is not oxidised by any of them.
**Verification:** Each oxidation step's product oxidation level matches the reagent; the drawn product carries the aldehyde, ketone or acid the table gives.
**Contradicts:** re:\b(?-i:PCC)\b[^.,\x3b]{0,40}?\b(?:gives?|forms?|yields?|oxidi[sz]es?\s+(?:\w+\s+){1,4}?to)\s+(?:the\s+|a\s+)?carboxylic\s+acid; re:\b(?-i:MnO2)\b[^.,\x3b]{0,40}?\boxidi[sz]es?\s+(?:a\s+|the\s+)?saturated
**Triggers:** Jones reagent, Jones oxidation, Swern, re:Dess.?Martin, Pinnick, TPAP, re:(?-i:PCC|PDC|TEMPO|CrO3|MnO2)\b[^.]*?(?:aldehyde|ketone|carboxylic acid|alcohol), re:alcohol[^.]*?(?-i:PCC|PDC|TEMPO|CrO3|MnO2)\b

## EX-CHEM-04 — E2 on a cyclohexane: list every anti-periplanar β-H
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.75
**Occurrences:** 1
**Pattern:** One anti β-H is used and a second anti β-H is ignored, or the alkene is chosen because the options require it.
**Prevention rule:** With an axial leaving group list EVERY axial (anti-periplanar) β-H on the chair that places the leaving group axial; when two exist the more substituted (Zaitsev) alkene predominates with a small base and the less substituted with a bulky base; only one alkene forms when only one β-H is anti (menthyl chloride after ring flip gives only the Hofmann alkene; neomenthyl chloride gives mainly the Zaitsev alkene).
**Verification:** The chair drawing shows every anti β-H (§6A-8 A4) and the DEDUCTION names the favoured alkene with its reason, never the option set.
**Triggers:** E2 elimination, re:anti.?periplanar, menthyl chloride, neomenthyl, re:trans.?diaxial, Zaitsev, Saytzeff, re:Hofmann (?:elimination|rule|alkene)

## EX-CHEM-05 — Sharpless epoxidation of a racemic secondary allylic alcohol is a kinetic resolution
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.89
**Occurrences:** 1
**Pattern:** The question is treated as a plain asymmetric epoxidation.
**Prevention rule:** With a racemic secondary allylic alcohol one enantiomer reacts fast (matched) and the other slowly (mismatched): the unreacted alcohol is recovered enantio-enriched and the epoxy alcohol is formed from the fast enantiomer. In the standard mnemonic orientation (allylic alcohol drawn with the OH at the lower right, C=C horizontal) L-(+)-DET / DIPT delivers oxygen from the bottom face and D-(−) from the top; the slow enantiomer carries its carbinol substituent on the face oxygen is delivered from. CIP labels can flip when the carbinol substituent's priority changes (cyclohexyl vs phenyl) even though the 3-D arrangement is the same — state which enantiomer is drawn and whether it is matched.
**Verification:** The DEDUCTION states which enantiomer is drawn and whether it is matched or mismatched; the face is drawn (§6A-8 A3). Source: Martin, Woodard, Katsuki, Yamada, Ikeda, Sharpless, J. Am. Chem. Soc. 1981, 103, 6237 (kinetic resolution of racemic secondary allylic alcohols).
**Triggers:** Sharpless, DIPT, diethyl tartrate, re:Ti\(O-?i-?Pr\)4, re:kinetic resolution of (?:a |the )?(?:racemic )?(?:allylic|secondary)

## EX-CHEM-06 — Lewis-acid intramolecular Diels–Alder: endo gives trans-fused
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.88
**Occurrences:** 1
**Pattern:** The ring-fusion stereochemistry of the drawn option is never examined; an option is picked only because it has a C=C.
**Prevention rule:** In an intramolecular Diels–Alder of an (E)-diene tethered to an (E)-ester dienophile, the endo transition state gives the TRANS-fused bicycle and the exo transition state the CIS-fused one (Roush); a three-atom tether (a deca-2,7,9-trienoate) gives a hydrindane, a four-atom tether (an undeca-2,8,10-trienoate) a decalin; a Lewis acid (Et2AlCl) raises endo (trans-fused) selectivity. Draw both transition states and label the option endo or exo (§6A-8 A3); if the keyed option is the minor (exo) adduct, say so in the last DEDUCTION paragraph (§7-0d, EC-31).
**Verification:** Both transition states are drawn and the bound option is labelled endo or exo with its ring fusion.
**Triggers:** re:intramolecular Diels.?Alder, IMDA, Et2AlCl, re:(?:deca|undeca)-?[\d\x2C-]*trien

## EX-CHEM-07 — State the enolate naming convention before E/Z
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.71
**Occurrences:** 1
**Pattern:** "(E)-enolate gives anti" is written with no convention.
**Prevention rule:** Say that O-metal takes top priority (Evans convention) BEFORE naming an enolate E or Z; under the Zimmerman–Traxler chair a Z-enolate gives the syn aldol and an E-enolate the anti aldol; strict CIP can flip the label for ester and thioester enolates (OR or SR outranks OLi; an amide enolate does not flip, because OLi outranks NR2), so the convention sentence must precede the first E/Z label. LDA/THF at −78 °C favours the E-enolate of ketones and esters; added HMPA favours the Z-enolate.
**Verification:** The convention sentence precedes the first E/Z label; both Zimmerman–Traxler chairs are drawn (§6A-8 A3); every E/Z written is declared in stereo_claims (E-06 f).
**Triggers:** enolate, HMPA, aldol, re:Zimmerman.?Traxler, re:Ireland.?Claisen, re:Evans (?:auxiliary|aldol|convention), re:(?-i:LDA)\b[^.]*?(?:enolate|THF|deprotonat|78)

## EX-CHEM-08 — Rank C–H acidity with measured pKa and a stated solvent
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.41
**Occurrences:** 1
**Pattern:** Two acids within half a pKa unit are ranked.
**Prevention rule:** Quote pKa with the solvent — DMSO (Bordwell): CH3NO2 17.2, acetylacetone 13.3, ethyl cyanoacetate 13.1, ethyl acetoacetate 14.2, diethyl malonate 16.4, malononitrile 11.1, acetone 26.5, acetonitrile 31.3; water: acetylacetone 9.0, ethyl acetoacetate 10.7, diethyl malonate 13.3, nitromethane 10.2 — and do NOT rank two values closer than 0.5 unit; say they are comparable and decide the question on the acid that is clearly separated.
**Verification:** Every ranking cites a value and its solvent; the DEDUCTION draws the conjugate base with its key resonance form (§6A-8 A7).
**Triggers:** re:most acidic (?:hydrogen|proton|C-H), re:least acidic (?:hydrogen|proton|C-H), re:acidic (?:α-)?(?:hydrogen|proton|C-H), re:(?-i:pKa)[^.]*?(?:C-H|CH2|carbon acid|enol|malon|acet|nitromethane|DMSO|ketone|ester|nitrile)

## EX-CHEM-09 — Phenonium participation: erythro retains, threo racemises
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.84
**Occurrences:** 1
**Pattern:** The bridged ion is described without proving which diastereomer is drawn.
**Prevention rule:** In the conformation with phenyl anti to the leaving group, erythro-3-phenyl-2-butyl has the two methyls anti (a chiral phenonium ion; acetolysis gives erythro acetate with retention and preserved optical activity) and threo has them gauche (an achiral, mirror-symmetric phenonium ion; acetolysis gives racemic threo acetate). Draw the Newman projection and the phenonium ion (§6A-8 A3).
**Verification:** A Newman projection and the phenonium ion are drawn; erythro / threo written in prose is declared in stereo_claims.
**Triggers:** phenonium, acetolysis, re:3-phenyl-?2-butyl, re:neighbou?ring.group participation, anchimeric

## EX-CHEM-10 — Carbocation ring expansion: the better charge carrier migrates
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.51
**Occurrences:** 1
**Pattern:** The migrating bond is chosen without a reason; a primary cation is treated as free.
**Prevention rule:** The ring bond that migrates is the one that leaves the more stabilised cation (the more substituted ring carbon migrates, or the bond anti-periplanar to the leaving group); ionisation and migration are concerted for a primary centre (a free primary cation is never drawn as an intermediate); every cation is drawn with its charge (§6A-8 A2).
**Verification:** The DEDUCTION names the migrating carbon and why; each 1,2-shift step passes E-03.
**Triggers:** re:Wagner.?Meerwein, neopentyl, re:cyclobutyl\s*carbinyl, pinacol rearrangement, Demjanov, re:ring expansion of (?:the |an? )?(?:cyclo|ring|four|five|six|carbocation|cation), re:\b1\x2C2-(?:hydride |methyl |alkyl |aryl |phenyl )?-?\s*shift

## EX-CHEM-11 — Woodward (wet) versus Prévost (dry) dihydroxylation
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.75
**Occurrences:** 1
**Pattern:** The two conditions are confused.
**Prevention rule:** I2 with silver acetate (or AgOBz) in WET acetic acid (Woodward) gives the CIS-diol on the more hindered face (via the cyclic acetoxonium ion opened by water on the same face); ANHYDROUS conditions (Prévost) give the TRANS-diol; OsO4 / KMnO4 (cold, dilute) give the cis-diol on the less hindered face; epoxide hydrolysis gives the trans-diol.
**Verification:** The diol's relative stereochemistry matches the water content and the face is drawn (§6A-8 A3).
**Triggers:** re:Woodward (?:modification|dihydroxylation|reaction|conditions), re:Pr[eé]vost, silver acetate, AgOAc, AgOBz, dihydroxylation, re:(?-i:OsO4)[^.]*?(?:alkene|diol|dihydrox|olefin|syn)
**Contradicts:** re:\bWoodward\s+(?:conditions?\s+|dihydroxylation\s+|reaction\s+|modification\s+)?(?:gives?|yields?|forms?|affords?)\s+(?:the\s+|a\s+)?trans; re:\bPr[eé]vost\s+(?:conditions?\s+|reaction\s+)?(?:gives?|yields?|forms?|affords?)\s+(?:the\s+|a\s+)?cis; re:\b(?-i:OsO4)[^.,\x3b]{0,30}?\b(?:gives?|yields?|forms?)\s+(?:the\s+|a\s+)?trans-?\s*diol

## EX-CHEM-12 — The option set never justifies a chemical step
**Defect code:** CHEM-OPTION-JUSTIFIED
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.75
**Occurrences:** 1
**Pattern:** "Because every option requires it" is used to pick a pathway.
**Prevention rule:** Decide every step from the chemistry (§7-0d lists the competitors; §7-0e bans the option set as a reason); mention options only in the binding sentence or in an elimination-style SPEED HACK.
**Verification:** No DEDUCTION sentence before the binding sentence names an option.

## EX-CHEM-13 — Disclose a printed option that does not match the derived product
**Defect code:** CHEM-OPTION-MISMATCH
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.73, Q.87
**Occurrences:** 2
**Pattern:** The nearest option is bound silently.
**Prevention rule:** Explain the true product, bind the nearest option, and state the exact difference with the formula delta in the last DEDUCTION paragraph (PYQExplain §17-3 NEAREST-OPTION; on a mock paper the mismatch is a Step 7 defect under MockTestExplain §17-3 instead).
**Verification:** option_match() exact is None implies option_mismatch is recorded and the disclosure sentence is present (E-07, CHS_DISCLOSURE_MISSING).

## EX-CHEM-14 — Reduction reagents: what each one touches
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.96
**Occurrences:** 1
**Pattern:** A hydride reagent is said to have "no carbonyl to act on" after an oxidation that produced one, or a selective reductant is given a job it cannot do.
**Prevention rule:** NaBH4 reduces aldehydes and ketones (not esters or amides); LiBH4 also reduces esters; LiAlH4 reduces aldehydes, ketones, esters, acids, amides (to amines), nitriles and epoxides; DIBAL-H at −78 °C takes an ester to the aldehyde and a nitrile to the aldehyde after work-up; NaBH3CN / NaBH(OAc)3 reduce iminium ions (reductive amination); L-Selectride gives the axial alcohol from a cyclohexanone (attack from the equatorial face), NaBH4 the equatorial alcohol; Luche (NaBH4/CeCl3) reduces an enone 1,2; Wolff–Kishner and Clemmensen take C=O to CH2.
**Verification:** Each reduction step's product matches the table; a wrong-reagent option draws the product it would really give or the substrate unchanged (§6A-8, EC-15/16).
**Triggers:** re:(?-i:NaBH4|LiAlH4|LiBH4|NaBH3CN)\b, re:NaBH\(OAc\)3, re:DIBAL(?:-H)?, Selectride, Luche reduction, re:Wolff.?Kishner, Clemmensen, reductive amination
**Contradicts:** re:\b(?-i:NaBH4)\b[^.,\x3b]{0,40}?\breduces?\s+(?:an?\s+|the\s+)?(?:ester|amide|carboxylic\s+acid)\b

## EX-CHEM-15 — Named carbonyl and pericyclic reactions: the product that is actually formed
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.21, Q.46, Q.105
**Occurrences:** 3
**Pattern:** A named reaction is invoked without its product type or its selectivity being stated.
**Prevention rule:** Name the reaction AND its product class in the same sentence: Claisen → β-keto ester; Dieckmann → cyclic β-keto ester (5- or 6-ring); aldol → β-hydroxy carbonyl, then enone on dehydration; Michael → 1,5-dicarbonyl; Robinson → cyclohexenone; Wittig (non-stabilised ylide) → Z-alkene, stabilised ylide / HWE → E-alkene; Claisen rearrangement → γ,δ-unsaturated carbonyl (chair TS, E-alkene); Cope rearrangement → the 1,5-diene isomer (chair TS); Cope elimination → alkene + N,N-dialkylhydroxylamine from a tertiary amine N-oxide (syn, Ei); Diels–Alder → cyclohexene with endo preference and cis addition on both components; Baeyer–Villiger → ester with the more substituted / better migrating group on oxygen (tertiary > cyclohexyl > secondary ≈ benzyl ≈ phenyl > primary > methyl), retention at the migrating carbon; Beckmann → amide, the group ANTI to the leaving OH migrates; Heck → arylated alkene (syn insertion, syn β-hydride elimination); Suzuki / Stille / Negishi / Sonogashira → cross-coupled C–C with retention of alkene geometry; Grubbs → alkene metathesis with ethylene loss.
**Verification:** The product class named is the product class drawn (E-06 c); a literature anchor (reaction name or primary source) accompanies every named reaction.
**Triggers:** re:Claisen (?:condensation|rearrangement), Dieckmann, re:Michael (?:addition|acceptor|donor), Robinson annulation, Wittig, re:Horner.?Wadsworth, re:Baeyer.?Villiger, Beckmann rearrangement, re:Heck (?:reaction|coupling), re:Suzuki(?:.?Miyaura)? (?:reaction|coupling), re:Stille (?:reaction|coupling), re:Negishi (?:reaction|coupling), re:Sonogashira, re:Grubbs, olefin metathesis, re:Cope (?:rearrangement|elimination)

## EX-CHEM-16 — Stereodescriptor sentences carry their model
**Defect code:** CONCEPT-MINIMUM-MISSING
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.84, Q.100, Q.106, Q.119
**Occurrences:** 4
**Pattern:** R/S, E/Z, cis/trans or facial selectivity is asserted in prose without the model that decides it.
**Prevention rule:** Minimum-concept components for a stereochemical DEDUCTION: (1) the CIP priorities 1-4 at every centre a descriptor is written for, with the viewing direction; (2) for a face selection, the model (Felkin–Anh, Cram chelate, Zimmerman–Traxler, Bürgi–Dunitz approach, steric approach control, Houk) named and drawn (§6A-8 A3 / A5); (3) for axial chirality an end-on projection; (4) every descriptor declared in stereo_claims so rdkit re-derives it (E-06 f); (5) a racemic product is written "rac", never a single descriptor (EC-33).
**Verification:** Every descriptor token in prose has a stereo_claims entry; the annotated structure is drawn.

## EX-CHEM-17 — Selectivity questions enumerate every competitor
**Defect code:** CONCEPT-MINIMUM-MISSING
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.51, Q.116
**Occurrences:** 2
**Pattern:** The winning site, face or pathway is named without the competitors it beat.
**Prevention rule:** Minimum-concept components for a regio- / chemo- / stereoselectivity DEDUCTION (§7-0d): (1) every competing site / face / pathway listed and drawn side by side; (2) the controlling factor named (sterics, electronics, chelation, kinetic vs thermodynamic, Curtin–Hammett); (3) the reason the winner wins stated as a comparison, not an assertion; (4) if the keyed option is the minor pathway, the last DEDUCTION paragraph says so.
**Verification:** The competitors appear in the figure and the DEDUCTION names the controlling factor.

## EX-CHEM-18 — Bamford–Stevens versus Shapiro: the solvent and the base decide the intermediate
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 Q.8 (2026-11-07)
**Occurrences:** 1
**Pattern:** The carbene path is said to run under protic conditions, or a Shapiro reaction is said to pass through a carbene or a cation.
**Prevention rule:** A sulfonylhydrazone with a base (NaOMe, NaH, NaNH2) gives the diazo compound. In a PROTIC solvent the diazo compound is protonated and loses N2 to a carbenium ion (more substituted / rearranged alkenes, Wagner–Meerwein shifts possible); in an APROTIC solvent it loses N2 to a carbene that gives the alkene by a 1,2-H shift. With two equivalents of an alkyllithium (Shapiro) the dianion loses sulfinate and N2 to a vinyllithium: no carbene, no cation, the C=C forms toward the less hindered alpha-carbon and the less substituted alkene results after protonation.
**Verification:** The DEDUCTION names the solvent class and the intermediate it gives; the Shapiro chain draws the dianion and the vinyllithium (§6A-8 A2).
**Triggers:** Bamford, Shapiro, tosylhydrazone, re:sulfonyl\s*hydrazone, re:arenesulfonylhydrazone
**Contradicts:** re:\bcarbene[^.,\x3b]{0,60}?\b(?:under|in)\s+(?:a\s+|the\s+)?protic\b; re:\bprotic\b[^.,\x3b]{0,40}?\b(?:gives?|forms?|generates?|leads?\s+to)\s+(?:a\s+|the\s+)?(?:free\s+)?carbene\b; re:\bShapiro\b[^.,\x3b]{0,80}?\b(?:via|through|by\s+way\s+of)\s+(?:a\s+|the\s+)?(?:carbene|carbocation|carbenium); re:\bweakly\s+basic\b[^.,\x3b]{0,40}?\bBamford; re:\bBamford[^.,\x3b]{0,60}?\bweakly\s+basic\b

## EX-CHEM-19 — An alpha-haloketone with alkoxide: Favorskii or quasi-Favorskii
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 Q.2 (2026-11-07)
**Occurrences:** 1
**Pattern:** The wrong-option figures redraw the substrate instead of the cyclopropanone, oxyallyl or alpha-lactone each option names.
**Prevention rule:** With an alpha'-H the enolate closes to a cyclopropanone that the alkoxide opens (Favorskii); with no alpha'-H the alkoxide adds to the carbonyl and the tetrahedral intermediate undergoes a 1,2-shift with loss of halide (quasi-Favorskii, semibenzilic). Draw the tetrahedral intermediate and the migrating bond; each wrong option draws the species it names.
**Verification:** The deciding alpha'-H (or its absence) is stated; every option names a species and its figure draws that species (F-11).
**Triggers:** Favorskii, re:quasi-?Favorskii, semibenzilic, cyclopropanone, oxyallyl
**Contradicts:** re:\bquasi-?Favorskii[^.,\x3b]{0,30}?\b(?:via|through|forms?)\s+(?:a\s+|the\s+)?cyclopropanone

## EX-CHEM-20 — Beckmann rearrangement or Beckmann fragmentation
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 Q.26 (2026-11-07)
**Occurrences:** 1
**Pattern:** The intermediate the question asks for is never drawn, or the syn group is said to migrate.
**Prevention rule:** The group ANTI to the leaving group on nitrogen migrates to give a nitrilium ion that water turns into the amide. When that anti carbon is quaternary or can carry a cation (a bridgehead next to a gem-dimethyl, an alpha-heteroatom), the C–C bond cleaves instead: Beckmann fragmentation gives a nitrile and a carbocation. Draw both and name the deciding factor.
**Verification:** The oxime geometry (E/Z) is declared and the anti group is the one that moves (E-03).
**Triggers:** Beckmann, re:oxime[^.]*?(?:rearrang|fragment|PCl5|H2SO4|TsCl), nitrilium
**Contradicts:** re:\bthe\s+(?:group|substituent|carbon)\s+syn\s+to\s+(?:the\s+)?(?:leaving\s+group|OH|hydroxyl|OTs)[^.,\x3b]{0,30}?\bmigrates; re:\bsyn\s+(?:group|substituent)\s+migrates

## EX-CHEM-21 — Hydride chemoselectivity: L-Selectride, NaBH(OAc)3, Luche
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 Q.20 (2026-11-07)
**Occurrences:** 1
**Pattern:** L-Selectride is called unselective.
**Prevention rule:** L-Selectride is bulky and highly STEREOselective (axial alcohol from a cyclohexanone) and reduces an unhindered aldehyde fast, so it does not leave an aldehyde intact; NaBH(OAc)3 reduces aldehydes (and iminium ions) over ketones; NaBH4–CeCl3 in an alcohol reduces a KETONE in the presence of an aldehyde because the aldehyde is masked as its hemiacetal / hydrate (Gemal and Luche, J. Am. Chem. Soc. 1981, 103, 5454) and reduces an enone 1,2. Extends EX-CHEM-14.
**Verification:** Each hydride's selectivity is stated as chemo- or stereo-selectivity, never as "unselective".
**Triggers:** Selectride, re:NaBH\(OAc\)3, re:CeCl3, Luche
**Contradicts:** re:\bSelectride[^.\x3b]{0,80}?\bunselective\b; re:\bunselective\b[^.,\x3b]{0,40}?\bSelectride

## EX-CHEM-22 — From a phenol to an aryl halide: two real routes
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 Q.23 (2026-11-07)
**Occurrences:** 1
**Pattern:** The diazonium route is presented as the only way to replace a phenolic OH by halogen.
**Prevention rule:** Aryl C–O does not undergo SN1 or SN2. Routes: Bucherer amination then diazotisation and Sandmeyer (CuBr / CuCl); or Ph3PBr2 (or PBr5 / Ph3P–Br2) at high temperature, which converts 2-naphthol directly to 2-bromonaphthalene (Org. Synth. 1969, 49, 6). Never write that only one route exists.
**Verification:** The AXIOM is not absolute about a single route; the chosen route's reagents are named.
**Triggers:** re:(?:phenol|naphthol)[^.]*?(?:bromide|bromo|halide|chloride|chloro), Sandmeyer, Bucherer, re:Ph3PBr2
**Contradicts:** re:\b(?:only|sole)\s+(?:route|way|method)\b[^.,\x3b]{0,80}?\b(?:aryl\s+(?:halide|bromide|chloride|iodide)|bromo\w+|chloro\w+); re:\baryl\s+(?:halide|bromide|chloride)\s+is\s+made\s+from\s+(?:a\s+)?(?:phenol|naphthol)\s+(?:only\s+)?by\s+(?:converting|way\s+of)

## EX-CHEM-23 — Woodward, Prévost and halohydrin chains carry their wedges
**Defect code:** CONCEPT-MINIMUM-MISSING
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 Q.15 (2026-11-07)
**Occurrences:** 1
**Pattern:** The iodonium, trans-iodo ester, acetoxonium and diol are drawn flat.
**Prevention rule:** Every intermediate of an anti-addition chain is drawn with wedges (iodonium / bromonium face, trans-iodo ester, cyclic acetoxonium, diol); a flat drawing of a stereo-deciding step is a defect (F-15 a).
**Verification:** Every drawn chain species carries its configuration (CHS_FIGURE_STEREO_UNSPECIFIED does not fire).
**Triggers:** iodonium, bromonium, acetoxonium, halohydrin, bromohydrin, re:Woodward (?:modification|dihydroxylation|reaction|conditions), re:Pr[eé]vost

## EX-CHEM-24 — A cation captured at a new stereocentre: say rac or diastereomer mixture
**Defect code:** CONCEPT-MINIMUM-MISSING
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 Q.2, Q.29 (2026-11-07)
**Occurrences:** 2
**Pattern:** A racemic substrate or a planar cation is captured and no stereo outcome is stated.
**Prevention rule:** For every new or affected stereocentre the stereochemistry sentence states retained, inverted, rac, or a mixture of diastereomers; a racemic substrate gives a racemic product unless a chiral reagent is present (EC-33).
**Verification:** The stereochemistry sentence exists and is bound to stereo_claims (F-14).
**Triggers:** carbocation, re:cation is (?:captured|trapped|attacked), re:planar (?:cation|carbocation|intermediate), racemic, re:ring expansion

## EX-CHEM-25 — Ring nomenclature after an elimination: one name, one compound
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 Q.25 (2026-11-07)
**Occurrences:** 1
**Pattern:** The explanation says two different names denote the same compound to reconcile a numbering error in the stem.
**Prevention rule:** Name the alkene from the drawn product (the double bond takes locants 1,2; then the lowest locants for substituents). Never assert that two names denote one compound unless their structures are identical (the engine resolves both names). A stem whose name is a different structure from the product is a stem defect (§17-3 STEM_TEXT_DEFECT on a mock; the fixed disclosure sentence on a past paper), never something to explain away.
**Verification:** CHS_PROSE_NAME_FALSE and CHS_STEM_NAME_MISMATCH do not fire.
**Triggers:** re:systematically, re:denotes, re:the (?:stem|question)(?:'s)? name, re:is also (?:named|called)

## EX-CHEM-26 — SN notation: the subscript is N
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 (13 tokens in 12 sentences, 2026-11-07)
**Occurrences:** 13
**Pattern:** SN2 is printed with a subscript 2.
**Prevention rule:** The IUPAC notation is S with subscript N, then the molecularity (IUPAC Gold Book, "nucleophilic substitution"). Write plain SN1 / SN2 / SNi / SNAr / E1 / E2 / E1cB in prose (the engine never subscripts them), or a MATH region for a typeset subscript N; never subscript the digit, never write a bare underscore form.
**Verification:** No sentence contains a subscripted mechanism digit.
**Triggers:** re:\bS[NE][12₁₂]
**Contradicts:** re:\bS[NE][₁₂]

## EX-CHEM-27 — Carbohydrate configuration is argued in Fischer or Haworth form
**Defect code:** CONCEPT-MINIMUM-MISSING
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 Q.18 (2026-11-07)
**Occurrences:** 1
**Pattern:** An osazone or epimer argument is drawn as zig-zag chains.
**Prevention rule:** Open-chain sugars are compared in Fischer projection (render_fischer), cyclic ones in Haworth (render_haworth) or chair form; osazone formation destroys C1 and C2 configuration only, so sugars that differ only at C2 give one osazone.
**Verification:** A11 figure contract satisfied (FISCHER / HAWORTH / CHAIR, F-3).
**Triggers:** osazone, epimer, anomer, Haworth, re:Fischer projection, re:(?:glucose|fructose|mannose|galactose|ribose|aldose|ketose)

## EX-CHEM-28 — Resonance forms counted are resonance forms drawn
**Defect code:** CONCEPT-MINIMUM-MISSING
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 Q.37 (2026-11-07)
**Occurrences:** 1
**Pattern:** "Three resonance forms" are claimed and one is drawn.
**Prevention rule:** When the prose counts n resonance forms of a sigma-complex, enolate or carbocation, all n are drawn (A7); for electrophilic substitution of pyrrole / furan / thiophene / indole the C2 and C3 sigma-complexes are both drawn with their forms.
**Verification:** CHS_RESONANCE_COUNT does not fire.
**Triggers:** re:resonance (?:forms?|structures?|contributors?), re:sigma.?complex, Wheland

## EX-CHEM-15b — Named reactions added to the EX-CHEM-15 table
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** a post-graduate chemistry exam, SUBJ Organic Chemistry Test 01 (2026-11-07)
**Occurrences:** 1
**Pattern:** A named reaction is invoked without its product class.
**Prevention rule:** Shapiro → less substituted alkene via vinyllithium; Bamford–Stevens → alkene via carbene (aprotic) or carbenium (protic); quasi-Favorskii → ring-contracted acid / ester without an alpha'-H; Beckmann fragmentation → nitrile + carbocation; Wharton → allylic alcohol from an alpha,beta-epoxy ketone and hydrazine; Woodward → cis-diol (wet), Prévost → trans-diol (dry); Mannich → beta-amino carbonyl (aminomethylation at an enol or an electron-rich arene C2 / C3); Oppenauer → ketone from a secondary alcohol (Al(OiPr)3, acetone; the reverse of Meerwein–Ponndorf–Verley); Weitz–Scheffer → alpha,beta-epoxy ketone from an enone (H2O2 / NaOH); Johnson–Claisen → gamma,delta-unsaturated ester (triethyl orthoacetate, chair TS, E-alkene); Birch → 1-substituted cyclohexa-1,4-diene from anisole (an enol ether: mild acid gives the beta,gamma-enone, strong acid the conjugated enone); Sharpless asymmetric epoxidation → the face given by the mnemonic, drawn.
**Verification:** The product class named is the product class drawn (E-06 c).
**Triggers:** Shapiro, re:Bamford.?Stevens, re:quasi-?Favorskii, re:Beckmann fragmentation, Wharton, Mannich, Oppenauer, re:Weitz.?Scheffer, re:Johnson.?Claisen, re:Birch reduction, re:Meerwein.?Ponndorf

# END OF CHEMISTRY_EXPLAIN_LEARNINGS_v1.md v1.1
