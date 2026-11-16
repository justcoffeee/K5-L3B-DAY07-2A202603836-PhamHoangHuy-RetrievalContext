# Dev context improvement plan

**Goal:** Audit the approved dev run and measure two context changes, without opening test for evaluation.

**Scope/authorization:** User accepted the previous dev results after the proposal to read/grade dev and try two context configurations. Continue inline in the existing feature branch. No new dependencies, paid judge, test run, commit or push.

**Design:** Dense is the current dev-leading retriever. Baseline remains the actual 800-character arrival-order run `20261116T024332489435Z/dense`. Configuration I1 changes budget to 2000 characters, keeping arrival order. Configuration I2 uses the same 2000-character budget but places the most recent search ranking ahead of earlier candidates. Both keep identical DeepSeek model, prompt, 3 searches, top 3 and corpus/index. Old results stay unchanged.

**Hypotheses:** Dense D04 and D07 retrieved correct evidence but discarded it during packing. I1 may retain it. I2 may replace stale initial candidates with better later results, but can also displace useful earlier evidence. Report either outcome, do not tune on test.

**Selection rule declared before new runs:** Rank configurations by grounded-answer total over all 15 answerable cases (0/1/2, errors and false refusals score zero); then correct abstention out of 2; fewer protocol/provider errors; higher final-context evidence rate; fewer total tokens; arrival policy if still tied. Labels are AI-assisted and provisional until user confirms. Choose a candidate only, with no test evaluation at this stage.

**Evaluation:** Read each answer, context, source and citation. Preserve 51 original traces and 34 new traces. Store versioned AI-assisted reviews and per-citation reasons, context 0/1/2, answer 0/1/2, refusal labels and explicit errors. Report successful-case starter aggregates separately from all-case quality totals so errors cannot improve the denominator. Flag inline citations absent from declared citation arrays rather than quietly rewriting traces.

## Tasks

- [x] 1. Read baseline outputs and record evidence-based review notes.
- [x] 2. Add failing tests for latest-candidate priority and compatibility with arrival order; implement configurable context policy/budget without changing defaults or prompt.
- [x] 3. Run offline checks, then 17 real Dense dev cases for I1 and 17 for I2. Persist full provenance, usage, traces; no test input or gold sent to model.
- [x] 4. Read all new outputs, write AI-assisted reviews, compare metrics/cost, nominate a configuration using the stated rule. Verify hashes, secrecy, review alignment and unchanged store.
- [x] 5. Report results and stop for user's approval before test/final submission work.

## Ledger

- Skill workflow: brainstorming scoped to the already approved experiments, writing-plans and executing-plans inline, test-driven development and verification before claiming completion.
- No further model/prompt/refusal-schema changes in these experiments: isolate context packing effects. Protocol errors remain errors.
- I1 run `20261116T030001129031Z`: 14 answered, 2 abstain, 1 provider error (D07). Known usage 40291 tokens; 1 failed request without usage. AI-assisted answer total 28/30, abstention 2/2.
- I2 run `20261116T030303500415Z`: 7 answered, 1 abstain, 9 provider errors. Known usage 23215 tokens; 9 failed requests without usage. AI-assisted answer total 14/30, abstention 1/2. Provider failures confound policy comparison; no claim latest is intrinsically worse.
- Recorded 85 per-case AI-assisted reviews with reasons and trace hashes. Original traces and blank review templates unchanged. Baseline Dense D04 unlisted inline citation flagged. Prepared context vs successful-pipeline context separated.
- Independent read-only code/audit review found no material issues. Labels remain AI-assisted, not human-independent, and await user confirmation.
- Proposed I1 using the predeclared rule; stored candidate is pending review and does not authorize test. No new packages, paid judge, reruns replacing failures, commits or pushes.
