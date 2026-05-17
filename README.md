# LLM Evaluation for Cybersecurity

## Overview

This project evaluates local large language models (LLMs) for cybersecurity use cases. We tested multiple open-source models running locally via Ollama and assessed their performance across a range of cybersecurity topics including factual knowledge, practical command generation, offensive security reasoning, code review, and hallucination resistance.

---

## Models Evaluated

### Finalists
| Model | Size | Type | HuggingFace |
|-------|------|------|-------------|
| ZySec-7B-v1 | 7B | Fine-tune | [Link](https://huggingface.co/koesn/ZySec-7B-v1-GGUF) |
| CTFsolver | 7B | Fine-tune (CTF/Offensive) | [Link](https://huggingface.co/MarkBruzon/CTFsolver-Q4_K_M-GGUF) |
| Gemma-4-E4B-it-Uncensored | 4B | Uncensored | [Link](https://huggingface.co/TrevorJS/gemma-4-E4B-it-uncensored-GGUF) |
| Qwen2.5-7B-Instruct-Uncensored | 7B | Uncensored | [Link](https://huggingface.co/QuantFactory/Qwen2.5-7B-Instruct-Uncensored-GGUF) |
| Qwen2.5-7B-Instruct | 7B | General (control) | [Link](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) |

### Screened but Eliminated
- Seneca Cybersecurity LLM
- SecurityLLM
- NVIDIA-Orchestrator-Cybersecurity-8B
- XSS-strix-8B
- MinimoSec-V4
- Cyber-Analyst-4B
- Lily-Cybersecurity-7B-Uncensored

---

## Evaluation Methodology

Models were run locally using **Ollama** with the following default parameters:

```
Temperature: 0.0 (baseline), 0.5, 1.0
Top-p: 0.9
Max tokens: 1000
Context window: 1024
```

We evaluated models across 22 questions in 5 categories:

| Category | Description |
|----------|-------------|
| Factual | Basic cybersecurity knowledge (cryptography, networking) |
| Conceptual | Security concepts (authentication, authorization) |
| Practical | Command generation, applied security tasks |
| Sensitive / Offensive | Reverse shells, Active Directory attacks, exploit reasoning |
| Code Review Trap | Finding vulnerabilities in deliberately flawed code |
| Hallucination Trap | Fabricated attack techniques to test model honesty |

Each response was scored on:
- **Clarity** — well written and on topic
- **Technical accuracy** — factually correct
- **Completeness** — covers all key points
- **Usefulness** — practical and actionable
- **Cooperativeness** — willingness to answer security questions
- **Hallucination resistance** — does not fabricate information

---

## Key Findings

- **ZySec and CTFsolver** produced the strongest practical cybersecurity responses overall
- **CTFsolver** was the best for offensive security and code review tasks
- **Gemma** was the best choice for limited hardware (≤8 GB RAM)
- **Hallucination resistance** was the weakest area across all models — most fabricated explanations for nonexistent attack techniques
- Model size did not strongly predict quality — specialization and fine-tuning mattered more

---

## Recommendations

| Scenario | Recommended Model |
|----------|------------------|
| Limited hardware (≤8 GB RAM, no GPU) | Gemma-4-E4B-it-Uncensored |
| Decent GPU (16 GB VRAM) | ZySec-7B-v1 |
| Offensive security tasks | CTFsolver |

---

## Files

| File | Description |
|------|-------------|
| `evaluation_pipeline.py` | Python script that runs all models via Ollama and saves results to CSV |
| `LLM_Report.md` | Full evaluation report with screening results, scores, and analysis |

---

## How to Run

### Requirements

```bash
pip install ollama pandas
```

Make sure Ollama is installed and running: [https://ollama.com](https://ollama.com)

Pull the models you want to test:

```bash
ollama pull zysec
ollama pull ctfsolver
ollama pull gemma
```

Create a `questions.csv` file with columns: `question_id`, `category`, `question`.

Then run:

```bash
python evaluation_pipeline.py
```

Results are saved to `evaluation_scores.csv`.
