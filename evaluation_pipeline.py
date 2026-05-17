import ollama
import pandas as pd
from datetime import datetime
import os

print("SCRIPT STARTED", flush=True)

models = [
    "zysec",
    "qwen-uncensored",
    "ctfsolver"
    "gemma"
]

temperatures = [0, 0.5, 1.0]

questions = pd.read_csv("questions.csv")
output_file = "evaluation_scores.csv"


if os.path.exists(output_file):
    results_df = pd.read_csv(output_file, sep=";")
    results = results_df.to_dict("records")

    completed = set(
        zip(
            results_df["model"],
            results_df["temperature"].astype(float),
            results_df["question_id"].astype(str)
        )
    )

    print(f"Loaded {len(results)} existing results. Resume mode enabled.", flush=True)

else:
    results = []
    completed = set()
    print("No existing results found. Starting fresh.", flush=True)

for model in models:
    for temp in temperatures:
        for _, row in questions.iterrows():
            question_id = str(row["question_id"]).strip()
            question = row["question"]
            category = row["category"]

            key = (model, float(temp), question_id)

            if key in completed:
                print(f"Skipping already completed: {model} | temp={temp} | {question_id}", flush=True)
                continue

            print(f"\nRunning {model} | temp={temp} | {question_id}", flush=True)

            try:
                response = ollama.chat(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": question
                        }
                    ],
                    options={
                        "temperature": temp,
                        "top_p": 0.9,
                        "num_predict": 4096,
                        "num_ctx": 8192
                    }
                )

                answer = response["message"]["content"].replace("\n", " ").replace("\r", " ")

            except Exception as e:
                answer = f"ERROR: {e}"

            print(f"\n--- {question_id} ---")
            print(f"Model: {model}")
            print(f"Temperature: {temp}")
            print(f"Category: {category}")
            print(f"Question: {question}")
            print(f"Answer:\n{answer}")
            print("\n" + "=" * 80 + "\n")

            results.append({
                "model": model,
                "temperature": temp,
                "question_id": question_id,
                "category": category,
                "question": question,
                "raw_response": answer,
                "timestamp": datetime.now().isoformat()
            })

            completed.add(key)

            pd.DataFrame(results).to_csv(
                output_file,
                index=False,
                encoding="utf-8",
                sep=";"
            )

print(f"Done. Results saved to {output_file}")
