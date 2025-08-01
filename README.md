```markdown
# Architectural Reviewer (Lint Bot)

Uses OpenAI's GPT-4o model to evaluate your Python project's architecture based on principles like SOLID, layering, modularity, and abstraction.

## 🧠 Purpose
Ensures architectural consistency as part of your CI/CD pipeline.

## 📦 Requirements
- Python 3.11+
- `OPENAI_API_KEY` set in GitHub Secrets

## 🔧 Installation
```bash
pip install -r requirements.txt
```

## 🚀 Run Manually
```bash
python architect-reviewer.py --project-root . --output architectural_review.md
```

## 🛠 GitHub Integration
Add the `.github/workflows/architect-review.yml` file. It will run on every PR or push to `main`.

## 📄 Output
The review is saved to `architectural_review.md` with:
- Architectural impact assessment
- Pattern compliance checklist
- Violations & recommended refactors
- Long-term implications
```

