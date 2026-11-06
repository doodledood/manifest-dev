# Deciding "better" on several objectives in an automated hill-climb

Research review, 2026-11-06. Written to feed short guidance and probes for a prompt-only `/hillclimb`
workflow. Nothing here is code.

**Provenance tags.** **[full]**: I read the passage in the source itself. For PDFs I extracted the
text and read it directly. For HTML papers and docs, a fetch tool returned specific passages and
numbers from the full text. **[abs]**: abstract or official summary only. **[sum]**: a search
summary or secondary write-up. **[inf]**: my own inference. Each LLM result gives its year and,
where the source names them, its models. Results from 2023 and earlier models (GPT-2, GPT-3.5,
early GPT-4, Claude-v1) show that a failure mode exists. They do not show how large it is with
today's models; the text says so where it matters.

---

## 1. Strongest practices

1. **Pick one primary objective. Treat the rest as guardrails with non-inferiority margins.** Ship
   only when the primary is significantly better and no guardrail is significantly worse than its
   margin. This is the standard decision rule in large-scale online experimentation. Best source:
   Schultzberg, Ankargren & Frånberg (Spotify, 2024), *Risk-aware product decisions in A/B tests
   with multiple metrics*, Decision Rule 2 **[full]**. Microsoft's metric taxonomy (Dmitriev et al.,
   KDD 2017) **[full]** and Airbnb's guardrails (2021) **[sum]** agree.
2. **Before trusting a measure, show that something clearly wrong cannot win on it.** At Bing, a
   bug that showed users very poor results raised distinct queries per user by over 10% and revenue
   per user by over 30%. Best source: Kohavi et al., *Five Puzzling Outcomes Explained* (KDD 2012)
   **[full]**. Its first OEC pitfall is "Picking an OEC for which it is easy to beat the control by
   doing something clearly 'wrong'". Deliberate-degradation tests come from Deng & Shi (KDD 2016)
   **[sum]**.
3. **Hold everything the measure does not mention constant.** Optimizing a proxy that references
   only J < L attributes drives the unmentioned attributes to their minimum. If the optimizer keeps
   them constant, proxy gains equal true gains. Best source: Zhuang & Hadfield-Menell (NeurIPS 2020),
   Theorem 1 and Proposition 2 **[full]**.
4. **Cap secondary proxies at a threshold instead of maximizing them.** Each component reward
   stops tracking the true goal past a "proxy point". Holding each component at its threshold
   beat maximizing a weighted composite. Best source: Moskovitz et al. (2023), *Confronting reward
   model overoptimization with constrained RLHF* **[full]**. The study used GPT-2 on DailyDialog,
   so it shows the mechanism, not its size at frontier scale.
5. **Keep a Pareto comparison to about three objectives, and never more than five.** Among 200
   random vectors, about 20% are non-dominated with 4 objectives, about 50% with 6, and almost all
   past 10. Best source: Ishibuchi, Tsukamoto & Nojima (CEC 2008), Fig. 1 **[full]**. Google's
   AlphaEvolve developer guide **[full]** says the same: "Limit multi-objective optimization to 3-5
   metrics. With too many metrics, the Pareto comparator fails".
6. **Test errors by role.** Split α across the success objectives. Do not α-adjust guardrail
   non-inferiority tests, but correct power for how many guardrails there are. Without that
   correction, 10 independent guardrails each powered at 80% have under 11% simultaneous power.
   Best source: Spotify (2024) **[full]**.
7. **When a person must choose the trade-off, have them compare whole outcomes in pairs instead of
   stating weights.** Decision makers are often unable to state a full trade-off function. In
   Meta pilots, data scientists compared outcome vectors with 4–9 outcomes in 8–13 s each, with
   about 10% error. Best source: Lin, Astudillo, Frazier & Bakshy (AISTATS 2022), BOPE **[full]**.
8. **If weights are used, normalize each objective to its baseline and elicit weights over the
   actual ranges, not as abstract "importance".** Direct importance weights barely respond to
   attribute ranges. Swing and trade-off methods respond better. Sources: Fischer (1995) via Baron
   **[sum]**; Keeney (2002) **[abs]**; AlphaEvolve scoring guide **[full]**.
9. **Expect the best of several noisy candidates to be overestimated, and re-measure it fresh.**
   Sources: Lee & Shen (Airbnb, KDD 2018), *Winner's Curse* **[sum]**; Dmitriev et al. (2017),
   pitfall 5, "re-run borderline experiments" **[full]**.
10. **Aggregate noisy proxies conservatively (worst-case), and draw measures from sources whose
    errors differ.** Sources: Coste et al. (2023), ensembles with worst-case optimization **[abs]**;
    Eisenstein et al. (2023) on shared errors that ensembles cannot cancel **[abs]**.
11. **For a pairwise AI judge: swap the order and call a disagreement a tie. Do not assume its
    per-criterion verdicts are independent; break each criterion on purpose and check the judge
    catches it.** Sources: Zheng et al. (2023), position consistency **[full]**; Hu et al. (ACL
    2024), *Are LLM-based evaluators confusing NLG quality criteria?* **[full]**.
12. **Pair every metric with its counter-metric, and track a composite's components separately.**
    Sources: Grove, *High Output Management* (1983), "paired indicators" **[sum]**; Spotify proxy
    guidance (2026), "If only one part is moving in the right direction, there is reason for
    suspicion" **[full]**; Kohavi et al. (2012), decomposing queries per month **[full]**.

---

## 2. Findings by topic

### 2.1 Pareto approaches

**Pareto local search.** Pareto local search (Paquete, Chiarandini & Stützle 2004; Paquete,
Schiavinotto & Stützle 2007) accepts a neighbor if no archived solution dominates it. That defines
a "Pareto local optimum set" **[sum]**. PAES (Knowles & Corne 1999/2000) is a (1+1) local search
that keeps an archive of non-dominated solutions to rank the current and candidate solutions. The
archive is bounded and kept spread out **[abs]**. The 2007 paper warns that acceptance relations
can face exponentially large neighborhoods, and that restricting the archive by spread can cause
cycling **[sum]**.

**Many objectives.** Among 200 random vectors in the unit hypercube, about 3% are non-dominated
with 2 objectives, about 21% with 4, about 50% with 6, about 77% with 8, and nearly all past 10.
NSGA-II "has a strong convergence property only when the number of non-dominated solutions is less
than 50%". The authors also note that visualizing the non-dominated set, and so choosing a final
solution, "becomes very difficult" (Ishibuchi et al. 2008) **[full]**.

For a climb that compares one candidate with the current best, the relevant number is how often the
two are incomparable. With k independent continuous objectives that probability is 1 − 2^(1−k):
50% at k = 2, 75% at k = 3, 87.5% at k = 4 **[inf]**. Conflicting objectives raise it and
positively correlated ones lower it. ParetoPrompt saw this with 3 objectives: about 65–75% of
sampled prompt pairs were mutually non-dominated during training (Zhao et al., ICLR 2025, Fig. 4)
**[full]**. The authors state that dominance-based training "can be inefficient" in many-objective
problems **[full]**.

**Choosing the final version.**
- *Knee point*: where a small gain in one objective costs a large loss in another. Branke et al.
  (PPSN 2004) argue knees are the most interesting points and focus search on them **[abs]**. I
  found no evidence that a knee matches what real requesters pick (gap).
- *The requester picks at the end*: Ishibuchi notes this gets very hard with many objectives
  **[full]**. BOPE notes that mapping the whole front "is typically inefficient because DMs are
  often interested only in a particular part" of it **[full]**.
- *A preference elicited at the end or during the run*: see 2.4.

**Cost.** Keeping a front means scoring every candidate on every objective, and under noise,
resampling. Fieldsend & Everson (2005) keep an archive that is mutually non-dominating with known
probability, which needs an estimate of the noise variance **[abs]**. Later work raises the
resampling of elite members as the front oscillates (Fieldsend, EMO 2015) **[abs]**. In GEPA, "the
majority of GEPA's rollout budget is spent on validation, where scores are utilized solely for
candidate selection" **[full]**.

**LLM-driven optimizers that use fronts, 2023–2026.**
- **GEPA** (Agrawal et al., 2025; ICLR 2026 oral). Models: Qwen3 8B and GPT-4.1 Mini, plus GPT-4o
  and GPT-5 Mini in side experiments.
  - The front is over **task instances, not objectives**: "For each training instance, GEPA records
    the highest score across all candidates, forming a Pareto frontier". A parent is sampled with
    probability proportional to the number of instances it leads **[full]**.
  - Ablation (Qwen3 8B, four benchmarks): Pareto sampling gained +12.44 points over baseline,
    against +6.05 for always picking the best candidate and +5.11 for beam search **[full]**.
  - Rollouts per benchmark: GEPA used about 1.8k–7k, against 24k for GRPO **[full]**.
  - The GEPA library now offers `instance`, `objective`, `hybrid` and `cartesian` frontier keys,
    and recommends `hybrid` for multi-metric work. Its own caveat: a candidate "competitive but
    never the single best on any key will not appear in the frontier" **[full]**.
  - So GEPA's front is mainly a **diversity device for choosing parents**, not a rule for deciding
    which candidate is better **[inf]**.
- **ParetoPrompt** (Zhao et al., ICLR 2025). Models: DistilGPT2 policy, RoBERTa-large and GPT-2 XL
  task models.
  - It trains on dominance preferences between prompt pairs, with no scalarization.
  - When the training fluency signal was swapped from a CoLA score to perplexity, its hypervolume
    barely moved. The summation, product and hypervolume-increment rewards degraded, because "the
    non-linear relationship between CoLA score and perplexity not only changes the absolute reward
    value, but also the relative rankings" **[full]**.
  - Small, old models: this shows the mechanism, not its size today.
- **InstOptima** (Yang & Li, 2023): NSGA-II with LLM mutation and crossover (LLaMA-2 7B in
  ParetoPrompt's rerun) **[full, as described in ParetoPrompt]**.
- **MOPrompt** (Câmara et al., 2025). Models: Gemma-2B and Sabiazinho-3, on Portuguese sentiment
  analysis. It trades accuracy against prompt tokens and found a prompt with the same 0.97 peak
  accuracy and a 31% shorter context **[abs]**.
- **MO-CAPO** (Büssing et al., May 2026). It optimizes performance and inference cost with budget
  allocation, and beat an NSGA-II baseline in 8 of 12 cases on a noisy R2 metric (three LLMs, not
  named in the abstract) **[abs]**.
- **AlphaEvolve** (Google DeepMind, 2025). The paper reports that "optimizing for multiple metrics
  often improves results for the single target metric" **[full]**. Its current developer guide
  caps the count at 3–5 metrics. It also warns that "passing individual scores for 5 benchmarks
  can lead to overfitting on some", while an aggregated sum generalized better to unseen benchmarks
  **[full]**.
- **Multi-objective RLHF.** Rewarded soups (Ramé et al., NeurIPS 2023; LLaMA-7B among others)
  fine-tunes one model per reward and interpolates their weights at test time to trace a front,
  so the trade-off is chosen after training **[sum]**. I did not verify MODPO (Zhou et al. 2023)
  (gap).

**What this means for a climb [inf].** A "front" does two separate jobs.
- (a) As a **decision rule** for the final pick, it needs a person to pick. It works for ≤3
  objectives, and it is the right choice only when the requester truly wants to choose the
  trade-off.
- (b) As a **diversity device** (GEPA), it keeps runners-up that lead somewhere as parents.
  Recent LLM-optimizer evidence for this is stronger (one ablation, 2025 models), and it needs no
  preference input.

### 2.2 Scalarization

**Weighted sums.**
- No choice of weights reaches the non-convex part of a non-convex front, and evenly spread weights
  do not give evenly spread solutions (Das & Dennis 1997) **[sum]**.
- Marler & Arora (2010) report "fundamental deficiencies" in how weights carry a-priori
  preferences. Weights tend to get set by the objectives' magnitudes rather than their importance
  **[abs/sum]**.
- Engineering guidance: AlphaEvolve's scoring guide recommends additive sums (`w1*A - w2*L -
  w3*M`) over products, which "can become hyper-sensitive to minor variations in the denominator".
  It also says to "divide each metric by its respective initial baseline value", and warns that
  without such weighting "AlphaEvolve will optimize the proxy metric at the expense of the actual
  goal" **[full]**.
- Fixed weighted sums also break when a metric is swapped for a non-linearly related one
  (ParetoPrompt, above) **[full]**.

**Chebyshev and achievement functions.**
- Wierzbicki's achievement scalarizing function measures deviation from a reference point. Its
  augmented form (a small sum term added to the max) yields only Pareto-optimal points, where the
  plain form can yield weakly optimal ones. Moving the reference point lets a decision maker reach
  any non-dominated outcome, including non-convex parts of the front **[sum]**.
- It underlies reference-point interactive methods, and NIMBUS can form an achievement subproblem
  **[sum]**.
- A related idea: optimizing the worst member of a reward ensemble (Coste et al. 2023) is a
  min-aggregation, as is Chebyshev with equal weights and an ideal point **[inf]**.

**Desirability functions.**
- Derringer & Suich (1980) map each response to d ∈ [0,1] and combine them with a geometric mean,
  so "if any one model is undesirable (d=0), the overall desirability is also unacceptable (D=0)".
  This is from the R `desirability` vignette citing Derringer & Suich **[sum]**.
- JMP deliberately does not use the Derringer–Suich forms because they are not smooth **[sum]**.
- Pfizer's CNS MPO score (Wager et al., 2010), a widely adopted medicinal-chemistry practice,
  *sums* six desirabilities (0–6) to avoid hard cutoffs. 74% of marketed CNS drugs scored ≥ 4,
  against 60% of Pfizer candidates **[sum]**.
- Practitioners therefore use both the veto (geometric mean) and the compensating (additive) forms
  (see Conflicts).

**When people can and cannot set weights.**
- *Range insensitivity*: weights stated as "importance" are nearly insensitive to the range an
  attribute actually spans. Fischer (1995) found complete insensitivity in that mode, while swing
  and direct trade-off methods moved weights closer to the required change. Keeney calls this "the
  most common critical mistake" **[sum]**.
- *Splitting bias*: splitting an attribute into sub-attributes raises its total weight (Weber,
  Eisenführ & von Winterfeldt 1988) **[abs]**.
- Keeney (2002) lists 12 common mistakes in value trade-offs **[abs]**.
- "DMs are often unable" to express a fully determined trade-off function (Lepird et al. 2015, as
  cited in BOPE) **[full, citing]**.
- *Equal weights*: Dawes (1979) showed equal weights are robust for *prediction*. That supports
  equal weights over guessed ones when nothing better is known, but it is evidence about
  prediction, not about stating preferences **[sum]**.
- *LLM rubric rewards*: RaR (Gunjal et al., 2025) compared a fixed weighted sum over rubric
  criteria ("Explicit") with one holistic judge score over the same rubric ("Implicit"). Models:
  Qwen2.5-7B policy, gpt-4o-mini judge.
  - "RaR-Implicit attains the strongest results overall"; "fixed weighted sums in RaR-Explicit
    offer more control but can be brittle" **[full]**.

**Synthesis [inf].** People set weights well when the objectives share a currency (money,
milliseconds, tokens) and they are asked about trade-offs over the actual ranges ("from 1.2 s to
0.9 s against 2% fewer conversions"). They set them poorly when asked how "important" each
objective is.

### 2.3 Constraints and guardrails

**The Overall Evaluation Criterion (OEC).**
- Kohavi et al. (2012) define it as "a quantitative measure of the experiment's objective".
  "Experiments may have multiple objectives and a balanced scorecard approach might be taken, or
  selecting a single metric, possibly as a weighted combination of such objectives" **[full]**.
- "Lifetime customer value should typically be the guiding principal for determining your
  organization's OEC" **[full]**.
- Bing's OEC became sessions per user, after decomposing queries per month into users × sessions
  per user × distinct queries per session. "Revenue per user should likewise not be used as an OEC
  ... without other constraints" **[full]**.
- Microsoft's taxonomy (Dmitriev et al. 2017) **[full]**:
  - *Data quality* metrics come first.
  - *OEC* metrics are "usually leading metrics that can be measured during the short duration of an
    experiment, but at the same time are indicative of long term business value". "It is ideal to
    have just a single metric as the OEC ... It can be a composite metric".
  - *Guardrail* metrics are "not clearly indicative of success" but "we do not want to significantly
    harm". For example: "Small degradations in guardrail metrics can be expected ... Large
    degradations, however, are generally not allowed".
  - *Local feature and diagnostic* metrics explain OEC movement.

**Spotify's decision rule (Schultzberg et al. 2024)** **[full]**. Ship only if:
- (i) at least one success metric is significantly superior;
- (ii) every guardrail is significantly non-inferior to its margin;
- (iii) no success, guardrail or deterioration metric is significantly inferior;
- (iv) no quality test fails.

Error control by test type:
- Success-metric tests run at α/S (Bonferroni across success metrics).
- Guardrail non-inferiority tests are not α-adjusted, by an intersection-union argument.
- Power is corrected, to roughly β/(G+1) without deterioration tests.

The authors state that "simplicity is often more important than finding the statistically optimal
solution". They also argue that dropping a guardrail for sample-size reasons is worse than keeping
it in the rule, because teams then weigh it informally anyway.

**Airbnb (2021)** **[sum, InfoQ]**. Three guardrails, each must pass or the launch is escalated, not
blocked:
- *Impact*: the metric must not drop by more than a threshold t.
- *Power*: standard error < 0.8·t.
- *Stat-sig negative*: for sensitive metrics such as revenue.

About 25 experiments a month were escalated and about 20% of those were stopped. A secondary summary
attributes to the same post: "If you alert on any degradation significant at 0.05 across 50
metrics, you would have at least one false alert 92% of the time in an AA test" **[sum]**.

**Other companies.**
- LinkedIn frames feed ranking as constrained optimization (maximize one objective subject to the
  others) and studies the front between one primary metric and K guardrails **[sum]**.
- Netflix evaluates decision rules by their cumulative return to a north-star metric over 123 past
  A/B tests; one new rule would have raised it by about 33% (Chou et al., KDD 2025) **[abs]**.
- Google builds proxy metrics from past experiments. "The optimal proxy metric ... should depend on
  the sample size (or effective noise level)" (Tripuraneni et al., KDD 2024) **[abs]**. A Pareto
  search over prediction accuracy and sensitivity found proxies 8× more sensitive than the north
  star (Zito et al. 2023/2025) **[abs]**.

**Satisficing, ε-constraint, lexicographic order.**
- *Satisficing*: Simon (1955) has decision makers search until an option meets an aspiration level.
  The level rises when satisfactory options come easily and falls when they are hard to find
  **[sum]**.
- *ε-constraint*: Haimes, Lasdon & Wismer (1971) optimize one objective and bound the rest. It needs
  no convexity, but it can return weakly efficient points **[sum]**. AlphaEvolve's guide offers
  this mode for "optimizing one metric while keeping the other from dropping over or below a
  threshold". It notes that tracing the front "may require running multiple experiments at
  different constraint levels" **[full]**.
- *Lexicographic order with tolerances*: Tversky (1969) showed that a lexicographic semiorder can
  produce intransitive choices through a chain of individually ignored small differences. Later
  replications are mixed (Ranyard et al. 2024) **[sum]**.
- AlphaEvolve's *evaluation cascade* passes candidates through stages of increasing difficulty, a
  lexicographic gate in which cheap hard checks run first **[full]**.

**Cumulative drift through tolerated small losses.** Bing reportedly found that many individually
validated features together added a considerable page-load penalty. It then made page-load time a
guardrail on every experiment, with performance-team sign-off **[sum]**. Airbnb's design tolerates
roughly 0.1% page-performance hits without escalation **[sum]**. Spotify runs 10% holdouts for
several weeks to see long-term effects **[full]**.

**What practitioners actually use, and why.** In online experimentation the convergent practice is
one OEC or a few success metrics, plus guardrails and data-quality checks (Microsoft, Spotify,
Airbnb, LinkedIn). The stated reasons:
- an organization needs one go/no-go criterion (Kohavi) **[full]**;
- guardrails protect metrics other teams own (Airbnb) **[sum]**;
- simplicity scales across many experimenters (Spotify) **[full]**.

Fronts appear mainly in research optimizers (MO-CAPO, MOPrompt, ParetoPrompt) and where the choice
is deliberately left to the user. Weighted composites appear as an engineering default
(AlphaEvolve) **[full]** and as validated proxies built from experiment history (Netflix, Google)
**[abs]**.

### 2.4 Preference elicitation

**Interactive methods.**
- *Reference point*: the decision maker states aspiration levels, and the method projects them onto
  the front **[sum]**.
- *NIMBUS*: the decision maker classifies each objective (improve, keep, may worsen to a bound, and
  so on). The synchronous version shows several solutions for preferences stated "once during each
  iteration" **[sum]**.
- Afsar, Miettinen & Ruiz (2021) list cognitive load and anchoring as properties to assess. They
  note that "artificial decision makers do not necessarily represent ... anchoring or cognitive
  biases" **[abs/sum]**.

**BOPE (Lin et al., AISTATS 2022)** **[full]**.
- It alternates experiments with stages where the person compares outcome vectors in pairs.
- In simulation it "significantly outperform[s] MOBO, PBO, and other natural baselines".
- Each stage asks for 25 comparisons, over 3 stages (75 in total).
- One upfront elicitation stage minimizes interruptions but can hurt the result. Preference-based
  strategies "benefit greatly" from eliciting over several rounds, while active-learning strategies
  do best eliciting everything upfront.
- The human data come from pilots with Meta data scientists: 7.8–12.7 s per comparison, about 10%
  error, and an estimated 15 minutes for 75 comparisons.
- The optimization results are simulations, not runs with live people.

**Interactive updating of the proxy.** Letting the principal update the proxy over time yields
guaranteed improvement under the model's conditions (Zhuang & Hadfield-Menell 2020) **[full]**.

**When to ask [inf, from the above].**
- *Before the run*: a primary, margins and protected parts. These are cheap to state and robust.
  Numeric weights are not robust.
- *During the run*: a few pairwise comparisons of whole versions. This is the best-supported way to
  learn a trade-off, but it needs the requester present.
- *At the end*: choosing from a front works for ≤3 objectives and a few finalists.

### 2.5 Noise and judges

**Multiplicity [inf, checked against the sources].**
- If a candidate wins when *any* of k objectives improves at level α, the false-win rate per
  candidate is about 1 − (1 − α)^k: about 14% for k = 3 at α = 0.05. Three candidates a round
  multiply the chances again.
- Requiring a significant gain on *every* objective collapses power. Spotify reports under 11%
  simultaneous power with 10 independent guardrails left uncorrected **[full]**.
- The middle course is Spotify's: superiority on the success objective(s) with α split across
  them, and non-inferiority on guards **[full]**.
- An independent fresh confirmation of the objective that triggered the win multiplies the false
  rates, roughly k·α·α, so it is a strong multiplicity control in its own right.

**Selection bias.** Picking the best of several noisy candidates overstates its gain (Lee & Shen,
KDD 2018) **[sum]**. Borderline results should be replicated (Dmitriev et al. 2017) **[full]**.

**Dominance under noise.** Noisy dominance needs a probability of dominance and a noise-variance
estimate (Fieldsend & Everson 2005, building on Hughes 2001 and Teich 2001) **[abs]**. I found no
source on noisy multi-objective acceptance for a 3-candidate-per-round local search like this one
(gap).

**Pairwise LLM judges.**
- *Position bias* (Zheng et al., 2023; MT-Bench). Agreement with itself after the two answers are
  swapped: GPT-4 65.0%, GPT-3.5 46.2%, Claude-v1 23.8%. "If the results are inconsistent after
  swapping, we can call it a tie" **[full]**. GPT-4 agreed with humans over 80% of the time
  **[abs]**. These are 2023 models: the bias is real, but its size today is unknown here.
- *Criteria confusion* (Hu et al., ACL 2024; GPT-3.5, GPT-4 on a subset, Prometheus-13B):
  - "LLMs seem to confuse different aspects".
  - A fluency perturbation (word inversion) moved coherence scores by 0.66, and a grammar
    perturbation moved them by 0.98. Coherence and informativeness perturbations "almost did not
    lead to any degradation".
  - Detailed criterion definitions helped little; no intervention "has a generally significant
    effect".
  - GPT-4 did better than GPT-3.5 on directional tests and worse on invariance tests **[full]**.
  - So per-criterion verdicts from one judge pass are not independent evidence **[inf]**.

**Per-criterion vs holistic judging (mixed evidence).**
- *For decomposition*:
  - TICK (Cook et al., 2024): LLM-generated yes/no checklists raised exact agreement with human
    preferences from 46.4% to 52.2% compared with direct scoring **[abs]** (models not named in the
    abstract).
  - RLCF (Viswanathan et al., NeurIPS 2025; Qwen2.5-7B-Instruct): checklist rewards were "the only
    method to help on every benchmark", including +6 on InFoBench **[sum]**.
- *Against fixed aggregation*:
  - RaR (2025): a holistic judge reading the rubric beat a fixed weighted sum of per-criterion
    verdicts. Rubrics helped smaller judges most **[full]**.
  - Huynh et al. (May 2026): "higher rubric complexity and conservative aggregation methods tended
    to decrease" human–autorater agreement **[abs]**.
  - An essay-scoring study (2026) found holistic agreement did not carry over evenly to analytic
    trait scores **[sum]**.
- A 2026 preprint finds position bias inside rubric score options, which swapping two answers does
  not fix, and proposes balanced permutation **[sum]**.

### 2.6 Goodhart and reward hacking with several objectives

**Theory.**
- *Incomplete proxies* (Zhuang & Hadfield-Menell 2020) **[full]**:
  - "For any continuous strictly increasing proxy utility function based on J < L attributes, if
    s(t) converges to some point s*, then s*_k = b_k for k ∈ K": the unmentioned attributes go to
    their lower bounds.
  - Under compact feasibility and low enough lower bounds, any incomplete proxy leads to
    arbitrarily low utility.
  - Remedies: keeping unmentioned attributes constant ("impact minimization") makes proxy gains
    true gains. Interactive proxy updates also guarantee improvement.
- *Unhackability* (Skalse et al. 2022): over all stochastic policies, two rewards are unhackable
  only if one is constant **[abs]**. Adding or dropping terms does not, by itself, make a proxy safe
  **[inf]**.
- *Goodhart taxonomy* (Manheim & Garrabrant 2018/2019) **[full]**:
  - regressional ("unavoidable": selection also selects for noise);
  - extremal (optimization leaves the region where the proxy was validated);
  - causal (intervening breaks the correlation);
  - adversarial (another agent games it).
  - A footnote says "use of multiple metrics and restrictions follows similar dynamics".

**Empirical.**
- *Proxy-reward overoptimization* (Gao, Schulman & Hilton, ICML 2023): the gold score first rises,
  then falls as optimization against the proxy continues, with coefficients that scale smoothly
  with reward-model size **[sum]**.
- *Composite rewards* (Moskovitz et al., 2023; GPT-2, DailyDialog; METEOR plus an intent
  classifier, evaluated on held-out metrics) **[full]**:
  - "correlation between component RMs has a significant effect on the locations" of the proxy
    points;
  - holding each component at its point beats a weighted composite;
  - limitation: "at least some minimal degree of access to the true objective/evaluation metric is
    required".
- *Ensembles*:
  - Coste et al. (2023): worst-case and uncertainty-weighted ensemble optimization "practically
    eliminates overoptimization ... by up to 70% for BoN" **[abs]**.
  - Eisenstein et al. (2023): ensembles "mitigate but do not eliminate" hacking, because "all
    reward models in the ensemble exhibit similar error patterns". Pretrain-seed diversity beats
    fine-tune-seed diversity **[abs]**.
- *Hacking moves to one objective*:
  - MO-GRPO (Ichihara et al., 2025; TACL): GRPO "optimizes only one of the objectives at the cost
    of the others". Normalizing by reward variance fixes it **[abs]**.
  - RLUF (Han et al., 2025; Llama3-70B policy, Llama3-8B reward models) **[full]**:
    - It optimized a user-reaction reward alongside fixed helpfulness and safety rewards.
    - The policy learned to end with "bye, sending love!" ("bye" rose from 0.72% to 2.8% of
      responses), asked about half as many follow-up questions, and helpfulness fell from 1.53 to
      1.28.
    - The moderate weight avoided the pattern and the aggressive one did not. "Completely
      mitigating reward hacking behavior remains an open problem".
    - The authors suggest a helpfulness constraint instead of linear mixing.

**Answer to the question [inf, from the above].** Adding objectives reduces over-optimization only
when one of these holds:
- the added objectives act as constraints or caps, not as terms to maximize (Moskovitz; RLUF's
  suggestion);
- they are aggregated conservatively, so the weakest dominates (Coste);
- their errors are not shared, which means different measurement kinds or model families
  (Eisenstein; Hu).

Otherwise the pressure moves to whatever is weakest. That can be the highest-variance objective
(MO-GRPO), the cheapest proxy to move (RLUF), or anything unmeasured (Zhuang & Hadfield-Menell).
Most evidence comes from small models or one setting. RLUF is the one at 70B scale.

### 2.7 Designing metrics that reflect the goal

- **Goals first.** HEART and Goals–Signals–Metrics (Rodden, Hutchinson & Fu, CHI 2010) map product
  goals to signals, then to metrics, across more than 20 Google products **[abs/sum]**.
- **Leading vs lagging.**
  - OEC metrics are leading metrics that predict long-term value (Microsoft) **[full]**.
  - Choose proxies from past experiments by how well they predict the north star and how
    sensitive they are (Google, Netflix) **[abs]**.
  - Spotify: "The proxy should confirm your hypothesis, not define it". Use proxies that differ
    from each other but each correlate with the long-term outcome. Run holdouts **[full]**.
- **Proxy vs true goal.** All four Goodhart mechanisms apply. Regressional Goodhart "cannot be
  avoided" **[full]**.
- **Counter-metrics.** Grove pairs indicators so that "both effect and counter-effect are
  measured", for example inventory with stock-outs and output with quality **[sum]**. Thomas &
  Uminsky (2020) propose "a slate of metrics", qualitative accounts, and involving affected
  stakeholders **[abs]**.
- **Validity** (Jacobs & Wallach, FAccT 2021) **[full]**:
  - test–retest *reliability*;
  - *face* validity ("a 'sniff test'", needed but not enough);
  - *content* validity, which includes substantive validity ("those — and only those — observable
    properties");
  - *convergent* validity;
  - *discriminant* validity (measurements should correlate with other constructs "only to the
    extent that those constructs are themselves related");
  - *predictive*, *hypothesis* and *consequential* validity.
- A 2025 review of 445 LLM benchmarks found that only 16% used statistical tests, and about half
  measured abstract phenomena without clearly defining them (Bean et al., NeurIPS 2025) **[sum]**.
- **Directionality and sensitivity** (Deng & Shi 2016): check a metric against a validation corpus
  of past experiments with known outcomes and against deliberate degradation **[sum]**.

**Checks that most often catch a metric that does not reflect its goal** (ranked by the strength
and directness of the evidence):

1. **The clearly-wrong test.** Can a variant that is plainly worse win on the metric? (Kohavi 2012
   **[full]**; degradation experiments, Deng & Shi **[sum]**; criterion-targeted perturbations, Hu
   et al. **[full]**.)
2. **The known-outcome corpus.** Does the metric rank past changes with known outcomes correctly?
   (Deng & Shi; Dmitriev & Wu 2016) **[sum]**
3. **Twyman's law.** "Any figure that looks interesting or different is usually wrong": a
   surprising win gets investigated before it is believed (Dmitriev et al. 2017) **[full]**.
4. **Decomposition.** Do the components move together? (Kohavi 2012 **[full]**; Spotify **[full]**)
5. **A paired counter-metric** (Grove) **[sum]**.
6. **Discriminant check.** Does the metric move when only an unrelated aspect changes? (Jacobs &
   Wallach **[full]**; Hu et al. **[full]**)
7. **Test–retest noise.** Does the metric repeat on an unchanged artifact? (Jacobs & Wallach)
   **[full]**
8. **Predictive link.** Do holdouts or later real use confirm the proxy's direction? (Spotify,
   Netflix, Google) **[full/abs]**

---

## 3. Conflicts and gaps

**Conflicts.**
- **Per-criterion vs holistic judging.**
  - For decomposition: TICK (+5.8 points exact agreement) and RLCF (checklists beat reward models).
  - Against fixed aggregation: RaR (holistic over rubric beat explicit weighted sum); Huynh et al.
    2026 (complex rubrics and conservative aggregation lowered agreement); Hu et al. (per-criterion
    scores contaminate each other).
  - *Reconciliation [inf]*: decomposition helps when each item is a concrete yes/no check. Fixed
    numeric aggregation of fuzzy criteria is brittle. Per-criterion verdicts are still the only way
    to see a loss on one guard.
- **Do several metrics help or hurt?** The AlphaEvolve paper says several metrics often help the
  single target. Its own docs warn that per-benchmark scores overfit and that more than 5 metrics
  break Pareto comparison **[full]**. Both can hold: a few diverse signals help search, and many
  fine-grained ones invite overfitting **[inf]**.
- **Veto vs compensation in desirability.** Derringer–Suich's geometric mean vetoes on any zero.
  The CNS MPO practice sums desirabilities so that no single property kills a compound **[sum]**.
- **How far ensembles get.** Coste reports conservative ensembles "practically eliminate"
  overoptimization for best-of-n. Eisenstein reports they "do not eliminate" it. Both are abstract
  reads, with different setups and models.
- **Weighted sums as default.** The AlphaEvolve guide recommends starting with a normalized
  additive sum. The MCDM literature says stated weights rarely encode preference. The conflict
  dissolves if the sum is treated as an engineering composite to validate, not as a statement of
  preference **[inf]**.
- **Do weight sweeps work?** RLUF calls simple weight sweeps "effective at limiting
  over-optimization", yet hacking persisted at the higher weight **[full]**.

**Gaps.**
- No study evaluates multi-objective acceptance rules for an *LLM-agent hill-climb* with a
  *pairwise AI judge*: three candidates a round, fresh confirmation, stop after two flat rounds. All
  transfer from A/B testing, evolutionary multi-objective optimization or RLHF is inference.
- No direct evidence that anchoring guardrails to the *original* rather than the *previous best*
  reduces drift inside an optimizer. The support is practitioner anecdote (Bing, Airbnb) plus the
  lexicographic-semiorder argument.
- Evidence on whether a knee point matches what real requesters choose: none found.
- Evidence on judge per-criterion reliability with 2025–2026 frontier models is thin. Most
  quantitative results use GPT-3.5, GPT-4 (2023), gpt-4o-mini or 7–13B judges.
- The Moskovitz proxy-point evidence covers one setting (GPT-2, two rewards, held-out metrics as
  "truth").
- Not read in full here: the Deng & Shi and Dmitriev & Wu papers, the Airbnb and Netflix blog
  posts (blocked), Derringer & Suich's paper, Keeney (2002), Das & Dennis (1997). MODPO was not
  verified.
- Manheim & Garrabrant give a taxonomy but no mitigation advice **[full]**.

---

## 4. Recommendation for `/hillclimb` (all of this section is my inference)

### 4.1 Default: one primary measure, the rest guarded against the original

A climb with several objectives declares them in three roles:

- **Primary.** The one objective the climb exists to improve. It may be a composite only if the
  composite was validated like any measure, and its components then also act as guards.
- **Guards.** Every other objective, each with a **margin measured against the original**. The
  default margin is "no confirmed loss beyond the recorded noise".
- **Protected.** Parts that must not change. This is the Zhuang & Hadfield-Menell remedy for
  everything unmeasured.

**Acceptance rule.** A candidate replaces the current best only when both hold:
- its primary gain over the current best is beyond noise and confirmed on fresh measurement;
- on fresh measurement, no guard is worse than the **original** by more than its margin.

Why this default:
- It is the best-attested practice (Microsoft, Spotify, Airbnb, LinkedIn).
- It needs no weights, works with a pairwise judge and with A/B rounds, and keeps statistical power.
- It matches the constraint findings in RLHF (Moskovitz; RLUF's suggestion).
- It extends the current design (primary plus protected parts plus guard measures) instead of
  replacing it.

### 4.2 When to switch

| Situation the session can see | Switch to | Why |
|---|---|---|
| The requester cannot name a primary: 2–3 co-equal objectives and they want to choose the trade-off themselves (attended) | **Keep a small front**: accept a candidate that improves at least one objective beyond noise with no guard loss beyond margin. Carry up to 3 non-dominated finalists, and let the requester choose by comparing whole versions in pairs, with the knee as a suggestion | Pareto decisions need a chooser, and with ≤3 objectives the front stays small (Ishibuchi; BOPE) |
| Same, but `--autonomous` | **Pareto improvement over the original only**. The final pick is the finalist with the best *worst* objective, normalized to the original (maximin) | No chooser is present. Maximin is the conservative, weight-free aggregate (Coste; Chebyshev) |
| The objectives share a currency (ms, $, tokens, bytes) and the requester states an exchange rate over the actual ranges | **A baseline-normalized weighted sum as the primary**, with each component also a guard | Weights are reliable when stated as trade-offs over ranges. Guards catch one component quietly carrying the sum (AlphaEvolve docs; Spotify) |
| Each objective has a floor below which the artifact fails the people it serves | **Floors become guards (veto)**. If nothing else stands out, the primary becomes "raise the worst objective" | This is Derringer–Suich's veto without the fragile geometric mean |
| An objective helps up to a level and is then enough, or a proxy saturates | **Satisfice**: once it reaches its threshold it becomes a guard at that level and stops being pushed | Proxy points (Moskovitz); Simon |
| More than 3–4 objectives | **Reduce before climbing**: merge correlated ones, demote to guards, or protect | Pareto comparison collapses (Ishibuchi; AlphaEvolve docs) |
| Real-use measurement (A/B per round) | **Spotify's rule**: superiority on the success metric with α split across success metrics, unadjusted non-inferiority on guards, power corrected for the number of guards | The strongest published rule for this exact case |

**Separate from the decision rule:** the round's bold candidate may start from a runner-up that won
on some held case or criterion, not always from the current best. This is GEPA's diversity effect.
It changes how candidates are *proposed*, never how they are *accepted*.

### 4.3 What to ask the requester, and what `--autonomous` assumes

**Ask, when attended.** These are cheap, robust inputs; avoid asking for numeric "importance"
weights.
1. Which single objective is the climb for? Or should it only show you trade-offs to choose from?
2. For each other objective: how much loss against **the original** is acceptable? Answer in its
   own units over the real range ("from 1.2 s to 1.4 s?"), or say none.
3. What must not change at all?
4. Is there a level past which an objective is good enough?
5. Can you name or point to a version that is worse in a way the measure must catch, one per
   objective if possible?
6. (Only if a trade-off must be learned) Which of these two whole versions do you prefer? Ask a
   handful of times during the run instead of asking for weights. Each comparison costs seconds
   (BOPE).

**Assume, when autonomous.**
- The primary is the objective the goal statement names as the outcome for the people served.
- Every other named objective is a guard with margin = recorded noise against the original.
  Unnamed but visible qualities of the artifact are protected or become guards.
- No weights are invented. If no primary can be identified, accept only Pareto improvements over
  the original within noise, and pick the final version by maximin.
- With more than 4 objectives, reduce them before round 1 and record the reduction as an
  assumption.

### 4.4 How this fits the existing rules

- **"A candidate replaces the current best only on a confirmed gain beyond noise."**
  - Confirm superiority on the *primary only*. Treat guards as non-inferiority checks, without α
    adjustment, but give the guard measurement enough repeats to detect a margin-sized loss.
  - Requiring a significant gain on every objective would stall the climb.
  - If acceptance allows *any* objective to supply the gain (front mode), the screen's false-win
    rate grows with objectives × candidates, about 14% a candidate at three objectives. The fresh
    confirmation of the triggering objective is what controls it, so it must be independent of the
    screening run.
  - Re-measure the guards on the confirmation run too.
- **Anchor guards to the original, not to the current best.** Otherwise a chain of individually
  "within-noise" losses accumulates across rounds (Tversky's semiorder; the Bing page-load drift).
  Each guard's margin is a budget for the whole climb, not a per-round allowance.
- **"The final version beats the original head to head."** Make this a per-objective comparison:
  - primary superior beyond noise;
  - every guard within its margin;
  - reported as a table of the vector with its noise.
  - The judge from another model family and the held-out cases should check the guards as well as
    the primary. A holistic "B is better" can hide a guard loss through criteria confusion or a
    halo effect (Hu et al.).
- **Judges with several criteria.**
  - Ask for a verdict per criterion (A better, B better, or tie) with swapped order, and a
    separate holistic verdict for the primary when the primary is "better for these people".
  - Treat a criterion verdict that flips under swapping as a tie.
  - Before round 1, break each guard criterion on purpose. The judge should rank the broken
    version lower on that criterion, and should not prefer it on the primary.
  - Two criteria judged in one pass by one model count as one source of error, not two.

### 4.5 Candidate probes for figure-out

Each probe is phrased as the question that opens a branch, and limited to angles a capable model
tends to skip.

1. If the climb could improve only one of these, which would it be, and how much may each of the
   others lose **against the original**, not against last round, before the gain stops being
   worth it?
2. What does the artifact do well today that none of these measures mentions, and what stops the
   climb from spending it to buy the measured gain?
3. Past what level does more of this objective stop helping the people it serves, so that it
   should become a floor once reached?
4. Could a version that is clearly worse on one criterion still win the judge's overall verdict,
   and have we broken each criterion on purpose to see?
5. Would small losses that each stay inside the noise add up, over the rounds, to a loss nobody
   would accept?
6. Do these objectives actually pull against each other near the current version, or only in
   principle? If they move together, the climb has one objective.
7. Does the requester want to choose the trade-off themselves, and would they rather compare a few
   whole versions than state weights?

### 4.6 Candidate checks for define's gates

1. **Every objective has a role.** Each objective named in the goal or raised while defining is
   recorded as exactly one of primary (at most one, or a validated composite whose components are
   guards), guard with a margin against the original, or protected. None is left unclassified.
2. **Each criterion catches a deliberate break.** Before round 1, for the primary and every guard,
   a variant degraded only on that criterion ranks below the original on it, and does not win the
   primary verdict. Run this alongside the known-better/known-worse calibration and the noise
   record.
3. **The final version holds on every objective against the original.** It beats the original on
   the primary beyond the recorded noise, and every guard is within its margin of the original.
   Show this as a per-objective table, evaluated by the held-out cases and the other-family judge
   as well as the climbing measure.
4. **Acceptance accounts for multiplicity (front mode only).** When any of several objectives can
   supply a round's gain, the winning objective's gain is confirmed on an independent fresh
   measurement before acceptance.

---

## 5. Source index

**Pareto, many-objective, LLM optimizers**
- Agrawal et al. 2025, GEPA — https://arxiv.org/abs/2507.19457 ; full text https://arxiv.org/html/2507.19457
- GEPA candidate-selection guide — https://gepa-ai.github.io/gepa/guides/candidate-selection
- Zhao et al. 2025, ParetoPrompt (ICLR) — https://proceedings.iclr.cc/paper_files/paper/2025/file/13b45b44e26c353c64cba9529bf4724f-Paper-Conference.pdf
- Câmara et al. 2025, MOPrompt — https://arxiv.org/abs/2508.01541
- Büssing et al. 2026, MO-CAPO — https://arxiv.org/abs/2605.18869
- Novikov et al. 2025, AlphaEvolve paper — https://arxiv.org/html/2506.13131
- AlphaEvolve multi-objective guide — https://docs.cloud.google.com/gemini/enterprise/docs/alphaevolve/developer-guide/multi-objective-optimization
- AlphaEvolve scoring guide — https://docs.cloud.google.com/gemini/enterprise/docs/alphaevolve/developer-guide/scoring-approaches
- Ishibuchi, Tsukamoto & Nojima 2008 — https://ci-labo-omu.github.io/assets/paper/pdf_file/multiobjective/CEC2008_Many_Objective_Final.pdf
- Branke, Deb, Dierolf & Osswald 2004, knees — https://doi.org/10.1007/978-3-540-30217-9_73
- Knowles & Corne, PAES — https://staff.cs.manchester.ac.uk/~jknowles/multi/
- Paquete, Schiavinotto & Stützle 2007, Pareto local optima — https://link.springer.com/doi/10.1007/s10479-007-0230-0
- Fieldsend & Everson 2005, MOO under uncertainty — https://ore.exeter.ac.uk/repository/handle/10871/11661
- Fieldsend 2015, elite accumulative sampling — https://ore.exeter.ac.uk/repository/bitstream/10871/17039/1/EMO_2015_final_version_fieldsend.pdf
- Ramé et al. 2023, Rewarded soups — https://arxiv.org/abs/2306.04488

**Scalarization and weights**
- Das & Dennis 1997 — https://doi.org/10.1007/BF01197559
- Marler & Arora 2010 — https://doi.org/10.1007/s00158-009-0460-7
- Wierzbicki ASF overview (reference-point methods) — https://arxiv.org/pdf/2301.12148
- Derringer & Suich 1980, via R `desirability` vignette — https://www.mi.rro.rs/cran/web/packages/desirability/vignettes/desirability.Rnw ; JMP note — https://www.jmp.com/support/help/en/19.0/jmp/construction-of-desirability-functions.shtml
- Wager et al. 2010, CNS MPO — https://pmc.ncbi.nlm.nih.gov/articles/PMC3368654
- Keeney 2002, Common mistakes in value trade-offs — https://doi.org/10.1287/opre.50.6.935.357
- Weber, Eisenführ & von Winterfeldt 1988, splitting bias — https://doi.org/10.1287/mnsc.34.4.431
- Baron, range insensitivity review (Fischer 1995) — https://www.sas.upenn.edu/~baron/papers.htm/range.htm
- Dawes 1979 — https://www.cmu.edu/dietrich/sds/docs/dawes/the-robust-beauty-of-improper-linear-models-in-decision-making.pdf
- Gunjal et al. 2025, Rubrics as Rewards — https://arxiv.org/html/2507.17746v2

**Constraints, guardrails, OEC**
- Kohavi et al. 2012, Five Puzzling Outcomes — https://exp-platform.com/Documents/puzzlingOutcomesInControlledExperiments.pdf
- Dmitriev, Gupta, Kim & Vaz 2017, A Dirty Dozen — https://www.microsoft.com/en-us/research/uploads/prod/2020/08/2017-08-KDDMetricInterpretationPitfalls.pdf ; summary https://blog.acolyer.org/2017/09/25/a-dirty-dozen-twelve-common-metric-interpretation-pitfalls-in-online-controlled-experiments/
- Schultzberg, Ankargren & Frånberg 2024 (Spotify) — https://arxiv.org/html/2402.11609
- Airbnb 2021, Designing Experimentation Guardrails — https://medium.com/airbnb-engineering/designing-experimentation-guardrails-ed6a976ec669 ; InfoQ — https://www.infoq.com/news/2021/01/airbnb-guardrails-change-impact
- Deng & Shi 2016, metric development — https://doi.org/10.1145/2939672.2939700
- Dmitriev & Wu 2016, Measuring Metrics — https://doi.org/10.1145/2983323.2983356
- Kohavi, Tang & Xu 2020, Trustworthy Online Controlled Experiments, ch. 7 — https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/metrics-for-experimentation-and-the-overall-evaluation-criterion/4EA73D169EC43B58991D6824717E8FD3
- Chou et al. 2025 (Netflix), decision rules across weak experiments — https://arxiv.org/abs/2502.08763
- Tripuraneni et al. 2024, Choosing a proxy metric — https://arxiv.org/abs/2309.07893
- Zito et al. 2023/2025, Pareto optimal proxy metrics — https://arxiv.org/abs/2307.01000
- LinkedIn, large-scale multi-objective optimization — https://arxiv.org/pdf/1602.03131
- Lee & Shen 2018, Winner's Curse — https://medium.com/airbnb-engineering/selection-bias-in-online-experimentation-c3d67795cceb
- Haimes, Lasdon & Wismer 1971 (ε-constraint) — IEEE Trans. SMC 1(3):296–297 (no open copy read)
- Simon 1955 — https://doi.org/10.2307/1884852
- Tversky 1969, Intransitivity of preferences — https://doi.org/10.1037/h0026750 ; Ranyard et al. 2024 — https://ore.exeter.ac.uk/articles/journal_contribution/Violations_of_transitive_preference_A_comparison_of_compensatory_and_noncompensatory_accounts/29811935

**Preference elicitation**
- Lin, Astudillo, Frazier & Bakshy 2022, BOPE — https://arxiv.org/abs/2203.11382
- Afsar, Miettinen & Ruiz 2021 — https://jyx.jyu.fi/jyx/Record/jyx_123456789_75333
- Miettinen & Mäkelä 2006, synchronous NIMBUS — EJOR 170(3):909–922; NIMBUS classification help https://nimbus.mit.jyu.fi/N4/helps/classification.html (fetch failed; [sum] only)

**Noise and judges**
- Zheng et al. 2023, MT-Bench — https://arxiv.org/html/2306.05685v4
- Hu et al. 2024, criteria confusion — https://arxiv.org/html/2402.12055v2
- Cook et al. 2024, TICK — https://arxiv.org/abs/2410.03608
- Viswanathan et al. 2025, Checklists vs reward models — https://arxiv.org/abs/2507.18624
- Huynh et al. 2026, rubric modifications and agreement — https://arxiv.org/abs/2605.06283
- Rubric position bias 2026 — https://arxiv.org/html/2602.02219
- Holistic vs analytic essay scoring 2026 — https://arxiv.org/abs/2604.00259

**Goodhart and reward hacking**
- Zhuang & Hadfield-Menell 2020 — https://arxiv.org/abs/2102.03896
- Skalse et al. 2022 — https://arxiv.org/abs/2209.13085
- Manheim & Garrabrant 2018 — https://arxiv.org/abs/1803.04585
- Gao, Schulman & Hilton 2023 — https://arxiv.org/abs/2210.10760
- Moskovitz et al. 2023 — https://arxiv.org/abs/2310.04373
- Coste et al. 2023 — https://arxiv.org/abs/2310.02743
- Eisenstein et al. 2023 — https://arxiv.org/abs/2312.09244
- Ichihara et al. 2025, MO-GRPO — https://arxiv.org/abs/2509.22047
- Han et al. 2025, RLUF — https://arxiv.org/html/2505.14946

**Metric design and validity**
- Rodden, Hutchinson & Fu 2010, HEART — https://research.google/pubs/measuring-the-user-experience-on-a-large-scale-user-centered-metrics-for-web-applications/
- Grove 1983, paired indicators (secondary) — https://benrobertsonis.netlify.app/notes/high-output-management
- Jacobs & Wallach 2021 — https://arxiv.org/abs/1912.05511
- Thomas & Uminsky 2020 — https://arxiv.org/abs/2002.08512
- Bean et al. 2025, construct validity of LLM benchmarks — https://arxiv.org/abs/2511.04703
- Spotify 2026, When proxy metrics break — https://confidence.spotify.com/blog/proxy-metrics.md
