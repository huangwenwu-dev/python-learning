import json

with open("week14/eval_dataset.json", encoding="utf-8") as f:
    dataset = json.load(f)

with open("week14/eval_dataset.jsonl", "w", encoding="utf-8") as f:
    for item in dataset:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")