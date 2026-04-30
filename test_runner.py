from pass_analysis import get_safe_metrics
from prompt_builder import build_prompt
from ollama_client import OllamaClient
from test_cases import TEST_PASSWORDS


def run_analysis_tests():
    print("\n=== Password Analysis Tests ===\n")

    current_category = None

    for test in TEST_PASSWORDS:
        if test["category"] != current_category:
            current_category = test["category"]

            # Rename category for display only
            display_category = "Moderate" if current_category == "Okay" else current_category
            print(f"\n--- {display_category} Tests ---")

        metrics = get_safe_metrics(test["password"])
        expected = test["expected"]
        passed = True
        issues = []

        # Weak / Moderate / Strong → score + severity ONLY
        if test["category"] in ["Weak", "Moderate", "Strong"]:

            if "severity" in expected:
                if metrics["severity"] != expected["severity"]:
                    issues.append(
                        f"Severity mismatch: expected {expected['severity']}, got {metrics['severity']}"
                    )
                    passed = False

            if "score_min" in expected:
                if metrics["total_100"] < expected["score_min"]:
                    issues.append(
                        f"Score too low: expected >= {expected['score_min']}, got {metrics['total_100']}"
                    )
                    passed = False

            if "score_max" in expected:
                if metrics["total_100"] > expected["score_max"]:
                    issues.append(
                        f"Score too high: expected <= {expected['score_max']}, got {metrics['total_100']}"
                    )
                    passed = False

        # Dictionary / Patterns / Breach → feature checks ONLY
        else:
            for key, expected_value in expected.items():

                if key == "Patterns_low":
                    if metrics["scores"]["Patterns"] >= 6:
                        issues.append(
                            f"Patterns score too high: expected low pattern score, got {metrics['scores']['Patterns']}"
                        )
                        passed = False

                else:
                    if metrics.get(key) != expected_value:
                        issues.append(
                            f"{key} mismatch: expected {expected_value}, got {metrics.get(key)}"
                        )
                        passed = False

        result = "PASS" if passed else "FAIL"

        print(f"{result}: {test['name']}")
        print(f"   Password: {test['password']}")

        # Only show score/severity for evaluation categories
        if test["category"] in ["Weak", "Moderate", "Strong"]:
            display_severity = "Moderate" if metrics["severity"] == "Okay" else metrics["severity"]
            print(f"   Score: {metrics['total_100']} | Severity: {display_severity}")

        # Print issues AFTER result
        if issues:
            for issue in issues:
                print(f"   {issue}")


def main():
    run_analysis_tests()


if __name__ == "__main__":
    main()