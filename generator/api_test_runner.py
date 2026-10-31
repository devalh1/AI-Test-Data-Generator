
from pathlib import Path
import json
import requests


PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "output" / "generated_test_cases.json"
REPORT_FILE = PROJECT_ROOT / "output" / "test_run_report.json"

BASE_URL = "http://127.0.0.1:8000"


def run_tests():
    with INPUT_FILE.open("r", encoding="utf-8") as file:
        endpoints = json.load(file)

    results = []

    for endpoint in endpoints:
        method = endpoint["method"].upper()
        path = endpoint["endpoint"]

        for test_case in endpoint["test_cases"]:
            request_body = test_case["request_body"]
            expected = test_case["expected"]

            result = {
                "endpoint": path,
                "method": method,
                "test_type": test_case["test_type"],
                "field": test_case["field"],
                "expected": expected,
                "request_body": request_body,
            }

            try:
                response = requests.request(
                    method=method,
                    url=f"{BASE_URL}{path}",
                    json=request_body,
                    timeout=10,
                )

                status_code = response.status_code

                if expected == "valid":
                    passed = 200 <= status_code < 300
                else:
                    passed = 400 <= status_code < 500

                result["status_code"] = status_code
                result["actual"] = (
                    "valid" if 200 <= status_code < 300 else "invalid"
                )
                result["result"] = "PASS" if passed else "FAIL"

                try:
                    result["response_body"] = response.json()
                except ValueError:
                    result["response_body"] = response.text

            except requests.RequestException as error:
                result["status_code"] = None
                result["actual"] = "no response"
                result["result"] = "ERROR"
                result["error"] = str(error)

            results.append(result)

            print(
                f"{result['result']} | {method} {path} | "
                f"{result['test_type']} | "
                f"HTTP {result['status_code']}"
            )

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with REPORT_FILE.open("w", encoding="utf-8") as file:
        json.dump(results, file, indent=2, ensure_ascii=False)

    passed_count = sum(r["result"] == "PASS" for r in results)
    failed_count = sum(r["result"] == "FAIL" for r in results)
    error_count = sum(r["result"] == "ERROR" for r in results)

    print("\n========== TEST SUMMARY ==========")
    print(f"Total:  {len(results)}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {failed_count}")
    print(f"Errors: {error_count}")
    print(f"Report: {REPORT_FILE}")


if __name__ == "__main__":
    run_tests()
