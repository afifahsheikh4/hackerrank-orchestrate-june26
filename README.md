# 🚀 Damage Claim Verification System

This project implements a **rule-based multimodal system** to verify damage claims across three object types:

- 🚗 Cars  
- 💻 Laptops  
- 📦 Packages  

Built for **HackerRank Orchestrate (June 2026 Hackathon)**.

---

## 🧠 Overview

The system processes:

- 📄 Claim conversations (text)
- 📸 Image metadata (image paths and count)
- 📊 User claim history

It determines whether the submitted evidence:

- ✅ **Supported** → Evidence matches the claim  
- ❌ **Contradicted** → Evidence conflicts with claim  
- ⚠️ **Not Enough Information** → Insufficient or unclear evidence  

---

## ⚙️ Approach

This solution uses a **deterministic rule-based pipeline**:

### 🔍 Key Components

- **Evidence Evaluation**
  - Checks if sufficient images are provided

- **Issue Detection**
  - Identifies damage type (crack, dent, broken, etc.)

- **Object Part Classification**
  - Maps claims to parts (bumper, screen, keyboard, etc.)

- **Risk Analysis**
  - Uses historical claims to assign risk levels

- **Claim Decision Engine**
  - Outputs: `supported`, `contradicted`, or `not_enough_information`

- **Safety Layer**
  - Detects malicious instructions (prompt injection attempts)

---

## ✅ Features

- ✅ Fully offline system (no APIs used)
- ✅ Explainable decision-making
- ✅ Safety-first design (avoids overconfidence)
- ✅ Handles ambiguous and low-evidence cases
- ✅ Clean structured output

---

## 📂 Project Structure
.
├── code/
│   └── main.py              # Main system logic
├── dataset/
│   ├── claims.csv           # Input claims
│   ├── user_history.csv     # User risk data
│   ├── evidence_requirements.csv
│   └── output.csv           # Generated predictions
└── README.md

---

## ▶️ How to Run

```bash
python code/main.py
```

Output will be generated at:
dataset/output.csv


📊 Output Format
Each claim produces:

evidence_standard_met
evidence_standard_met_reason
risk_flags
issue_type
object_part
claim_status
claim_status_justification
supporting_image_ids
valid_image
severity


⚠️ Limitations

Uses keyword-based matching (no deep vision models)
Does not perform actual image pixel analysis
May classify complex claims as not_enough_information


🚀 Future Improvements

🔹 Integrate vision-language models (VLMs)
🔹 Use embeddings for better semantic understanding
🔹 Add confidence scoring
🔹 Improve severity estimation


📝 Notes

✅ No hardcoded answers
✅ No external APIs
✅ Built under hackathon constraints (time + resources)


🏆 Summary
This system prioritizes:

✅ Accuracy over guessing
✅ Safety over overconfidence
✅ Explainability over complexity