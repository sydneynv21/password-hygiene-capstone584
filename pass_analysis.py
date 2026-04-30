import re
import json
from typing import Dict, Any

#load breached password database json
def load_rockyou(file_path: str = "rockyou_trimmed.txt"):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return set(line.strip() for line in f)

BREACHED_PASSWORDS = load_rockyou()

# Load dictionary json
def load_dictionary(file_path="words_dictionary.json"):
    with open(file_path, "r") as f:
        return set(json.load(f))

DICTIONARY_WORDS = load_dictionary()


def password_strength(password: str) -> Dict[str, int]:
    #set up score variables
    length_score = 0
    predictability_score = 0
    patterns_score = 0
    variety_score = 0

    # Score length 
    if len(password) < 8:
        length_score = 1
    elif 8 <= len(password) < 12:
        length_score = 4
    elif 12 <= len(password) < 15:
        length_score = 7
    else:
        length_score = 10

    # Score predictability
    # - subtracts from 5 each time 3 or more characters or numbers appear in sequence
    predictability_score = 5
    if re.search(r"[a-zA-Z]{3,}", password):
        predictability_score -= 2
    if re.search(r"\d{3,}", password):
        predictability_score -= 2
    predictability_score = max(0, predictability_score)

    # Patterns 
    # - repeated char 3+ times (aaa, 111)
    # - simple sequences (abc, 123)
    patterns_score = 10


    if re.search(r"(.)\1\1", password):
        patterns_score -= 5

    lowered = password.lower()
    common_seqs = ["0123", "1234", "2345", "3456", "4567", "5678", "6789",
                   "abcd", "bcde", "cdef", "qwer", "asdf", "zxcv"]
    if any(seq in lowered for seq in common_seqs):
        patterns_score -= 4

    patterns_score = max(0, patterns_score)

    # Scores character/digit variety
    has_digit = any(c.isdigit() for c in password)
    has_letter = any(c.isalpha() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if has_digit and has_letter and has_special:
        variety_score = 10
    elif (has_letter and has_digit) or (has_letter and has_special) or (has_digit and has_special):
        variety_score = 6
    else:
        variety_score = 2

    return {
        "Length": length_score,
        "Predictability": predictability_score,
        "Patterns": patterns_score,
        "Variety": variety_score
    }
#checks to see if password is in list of dictionary words from json file (min 4 characters)
def check_password_in_dictionary(password: str) -> Dict[str, str]:
    password = password.lower()
    MIN_LENGTH = 4

    for i in range(len(password)):
        for j in range(i + MIN_LENGTH, len(password) + 1):
            if password[i:j] in DICTIONARY_WORDS:
                return {"in_dictionary": "yes"}

    return {"in_dictionary": "no"}

def check_password_in_breach(password: str) -> Dict[str, str]:
    if password in BREACHED_PASSWORDS:
        return {"breach_detected": "yes"}
    return {"breach_detected": "no"}

#Combines checks into one metrics object that is safe to send to an LLM.
#DOES NOT include the raw password.
def get_safe_metrics(password: str) -> Dict[str, Any]:
    
    scores = password_strength(password)
    dict_hit = check_password_in_dictionary(password)
    breach_hit = check_password_in_breach(password)

    total_raw = scores["Length"] + scores["Predictability"] + scores["Patterns"] + scores["Variety"]

    # Apply penalties
    if dict_hit["in_dictionary"] == "yes":
        total_raw -= 3

    if breach_hit["breach_detected"] == "yes":
        total_raw -= 8  # heavier penalty

    total_raw = max(0, total_raw)
    total_100 = round((total_raw / 35) * 100)

    if total_100 < 40:
        severity = "Weak"
    elif total_100 < 70:
        severity = "Moderate"
    else:
        severity = "Strong"

    has_digit = any(c.isdigit() for c in password)
    has_letter = any(c.isalpha() for c in password)
    has_special = any(not c.isalnum() for c in password)

    return {
        "scores": scores,
        "total_100": total_100,
        "severity": severity,
        "length": len(password),
        "has_digit": has_digit,
        "has_letter": has_letter,
        "has_special": has_special,
        "in_dictionary": dict_hit["in_dictionary"],
        "breach_detected": breach_hit["breach_detected"],
    }

