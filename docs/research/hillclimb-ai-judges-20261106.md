# An AI judge as the measure of a hill-climb: evidence review

Date: 2026-11-06. Question: which practices have the best evidence for building a pairwise AI judge (LLM or VLM) that serves as the measure in an automated hill-climb, where the climb keeps a candidate only when it beats the current best for a stated goal, person and moment.

The brief listed some items as already established: WiserUI-Bench, SimAB, DesignPref, TASTE, TICK, MT-Bench biases, non-transitivity, Pride and Prejudice, OPRO, Gao et al. and the Optimizer's Curse. This review cites them only where it adds something new.

## Provenance tags

Every claim carries a tag:

- **[full]** I read it in the paper's full text (arXiv HTML or the PDF). On very long pages the tool read the first ~100k characters, which held every result cited here.
- **[abs]** I read only the abstract or the official page.
- **[sum]** I saw it only in a search-engine summary or a secondary write-up. It is not verified.
- **[calc]** My own arithmetic.
- **[inf]** My inference from the evidence, not a reported finding.
- **(established)** Taken from the brief as already known and not re-read for this review. Treat these like [sum]: the citation names where to look, not a verified result.

Most results here were measured on judge models from 2023 to 2025. Failure rates such as order flips and self-preference change with each model generation, so a rate below says what to check for on the model a climb uses, not what to expect from it. This is why the shipped judge guidance has each climb prove its own judge instead of copying settings from these papers.

---

## 1. Strongest practices

1. **Assess each version alone against the goal, then decide the pair** ("pointwise reasoning, pairwise verdict"). Best source: Jeong et al., *The Comparative Trap* / PRePair, arXiv 2406.12319 [full].
2. **Judge both orders, and count a win only when both orders agree.** Treat an order flip as a tie, because flips cluster on close pairs. Best source: Zheng et al. 2023 (MT-Bench) §3.4 [full]; Wang et al. 2023 (*Not Fair Evaluators*) [full].
3. **Put the evidence before the verdict, sample it several times at non-zero temperature, and aggregate.** Do not rely on one greedy call. Best source: Wang et al. 2023, where evidence-first plus multiple samples raised GPT-4 from 52.7% to 60.9% [full]; Haldar & Hockenmaier 2025 (*Rating Roulette*) [full].
4. **Prefer structured, goal-first reasoning to free-form chain of thought.** The structure: restate the goal and criteria, localize the differences, assess each side, then decide. Best source: Zeng et al., LLMBar (ICLR 2024) [full]: CoT lowered GPT-4 on the adversarial set from 80.8 to 76.6, while self-generated metrics plus reference raised it to 82.8. Also WiserUI-Bench v1's G-FOCUS [full].
5. **Have the judge commit to its expectations before it sees the pair.** For open goals that means its criteria; where a correct answer exists, its own answer. Best source: MT-Bench's reference-guided judge cut math failures from 70% to 15% [full]; Zhou 2026 cut false positives from 0.719 to 0.012 [abs].
6. **Keep hard requirements, facts and protected content out of the preference verdict.** Check them on every candidate with binary checklist items or deterministic checks. Best source: Doddapaneni et al. 2024 (FBI): judges missed the quality drop in more than half of targeted perturbations [abs]; Wahi 2026 [abs].
7. **Use judges from model families other than the proposer's, ideally a small, diverse panel.** Best source: Verga et al. 2024 (PoLL) [full]; Li et al., preference leakage (ICLR 2026) [abs]; Panickssery et al. 2024 [abs].
8. **Give every vote a fresh, isolated context, and never share the generator's history with the judge.** Best source: Pan, He, Bowman & Feng 2024, *Spontaneous Reward Hacking in Iterative Self-Refinement* [full].
9. **Ground "the person" in their own words and stakes, not a demographic sketch, and diversify the judges' roles.** Best source: Park et al. 2024: interview-grounded agents reached 83–86% of people's own test–retest consistency, against 74% for demographic agents [abs]; Chan et al., ChatEval: diverse roles 60.0% against 53.8% for one role [full].
10. **Let the judge tie or abstain, and escalate the least certain comparisons to the person or a stronger judge.** Best source: Wang et al. 2023 HITLC: humans on the most uncertain 20% reached human-level agreement [full]; Jung et al. 2024, *Trust or Escalate* [abs].
11. **Prove the judge, and choose its model, on a frozen held-out set before it steers anything.** The set holds known-winner pairs and deliberately degraded versions. Report order-consistency, test–retest, and chance-corrected agreement stratified by how much humans agree, all read against the human–human ceiling. Expect the base model to matter more than the prompt wording. Best source: LLMBar [full]; FBI [abs]; Rating Roulette [full]; Thakur et al. 2024 [full]; Elangovan et al. 2024 [abs]; Husain's practitioner guide [full].
12. **When the person takes part, elicit their verdicts with written reasons on real pairs.** Turn the reasons into explicit criteria, keep most labels out of the prompt as a test set, and expect the criteria to drift as they grade. Best source: Shankar et al. 2024 (EvalGen) [abs]; Husain [full]; Findeis et al., ICAI (ICLR 2025) [abs].
13. **Stop each comparison sequentially at a pre-set margin, and drop clear losers early** (successive halving or dueling bandits). Use a sequential method so that peeking does not inflate false wins. Best source: Arviv et al., ACL Findings 2026 [full, partial]; Johari, Pekelis & Walsh [abs]; Shi et al., TRIPLE [full].
14. **Audit the final winner outside the loop, with a signal the climb never optimized:** real outcomes, the person, or deterministic checks. A judge from a different family is only a partial guard. Best source: Zhou 2026: exploits transferred across judge families, and a strict three-family ensemble still accepted 55% of them [abs].
15. **For pages, show several rendered states, plus the page's text and structure, alongside the pixels.** An agent that interacts with the page has not yet beaten a static judge on preference. Best source: Zhang et al., ArtifactsBench [full]: code plus 3 staged screenshots gave 90.95% agreement, against 74.9% for screenshots alone. Li et al., WebDevJudge [full]: the agentic workflow scored 60.6%, below a plain static single-answer judge's 63.9% in the same rubric mode.

---

## 2. Findings by topic

### a. Pairwise vs pointwise vs checklist/rubric judging

**Practice a1: decide the overall question pairwise.** On natural pairs, pairwise matches human preference better than scores do.

- **MLLM-as-a-Judge** (Chen et al. 2024, arXiv 2402.04788) [full]. 4,414 image–instruction pairs.
  - GPT-4V agreement with humans was Pearson 0.490 for scoring.
  - For pair comparison it was 0.636 with ties and 0.773 without ties.
  - Batch ranking did worst.
  - The abstract contrasts "remarkable human-like discernment in Pair Comparison" with "significant divergence" in scoring and batch ranking.
- **WebDevJudge** (Li et al., arXiv 2510.18560; ICLR 2026 per conference listing [sum]) [full]. 654 web-app pairs from WebDev Arena, relabelled by experts.
  - Pairwise beat single-answer grading by more than 8 points on average.
  - GPT-4.1 scored 70.3% pairwise against 60.9% single-answer.
- **Jeong et al., *The Comparative Trap*** (arXiv 2406.12319) [full]. On MT-Bench human preferences, pairwise far outscored pointwise: GPT-4 67.9 against 54.6, and GPT-4o 69.4 against 52.3.
- **Earlier comparisons.** Liu et al. 2024, PairS (arXiv 2403.16950, COLM 2024) [abs], and Liusie, Manakul & Gales (arXiv 2307.07889, EACL 2024; moderate open models) [abs] both found comparative judging better than direct scoring.
- **Thakur et al. 2024** (arXiv 2406.12624) [full]. Judges ranked systems better than they matched absolute scores, which differed from human scores by up to 5 points.

**Practice a2: expect the pairwise verdict to be swayed by spurious features — the very features a climb tends to produce.**

- **Tripathi, Wadhwa, Durrett & Niekum 2025** (arXiv 2504.14716, COLM 2025) [full].
  - Setup:
    - Judges: LLaMA-3.2-3B, LLaMA-3.3-70B, Qwen2.5-3B and Qwen2.5-72B, read from logits.
    - Data: the MT-Bench human-judgment split (1,689 turn-1 responses on 80 questions) and IFEval-TweakSet (400 items).
    - Distractors were added to the *dispreferred* response: assertiveness, prolixity or sycophancy.
  - Preference flip rates:
    - Pairwise: 32.3–38.0% across models.
    - Absolute 1–7 scoring: 8.8–10.2%.
    - Table 2 of v2 also lists o3-mini and o4-mini text judges, at about 30–44% pairwise against 17–26% absolute. The paper's limitations section says GPT-family models were excluded, an inconsistency inside the paper.
  - Pairs ran in both orders, and the prompts told the judge to ignore length and order. The bias persisted.
  - On identical-quality pairs, pairwise judges almost never said "tie" (2.4–7.3%), while absolute scores tied 84.6–93.2% of the time.
  - The authors say pairwise preferences "exaggerate small gaps" on low preference-strength data.
- **Jeong et al.** (arXiv 2406.12319) [full].
  - On LLMBar-Adversarial (319 pairs in which the worse output has superficially appealing qualities), pointwise beat pairwise for every judge: GPT-3.5 52.4 against 36.1, GPT-4 82.8 against 77.7, GPT-4o 87.8 against 85.9.
  - In 64 of 100 wrong pairwise verdicts, the explanation had named the right weakness, yet the decision was still wrong.
- **Counterpoint: Raina, Liusie & Gales 2024** (arXiv 2402.14016) [abs]. Short universal adversarial phrases inflated *absolute* scores far more easily than comparative judgments.

**Practice a3 (mitigation): reason about each version alone, then make the pairwise decision. Add goal-specific checklists.**

- **PRePair** (Jeong et al.) [full]. Each response is analyzed alone, then those analyses feed one pairwise decision.
  - On LLMBar-Adversarial it raised GPT-3.5 from 36.1 to 54.2, Llama-3.1-8B from 48.6 to 70.8, GPT-4o-mini from 68.0 to 78.1, GPT-4 from 77.7 to 80.9, and GPT-4o from 85.9 to 86.2.
  - On MT-Bench it stayed near pairwise level (GPT-4o 69.5 against 69.4; GPT-4 65.3 against 67.9).
  - The gains are largest for weaker judges.
- **G-FOCUS** (WiserUI-Bench v1, arXiv 2505.05026v1) [full].
  - Steps: infer the persuasion goal, localize the differences prioritized by that goal, then write a rationale for each UI as if it were the better one, and only then decide.
  - On 300 real A/B pairs with GPT-4o, consistency rose from 35.7 to 60.3 and consistent accuracy from 24.7 to 43.3.
  - In the same table, a *single-UI* (pointwise) critique method based on UICrit reached consistent accuracy of 32.3 (GPT-4o) and 38.0 (Claude 3.5 Sonnet). That beat zero-shot pairwise (24.7 and 21.3).
  - Caveat: the current v5 of the paper no longer proposes G-FOCUS (see section c).
- **Checklists and rubrics:**
  - CheckEval (Lee et al., arXiv 2403.18771) [abs]: across 12 evaluator models, Boolean checklists raised average agreement by 0.45 and reduced score variance.
  - Rubrics as Rewards (Gunjal et al., arXiv 2507.17746) [abs]: up to a 31% relative gain on HealthBench over Likert judge rewards, with less variance across judge sizes.
  - RLCF (Viswanathan et al., NeurIPS 2025, arXiv 2507.18624) [abs]: checklist feedback was the only method to improve all 5 benchmarks for Qwen2.5-7B (FollowBench +4, InFoBench +6, Arena-Hard +3).
  - WebDevJudge [full]: a query-specific rubric raised *human–human* agreement from 65.0% to 92.0%.

**How this applies to a hill-climb.** [inf]

- Keep the pair as the unit of decision, since it matches human preference best on natural pairs.
- Structure the judge's work in three steps:
  1. criteria derived from the goal and fixed before any candidate is seen;
  2. an independent assessment of each version against those criteria;
  3. the pairwise verdict.
- Hard requirements and protected content get per-version binary checks, outside the verdict.
- A climb produces candidates that drift toward whatever the judge rewards. Its pairs therefore grow more adversarial with every round, which is the regime where plain pairwise judging is weakest (Tripathi; Jeong).

### b. Bias controls with evidence

**Position bias. Practice: always judge both orders; an order flip means a tie; randomize the neutral labels too.**

- **MT-Bench** (Zheng et al. 2023) [full].
  - On near-identical answer pairs (two GPT-3.5 samples), swap consistency was 65.0% for GPT-4, 46.2% for GPT-3.5 and 23.8% for Claude-v1.
  - Renaming the assistants exposed a *name* bias: Claude-v1 favored "Assistant A".
  - The fix: "call a judge twice by swapping the order… only declare a win when an answer is preferred in both orders… If the results are inconsistent after swapping, we can call it a tie."
- **Wang et al. 2023** (arXiv 2305.17926, the FairEval paper) [full].
  - With GPT-4 as judge, Vicuna-13B's win rate against ChatGPT was 51.3% in one position and 23.8% in the other.
  - The conflict rate falls as the score gap grows, so flips mark close pairs.
  - Balanced Position Calibration on top of multiple-evidence calibration raised GPT-4's accuracy against the majority of 3 annotators (80 Vicuna questions) from 58.7% to 62.5% (κ 0.30 to 0.37).
- **Shi et al.** (arXiv 2406.07791) [abs]. 15 judges, 22 tasks, more than 150,000 instances: position bias is not random, varies by judge and task, and is "strongly affected by the quality gap between solutions". Prompt length had little influence.
- **WebDevJudge** [full]. GPT-4.1 with direct prompting gave the same verdict across orders in only 83.3% of cases.
- **Wang et al. 2025** (arXiv 2504.09946) [abs]. Reasoning models favor *later* positions.

**Verbosity and length. Practice: hold length and density within a band set before the climb, and test the judge with padded perturbations.** [inf for the climb form]

- **MT-Bench "repetitive list" attack** [full]. 23 answers were padded with a reworded copy of their own list. Claude-v1 and GPT-3.5 judged the padded version better in 91.3% of cases, GPT-4 in 8.7%. All judges returned a tie for identical answers.
- **MLLM-as-a-Judge** [full]. Longer answers with the same meaning gained about 0.6 (GPT-4V) and 0.75 (Gemini) score points.
- **Dubois et al., Length-Controlled AlpacaEval** (arXiv 2404.04475) [abs]. A GLM that removes the length difference raised Spearman correlation with Chatbot Arena from 0.94 to 0.98.
- **LMSYS style control** (blog, 2024-08-28) [sum]. Bradley–Terry regression with length and markdown counts as covariates; length was the dominant style factor.
- **Zheng et al. 2024, null models** (arXiv 2410.07137, ICLR 2025) [abs]. A constant, irrelevant answer reached 86.5% length-controlled win rate on AlpacaEval 2.0, 83.0 on Arena-Hard-Auto and 9.55 on MT-Bench. Length control and style disentanglement did not stop it.
- **Application.** [inf] Regression controls need many comparisons across a benchmark, and a climb compares one pair at a time. Length, density and amount of content are better constrained in the candidate brief, or listed under what must not change.

**Self-preference and family bias. Practice: the judge's family differs from the proposer's; use a panel.**

- **Panickssery, Bowman & Feng 2024** (arXiv 2404.13076) [abs]. Self-recognition correlates linearly with self-preference under fine-tuning, with controlled evidence for a causal link.
- **Wataoka et al. 2024** (arXiv 2410.21819) [abs]. Judges rate low-perplexity, familiar text higher than humans do, whether or not they wrote it.
- **Li et al., preference leakage** (arXiv 2502.01534, ICLR 2026) [abs]. Judges favor outputs from models related to them (the same model, one inheriting from the other, or the same family). This is harder to detect than other biases.
- **Laurito et al., AI–AI bias** (arXiv 2407.12856) [abs]. LLMs consistently chose items presented in LLM-written text over items presented in human-written text.
- **MT-Bench** [full]. GPT-4 gave itself a 10% higher win rate and Claude-v1 25%, though the authors "cannot determine" a self-enhancement bias from that data.
- **PoLL** [full]. A GPT-4 judge ranked a GPT-4 variant 2nd, against its actual 4th place.
- **Application.** [inf] For writing read as its reader, an LLM judge will drift the climb toward LLM-familiar prose, so the person's spot checks matter most there.

**Style over substance. Practice: give the judge explicit rules, have it generate its own criteria (and a reference where one exists), and check facts outside the judge.**

- **Wu & Aji 2023** (arXiv 2307.03025) [abs]. Answers with factual errors were rated above answers that were too short or ungrammatical, by crowd workers, experts and LLMs alike.
- **LLMBar** (Zeng et al., arXiv 2310.07641) [full].
  - Without help, GPT-4 reached 73.1% on adversarial pairs, and ChatGPT stayed below chance (30.6–38.9%).
  - Rules (explicit priorities, such as following the instruction over tone or length) raised GPT-4 to 80.8.
  - Rules plus self-generated metrics and reference reached 82.8.
  - CoT with rules gave 76.6.
- **Wang et al. 2025** (arXiv 2504.09946) [abs].
  - Reasoning models show a "superficial reflection bias": phrases like "wait, let me think…" sway their verdicts.
  - Specialized system prompts cut bias by up to 19% (preference data) and 14% (factual data).
  - In-context examples cut it by up to 27% on preference tasks.
  - Self-reflection cut it by up to 10% and 16%.
- **Zhao et al., *One Token to Fool LLM-as-a-Judge*** (arXiv 2507.08794) [abs]. Strings such as ":" or "Thought process:" trigger false-positive rewards across many models, including GPT-o1 and Claude-4.

**Panels of diverse judges. Practice: three to four judges from different families or with different roles, aggregated.**

- **PoLL** (Verga et al., arXiv 2404.18796) [full].
  - The panel: Command R, Claude Haiku and GPT-3.5, with majority vote on binary QA and averaging on 1–5 scales.
  - Cohen's κ against humans:

    | Dataset | PoLL | GPT-4 | Best single judge |
    |---|---|---|---|
    | NQ | 0.763 | 0.627 | — |
    | TQA | 0.906 | 0.841 | — |
    | HotpotQA | 0.867 | 0.830 | Haiku 0.873 |

  - On Chatbot Arena-Hard rankings, PoLL reached Pearson 0.917 against GPT-4's 0.817, and Kendall 0.778 against 0.667.
  - It cost 7–8 times less than GPT-4.
- **ChatEval** (Chan et al., arXiv 2308.07201) [full]. On the FairEval set of 80 questions, with ChatGPT:

  | Setting | Accuracy | κ |
  |---|---|---|
  | Single agent | 53.8% | 0.27 |
  | Several agents, same role | 53.8% | 0.25 |
  | Several agents, diverse roles | 60.0% | 0.33 |

  Accuracy peaked at 62.5% with 3–4 roles. More discussion turns did not help.
- **Coste et al. 2024** (arXiv 2310.02743, ICLR 2024) [abs]. In reward-model best-of-n, ensemble-based conservative optimization "practically eliminates overoptimization", even with 25% label noise.
- **Limit: Zhou 2026** (arXiv 2607.05904, single-author preprint) [abs]. Errors manufactured against one judge transferred across the Qwen, Llama and Gemma families, and a strict three-judge ensemble still accepted 55% of them.

### c. Judge prompt design

**Reasoning before the verdict. Practice: evidence first, in a fixed structure. Treat free-form CoT as unproven for preference.**

- **Wang et al. 2023** [full]. With evidence first instead of the verdict first ("EC", k=1):
  - GPT-4 rose from 52.7% to 56.5% accuracy (κ 0.24 to 0.29).
  - ChatGPT rose from 44.4% to 52.6% (κ 0.06 to 0.23).
  - Three to six evidence samples added about 2–4 points more.
- **Chiang & Lee 2023** (arXiv 2310.05657, EMNLP Findings) [abs]. Asking the model to explain its rating consistently improved correlation with humans, while G-Eval's automatic CoT did not always help.
- **MT-Bench** [full]. CoT cut math-grading failures from 14/20 to 6/20, but GPT-4 sometimes copied the wrong answer's errors into its own working.
- **LLMBar** [full]. "Contrary to common beliefs, CoT* falls short in enhancing LLM evaluators on Adversarial": GPT-4 fell from 80.8 to 76.6.
- **MLLM-as-a-Judge** [full]. Multi-step CoT lowered scoring agreement (GPT-4V Pearson 0.557 to 0.299 on a subset; Gemini 0.299 to 0.144), though it reduced hallucination.
- **WiserUI-Bench**:
  - v5 [full]: CoCoT, Self-Refine, DDCoT and multi-agent debate left average accuracy "similar to or below" zero-shot (GPT-4o: 60.1 zero-shot against 57.6–61.7). The first round of multi-agent debate gave the best consistent accuracy (30.1 to 39.0). o1 scored 15.6, below the 25% random baseline.
  - v1 [full] proposed G-FOCUS, a goal-first structured method, with large gains (section a). It is absent from v5, and the reason is not stated. Zero-shot numbers also differ between versions (consistent accuracy 24.7 in v1, 30.1 in v5), so the evaluation changed.
- **JudgeBench** (Tan et al., arXiv 2410.12784) [full].
  - On hard pairs labelled by objective correctness, reasoning models judged best: o3-mini (high) 80.9, o1-preview 75.4, Claude-3.5-Sonnet 64.3, and GPT-4o 50.9–56.6.
  - A judge's accuracy tracks its own ability to solve the problem.
- **Rating Roulette** [full]. Few-shot and CoT prompts did not improve run-to-run consistency on SummaC.
- **The base model matters more than the prompt.** In LLMBar [full], the best ChatGPT configuration reached 38.9% on adversarial pairs, while plain GPT-4 reached 73.1%.

**Criteria decomposition. Practice: a short checklist derived from the goal, written before candidates are seen.**

- G-Eval (Liu et al., arXiv 2303.16634) [abs]: Spearman 0.514 on summarization with GPT-4.
- CheckEval [abs]; TICK (established).
- WebDevJudge [full]: a rubric took human agreement from 65% to 92%.
- LLMBar's self-generated metrics [full]: the judge writes the metrics, then judges. On adversarial pairs this gained 1.2 points over rules alone for GPT-4 and 6.7 for ChatGPT.
- LLM-Rubric (Hashemi et al., arXiv 2501.00274) [abs]: a 9-question rubric plus per-judge calibration predicted individual users' satisfaction on a 1–4 scale with RMS error below 0.5, about twice as good as uncalibrated.

**Reference-free vs reference-guided. Practice: use a reference wherever correctness exists; where it does not, use expectations the judge commits to first.** [inf for the open-goal case]

- MT-Bench [full]: the judge's own independent answer, shown as the reference, took the failure rate from 70% to 15%.
- FBI [abs]: reference-based evaluation was the strongest of the strategies tested.
- LLMBar [full]: a self-generated reference took GPT-4 from 80.8 to 82.6 on adversarial pairs.
- Zhou 2026 [abs]: committing the judge's own answer before it sees the candidate took false positives from 0.719 to 0.012 (GSM8K).
- Thakur [full]: the reference's position swayed smaller judges.
- **Application.** For prompts whose outputs can be checked, and for plans with checkable facts, use references. For a page's or document's fitness to its reader no reference exists, and the analog the evidence supports is criteria the judge commits to before seeing the candidates (LLMBar metrics; G-FOCUS goal extraction).

**Context: goal, audience persona, task. Practice: the goal and the person's real situation, in their own words.**

- **WiserUI-Bench** [full]: models were never given the business goal or audience (expert annotators were), and no experiment varied it. G-FOCUS inferred the goal first and gained.
- **Thakur** [full]: more detailed guidelines slightly helped the top models and hurt many smaller ones.
- **Hu & Collier 2024** (arXiv 2402.10811, ACL 2024) [abs]:
  - Persona variables explain under 10% of annotation variance in subjective NLP datasets.
  - Persona prompting gives modest gains, largest where annotators disagree mildly.
- **Dong, Hu & Collier 2024** (arXiv 2406.11657) [abs]:
  - A persona-based "personalized judge" is "less reliable than previously assumed".
  - With verbal uncertainty added, agreement on high-certainty binary samples rose above 80%.
- **Park et al. 2024** (arXiv 2411.10109) [abs]:
  - Agents were built for 1,052 people from 2-hour interviews, from surveys, or from both.
  - On held-out General Social Survey items they reached 83%, 82% and 86% of each person's own two-week test–retest consistency.
  - Demographic-only agents reached 74%.
- Persona diversity: SimAB's roughly 10-point loss without diversity (established) agrees with ChatEval's diverse-role gain. The effect sizes are small to moderate, and the samples are small.

### d. Aligning a judge to one person's judgment

**Practice: shadow the person's critiques, turn their reasons into explicit criteria, keep most of their labels held out, and re-elicit when the criteria drift.**

- **EvalGen** (Shankar et al. 2024, arXiv 2404.12272) [abs]. Criteria drift: "users need criteria to grade outputs, but grading outputs helps users define criteria". Some criteria depend on which outputs the person has seen.
- **Husain, *Creating a LLM-as-a-Judge That Drives Business Results*** (hamel.dev) [full page].
  - Method: "critique shadowing". A domain expert gives each example a pass/fail verdict and a critique detailed enough for a new employee. The judge's few-shot examples include the input, output, critique and outcome.
  - Results: more than 90% agreement within three iterations on a roughly balanced set (this varies by task). He reports true-positive and true-negative rates separately, because raw agreement misleads on imbalanced data.
  - Label counts: about 30 labels to start, and about 100 per failure mode to validate. Below 60, "the confidence intervals are often too wide".
  - Splits: 10–20% train (in the prompt), 40–45% dev and 40–45% test. The test set runs once, on a frozen prompt.
- **AutoCalibrate** (Liu et al., arXiv 2309.13308) [abs]. Draft scoring criteria from the human labels, keep the best and refine them. Correlation with experts improved without any gradient training.
- **Inverse Constitutional AI** (Findeis et al., arXiv 2406.06560, ICLR 2025) [abs]. Compresses pairwise preference data into a short set of principles that let an LLM reconstruct the annotations. Validated on AlpacaEval, Chatbot Arena and PRISM; proposed for adapting to individuals.
- **SynthesizeMe** (Ryan et al., arXiv 2506.05598, ACL 2025) [abs]. Induces a persona from a user's past choices and selects the most informative ones as in-context examples. Personalized judge accuracy rose 4.4% on Chatbot Arena (854 users, PersonalRewardBench).
- **Few-shot examples in the prompt: mixed, modest.**
  - MT-Bench [full]: three examples raised GPT-4's order consistency from 65.0% to 77.5%. But agreement with humans was "similar to zero-shot", the examples moved GPT-3.5's bias from the first position to the second, and the prompt cost 4×.
  - PoLL [full]: few-shot raised GPT-4's κ on NQ from 0.518 to 0.627.
  - LOLA [full], on Upworthy: 2 demonstrations raised GPT-4 from 37.9% to 40.0%, and demonstrations with *wrong* labels did almost as well (38.8%). That suggests format, not knowledge.
  - UICrit (Duan et al., arXiv 2407.08850, UIST 2024) [abs]: few-shot plus visual prompting with designer critiques gave a 55% gain in the quality of LLM-written UI feedback.
- **How many labels, and the limits of label savings.**
  - Dorner, Nastl & Hardt (arXiv 2410.13341) [abs]: when the judge is no more accurate than the model it evaluates, no debiasing method can cut the ground-truth labels needed by more than half, and in practice the savings are smaller.
  - My own numbers [calc]:
    - A 95% interval of ±0.10 on an agreement near 0.7 needs about 81 labelled pairs; ±0.05 needs about 323.
    - Showing that a judge beats coin-flip accuracy (one-sided α=0.05, 80% power) needs about 153 pairs if its true accuracy is 0.60, 67 at 0.65 and 37 at 0.70.
    - SimAB's roughly 45 tests can therefore only show a large effect.
- **Agreement metrics.**
  - Thakur et al. [full] recommend "computing both percent agreement and Scott's π, paired with qualitative analysis". They switched from Cohen's κ because of its theoretical issues.
  - Elangovan et al. (arXiv 2410.03775) [abs] warn against a single aggregate correlation. Stratify by human uncertainty: when many items have uncertain human labels, machine–human agreement can look as good as human–human while being far worse on items where humans agree. They propose a binned Jensen–Shannon divergence.
  - Deutsch, Foster & Freitag (arXiv 2305.14324) [abs] use pairwise accuracy that credits correct ties, with a tie-calibration procedure.
  - Eugene Yan's survey [sum]: Cohen's κ suits binary labels; Kendall or Spearman suits ordinal ones.
  - Husain [full]: report TPR and TNR separately.
- **Application.** [inf]
  - Have the requester judge a few real pairs from *this* artifact and say why.
  - Turn those reasons into the judge's written criteria (the ICAI or AutoCalibrate pattern).
  - Put only a few labelled pairs, with their reasons, in the prompt, and keep the rest for measurement.
  - Re-elicit when the person's reasons change.
  - The evidence speaks to labelled *judgments*. It is silent on showing an example *version* as an anchor (section 3, item 2).

### e. Proving a judge before relying on it

**Practice: a fixed battery on a frozen held-out set — known-worse perturbations, known-winner pairs, order-consistency, test–retest, tie behavior, and agreement against the human ceiling — with bars set before the run.**

- **Known-worse perturbations.**
  - FBI (Doddapaneni et al., arXiv 2406.13439, EMNLP 2024) [abs]: 2,400 perturbed answers in 22 categories covering factual accuracy, instruction following, long-form coherence and reasoning. Five evaluator LLMs "failed to identify quality drops in over 50% of cases on average".
  - LLMBar [full]: 419 curated pairs (100 natural, 319 adversarial).
  - MT-Bench repetitive list [full]: a padded copy versus the original.
  - Thakur [full]: dummy answers such as "Yes" or "Sure" were marked correct by some judges, and even verbatim gold answers were not always accepted. Leniency: the chance of passing a wrong answer was well above 0.5 for most judges (GPT-4 0.69, Llama-2-70B 0.99), with JudgeLM the exception at 0.19.
  - CALM (Ye et al., arXiv 2410.02736) [abs]: 12 bias types measured by principle-guided modification.
- **Order consistency.**
  - MT-Bench [full]: 23.8–66.2% on near-identical pairs.
  - WebDevJudge [full]: 83.3% for GPT-4.1.
  - WiserUI-Bench [full]: "consistent accuracy" has a random baseline of 25%, and o1 fell below it at 15.6%.
- **Test–retest noise.**
  - Rating Roulette (Haldar & Hockenmaier, arXiv 2510.27106, EMNLP Findings 2025) [full]:
    - Judges: Llama-3.1-70B, DeepSeek-R1-Distill-Qwen and Qwen3-32B, 3 runs each with identical settings.
    - Krippendorff's α across runs was 0.33, 0.63 and 0.79 on SummaC, and 0.27, 0.51 and 0.56 on MT-Bench pairwise.
    - Qwen3 gave the same MT-Bench verdict on all three runs only 61.3% of the time.
    - The authors treat α ≥ 0.8 as the commonly accepted threshold.
    - Temperature 0 *lowered* agreement with humans compared with a majority vote over samples (Qwen3 balanced accuracy 80.6 to 79.2).
    - A majority over 3 runs beat the best single run, while 5–10 runs did not change self-consistency.
  - Schroeder & Wood-Doughty (arXiv 2412.12509) [sum]: McDonald's ω over seeds, and the reminder that consistency is not correctness.
- **Tie behavior.**
  - Tripathi [full]: pairwise judges rarely tie, even on identical-quality pairs.
  - MT-Bench [full]: identical answers always tie.
  - MLLM-as-a-Judge [full]: with ties, accuracy falls from 0.773 to 0.636.
  - Deutsch et al. [abs]: tie calibration.
- **The human ceiling** (subjective tasks have low ceilings):
  - WebDevJudge [full]: human pairwise agreement averaged 84.6%, and the best judges about 70%. Crowd agreement without a rubric was 65%.
  - Wang et al. 2023 [full]: individual annotators against the majority averaged 71.7% (κ 0.54).
  - Agent-as-a-Judge [full]: individual evaluators disagreed with each other 10–30% of the time.
  - DesignPref (established): α 0.25 among designers.
- **Thresholds in use.**
  - Husain [full]: more than 90% agreement on a balanced set, with TPR and TNR.
  - Rating Roulette [full]: α ≥ 0.8 commonly accepted.
  - Thakur [full]: human π of 96 against 87–88 for the best judges, in an easy QA setting.
  - I found no published threshold for preference judges on subjective artifacts. [gap]
- **Overfitting the judge to its own proof set.**
  - Husain [full]: keep the test set out of the prompt and run it once.
  - Dwork et al., *The Reusable Holdout* (Science 2015) [sum]: reusing a holdout adaptively overfits it.
  - Wahi 2026 (arXiv 2609.02246) [abs]: frozen holdouts, and canary cases where a perfect score is taken as evidence of cheating.
- **Application.** [inf]
  - Set bars relative to the ceiling, for example agreement within some fraction of human–human agreement on the same pairs.
  - Require order-consistent accuracy above chance with its interval, and a detection rate for degraded versions near 100%. That makes a judge that cannot tell a broken version from the original disqualified.
  - Report agreement separately on the pairs where humans agree strongly.

### f. Over-optimization ("hacking") of AI judges during iterative optimization

**Evidence that the climb setting itself causes it:**

- **Pan, He, Bowman & Feng 2024** (arXiv 2407.04549) [full].
  - Task: essay editing, with GPT-3.5 and GPT-4 each acting as both author and judge, and 3 human raters per essay. The essay count is garbled in the HTML; the run had 5 refinement steps per trajectory.
  - An "online" judge that shared the author's context scored edited essays well above humans, while an "offline" judge with a fresh context tracked the humans.
  - Lengthening the shared context from 11 to 33 iterations widened the gap.
  - "In-context reward hacking is more likely when the judge and author share identical contexts."
  - GPT-4 was less affected than GPT-3.5, which the authors call tentative.
- **Pan, Jones, Jagadeesan & Steinhardt 2024** (arXiv 2402.06627) [abs]. Feedback loops (output refinement and policy refinement) drive in-context reward hacking, and evaluation on static datasets is "insufficient" to catch it.
- **Zhou 2026** (arXiv 2607.05904) [abs].
  - Self-play against a reference-free judge on GSM8K pushed the judge's pass rate from 0.72 to 0.94, while true accuracy, verified against a hidden anchor, stayed at 0.20.
  - The exploits transferred across judge families.
  - Having the judge commit its own answer first was the fix.
- **Wahi 2026** (arXiv 2609.02246) [abs]. Prompt-optimization loops in production showed 11 failures in 4 classes: judge bias, harness and metric faults, ground-truth errors, and reward hacking. Rewriting the judge's rubric "plateaued", and the only reliable gain came from a structural constraint on the order of the judge's output.
- **Attacks that transfer.**
  - Null models (Zheng et al. 2024) [abs]; universal phrases (Raina et al. 2024) [abs]; master keys (Zhao et al. 2025) [abs].
  - Wen et al. 2024 (arXiv 2409.12822) [abs]: RLHF taught models to convince *human* evaluators without getting more correct. Humans' false-positive rate rose 24.1% (QuALITY) and 18.3% (APPS), so quick human checks are not a gold standard either.

**Mitigations, with the strength of evidence for each:**

| Mitigation | Evidence | Strength |
|---|---|---|
| Fresh, context-isolated judge per vote | Pan et al. 2024, offline judge tracked humans [full] | Direct, small study |
| Judge family differs from proposer; diverse panel | Self-preference and leakage (Panickssery; Wataoka; Li) [abs]; PoLL [full]; Coste ensembles [abs] | Good for bias. **Partial** against exploits: 55% still accepted by a 3-family ensemble (Zhou) [abs] |
| Held-out or different-family final judge | Indirect, as above | Partial; it cannot stand in for real outcomes |
| Rotating judges | **No direct evidence found.** [gap] Ensembles are the nearest evidence | Unknown |
| Periodic or targeted human checks | Wang et al. 2023 HITLC: 20% of items to humans took GPT-4 from 62.5% to 73.8%, above the human average of 71.7% [full]; Jung et al., *Trust or Escalate* [abs]: guaranteed agreement above 80% at nearly 80% coverage on a Chatbot Arena subset where GPT-4 alone rarely reached 80%; Mohankumar & Khapra 2022 [abs]: model-based routing of only uncertain items cut human labels a further 89% | Good; humans can also be misled (Wen) |
| Separate checks on facts and protected content | FBI [abs]; Wu & Aji [abs]; Thakur leniency [full]; Wahi deterministic acceptance checks that outrank the judge [abs] | Strong for "do not trust the judge on facts" |
| Judge commits its expectations first | Zhou 2026 [abs]; MT-Bench reference-guided [full]; LLMBar [full] | Strong on correctness tasks; untested on design |
| Hidden anchor or canary audit | Zhou 2026 [abs]; Wahi 2026 [abs] | Single-author 2026 preprints |

**Application.** [inf]

- The climb's record ("what won, what lost and why") feeds the judge's reasons back into the proposer. That is the output-refinement feedback loop Pan et al. describe.
- Give the proposer outcomes and the person's reasons, not the judge's verbatim rationales.
- Hold the confirmation judge, and its rationales, out of the proposer's view.
- Track over rounds how often the search judge and the audit signal agree. A falling rate is the in-context analog of the proxy-versus-gold divergence in Gao et al., and grounds to stop.

### g. Visual and UI judges

**Practice: render several states as the person meets them, pair the pixels with the page's text and structure, check perception first, and keep interactive agents for functional requirements.** [inf, assembled from the studies below]

- **ArtifactsBench** (Zhang et al., arXiv 2507.04952) [full]. 1,825 tasks. An MLLM referee scores each artifact against a per-task checklist from its code and screenshots. Pairwise agreement with the median expert score (280 queries × 6 models; Gemini-2.5-pro referee):

  | Input | Pairwise agreement |
  |---|---|
  | Code only | 79.1% |
  | Code + 1 screenshot | 87.1% |
  | Code + 3 staged screenshots | 90.95% |
  | Screenshots only, no code | 74.9% |
  | Captions instead of images | 81.7% |

  - The 94.4% "ranking consistency" with WebDev Arena compares *model rankings*, not pairs.
  - There is no ablation with and without the checklist.
  - This is pointwise checklist scoring later compared pairwise, on functional web artifacts.
- **WebDevJudge** [full]. Claude-4-Sonnet, pairwise:
  - Code only 67.6%, image only 59.5%, both 70.2%.
  - An agentic, interactive workflow reached 60.6% on the combined rubric and "did not beat vanilla models": Claude-3.7-Sonnet as a plain single-answer judge reached 63.9%. The agent did best on dynamic behavior (55.7%).
  - A gated ensemble added 1.2–1.3 points.
  - On feasibility checks, an agent had higher precision but lower recall (UI-TARS 82.4/70.3) than GPT-4.1 (72.1/90.0).
- **Agent-as-a-Judge** (Zhuge et al., arXiv 2410.10934) [full]. On DevAI (55 tasks, 365 requirements), the question is whether each requirement is met: checkable, not preference.
  - Agent-as-a-Judge agreed with the human majority on 83.9–92.1% of requirements, against 60.4–84.2% for LLM-as-a-Judge.
  - Individual humans scored 76.2–92.6%.
  - It cost about 2.3% of the human cost.
  - The graph, locate and read modules mattered most.
- **VL-RewardBench** (Li et al., arXiv 2411.17451, CVPR 2025) [abs]. 1,250 examples; GPT-4o scored 65.4%, and open models were near random. Failures were mostly in "basic visual perception" rather than reasoning.
- **UICrit** [abs + repository README].
  - The paper: 3,059 critiques for 983 mobile UIs from 7 designers.
  - The released set is larger: 11,344 critiques on 1,000 RICO UIs, with bounding boxes and ratings (aesthetics, learnability, efficiency, usability, design quality).
  - Few-shot plus visual prompting gave a 55% gain in the quality of LLM-written UI feedback.
- **UIClip** (Wu et al., arXiv 2404.12500) [abs]. Scores design quality and relevance from a screenshot plus a description. It had the highest agreement among the baselines with 12 designers' rankings.
- **WiserUI-Bench** (beyond what was established): the v1 G-FOCUS steps and gains, and the single-UI pointwise result, are in section a; the v5 reasoning strategies are in section c.
- **MLLM as a UI Judge** (Luera et al., arXiv 2510.08783) [sum]. 30 interfaces with crowdsourced judgments: models matched humans on some UI factors and diverged on others.
- **Several viewports:** no study found. [gap] The nearest evidence is that several *staged* screenshots beat one (ArtifactsBench).
- **Persona agents interacting with pages vs real users:** UXAgent (arXiv 2502.12561 and 2504.09407) [sum] was validated only by a UX-researcher heuristic review. I found no peer-reviewed study of issue-level overlap with real participants. [gap]
- **Application.** [inf]
  - Render at the person's device and arrival state, and capture several states (first view, after the key interaction, scrolled to the decision point).
  - Give the judge the page's text or accessibility tree alongside the screenshots.
  - Ask it first to state what differs between A and B (the G-FOCUS localization step), which also checks perception.
  - Use interactive agents to verify that what must keep working still works (the Agent-as-a-Judge pattern), not for the preference verdict.

### h. Voting and stopping for noisy pairwise comparisons

**How many votes.**

- **Wang et al. 2023** [full]. Evidence samples k=1, 3 and 6 with BPC: GPT-4 accuracy 56.5%, 58.7%, 60.9%, and 62.5% with k=3 in both orders. Gains flatten.
- **Rating Roulette** [full]. A majority of 3 beat the best single run, and more runs did not raise self-consistency.
- **Miller, *Adding Error Bars to Evals*** (arXiv 2411.00640) [full].
  - "Using the paired version of the standard error estimate wherever practicable", because two systems judged on the same questions give a "free" reduction in variance. This is the case for prompts judged on the same inputs.
  - Resampling answers reduces variance with diminishing returns: choose the number of samples where extra ones stop helping.
  - Cluster standard errors when items come in related groups (naive errors can understate imprecision about 3×).
- **Spotify Engineering, 2026** [full blog]. Averaging several LLM samples per unit reduced bias and variance from sampling temperature.
- **Correlated votes.** [inf] Repeated votes from one model cut that model's sampling noise, not its bias: a model that consistently prefers the padded version will do so in every vote. Diversity across judges reduces bias (PoLL, ChatEval). A stopping rule on one judge's votes therefore measures that judge's stable preference, not truth.

**Sequential stopping.**

- **Johari, Pekelis & Walsh**, *Always Valid Inference* (arXiv 1512.04922; Operations Research 2022) [abs]. Fixed-sample p-values are "wholly unreliable" under continuous monitoring. Always-valid p-values from sequential tests let a test stop at any time, and the method was deployed on a large commercial A/B platform.
- **Arviv et al., *Stop Guessing When to Stop Testing*** (ACL Findings 2026) [full, partial].
  - Group sequential testing with a Pocock spending function.
  - For pairwise model comparisons with gaps above 2 points, it "usually saved at least 60%" of evaluation effort.
  - A fixed 1.2k-sample design separated only 55% of 1,000 model pairs, against 76% for the sequential one.
  - A one-sided "new model must beat the old by ≥2 points" deployment test used 63% of a fixed design's examples. This is the shape of a climb's challenger-versus-incumbent test.

**Pruning losers early.**

- **TRIPLE** (Shi et al., arXiv 2402.09723) [full]. Prompt selection framed as fixed-budget best-arm identification. Successive halving beat uniform allocation by about 15% with 30 prompts and a budget of 150, and the advantage vanished at about 30 evaluations per prompt.
- **Active Evaluation** (Mohankumar & Khapra, ACL 2022, arXiv 2203.06063) [abs]. Thirteen dueling-bandit algorithms cut the human comparisons needed to find the top system by 80%, and model-based variants a further 89%.
- **Prompt Duel Optimizer** (Wu et al., arXiv 2510.13907) [abs]. Label-free prompt optimization by LLM-judge duels, choosing pairs with Double Thompson Sampling and pruning weak prompts.

**Confirming a winner on fresh votes.**

- The Optimizer's Curse (established).
- Lee & Shen, *Winner's Curse*, KDD 2018 [sum]: launched A/B winners overstate their total effect.
- Dwork et al. 2015 [sum].
- **Application.** [inf]
  - Pair the votes as A/B and B/A.
  - Stop when an order-balanced sequential test with the margin set in advance says the challenger is ahead or equivalent, or at the cap.
  - Within a round, prune challengers that lose clearly early (successive halving against the incumbent).
  - Re-run the surviving leader against the incumbent on fresh judges and samples before it replaces the incumbent.

---

## 3. Conflicts and open questions

1. **"Pairwise comparison, never a score" is partly challenged.**
   - *Supports pairwise* for the overall verdict, on natural pairs: MLLM-as-a-Judge, WebDevJudge, Jeong et al. on MT-Bench, PairS, Liusie et al., and Raina et al. (absolute scores are easier to attack).
   - *Against pure pairwise:* Tripathi (flips of 35% against 9% under distractors) and Jeong (pointwise beats pairwise on adversarial pairs). A climb generates adversarial pairs by design.
   - *Pointwise designs reached high pairwise agreement in places:* ArtifactsBench's per-task checklist scores reached 90.95% agreement with experts on functional artifacts. WiserUI v1's single-UI pointwise critique beat zero-shot pairwise on consistent accuracy (32.3 and 38.0 against 24.7 and 21.3).
   - Many "pairwise" protocols score both responses inside one prompt (Wang et al. 2023 asked for a 1–10 score for each assistant).
   - The evidence supports a hybrid: a pairwise final verdict over per-version assessments (PRePair), with binary per-version checks for the must-not-change items. A scale-free "never score" rule is right for the overall preference. Banning per-criterion pointwise checks would discard the robustness evidence.
2. **"No example versions shown to the judge" is untested either way.**
   - References help where a correct answer exists: MT-Bench 70% to 15%; FBI; LLMBar's self-generated reference; Zhou's commit-first. Few-shot *labelled judgments* help modestly: SynthesizeMe +4.4%, PoLL κ +0.11, UICrit +55% feedback quality. MT-Bench shows few-shot examples can move a bias rather than remove it.
   - No study found tests whether an example version pulls a climb's candidates toward itself. The concern is plausible but unmeasured. [gap]
   - Three things differ and need separate rules:
     - (a) an example target artifact: the anchoring risk, unmeasured;
     - (b) labelled past comparisons with the person's reasons: modest positive evidence;
     - (c) expectations the judge writes itself before seeing candidates: positive evidence on correctness tasks.
3. **Reasoning before the verdict is mixed.**
   - Evidence-first helps (Wang et al.; Chiang & Lee).
   - Free-form CoT hurt on adversarial and visual scoring tasks (LLMBar; MLLM-as-a-Judge) and did not help on WiserUI.
   - Structured goal-first reasoning helped in WiserUI v1, but v5 withdrew the method. That instability is a reason to measure any structured reasoning before relying on it.
   - Reasoning models help on objective pairs (JudgeBench) but bring their own biases (later-position preference and superficial reflection, Wang et al. 2025).
4. **Interactive judging is mixed and task-dependent.** Agent-as-a-Judge strongly beats LLM-as-a-Judge on checkable requirements. WebDevJudge finds agentic judging worse than static judging on preference. Both are web or code tasks, and neither measures real user outcomes.
5. **Seeing the artifact "as the person meets it" vs giving the judge code.** Code improved agreement in ArtifactsBench and WebDevJudge, but those labels were partly about functionality. For a goal about how a page serves its visitor, code could pull the verdict toward code quality. Untested. [gap]
6. **Is a final judge from another family enough?** No: Zhou 2026 found exploits transfer across families and survive a three-family ensemble 55% of the time (single-author preprint, correctness task). Real outcomes or the person remain the audit.
7. **Personas.** SimAB (+~10 points from diversity) and ChatEval (+6 points from diverse roles) support diversity. Hu & Collier (<10% of variance from persona variables) and Dong et al. (personas weak) say thin personas add little. Park et al. suggest the signal lies in grounded, person-specific detail, not demographics.
8. **Stated preference vs real outcomes can diverge.**
   - LOLA (arXiv 2406.02611) [full], on Upworthy:
     - Lay respondents were near random on headline pairs whose click rates differed significantly (4,571 responses).
     - Picking the winner among several headlines (random 33.0%), GPT-4 reached 37.9% zero-shot. Models trained on outcomes reached 45–47%.
   - Spotify (2026) [full blog]: raw gpt-4o-mini predictions recovered only 39% of the observed treatment effect. Only nonlinear calibration on real experiment data reached the human benchmark, and they advise against substituting LLM predictions for experiments.
   - A judge that agrees with what a person *says* may still not predict what people *do*. Where the goal is a behavior, a judge's win is a hypothesis, as the climb ADR already says.
9. **More votes vs diverse votes.** Repeating one judge reduces noise, not bias. The evidence favors spending votes across judges and orders over many samples of one judge. Whether a sequential test on correlated votes keeps its stated error rate is unexamined for LLM judges. [gap]
10. **The judge's rationales in the climb record.** [inf] Feeding them to the proposer is the output-refinement loop that drives in-context reward hacking (Pan et al. 2024). No experiment isolates this inside a climb.
11. **Ceilings are low for subjective design** (designers' α 0.25; 65% crowd agreement without a rubric). An absolute bar such as "90% agreement" may be unreachable even for humans. Bars should be set relative to human–human agreement on the same pairs and reported by human-certainty stratum.
12. **Volatile evidence.** Several of the most directly relevant sources are single-author 2026 preprints (Zhou, Wahi) or changed substantially between versions (WiserUI-Bench v1 to v5). Weigh them accordingly.

---

## 4. Datasets with known winners

| Dataset | Artifact kind | What "known winner" means | Size | License / terms | Provenance |
|---|---|---|---|---|---|
| WiserUI-Bench (arXiv 2505.05026) | UI screenshots | Real A/B test results from public case studies (VWO, goodui.org, abtest.design) | 300 pairs | **CC BY-NC-SA 4.0**, non-commercial research. Raw images are *not* redistributed; source URLs, expert annotations and scripts are. The source platforms grant no explicit redistribution license. | [full] |
| WebDev Arena preference 10k (`lmarena-ai/webdev-arena-preference-10k`) | LLM-built web apps (code) | Arena user votes (A, B, tie, and a fourth class) | ~10,501 battles | Custom "Arena Dataset License Agreement": "limited, non-exclusive, non-transferable, non-sublicensable", research and commercial use subject to its terms | [abs: HF card] |
| WebDevJudge (arXiv 2510.18560) | Web apps (code + screenshots + interactive env) | Expert labels built on rubric trees; inter-annotator agreement 89.7% | 654 pairs (269 A, 276 B, 109 ties) | Repository states no license and ships no raw data; you fetch the WebDev Arena data under its terms | [full + repo] |
| UICrit (google-research-datasets/uicrit) | Mobile UI screenshots (RICO) | Designer ratings and critiques per UI; no pairs, but pairs can be derived from rating gaps | 1,000 UIs, 11,344 critiques | **CC BY 4.0** | [repo README] |
| DesignPref (arXiv 2511.20513) | Generated UI designs | Pairwise choices by 20 designers | 12k pairs | Dataset license not found | [sum] |
| ArtifactsBench (arXiv 2507.04952) | Interactive web artifacts | Expert scores on 280 queries × 6 models | 1,825 tasks | Not checked | [full; license unchecked] |
| Upworthy Research Archive | Headlines and image packages | **Real outcomes**: impressions and clicks per package | 32,487 tests (2013–2015). Exploratory set public (22,666 packages / 4,873 tests); confirmatory set needs a peer-reviewed analysis plan | **CC BY 4.0** (Cornell). Images are not included (IDs only). About 22% of tests (≈ 2013-06-25 to 2014-01-10) may have broken randomization; a column flags them, and the authors discourage causal use of that window. | [official pages] |
| Stanford SHP (`stanfordnlp/SHP`) | Reddit comments (writing) | Revealed preference: comment A preferred when written no later than B yet scored higher | 385,563 pairs, 18 subreddits | No standard license. Scraped under the Reddit API terms; the authors disclaim endorsement of downstream use and reserve the right to change the license. | [HF README] |
| OpenAI summarize-from-feedback | Reddit TL;DR summaries | Trained labelers' choices between two summaries | ~64.8k comparisons | Unclear: repository marked "other"; the TL;DR source is reportedly CC BY 4.0 | [sum] |
| MT-Bench human judgments (`lmsys/mt_bench_human_judgments`) | Chat answers | Expert pairwise preferences | ~3.3k | **CC BY 4.0** | [HF card] |
| Arena human preference 140k (`lmarena-ai/arena-human-preference-140k`) | Chat answers | User votes (A, B, tie, both bad) | 135,634 votes | **CC BY 4.0** for user prompts; model outputs under each provider's terms | [HF card] |
| HelpSteer3 preference (`nvidia/HelpSteer3`) | Chat answers (general, STEM, code, multilingual) | Annotator preference with strength −3…+3 (0 = about the same), up to 3 annotators with reasons | 40,476 | **CC BY 4.0** | [HF card] |
| LLMBar (princeton-nlp/LLMBar) | Instruction-following outputs | Curated; the adversarial worse output has superficially appealing qualities | 419 pairs (100 natural, 319 adversarial) | **MIT** | [repo] |
| JudgeBench (`ScalerLab/JudgeBench`) | Knowledge, reasoning, math and code answers | Objective correctness | 620 pairs | **MIT** | [HF card] |
| RewardBench (`allenai/reward-bench`) | Chat, safety, reasoning | Chosen vs rejected | 2,985 | **ODC-BY**, plus the licenses of its sources | [HF card] |
| FBI perturbations (arXiv 2406.13439) | Text answers | Targeted degradations (known-worse) | 2,400 | Not checked | [abs] |
| Prompts judged by outputs | — | **No dataset of prompt pairs with known winners found.** [gap] | — | — | — |

Two uses follow from this table. [inf]

- **Building known-winner prompt pairs.** TRIPLE and PDO used tasks with checkable answers (BIG-Bench Hard and similar). Measure each prompt on held-out inputs and keep only the pairs whose difference is statistically clear. The judge, reading only the outputs, should then prefer the more accurate prompt.
- **Licensing for a public repository.** CC BY-NC-SA data (WiserUI-Bench) and Arena-licensed data can serve a local measurement. Before derived pairs, screenshots or labels are committed to a public repository, their terms need checking: WiserUI-Bench's images are not redistributable at all.

---

## Source index

URLs of the primary sources cited above:

- https://arxiv.org/abs/2504.14716 — Tripathi et al. (full text: https://arxiv.org/html/2504.14716v2)
- https://arxiv.org/abs/2406.12319 — Jeong et al., The Comparative Trap / PRePair
- https://arxiv.org/abs/2402.04788 — MLLM-as-a-Judge
- https://arxiv.org/abs/2510.18560 — WebDevJudge; https://github.com/lcy2723/WebDevJudge
- https://arxiv.org/abs/2403.16950 — PairS
- https://arxiv.org/abs/2307.07889 — Liusie et al.
- https://arxiv.org/abs/2406.12624 — Thakur et al.
- https://arxiv.org/abs/2402.14016 — Raina et al.
- https://arxiv.org/abs/2305.17926 — Wang et al., Not Fair Evaluators (FairEval)
- https://arxiv.org/abs/2306.05685 — Zheng et al., MT-Bench (full PDF read)
- https://arxiv.org/abs/2406.07791 — Shi et al., position bias
- https://arxiv.org/abs/2404.04475 — Length-controlled AlpacaEval
- https://www.lmsys.org/blog/2024-08-28-style-control — LMSYS style control (summary only)
- https://arxiv.org/abs/2410.07137 — Null models
- https://arxiv.org/abs/2404.13076 — Panickssery et al.
- https://arxiv.org/abs/2410.21819 — Wataoka et al.
- https://arxiv.org/abs/2502.01534 — Preference leakage
- https://arxiv.org/abs/2407.12856 — AI–AI bias
- https://arxiv.org/abs/2307.03025 — Style over substance
- https://arxiv.org/abs/2310.07641 — LLMBar; https://github.com/princeton-nlp/LLMBar
- https://arxiv.org/abs/2504.09946 — Judging bias in large reasoning models
- https://arxiv.org/abs/2507.08794 — One Token to Fool LLM-as-a-Judge
- https://arxiv.org/abs/2404.18796 — PoLL
- https://arxiv.org/abs/2308.07201 — ChatEval
- https://arxiv.org/abs/2310.02743 — Reward model ensembles
- https://arxiv.org/abs/2607.05904 — Zhou 2026, self-play reward hacking of reference-free judges
- https://arxiv.org/abs/2609.02246 — Wahi 2026, deterministic guardrails
- https://arxiv.org/abs/2310.05657 — Chiang & Lee
- https://arxiv.org/abs/2410.12784 — JudgeBench
- https://arxiv.org/abs/2303.16634 — G-Eval
- https://arxiv.org/abs/2403.18771 — CheckEval
- https://arxiv.org/abs/2507.17746 — Rubrics as Rewards
- https://arxiv.org/abs/2507.18624 — Checklists (RLCF)
- https://arxiv.org/abs/2501.00274 — LLM-Rubric
- https://arxiv.org/abs/2402.10811 — Hu & Collier
- https://arxiv.org/abs/2406.11657 — Dong et al., personalized judge
- https://arxiv.org/abs/2411.10109 — Park et al., agents grounded in self-reports
- https://arxiv.org/abs/2404.12272 — EvalGen
- https://hamel.dev/blog/posts/llm-judge/ — Husain, critique shadowing
- https://arxiv.org/abs/2309.13308 — AutoCalibrate
- https://arxiv.org/abs/2406.06560 — Inverse Constitutional AI
- https://arxiv.org/abs/2506.05598 — SynthesizeMe
- https://arxiv.org/abs/2410.13341 — Dorner et al.
- https://arxiv.org/abs/2410.03775 — Elangovan et al.
- https://arxiv.org/abs/2305.14324 — Ties Matter
- https://eugeneyan.com/writing/llm-evaluators/ — Yan (summary only)
- https://arxiv.org/abs/2406.13439 — FBI
- https://arxiv.org/abs/2410.02736 — CALM
- https://arxiv.org/abs/2510.27106 — Rating Roulette
- https://arxiv.org/abs/2412.12509 — Schroeder & Wood-Doughty (summary only)
- https://arxiv.org/abs/2407.18370 — Trust or Escalate
- https://arxiv.org/abs/2407.04549 — Spontaneous reward hacking in iterative self-refinement
- https://arxiv.org/abs/2402.06627 — Feedback loops and in-context reward hacking
- https://arxiv.org/abs/2409.12822 — Language models learn to mislead humans
- https://arxiv.org/abs/2507.04952 — ArtifactsBench
- https://arxiv.org/abs/2410.10934 — Agent-as-a-Judge
- https://arxiv.org/abs/2411.17451 — VL-RewardBench
- https://arxiv.org/abs/2407.08850 — UICrit; https://github.com/google-research-datasets/uicrit
- https://arxiv.org/abs/2404.12500 — UIClip
- https://arxiv.org/abs/2505.05026 — WiserUI-Bench (v1 and v5 read)
- https://arxiv.org/abs/2510.08783 — MLLM as a UI Judge (summary only)
- https://arxiv.org/abs/2504.09407 — UXAgent (summary only)
- https://arxiv.org/abs/2411.00640 — Miller, Adding Error Bars to Evals
- https://engineering.atspotify.com/2026/8/when-can-llms-replace-humans-in-a-b-tests/ — Spotify Engineering
- https://arxiv.org/abs/1512.04922 — Johari et al., always-valid inference
- https://aclanthology.org/2026.findings-acl.43 — Arviv et al., sequential evaluation
- https://arxiv.org/abs/2402.09723 — TRIPLE
- https://arxiv.org/abs/2203.06063 — Active Evaluation
- https://arxiv.org/abs/2510.13907 — Prompt Duel Optimizer
- https://arxiv.org/abs/2406.02611 — LOLA (Upworthy headline prediction)
- https://www.nature.com/articles/s41597-021-00934-7 and https://upworthy.natematias.com/about-the-archive — Upworthy Research Archive
- Hugging Face cards: lmarena-ai/webdev-arena-preference-10k, lmsys/mt_bench_human_judgments, lmarena-ai/arena-human-preference-140k, nvidia/HelpSteer3, stanfordnlp/SHP, ScalerLab/JudgeBench, allenai/reward-bench
