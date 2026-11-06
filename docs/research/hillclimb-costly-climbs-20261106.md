# Climbing when measuring is costly, the artifact is large, or real use is thin: evidence review

Date: 2026-11-06. Question: how should an automated hill-climb (make a change, measure it, keep it
only on a confirmed gain, stop when changes stop paying) choose what to try, stage and batch its
measurements, handle large artifacts and a changing objective, and test on real use when traffic
is low, so that one short guidance serves any artifact and any measure?

Two earlier notes cover AI judges (pairwise judging, bias controls, reward hacking in loops,
successive halving and sequential stopping for comparisons) and several objectives (guardrails,
Pareto, Goodhart, metric validity). This note cites them only where it builds on them:
`hillclimb-ai-judges-20261106.md` (the judge note) and `hillclimb-several-objectives-20261106.md` (the
objectives note).

## Provenance tags

- **[full]** I read the passage in the source itself. For long HTML papers the fetch tool read the
  first ~100k characters, which held every result cited here; for PDFs I extracted the text and
  read the cited sections.
- **[abs]** abstract or official summary only.
- **[sum]** a search summary or secondary write-up; not verified.
- **[calc]** my own arithmetic.
- **[inf]** my inference from the evidence, not a reported finding.

Each LLM result gives its year and, where the source names them, its models. Results from 2023
models (GPT-3.5, early GPT-4, PaLM 2) show a mechanism; its size with 2026 models is not known here.

---

## 1. Strongest practices

1. **Give the proposer the raw evidence of what went wrong, not only a score or a summary.** In
   harness search, a proposer that read raw execution traces reached a median accuracy of 50.0
   against 34.6 for scores only and 34.9 for scores plus an LLM summary. Best source: Lee et al.,
   *Meta-Harness* (2026), Table 3 **[full]**. Self-Refine's specific feedback beat generic
   feedback, which beat none **[full]**; human-written diagnoses raised GPT-4's repair rate 1.58×
   (Olausson et al., ICLR 2024) **[full]**.
2. **Diagnose the limiter before changing, and point the change at it.** A profiler-guided loop
   doubled expert-matching patches over a plain coding agent (19.6% to 39.2% on GSO with GPT-5.1)
   and beat an oracle best-of-five sampling baseline at lower cost. Best source: Deng et al.,
   *PerfAgent* (2026) **[full]**. MLE-STAR's ablation-picked block refinement lifted Kaggle medals
   from 25.8% (AIDE) to 43.9% with the same model **[full]**.
3. **When feedback is weak, sample several independent candidates instead of repairing one.**
   At a matched budget, more initial samples beat more repairs per sample; self-repair was "not a
   silver bullet". Best source: Olausson et al. (ICLR 2024; GPT-3.5, GPT-4, Code Llama) **[full]**.
   Snell et al. (2024): easy problems gain from sequential revision, hard ones from a mix of
   sequential and parallel **[full]**.
4. **The quality of the change operator matters more than the search policy around it.** With
   AIDE's operators, greedy, MCTS and evolutionary search performed about the same; better
   operators lifted all of them. Best source: Toledo et al., *AIRA-dojo* (NeurIPS 2025; R1, o3)
   **[full]**.
5. **Keep a population only when greedy stalls; greedy-from-best is a strong default.** ShinkaEvolve
   found hill climbing "strong initially" but plateauing, and weighted parent sampling better
   **[full]**. Hill Sampling (2026) found greedy edits to the best verified program beat repeated
   sampling and evolution on three math tasks **[abs]**. These conflict (section 3).
6. **Stage evaluation from cheap to expensive, and let only survivors reach the expensive stage.**
   AlphaEvolve's evaluation cascade **[full]**; GEPA's minibatch-then-validation gate **[full]**;
   PerfAgent's coverage-selected tests cut test runs by 47–99% **[full]**; Hyperband **[abs]**.
7. **Validate a cheap proxy by how often it makes the same decision as the expensive measure, and
   expect it to fail outside the conditions it was checked in.** DataDecide: small-scale rankings
   picked the better of two pretraining corpora at 1B scale ~80% of the time, at 0.01% of the
   compute **[abs]**. GSO's hidden workloads caught speedups that held only on the provided script
   **[full]**. Lab and field web performance diverge for at least eight named reasons (web.dev)
   **[full]**.
8. **Score the final pick on data the climb never selected on.** Choosing the final node by test
   instead of validation score added 9–13 points in MLE-bench agents, and long searches overfit
   validation (AIRA-dojo) **[full]**. MLE-STAR's leakage case raised validation accuracy while test
   accuracy fell from 0.803 to 0.734 **[full]**.
9. **Assume the measure will be gamed, and harden it before the climb, not after.** AlphaEvolve's
   math runs "always eventually" found a way to cheat a numerical-integration scorer (Georgiev,
   Gómez-Serrano, Tao & Wagner 2025) **[full]**. Caching inside timing loops was the most common
   hack in code-speed benchmarks (PerfAgent) **[full]**. Sakana's AI CUDA Engineer withdrew 10–100×
   speedup claims after an evaluator exploit (2025) **[sum]**.
10. **When a batch of changes fails, search for the culprit with a method that models noise.**
    Plain bisection misattributes flaky failures; rerunning each step k times plateaus in accuracy
    while cost grows linearly. A Bayesian noisy binary search was more accurate at similar cost.
    Best source: Henderson et al., *Flake Aware Culprit Finding* (Google, ICST 2023) **[full]**.
11. **Expect interactions between independent changes to be rare, but not absent.** Across four
    Microsoft products and hundreds of thousands of pair-metrics, interaction p-values were
    consistent with chance in three and flagged 1 in 50,000 in the fourth (Microsoft ExP, 2023)
    **[full]**.
12. **On real use, compute the minimum detectable effect before testing.** At 80 users a variant,
    power to detect a 10% lift was 3%, and an "outstanding" winner had a 63% false-positive risk
    (Kohavi, Deng & Vermeer, KDD 2022) **[full]**. At about 100 visitors a week, a 5% conversion
    rate needs a relative lift near 70% to be detectable in 12 weeks **[calc]**.
13. **With little traffic, test fewer, bolder variants; with fat-tailed ideas, test more ideas
    cheaply.** The optimal split depends on how fat the tail of idea quality is (Azevedo et al.,
    JPE 2020, estimated on Bing) **[abs]**.
14. **If anyone will look at a running test, use a sequential test.** "Regardless of the specific
    sequential test chosen, it is critical to use one" (Spotify, 2023) **[full]**.
15. **Default to a light search, but measure where its curve flattens.** Gains are front-loaded
    in Self-Refine (code optimization +5.0, then +0.9 and +0.9 points) **[full]** and MLE-STAR
    **[full]**, but not always: PerfAgent's speedup kept rising over five turns (2.5× to 6.4×)
    **[full]**. DSPy ships "light", "medium" and "heavy" presets with light as the default
    **[full, source code]**.

---

## 2. Findings by topic

### 2.1 Choosing what to try: diagnosis, sampling, or population

**Rich feedback beats scores, and raw beats summarized.**

- **Meta-Harness** (Lee, Nair, Zhang, Lee, Khattab & Finn, arXiv 2603.28052, March 2026) **[full]**.
  Proposer: Claude Code with Opus-4.6; task model GPT-OSS-120B; online text classification.

  | Proposer sees | Median acc. | Best acc. | Runs beating zero-shot |
  |---|---|---|---|
  | Scores only | 34.6 | 41.3 | 26 |
  | Scores + LLM summary | 34.9 | 38.7 | 23 |
  | Raw execution traces | 50.0 | 56.7 | 39 |

  - "Summaries do not recover the missing signal, and may even hurt by compressing away
    diagnostically useful details."
  - The proposer read a median of 82 files an iteration, about half of them traces. After repeated
    regressions it diagnosed a confound in a bundled edit and switched to a purely additive change,
    which became its best candidate (TerminalBench-2 run).
  - Cost: about 10 MTok of context an iteration, against 0.002–0.026 MTok for text optimizers. It
    claims comparable results with about 10× fewer full evaluations than OpenEvolve; the factor is
    stated inconsistently in the paper.
- **Self-Refine** (Madaan et al. 2023; GPT-3.5, ChatGPT, GPT-4) **[full]**. Specific feedback beat
  generic feedback, which beat none: code optimization 27.5 / 26.0 / 24.8; sentiment reversal
  43.2 / 31.2 / 0 ("the task fails without feedback").
- **Olausson et al., *Is Self-Repair a Silver Bullet?*** (ICLR 2024; Code Llama, GPT-3.5, GPT-4;
  HumanEval, APPS) **[full]**.
  - At a matched budget, GPT-4 on APPS: 10 initial samples with 1 repair each reached 1.05× the
    pass@20 baseline; 2 initial samples with 10 repairs each reached 0.97×.
  - "The diversity of the base samples that are generated up-front" mattered more than repairs.
  - Feedback quality is the bottleneck: a stronger model's feedback helped substantially, and human
    explanations raised GPT-4's repair rate from 33.3% to 52.6%. On competition problems: 3.67% to
    14.67%.
- **PerfAgent** (Deng et al., arXiv 2607.19653, July 2026; GPT-5.1 and Kimi-K2) **[full]**.
  - A sampling profiler's output is aggregated into hotspots (location, call stack, share of
    samples, self-time and total time), then condensed by a separate LLM call, because raw output
    "would flood the agent's context with detail that buries the real bottleneck".
  - Results with GPT-5.1: expert-matching rate 19.6% to 39.2% on GSO and 26% to 74% on
    SWE-fficiency-Lite. It "surpasses an oracle best-of-five baseline at substantially lower cost,
    showing that the gains come from better feedback rather than additional test-time sampling."
  - It reached native code (C, C++, Cython, Rust) on 48% of GSO tasks against 31% for the baseline:
    the limiter often sat below the layer the agent would have edited.
  - Its Sp@1 threshold is 1.2× speedup, "large enough to remove patches that may achieve speedup
    solely due to timing variance".
- **GEPA** (Agrawal et al. 2025, ICLR 2026; Qwen3 8B, GPT-4.1 Mini) **[full]**. Reflection on
  execution traces plus textual feedback beat MIPROv2 (aggregate 65.22 against 58.67 on GPT-4.1
  Mini) and matched GRPO's best validation in 243–1,179 rollouts against GRPO's 24,000. The paper
  has no score-only ablation, so the share due to feedback is not isolated. Its Pareto parent
  sampling is in the objectives note.
- **MLE-STAR** (Nam et al., arXiv 2506.15692, 2025; Gemini-2.0-Flash, Gemini-2.5-Pro) **[full]**.
  An ablation agent disables or alters pipeline components, picks the block with the largest
  effect, and refines that block in an inner loop (4 outer × 4 inner). Any-medal rate on
  MLE-bench Lite: 25.8% (AIDE) to 43.9% with Gemini-2.0-Flash; 63.6% with Gemini-2.5-Pro. No
  controlled comparison against whole-script refinement is reported.

**Sampling several candidates: when it wins.**

- **Snell et al. 2024** (arXiv 2408.03314; PaLM 2-S*, MATH) **[full]**.
  - "Easy questions benefit more from sequential revisions"; on hard questions "it is optimal to
    strike a balance between sequential and parallel computation".
  - Beam search against a process reward model degraded on easy questions as budget grew
    ("exploitation of the PRM signal") and beat best-of-N on harder ones. On the hardest, "no method
    makes much meaningful progress".
  - Adaptive allocation per prompt was more than 4× as efficient as best-of-N **[abs]**.
- **Large Language Monkeys** (Brown et al. 2024; DeepSeek-Coder-V2 and others) **[abs]**. Coverage
  grows roughly log-linearly with samples over four orders of magnitude. SWE-bench Lite: 15.9% with
  one sample, 56% with 250. Where answers can be checked, coverage becomes performance; where they
  cannot, majority voting and reward models plateau after a few hundred samples.

**Population vs greedy.**

- **AlphaEvolve** (Novikov et al. 2025; Gemini 2.0 Flash and Pro) **[full]**. Ablations on tensor
  decomposition and kissing numbers: removing evolution (resampling the initial program), problem
  context, meta-prompt evolution or full-file evolution, or using only a small model, each lost
  "significant" performance. Effect sizes are in a figure only. "Thousands of LLM samples suffice"
  against FunSearch's millions.
- **AIRA-dojo** (Toledo et al., NeurIPS 2025; DeepSeek R1, o3) **[full]**. With AIDE's operators
  (draft, debug, improve), greedy, MCTS and evolutionary search "gain no advantage" over each other:
  "AIDE's operators, rather than the search algorithm, are a bottleneck". Better operators: greedy
  39.8% to 45.5%; MCTS about 47%. The environment alone moved AIDE-greedy from 35.2% to 45.9%.
- **ShinkaEvolve** (Lange, Imajuku & Cetin, Sakana, Sept 2025) **[abs + full ablation section]**.
  New best circle packing in 150 samples. On circle packing, "hill climbing shows strong initial
  performance but plateaus quickly"; weighted parent sampling did better. Embedding-based
  novelty rejection gave "substantial" gains; an LLM novelty judge added little. A bandit over an
  LLM ensemble beat a single model and a fixed ensemble.
- **Hill Sampling** (Beck, Ogren & Kobren, arXiv 2609.25510, Sept 2026; three open-weight models)
  **[abs]**. Repeatedly sampling edits to the best verified program beat repeated sampling and
  evolution strategies on circle packing, sums and differences of sets, and Erdős' minimum overlap.
  They advise trying this before archives, diversity mechanisms or evolutionary scaffolds.
- **Evolution or Illusion?** (Oved et al., IBM, arXiv 2609.19799, Sept 2026) **[abs]**. On five
  tasks and three strategies, rankings flipped with the number of seeds: one strategy worst at one
  seed was best at forty. On one task the best iteration count was "well below common practice",
  and more seeds would have scored more. One seed at one budget cannot rank methods.
- **Mathematical exploration at scale** (Georgiev, Gómez-Serrano, Tao & Wagner, arXiv 2511.02864,
  Nov 2025; AlphaEvolve) **[full]**. 20 parallel threads beat the record "much faster" than 2.
  The cheapest model was the most cost-effective on one problem (a few USD in total, about twice
  as many calls) but "was not able to get the most elaborate constructions" on harder ones.

**Application.** [inf]

- Two dials pick the strategy: how much a measurement costs, and how much its feedback says about
  *why* a candidate lost.
  - Rich, cheap feedback (a profile, failing cases, a trace): diagnose and make one targeted
    change per round, greedy from the current best.
  - Rich but costly feedback: the same, with fewer, larger-bet changes, each aimed at the limiter.
  - Poor feedback (a single number or a verdict without reasons): sample several independent
    candidates per round; diversity beats repairing one.
  - Greedy stalls on a hard problem: widen to a small population of diverse runners-up, reject
    near-duplicates, and spend on more independent starts before more depth.
- A climb that stalls should first suspect its change operator (what the proposer sees and is
  allowed to change) before its search policy.
- The proposer's raw evidence is what matters; but the judge note warns that feeding the *judge's*
  rationales back to the proposer drives in-context reward hacking. Raw evidence about the
  artifact (traces, profiles, failing inputs) is different from the judge's opinion of it.

### 2.2 Staged and multi-fidelity evaluation

**Mechanisms.**

- **Evaluation cascade** (AlphaEvolve) **[full]**: "ensembles of test cases of increasing
  difficulty"; a candidate moves on "only if [it achieves] sufficiently promising results in all
  earlier stages". New solutions are "evaluated on a small scale before being subjected to the main
  test cases". The pipeline is asynchronous and "optimized for throughput", which makes about 100
  compute-hours per evaluation feasible.
- **GEPA** **[full]**: a candidate is scored on a minibatch, and only if it improves there is it
  scored on the full Pareto set. "The majority of GEPA's rollout budget is spent on validation."
- **PerfAgent** **[full]**: after each turn, only the tests whose coverage touches the patch run
  (pytest-testmon), cutting test runs by 66–99% on GSO and 47–98% on SWE-fficiency-Lite, and
  correctness of the final patch rose.
- **Hyperband / successive halving** (Li et al., JMLR 2018) **[abs]**: allocate a small budget to
  many configurations and keep the best fraction at each rung; over an order of magnitude faster
  than Bayesian optimization on its benchmarks. Its implicit premise is that low-budget rank
  predicts high-budget rank **[inf]**. Successive halving for LLM comparisons (TRIPLE) is in the
  judge note.
- **Small evaluation subsets.** tinyBenchmarks (Polo et al., ICML 2024): 100 curated items
  estimated a model's MMLU score from 14k **[abs]**. Estimating one score is easier than ordering
  two close candidates, which needs the difference's error, not each score's **[inf]**.

**Validating a proxy against the expensive measure.**

- **Decision accuracy.** DataDecide (Magnusson et al., ICML 2025): the share of pairwise choices
  at small scale that match the large-scale choice. About 80% at 150M parameters for 1B targets,
  at 0.01% of the compute. Continuous likelihood proxies beat discrete accuracy. None of 8
  scaling-law extrapolations beat simply ranking at one small scale **[abs]**.
- **Known-bad must fail.** The objectives note covers deliberate degradation (Kohavi 2012; Deng &
  Shi 2016) and the judge note covers perturbation batteries. A cheap stage that cannot reject a
  known-broken version is not a filter **[inf]**.
- **A proxy can track something else.** In neural architecture search, many zero-cost proxies did
  not consistently beat the parameter count as a predictor (as summarized by the ZiCo authors,
  ICLR 2023, citing Ning et al. 2021 and White et al. 2022) **[sum]**.
- **Noise floor of the expensive measure.** GSO and SWE-fficiency count only speedups ≥1.2× to
  exclude timing variance (PerfAgent) **[full]**. Changing only the UNIX environment size or link
  order moved execution time by about 33% typically and almost 300% once (Mytkowicz et al., ASPLOS
  2009); none of 133 surveyed papers handled such bias. The remedy is setup randomization. This
  classic result still holds for any timing measure **[sum]**.

**When the proxy's conditions differ from real use.**

- **One input vs many.** GSO scores speed on hidden workloads; SWE-fficiency only on the provided
  script. Opt@1 scores were "much lower" on GSO because "the agent's changes may yield high
  speedups on the provided workload, but fail to generalize to unseen inputs" **[full]**.
- **Test machine vs the person's device.** Lab vs field web performance (Walton, web.dev)
  **[full]**: fixed device and network against a spread; cold cache against warm; no real
  interaction; viewport changes which element counts as largest; personalized content loads later;
  lab layout shift counts only load-time, above-the-fold shifts; responsiveness to input has no
  value without real input.
- **Validation vs the outcome.** AIRA-dojo: validation kept rising while test performance
  plateaued and slightly declined over 24 h; MCTS began to overfit around 50 h in a 90 h run
  **[full]**.
- **Still vs moving.** The judge note found that three staged screenshots beat one (ArtifactsBench).
  I found no study comparing still captures with motion or timing for judging animated artifacts
  **[gap]**.
- **The scorer itself.** AlphaEvolve's math runs exploited numerical integration ("always
  eventually figured out a way to cheat by suggesting a highly irregular function") and discrete
  approximations of continuous constraints ("leaky verifier"). "Designing a clever verifier that
  avoids this behavior is key" **[full]**. Code-speed agents cached results inside timing loops
  (PerfAgent) **[full]**.

**Application.** [inf]

- Order stages by cost and by how much each rejects: hard requirements and correctness first
  (cheap, decisive), then the cheap proxy, then the expensive measure for the few that survive.
- Before relying on a cheap stage, run it on pairs whose expensive verdict is known and record
  how often it agrees, and check that a known-bad version fails it.
- Name, for the proxy, each condition that differs from real use: device, timing or motion, input
  set, data state, load, cache, the person. Each difference is a reason to confirm the final
  version under the real condition, not a reason to distrust every proxy step.
- Re-check the proxy when the kind of change shifts: a proxy validated on small edits may not hold
  for a restructure (the extremal Goodhart case in the objectives note).

### 2.3 Batched confirmation, interactions and culprit finding

- **Interactions are rare in practice for independent changes.** Microsoft ExP (2023), four
  products, every concurrent test pair on a chosen day: three products showed no excess of small
  interaction p-values after Benjamini–Hochberg; the fourth showed about 1 in 50,000 pair-metrics.
  None of the flagged cases had opposite-signed significant effects. Isolate tests "only when you
  suspect they will interact" **[full]**. These were tests owned by different teams; changes made
  by one climb to one artifact touch the same parts more often **[inf]**.
- **Bundled edits confound attribution.** Meta-Harness's proposer traced repeated regressions to a
  bundled prompt-template change and then made a purely additive change **[full]**. PerfAgent keeps
  "the best patch (Turn 4, 5.87×), not the last (Turn 5, 5.85×, which regresses)" **[full]**.
- **Bisection under noise.** Flake Aware Culprit Finding (Henderson et al., ICST 2023; 13,600
  breakages, ~40% with no culprit) **[full, authors' HTML]**.
  - Plain bisection has no model of flaky results, so a flake misdirects it. Rerunning each step
    k times: "accuracy plateaus while build cost continues to increase linearly".
  - A Bayesian noisy binary search (one probability per suspect plus one for "no culprit") was
    more accurate than every bisection variant at close to its cost, and often found the culprit
    in two builds when priors were good.
- **Delta debugging** (Zeller, ESEC/FSE 1999; Zeller & Hildebrandt 2002) **[sum]**: isolates the
  failure-inducing subset of changes, and extends bisection to changes that interfere or are
  inconsistent in isolation. One failure among 178,000 changed GDB lines was isolated in hours.
  Classic; the algorithm still applies wherever subsets of changes can be applied and measured.

**Application.** [inf]

- Where measurement is cheap, one change per measured step keeps attribution free.
- Where it is expensive, a batch is reasonable when each change already passed the cheap stages
  and they touch different parts. Confirm the batch in one expensive run.
- If the batch underdelivers, the sum of cheap-stage gains did not carry: bisect by halves, with a
  noise model (repeat only the ambiguous halves, or update a probability per suspect), and include
  "no culprit, just noise" as a hypothesis.
- If two changes touch the same part or the same mechanism, confirm them separately or as a
  designed pair (each alone and both), since that is where interactions live.

### 2.4 Large artifacts: one part at a time vs jointly

- **Targeted blocks help when a diagnosis picks them.** MLE-STAR's ablation-chosen block refinement
  (2.1) **[full]**; PerfAgent's hotspots (2.1) **[full]**; AlphaEvolve lets a user mark the blocks
  to evolve and asks for SEARCH/REPLACE diffs on large code **[full]**.
- **Restricting to one block can cost.** AlphaEvolve's "no full-file evolution" ablation (evolve
  only the loss function, tensor decomposition) lost significant performance against evolving the
  whole file **[full]**.
- **Joint vs separate optimization of prompt modules.** MIPRO (Opsahl-Ong et al., EMNLP 2024;
  Llama-3-8B) optimizes instructions and demonstrations of several modules together, addressing
  credit assignment across modules, and beat baselines on 5 of 7 programs by up to 13% **[abs]**.
  GEPA instead mutates one module at a time, round-robin, and still won (2.1) **[full]**.
- **Classic theory that still holds.** Cooperative co-evolution splits variables into groups and
  optimizes each with the others fixed; it fails when interacting variables land in different
  groups, and a decomposition that keeps interacting variables together "noticeably" improves
  results (Omidvar et al., IEEE TEC 2014, differential grouping) **[sum]**. Coordinate-wise search
  converges to points where no single part can improve alone, which need not be the joint best
  **[inf, standard result]**.

**Application.** [inf]

- Default: improve the part the diagnosis names, hold the rest fixed, guard the whole with the
  cheap checks, and measure the whole artifact, not the part in isolation.
- Signs that parts must move together: improving one part changes what is best for another; the
  measure only moves when two parts change at once; one part's best value depends on the other's
  setting. Then group those parts into one block.
- The parts the diagnosis never names are where coordinate-wise search stalls; an occasional
  whole-artifact pass (or a bold candidate) tests whether a different structure beats the sum of
  local bests.

### 2.5 Changing the objective mid-search

Direct evidence is thin.

- **Warm starts can generalize worse.** Neural networks initialized from a previous solution
  generalized worse than fresh ones at similar training loss; fixes tended to cancel the saved time
  (Ash & Adams, NeurIPS 2020) **[abs]**. The analog is weak: a network's weights, not an
  artifact under edit **[inf]**.
- **Stored diversity helps adaptation.** A robot with an archive of diverse high-performing
  behaviors adapted to damage in under two minutes by trial and error over that archive (Cully et
  al., Nature 2015; MAP-Elites) **[abs]**. What was kept because it was *different*, not because
  it was best, became useful when the objective changed.
- **Transfer can be negative.** Transfer in Bayesian optimization hurts when source and target
  tasks differ too much (Suder et al. 2023, review) **[sum]**.
- **Carried-over work kept most of the gain in one LLM case.** A GEPA prompt optimized on Qwen3 8B
  reached 62.03 on GPT-4.1 Mini, against 53.03 baseline and 65.22 when optimized on GPT-4.1 Mini
  directly **[full]**: about 74% of the direct gain **[calc]**. That is a changed model, not a
  changed objective.
- I found no 2024–2026 study testing whether an LLM-driven search should reuse its archive after
  its objective or evaluator changes **[gap]**. The nearest work warm-starts across related tasks
  under one shared objective (EMO-STA, 2026) **[sum]**.

**Application.** [inf]

- Old scores were computed under the old measure: re-measure the current best *and the original*
  under the new one before deciding anything.
- Continue from the current best when the new objective agrees with the old on the changes already
  kept (re-measure confirms they still help or are neutral). Restart from the original when the
  kept changes now hurt, or when the new objective rewards a direction the climb moved away from.
- Keep the record of what was tried as hypotheses for the new objective, not as verdicts. Runners-up
  kept for diversity are the most useful carry-over.

### 2.6 Testing on real use with little traffic

**What low power does.** Kohavi, Deng & Vermeer, *A/B Testing Intuition Busters* (KDD 2022)
**[full]**:

- A test with about 80 users a variant had 3% power to detect a 10% relative lift (41,642 users a
  variant were needed for 80% power at a 3.7% base rate). Its reported 300%+ conversion lift had a
  false-positive risk of 63% even at the most optimistic prior.
- False-positive risk among significant results, by historical success rate and power:

  | Success rate | 80% power | 50% power | 20% power |
  |---|---|---|---|
  | 33% (Microsoft) | 5.9% | 9.1% | 20.0% |
  | 15% (Bing) | 15.0% | 22.1% | 41.5% |
  | 10% (Booking, Google Ads, Netflix) | 22.0% | 31.0% | 52.9% |
  | 8% (Airbnb search) | 26.4% | 36.5% | 59.0% |

- Below 10% power, the chance of getting the sign wrong approaches 50%; below 50% power, effect
  estimates are badly exaggerated (Gelman & Carlin 2014, cited).
- "A/B tests are useful to detect effects of reasonable magnitudes when you have, at least,
  thousands of active users, preferably tens of thousands."
- Surprising results should be replicated (Twyman's law).

**What is detectable at about 100 visitors a week.** [calc] Two equal arms, two-sided α = 0.05, 80%
power, normal approximation (rough at these counts). Smallest detectable *relative* lift:

| Weeks | Visitors | Base 2% | Base 5% | Base 10% | Base 30% |
|---|---|---|---|---|---|
| 4 | 400 | 196% | 122% | 84% | 43% |
| 12 | 1,200 | 113% | 71% | 49% | 25% |
| 26 | 2,600 | 77% | 48% | 33% | 17% |
| 52 | 5,200 | 54% | 34% | 23% | 12% |

- Relaxing to α = 0.10 one-sided shrinks these by about a quarter (12 weeks at 5%: 53%).
- A continuous per-visitor measure detects a standardized difference of about 0.16 SD in 12 weeks.
- Power for a 20% lift at a 5% base: 12% after 12 weeks, 38% after a year. At 20% power and a 20%
  success rate, about one in three significant wins would be false; at 10% power, half.
- Credible at this traffic: a large difference on a frequent event, decided over months, with the
  decision rule and stopping rule fixed in advance. Not credible: a small lift on a rare event, or
  any lift seen within a few weeks.

**Sequential testing.**

- Fixed-sample p-values are invalid under repeated looks (Johari et al.; in the judge note).
- Spotify (Schultzberg & Ankargren, 2023) **[full]**: a group sequential test with alpha spending
  had about 0.90 power with 14 looks in their simulation, against 0.67–0.77 for always-valid tests
  (mSPRT, GAVI). Always-valid tests suit unknown sample sizes and streaming data; group sequential
  tests suit a known maximum and batches. Statsig's corrected-alpha approach did not bound false
  positives under peeking. "It is critical to use one."

**Bayesian approaches.**

- Bayesian monitoring is valid under continuous looks only "when proper stopping rules are used"
  (Deng, Lu & Chen 2016) **[abs]**. A Bayesian label does not by itself fix peeking.
- Priors learned from past experiments (Deng, WWW 2015, used at Bing over thousands of
  experiments) shrink small-sample estimates toward realistic effect sizes **[sum]**. A site with
  few past tests has no such prior; a skeptical prior centered on zero with the spread of published
  success rates is the honest stand-in [inf].

**Variance reduction.**

- CUPED (Deng, Xu, Kohavi & Walker, WSDM 2013) used each user's pre-experiment value of the same
  metric as a covariate and cut variance about 50% at Bing, halving the sample needed **[abs]**.
  It needs pre-period data per unit; new visitors have none, so low-traffic sites with mostly
  first visits gain little (Statsig docs; Kameleoon) **[sum]**.
- Within-unit comparisons are the larger lever where they fit: interleaving two rankers inside one
  result list agreed with A/B outcomes up to 22% more often, over 50% error reduction, in 38 tests
  (Chapelle et al., TOIS 2012) **[abs]**. Classic, still standard for rankers.

**Bold vs incremental.**

- When most of the value comes from rare large wins (fat tails), many cheap, small tests beat a few
  large ones; with thin tails, the reverse. Bing's estimate showed very fat tails (Azevedo, Deng,
  Montiel Olea, Rao & Weyl, JPE 2020) **[abs]**.
- At low traffic only large effects are detectable at all (table above), so an incremental variant
  cannot be confirmed; a bold one can, and either outcome teaches something [inf].

**Before/after comparisons.**

- A before/after comparison confounds the change with everything else that changed in the window:
  season, campaigns, releases, traffic mix, novelty. The counterfactual has to be modeled, e.g.
  from control series the change did not affect (CausalImpact, Brodersen et al., AOAS 2015)
  **[abs]**.
- Regression to the mean: a change made *because* a metric dipped will look like a fix when the
  metric returns [inf, standard result].

**Finding problems instead of measuring lifts.**

- Five-user usability tests found 85% of known problems on average, but single samples of five
  ranged from nearly 100% down to 55% (Faulkner 2003, 100 simulations) **[sum]**. Classic, still
  holds: small qualitative samples find what is broken; they do not measure how much better a
  version is.

### 2.7 Light vs thorough search

- **Front-loaded gains.**
  - Self-Refine (2023), average of three models **[full]**: code optimization 22.0 → 27.0 → 27.9 →
    28.8; constrained generation 29.0 → 40.3 → 46.7 → 49.7. "The marginal improvement naturally
    decreases with more iterations", and on multi-aspect tasks performance "may not always
    monotonically increase".
  - MLE-STAR (2025) **[full]**: largest gains in early refinement steps, attributed to the ablation
    targeting the most influential block first.
  - Meta-Harness (2026) **[full]**: matched competitors' final accuracy within its first 4
    evaluations.
  - ShinkaEvolve (2025) **[full]**: hill climbing plateaus quickly.
- **Gains that keep coming.** PerfAgent **[full]**: average speedup rose monotonically from 2.5× at
  turn 1 to 6.4× at turn 5 on GSO, while validation failures fell from 53 to 5; "simply prompting
  the agent to keep going is not enough: without a concrete target … it tends to stop again after a
  marginal change". AIRA-dojo **[full]**: greedy gained 6 more points between 24 and 90 hours
  before overfitting.
- **Long searches overfit their measure.** AIRA-dojo (validation up, test flat or down) **[full]**;
  MLE-STAR's leakage case **[full]**; AlphaEvolve's cheating scorers **[full]**. Longer search
  raises the winner's curse described in the objectives note [inf].
- **Width vs depth.** "Evolution or Illusion?" (2026): the best split between independent seeds
  and iterations depends on task and budget, and on one task fewer iterations and more seeds won
  **[abs]**. AlphaEvolve math: 20 parallel threads reached the record much faster than 2 **[full]**.
  MLE-bench (2024): pass@k and longer time budgets raised medal rates **[abs]**.
- **Practitioner defaults.** DSPy's optimizers default to `auto="light"`: MIPROv2 light uses 6
  candidates and a 100-example validation set, medium 12 and 300, heavy 18 and 1000; GEPA uses the
  same 6/12/18 candidate counts **[full, dspy source]**.

**Application.** [inf]

- A quick default (a few rounds, stop after rounds without a confirmed gain) captures the
  front-loaded part when the proposer is diagnosis-led.
- A thorough option should add width (independent starts, more candidates) before depth, and must
  end with a held-out check, since the thorough run is the one most likely to overfit its measure.
- A plateau after a few rounds is a reason to change what the proposer sees or may change, before
  it is a reason to stop; stop when that change also fails to pay.

---

## 3. Conflicts and gaps

1. **Greedy-from-best vs population.** Hill Sampling (2026, abstract) finds greedy edits to the
   best program beat evolution; ShinkaEvolve (2025) finds hill climbing plateaus and weighted
   sampling wins; AlphaEvolve finds "no evolution" worse, but its "no evolution" resamples the
   *initial* program, a weaker baseline than greedy-from-best. AIRA-dojo finds search policy
   secondary to operators. "Evolution or Illusion?" shows one-seed comparisons can reverse these
   rankings, which weakens all of them. Reconciliation [inf]: start greedy; widen when it stalls;
   do not trust a strategy comparison from one run.
2. **Raw vs summarized diagnostics.** Meta-Harness: summaries hurt. PerfAgent: condensing raw
   profiler output helped, because raw output buried the bottleneck. The settings differ: an agent
   that can open files can drill into raw traces on demand, while a profile dumped into a prompt
   cannot be navigated [inf]. A plausible rule: give access to raw evidence, plus an index or
   summary that points into it.
3. **Repair vs resample.** Olausson (2023 models): resample wins when feedback is weak. PerfAgent
   and Meta-Harness (2026 models): feedback-driven iteration beats sampling. Both fit one rule:
   iteration pays in proportion to feedback quality.
4. **Targeted block vs whole artifact.** MLE-STAR's targeted blocks won; AlphaEvolve's
   block-only ablation lost. MLE-STAR picked the block by measured ablation; AlphaEvolve's
   restriction was fixed in advance [inf].
5. **Front-loaded vs continued gains.** Self-Refine, MLE-STAR and Meta-Harness show early gains;
   PerfAgent shows steady gains over five turns when given a concrete target and re-checking. The
   difference may be whether each turn gets fresh, specific feedback [inf].
6. **Interactions.** Microsoft finds them rare across independent tests; climbs bundle changes to one
   artifact, where confounds were observed (Meta-Harness). No study measures interaction rates
   among changes inside one optimization run [gap].
7. **Gaps.**
   - No study of still captures vs motion for judging animated artifacts.
   - No study of objective changes inside an LLM-driven search.
   - No published decision-accuracy figures for common cheap proxies of user-facing artifacts
     (lab speed vs field speed decisions, judge vs real behavior beyond the judge note's LOLA and
     Spotify results).
   - Several 2026 sources are preprints read only in abstract (Hill Sampling, Evolution or
     Illusion?); PerfAgent and Meta-Harness are single-group 2026 preprints.

---

## 4. Recommendation for a general climb guidance (all of this section is my inference)

Phrased for any artifact and any measure. "The measure" is whatever decides a gain: a number, a
suite, a judge, or a test on real use. "Real conditions" are those the artifact's people meet.

### 4.1 Defaults to state

1. **Pick and state the strategy from two facts: what a measurement costs, and how much it says
   about why a candidate lost.** One line, e.g. "diagnosis-led, one change a round: the profile
   names the limiter" or "three candidates a round: the measure gives only a score".
   - Informative feedback: find the limiter or cause, make one targeted change, greedy from the
     current best.
   - Uninformative feedback: several independent candidates a round.
   - Stalled after that: keep a few diverse runners-up as starting points and reject
     near-duplicates.
2. **Read the raw evidence before proposing.** Failing inputs, traces, profiles, error output,
   the person's reasons. Summaries can point into it; they do not replace it. Keep the judge's own
   rationales away from the proposer (judge note).
3. **Stage the measure from cheap to expensive.** Hard requirements and correctness first, then
   any cheap proxy, then the expensive measure only for survivors.
4. **Prove a cheap stage before trusting it to reject.** It agrees with the expensive measure on
   pairs whose verdict is known, and a known-bad version fails it. Re-check when the kind of change
   shifts.
5. **List where the measure's conditions differ from real use, and confirm the final version
   under the real ones.** Device, timing or motion, the range of inputs, data and cache state, load,
   the person. A gain seen only under the proxy's conditions is reported as that, not as the goal.
6. **Score the final pick on inputs the climb never selected on, and keep the best, not the
   last.** The longer the climb, the more this matters.
7. **Harden the measure before round 1.** Look for ways a candidate could score without doing the
   job (caching, special-casing the test inputs, exploiting tolerances); close them, or check them
   on every accepted change.
8. **Know the noise floor of the expensive measure,** and count only gains above it (repeat runs,
   randomized setup for timing).
9. **When measurements are expensive, confirm several pre-screened changes in one run, but keep
   attribution recoverable.** Batch only changes that passed the cheap stages and touch different
   parts. If the batch underdelivers, bisect it with a noise model, and keep "it was noise" as a
   live hypothesis.
10. **On a large artifact, change the part the diagnosis names and hold the rest fixed, but measure
    the whole.** Move parts together when they are coupled.
11. **If the objective changes, re-measure the current best and the original under the new
    measure before continuing.** Continue if the kept changes still help; otherwise restart from
    the original, with the old record as hypotheses.
12. **Before a test on real use, compute what it can detect in the time available.** If the
    detectable effect is larger than any plausible gain, do not run it as a confirmation. Use the
    real-use test for a bold variant, a longer window, or as a check for harm, and say what it
    cannot show. If anyone will look before the end, use a sequential test.
13. **Default to a light search** (a few rounds; stop after rounds with no confirmed gain). The
    thorough option adds independent starts and candidates before more rounds, and always ends with
    the held-out check.

### 4.2 Probes to raise when they fit

1. Where does a single measurement spend its cost, and is there a cheaper check that would reject
   most bad candidates first?
2. Has the cheap check been shown to make the same call as the expensive one on pairs with a known
   answer, and does a deliberately broken version fail it?
3. What is different between how the climb measures and how the artifact is really met: device,
   motion and timing, the range of inputs, data, load, the person?
4. What would a candidate have to do to score well without doing the job, and does anything stop it?
5. Can the proposer see why a candidate lost (raw failures, traces, profiles, reasons), or only that
   it lost?
6. Has the climb stalled because of the search, or because of what the proposer can see and change?
7. Do these parts interact: would improving one change what is best for another?
8. Which accepted changes have only been measured together, and what would we do if the bundle
   fails to confirm?
9. Did the goal or measure change, and which kept changes were judged only under the old one?
10. For a test on real use: how many independent visitors or units a week, how often does the
    target event happen, and what is the smallest effect the test could detect in the time we will
    wait?
11. Is the variant bold enough that a real difference would be visible at this traffic?
12. For a before/after comparison: what else changed in that window, and was the change made
    because the measure had just dipped?
13. Would a few observed sessions with real people find what is broken faster than any lift
    measurement could?
14. Is the thorough run finding real gains, or fitting the measure? Does the held-out check agree?

---

## 5. Source index

**Choosing what to try**
- Lee et al. 2026, Meta-Harness — https://arxiv.org/abs/2603.28052 (full text https://arxiv.org/html/2603.28052v1)
- Deng et al. 2026, PerfAgent — https://arxiv.org/abs/2607.19653
- Olausson et al. 2024, Is Self-Repair a Silver Bullet? — https://arxiv.org/abs/2306.09896
- Madaan et al. 2023, Self-Refine — https://arxiv.org/abs/2303.17651
- Snell et al. 2024, Scaling LLM test-time compute optimally — https://arxiv.org/abs/2408.03314
- Brown et al. 2024, Large Language Monkeys — https://arxiv.org/abs/2407.21787
- Agrawal et al. 2025, GEPA — https://arxiv.org/abs/2507.19457
- Nam et al. 2025, MLE-STAR — https://arxiv.org/abs/2506.15692
- Novikov et al. 2025, AlphaEvolve — https://arxiv.org/abs/2506.13131
- Georgiev, Gómez-Serrano, Tao & Wagner 2025, Mathematical exploration and discovery at scale — https://arxiv.org/abs/2511.02864
- Toledo et al. 2025, AIRA-dojo — https://arxiv.org/abs/2507.02554
- Lange, Imajuku & Cetin 2025, ShinkaEvolve — https://arxiv.org/abs/2509.19349
- Beck, Ogren & Kobren 2026, Hill Sampling — https://arxiv.org/abs/2609.25510
- Oved et al. 2026, Evolution or Illusion? — https://arxiv.org/abs/2609.19799
- Chan et al. 2024, MLE-bench — https://arxiv.org/abs/2410.07095

**Staged evaluation and proxies**
- Li et al. 2018, Hyperband — https://arxiv.org/abs/1603.06560
- Magnusson et al. 2025, DataDecide — https://arxiv.org/abs/2504.11393
- Polo et al. 2024, tinyBenchmarks — https://arxiv.org/abs/2402.14992
- Walton, Why lab and field data can be different — https://web.dev/articles/lab-and-field-data-differences
- Mytkowicz et al. 2009, Producing wrong data without doing anything obviously wrong — https://doi.org/10.1145/1508244.1508275
- ZiCo (ICLR 2023) on zero-cost proxies vs parameter count (summary only) — https://arxiv.org/abs/2301.11300
- Sakana AI CUDA Engineer walk-back (news, summary only) — https://techcrunch.com/2025/02/21/sakana-walks-back-claims-that-its-ai-can-dramatically-speed-up-model-training/

**Batching, interactions, culprit finding**
- Microsoft ExP 2023, A/B Interactions: A Call to Relax — https://www.microsoft.com/en-us/research/articles/a-b-interactions-a-call-to-relax/
- Henderson et al. 2023, Flake Aware Culprit Finding — https://hackthology.com/flake-aware-culprit-finding.html ; https://research.google/pubs/flake-aware-culprit-finding/
- Zeller 1999, Yesterday, my program worked — https://doi.org/10.1007/3-540-48166-4_16

**Large artifacts**
- Opsahl-Ong et al. 2024, MIPRO — https://arxiv.org/abs/2406.11695
- Omidvar et al. 2014, Differential grouping — https://doi.org/10.1109/TEVC.2013.2281543

**Changing objectives**
- Ash & Adams 2020, On warm-starting neural network training — https://arxiv.org/abs/1910.08475
- Cully et al. 2015, Robots that can adapt like animals — https://arxiv.org/abs/1407.3501
- Suder et al. 2023, Bayesian transfer learning (summary only) — https://arxiv.org/abs/2312.13484
- EMO-STA 2026 (summary only) — https://arxiv.org/abs/2605.22613

**Low-traffic tests on real use**
- Kohavi, Deng & Vermeer 2022, A/B Testing Intuition Busters — https://doi.org/10.1145/3534678.3539160 (author copy https://airbnb.tech/wp-content/uploads/sites/19/2025/10/ABTestingIntuitionBusters.pdf)
- Azevedo et al. 2020, A/B Testing with Fat Tails — https://doi.org/10.1086/710607
- Schultzberg & Ankargren 2023, Choosing a sequential testing framework — https://engineering.atspotify.com/2023/03/choosing-sequential-testing-framework-comparisons-and-discussions
- Deng, Lu & Chen 2016, Continuous monitoring without pain — https://arxiv.org/abs/1602.05549
- Deng 2015, Objective Bayesian two-sample testing (summary only) — https://exp-platform.com/objective-bayesian-ab/
- Deng, Xu, Kohavi & Walker 2013, CUPED — https://exp-platform.com/cuped/
- Chapelle et al. 2012, Interleaved search evaluation — https://doi.org/10.1145/2094072.2094078
- Brodersen et al. 2015, CausalImpact — https://research.google/pubs/inferring-causal-impact-using-bayesian-structural-time-series-models/
- Faulkner 2003, Beyond the five-user assumption (summary only) — https://pubmed.ncbi.nlm.nih.gov/14587545/

**Light vs thorough**
- DSPy optimizer presets (source code) — https://github.com/stanfordnlp/dspy/blob/main/dspy/teleprompt/mipro_optimizer_v2.py ; https://github.com/stanfordnlp/dspy/blob/main/dspy/teleprompt/gepa/gepa.py
