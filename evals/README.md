# Evaluation

The dataset contains 30 realistic research questions. Run `python -m evals.run_evaluation` to execute the real graph and write `evaluation_results/latest.json`. The local runner reports transparent proxy metrics so it remains runnable without a separate evaluation service. For a formal benchmark, connect the same dataset to Ragas/LangSmith and retain the actual run output. Never place invented scores in the README or CV.
