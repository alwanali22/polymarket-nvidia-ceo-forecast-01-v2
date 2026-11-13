# Forecasting Engine

This program implements a mean-reversion forecaster for trading market prices, based on a regime detection mechanism that determines if the market is 'chaotic' or 'calm'. It uses historical price data to establish a median price level and a volatility spread, projecting future price distributions using exponential decay models for both the median and variance over a 240-minute horizon.

## How to Run
To run the program locally, set the environment variables `MAKEFUN_INPUT_DIR` to your input directory and `MAKEFUN_OUTPUT_DIR` to your output directory, then execute the script:

```bash
export MAKEFUN_INPUT_DIR=/path/to/input
export MAKEFUN_OUTPUT_DIR=/path/to/output
python3 repo/main.py
```

## Practice Grades
tuning cases p00 to p02 loss 0.395741, holdout cases p03 to p05 loss 0.199243, all six practice cases loss 0.286746; per-case losses p00 0.472, p01 0.304, p02 0.411, p03 0.286, p04 0.197, p05 0.118; median error 0.7729 and 90 percent coverage 0.8427 over all six cases; house baseline loss 0.363589 on the same cases, so this entry beats the baseline by 19.3 percent on the practice and by 33.2 percent on the holdout cases. The regime detector classifies the earliest practice case as chaotic (fast reversion) and the other five as calm (slow reversion).
