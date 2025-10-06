# Evaluation Guide

## Present Damage Assessment
- **Accuracy**: Percentage of cases where the top predicted damage type and severity match ground truth.
- **F1 Score**: Computed on damage-type classifications across cases.
- **Cohen's κ**: Agreement metric between GPT predictions and expert annotations.

## Forecast Evaluation
- **Brier Score**: Calculate per horizon (30/90/180/365 days) using the forecast probabilities and observed outcomes.
- **Log-Loss**: Use probabilistic log-loss for each horizon to penalize overconfident errors.
- **Reliability Plots**: Bin forecast probabilities to visualize calibration across horizons.

## Severity & Action Matching
- Treat severity levels as ordered categories; near misses (±1 severity grade) should be noted separately.
- Map recommended actions using `schema/taxonomy.csv` to verify consistency with maintenance guidance.

## Reporting Standards
- Document evaluation runs in `eval/evaluation_log.md`.
- Store confusion matrices in `eval/confusion_matrices/` and calibration plots in `eval/plots/`.
