Here’s your README with **all sections wrapped in proper Markdown code blocks** so it will render exactly as you want:

````markdown
# Architectural Reviewer (Lint Bot)

Uses OpenAI's GPT-4o model to evaluate your project's architecture based on principles like **SOLID**, layering, modularity, and abstraction.

---

## 🧠 Purpose
- Ensures **architectural consistency** as part of your CI/CD pipeline.
- Adds **automated QA checks** for:
  - ✅ Deprecated modules
  - ✅ Unused functions
  - ✅ Architectural score & impact validation
  - ✅ Performance SLA verification
  - ✅ Safety checks (no ambiguous placeholders)

---

## 📦 Requirements
- Python 3.11+
- `OPENAI_API_KEY` set in GitHub Secrets
- [Promptfoo](https://promptfoo.dev/) installed globally:

```bash
npm install -g promptfoo
````

---

## 🔧 Installation

```bash
pip install -r requirements.txt
```

---

## 🚀 Running the Linter

### 1️⃣ Generate Architectural Review

```bash
python arc_lint.py --project-root ./sample_code --output reviews/architectural_review.md
```

### 2️⃣ Run QA Test Framework

```bash
python framework/run_tests.py
```

This runs:

* All rules in `framework/rules.yaml`
* Dynamic Promptfoo tests against every `.md` file in `reviews/`

---

## 📜 Rules in `framework/rules.yaml`

```yaml
rules:
  - name: Deprecated Modules Check
    icontains: "cgi"

  - name: Old Function Check
    icontains: "old_calculation"

  - name: Must Have Score
    icontains: "Overall Architectural Score: 65 / 100"

  - name: Must Have Impact
    icontains: "Impact Assessment"

  # Performance and Safety Checks
  - name: Performance SLA
    icontains: "Response Time < 5s"

  - name: Safety Check - No Ambiguity
    regex: "^(?!.*(maybe|TBD|\\?{3})).*$"
```

---

## 🧪 What This Covers

✅ **Measure Output Quality**

* Validates architectural review content against defined rules.
* Ensures consistency, completeness, and no placeholder text.

✅ **Validate AI Behavior**

* Runs test cases per file per rule to catch missing or incorrect sections.

✅ **Benchmark Performance**

* Checks for SLA compliance (e.g., `Response Time < 5s`).

✅ **Explore Safety & Reliability**

* Flags ambiguous words like `maybe`, `TBD`, or `???` in reviews.

---

## 🛠 GitHub Integration

Add `.github/workflows/architect-review.yml` to run automatically on PRs or pushes to `main`.

---

## 📄 Output

* Linter generates: `reviews/architectural_review.md`
* QA framework prints **pass/fail per file and rule** with a summary:

```text
====== TEST SUMMARY ======
❌ architectural_review.md: 2 failed
   - Must Have Score
   - Safety Check - No Ambiguity
✅ architectural_review2.md: All tests passed!
```

---

## 🔥 Example Usage

```bash
# Run linter
python arc_lint.py --project-root ./sample_code --output reviews/architectural_review.md

# Run QA checks
python framework/run_tests.py
```

```

👉 You can copy this entire block into `README.md` in VS Code. It will render perfectly with proper code highlighting and sections.
```
