# Approved held-out evaluation

User approved the AI-assisted dev reviews and I1 configuration, following the explicit proposal to check connectivity then run test. This phase executes only baseline Dense 800/arrival and selected Dense 2000/arrival on the same frozen seven test queries. No changes to agent, prompt, provider, retrieval or benchmark. No tuning against test, no replacing failures, no commit or push.

Use existing Day06 environment and offline model/store. New `src/run_test.py` provides a test-only gate, checks approved runtime hashes and query/corpus hashes, snapshots execution sources, registers one run and resumes missing cases only. Query-only data enters inference; gold loads after all executions. Keep failures and unknown usage explicit.

- [x] Record user acceptance of 85 AI-assisted dev reviews and freeze I1 for test in a separate approval artifact, preserving original review records.
- [x] Add failing tests for test-only query schema and frozen-runtime mismatch; implement runner and run offline suite.
- [x] Check real tool protocol with bounded probes unrelated to held-out questions. Run the two configurations only after two consecutive successful probes; save all probe attempts.
- [x] Execute 14 real agent cases, persist trace/usage after each; score retrieval and source-inspect all five answerable/two insufficient cases for both configurations. New labels remain AI-assisted pending user's confirmation.
- [x] Verify artifacts, index/corpus/secret handling, report results and stop for review before submission/report/demo phase.

Selection rule and I1 were chosen on dev before test. API failures are failures, not correct refusals. This phase evaluates the selected configuration even if it performs worse than baseline. Existing dev labels remain AI-assisted user-confirmed, not independent human annotation.

## Current execution state

External connection blocker: two bounded preflight runs (`20261116T032840548620Z`, `20261116T033151223927Z`) failed the two-consecutive-success condition. Thirteen provider requests were made for probes, five failed without HTTP status. Direct unauthenticated TLS/HEAD also timed out. No claim of a specific network/provider root cause, invalid key or quota exhaustion. No network settings changed.

Held-out execution has not started: both manifests retain `test_evaluated=false`, no registry exists and no baseline/I1 test traces or test grades were produced. Approvals and frozen runtime remain valid. Summary/logs at `results/test/preflight_summary.json` and README. Resume the authorized work once connectivity stabilizes; use a new invocation, not --resume on preflight-only directories.

31 offline tests pass; independent read-only runner review found no material issues. Do not mark held-out evaluation complete or create fictitious test results. No commit/push.

## Continued execution and transport ruling

User requested continuation and confirmed their network was otherwise functioning. A diagnostic outside the benchmark reproduced the suppressed underlying exception: `URLError` caused by `TimeoutError`, errno/winerror 10060, before HTTP status. The client retried HTTP 429/5xx only, so transient socket failures immediately aborted calls. GitHub HEAD returned 200 and DeepSeek HEAD returned 401 quickly in the control checks; do not attribute this to general user Internet failure.

Ruling before any test inference: extend the existing two-retry cap to transient timeout/reset connection exceptions, without changing model/prompt/payload/retrieval/context policy. Permission errors and malformed response errors do not retry. Each failed attempt remains recorded, with safe errno/class and unknown usage. This is a routine transport bugfix under the user's continued execution authorization, not a new model configuration or a change based on test outcomes.

Added regressions observed failing then passing; 33 tests pass. Read-only independent review found no material issue. Two dev query-only cases D04/D07 both answered with correct sources in validation `results/dev_transport_validation/20261116T034122650865Z`.

Preserved original approval bytes in `configs/selected_for_test_transport_v1.json`; recorded exact provider hash change, unchanged generation parameters, source validation and continuation authorization in `selected_for_test.json.transport_revision`. There was no test registry or held-out inference when freezing this revision. Baseline and I1 will share the same revised transport. Earlier dev measurements retain their original transport, so do not infer improvements in error rates solely from context budget.

## Completed held-out execution

Two consecutive successful probes admitted run `results/test/20261116T034326996108Z`. All 14 cases completed: 5 answered/2 abstained for both configurations; 0 terminal case errors. Five socket timeouts were recovered and remain in request logs (3 baseline, 2 I1); unknown usage is not fabricated. No case was replaced or rerun, and no generation code/config was changed after test began.

Strict frozen-gold Hit@1=3/5, Hit@3=4/5 and final-context hit=4/5 for both. Gold unchanged despite T04 alternative source. Source inspection produced 14 new AI-assisted reviews, not user-confirmed yet: baseline answer9/10, valid abstention1/2, citation5/6; I1 answer10/10, valid abstention2/2, citation10/10. Baseline T04 lacks the with antecedent in actual context, and baseline T06 falsely narrows the entire corpus to exceptions. Read-only independent AI review agreed with these conservative source/scope judgments.

Reports and audit hashes are saved alongside traces. Historical blocked reports and original transport approval are preserved. Current test entry README points to completed results; candidate selected before test remains I1. Stop for user confirmation of new test labels before report/demo/submission work. No commit/push.
