#!/usr/bin/env python3
"""
AuzEnergyz Proof Checker
Educational tool for identifying common risk indicators in
oil & gas Soft Corporate Offers (SCOs).

This tool does NOT confirm legitimacy and does NOT label scams.
It highlights patterns that may require extra verification.
"""

import sys
import re
from datetime import datetime

DISCLAIMER = """
AuzEnergyz Proof Checker (Educational Use Only)
------------------------------------------------
This tool highlights common risk indicators found in some
oil & gas Soft Corporate Offers (SCOs).

• It does NOT prove legitimacy
• It does NOT accuse or label scams
• Always verify independently via registries, refineries, and banks
"""

RED_FLAGS = [
    {
        "name": "Official mandate language",
        "pattern": r"official mandate",
        "severity": 2,
        "explanation": "Template SCOs often use this phrase without naming a verifiable mandate chain."
    },
    {
        "name": "FOB Rotterdam with Kazakhstan origin",
        "pattern": r"fob.*rotterdam.*kazakhstan|kazakhstan.*fob.*rotterdam",
        "severity": 2,
        "explanation": "This combination is commonly used in generic SCO templates and requires strong verification."
    },
    {
        "name": "Requests for MT760 or SBLC",
        "pattern": r"mt760|sblc",
        "severity": 3,
        "explanation": "Standby instruments requested early are a frequent high-risk indicator."
    },
    {
        "name": "Deposit requested before proof",
        "pattern": r"deposit|upfront|advance payment",
        "severity": 3,
        "explanation": "Upfront payments before verifiable proof-of-product are high risk."
    },
    {
        "name": "WhatsApp-only contact",
        "pattern": r"whatsapp",
        "severity": 2,
        "explanation": "Professional sellers usually provide multiple verifiable contact methods."
    }
]

PRODUCT_PATTERN = r"(d2|d6|jet\s*a1|lng|lpg|urea|bitumen|fuel oil)"
REFINERY_PATTERN = r"refinery|refining|plant"

def read_input():
    print("\nPaste the SCO text below.")
    print("When finished, type END on a new line and press Enter.\n")
    lines = []
    for line in sys.stdin:
        if line.strip() == "END":
            break
        lines.append(line)
    return " ".join(lines).lower()

def analyze(text):
    findings = []
    score = 0

    for flag in RED_FLAGS:
        if re.search(flag["pattern"], text):
            findings.append(flag)
            score += flag["severity"]

    if not re.search(REFINERY_PATTERN, text):
        findings.append({
            "name": "No refinery name mentioned",
            "severity": 2,
            "explanation": "Legitimate offers usually name a specific refinery or allocation holder."
        })
        score += 2

    products = re.findall(PRODUCT_PATTERN, text)
    if len(set(products)) >= 5:
        findings.append({
            "name": "Too many unrelated petroleum products",
            "severity": 2,
            "explanation": "Listing many unrelated products is common in template SCOs."
        })
        score += 2

    if score >= 8:
        risk = "HIGH"
    elif score >= 4:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return findings, score, risk

def save_report(findings, score, risk):
    filename = "proof_report.txt"
    with open(filename, "w") as f:
        f.write(DISCLAIMER + "\n\n")
        f.write(f"Date: {datetime.utcnow()} UTC\n")
        f.write(f"Risk score: {score}\n")
        f.write(f"Overall risk level: {risk}\n\n")

        if findings:
            f.write("Detected risk indicators:\n")
            for i, flag in enumerate(findings, 1):
                f.write(f"{i}. {flag['name']} – {flag['explanation']}\n")
        else:
            f.write("No red flags detected by this checker.\n")

        f.write("\nRecommended next steps:\n")
        f.write("- Verify company registration in official registries\n")
        f.write("- Confirm refinery and allocation directly\n")
        f.write("- Use bank-to-bank verification channels\n")

    return filename

def main():
    print(DISCLAIMER)
    text = read_input()
    findings, score, risk = analyze(text)

    print("\nRESULTS")
    print("--------")
    print(f"Risk score: {score}")
    print(f"Overall risk level: {risk}\n")

    if findings:
        for i, flag in enumerate(findings, 1):
            print(f"{i}. {flag['name']}")
            print(f"   - {flag['explanation']}")
    else:
        print("No red flags detected by this checker.")

    report_file = save_report(findings, score, risk)
    print(f"\nReport saved to: {report_file}")

if __name__ == "__main__":
    main()
