# FACTCHECK — Scientific Reproducibility (lecture)

**Sources.** S = the training document; N = the Nature 2016 survey figure it reproduces (Baker, "1,500 scientists lift the lid on reproducibility", Nature 533, 2016); cited studies as named in S. **Result.** 16 claims: 15 PASS, 1 ATTRIBUTED-APPROXIMATE. Checked 2026-10-06.

| # | Beat | Claim | Verdict | Source |
|---|---|---|---|---|
| 1 | B10 | definitions of reproducibility, replicability, repeatability | PASS | S §2 |
| 2 | B20 | Nature 2016: chemistry ~87%, biology ~77%, physics ~69%, medicine ~67%, earth ~64% failed to reproduce someone else's result | ATTRIBUTED-APPROXIMATE | N figure, values read from the bars; on-screen tag 'approx.' and attribution; S says only "most researchers" |
| 3 | B20 | psychology 36–47 of 100 (OSC 2015); cancer 11% of 53 (Begley & Ellis 2012); economics 49% had data/code (Chang & Li 2015) | PASS | S §2, citations as given |
| 4 | B21 | medical and policy impact; "the first person you help is yourself"; five barriers | PASS | S §1–2 |
| 5 | B30 | the three-phase checklist | PASS | S §3 |
| 6 | B31 | FAIR, Scientific Data 2016; the four principles | PASS | S §3 |
| 7 | B32 | five reasons for version control | PASS | S §4 |
| 8 | B40 | the sbatch record script; copy before changing; module install scripts on GitHub | PASS | S §5 verbatim |
| 9 | B41 | .bashrc runs in every shell; aliases fine; no module loads; conflicts | PASS | S §5 (the customised .bashrc verbatim, username generalised) |
| 10 | B50 | conda's five properties; the create session | PASS | S §5 verbatim |
| 11 | B51 B52 | seven habits; one-session reasoning | PASS | S §5 |
| 12 | B53 | managing commands; mamba; source activate vs conda init / OOD | PASS | S §5 verbatim |
| 13 | B54 B55 | environment.yml; complete workflow; conda in sbatch | PASS | S §5 verbatim (git checkout -b and push omitted) |
| 14 | B60 B61 B62 | data tree; chmod 555 with permission; naming rules and examples; data README; dictionary rows; 3-2-1 | PASS | S §6 |
| 15 | B70 B71 | README template; docstring; why-not-what | PASS | S §7 (templates shortened to fit the card) |
| 16 | B80 | five takeaways; the exercise; "any improvement is valuable" | PASS | S §8, Conclusion |
