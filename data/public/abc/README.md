# HMUBench-ABC

## Data

- `data/zh/questions.json`: 1,029 Chinese questions without answers.
- `data/en/questions.json`: 1,029 English questions without answers.
- `data/zh/with_answers.json`: Chinese reference answers.
- `data/en/with_answers.json`: English reference answers.
- Both editions have exactly aligned IDs, ordering, and ABC materials.

For model inference, use only the `materials` and `question` fields from
`questions.json`. During scoring, join `with_answers.json` by `id`. Do not add
gold answers to the model input.

## Version

The final revision identifier is `abc-manual-revision-20261008`.
`validation/current_dataset.json` records question counts, day distribution,
and bilingual alignment. ABC aggregate results are available at
`../../aggregate_results/abc_aggregate_results.json`.
