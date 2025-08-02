import os, yaml, subprocess, re, json, tempfile, time

REVIEWS_DIR = 'reviews'
RULES_FILE = 'framework/rules.yaml'
PROMPTFOO_CONFIG = 'promptfooconfig.yaml'

# ✅ Load rules
with open(RULES_FILE) as f:
    rules = yaml.safe_load(f)['rules']

# ✅ Collect all .md files
files = [f for f in os.listdir(REVIEWS_DIR) if f.endswith('.md')]

# ✅ Build promptfoo config
config = {
    "providers": [{"id": "echo"}],
    "prompts": ["{{ run_output }}"],
    "tests": []
}

# ✅ Create tests per file per rule
for file in files:
    with open(os.path.join(REVIEWS_DIR, file)) as f:
        content = f.read()

    for rule in rules:
        label = f"{file} :: {rule['name']}"
        test_case = {
            "name": label,
            "vars": {"run_output": f"Validating: {label}"},
            "assert": []
        }

        # ✅ icontains check
        if 'icontains' in rule:
            if rule['icontains'].lower() in content.lower():
                test_case["assert"].append({"type": "equals", "value": f"Validating: {label}"})
            else:
                test_case["assert"].append({"type": "equals", "value": "__FAIL__"})

        # ✅ regex check
        if 'regex' in rule:
            if re.search(rule['regex'], content, re.MULTILINE):
                test_case["assert"].append({"type": "equals", "value": f"Validating: {label}"})
            else:
                test_case["assert"].append({"type": "equals", "value": "__FAIL__"})

        config["tests"].append(test_case)

# ✅ Write config
with open(PROMPTFOO_CONFIG, 'w') as f:
    yaml.dump(config, f)

# ✅ Create temp JSON file
with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmpfile:
    result_file = tmpfile.name

# ✅ Run promptfoo
subprocess.run([
    "promptfoo", "eval", "--no-cache",
    "--output", f"json:{result_file}"
])

# ✅ Wait until JSON is written
for _ in range(10):
    if os.path.exists(result_file) and os.path.getsize(result_file) > 0:
        break
    time.sleep(0.5)

# ✅ Read results safely & summarize
if os.path.exists(result_file) and os.path.getsize(result_file) > 0:
    with open(result_file) as f:
        results = json.load(f)

    failed = {}
    for test in results.get('results', []):  # ✅ correct key
        file_name = test['name'].split(' :: ')[0]
        if not test['success']:
            failed.setdefault(file_name, []).append(test['name'])

    print("\n====== TEST SUMMARY ======")
    if failed:
        for fname, checks in failed.items():
            print(f"❌ {fname}: {len(checks)} failed")
            for c in checks:
                print(f"   - {c}")
    else:
        print("✅ All tests passed!")
else:
    print("⚠️ No results or output file missing!")
