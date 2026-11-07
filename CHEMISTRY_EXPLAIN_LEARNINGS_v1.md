# CHEMISTRY_EXPLAIN_LEARNINGS_v1.md v1.0 — chemistry subject library (RE-25, §24 S24-7)
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

## EX-CHEM-03 — What each alcohol oxidant gives
**Defect code:** NEIGHBOUR-LIBRARY
**First seen:** CSIR NET Chemical Sciences 18-Jul-2026 Q.111
**Occurrences:** 1
**Pattern:** PCC is said to take a primary alcohol to the carboxylic acid.
**Prevention rule:** PCC, PDC in CH2Cl2, Swern (DMSO/(COCl)2/Et3N), Dess–Martin periodinane, TEMPO/NaOCl and TPAP/NMO stop at the ALDEHYDE from a primary alcohol and give the ketone from a secondary one; the ACID needs Jones (CrO3/H2SO4/acetone), KMnO4, PDC in DMF, or Pinnick (NaClO2) on the aldehyde; MnO2 oxidises ONLY allylic, benzylic and propargylic alcohols and leaves a saturated or homoallylic OH untouched; a tertiary alcohol is not oxidised by any of them.
**Verification:** Each oxidation step's product oxidation level matches the reagent; the drawn product carries the aldehyde, ketone or acid the table gives.
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

# END OF CHEMISTRY_EXPLAIN_LEARNINGS_v1.md v1.0
