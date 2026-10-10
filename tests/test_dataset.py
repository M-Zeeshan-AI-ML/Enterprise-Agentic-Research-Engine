import json
def test_dataset_size():
 rows=[json.loads(x) for x in open('evals/dataset.jsonl') if x.strip()]; assert len(rows)>=30
