# test_cases.py

TEST_PASSWORDS = [
    #Dictionary tests
    {
        "category": "Dictionary",
        "name": "simple word",
        "password": "simple",
        "expected": {"in_dictionary": "yes"}
    },
    {
        "category": "Dictionary",
        "name": "word surrounded by numbers",
        "password": "12cyber34",
        "expected": {"in_dictionary": "yes"}
    },
    {
        "category": "Dictionary",
        "name": "multiple words",
        "password": "dogsarecool",
        "expected": {"in_dictionary": "yes"}
    },
     {
        "category": "Dictionary",
        "name": "words separated by symbols",
        "password": "*cannon#ball&",
        "expected": {"in_dictionary": "yes"}
    },

    #Repeated characters
    {
        "category": "Patterns",
        "name": "repeated letters",
        "password": "aaaaaaa",
        "expected": {"Patterns_low": True}
    },
    {
        "category": "Patterns",
        "name": "repeated digits",
        "password": "11111111",
        "expected": {"Patterns_low": True}
    },
    {
        "category": "Patterns",
        "name": "mixed repetition",
        "password": "aaaBBB111",
        "expected": {"Patterns_low": True}
    },

    #Weak passwords
    {
        "category": "Weak",
        "name": "very common password",
        "password": "password",
        "expected": {
            "severity": "Weak",
            "score_max": 40
        }
    },
    {
        "category": "Weak",
        "name": "short and simple",
        "password": "abc",
        "expected": {
            "severity": "Weak",
            "score_max": 40
        }
    },
    {
        "category": "Weak",
        "name": "repeated characters",
        "password": "aaaaaaa",
        "expected": {
            "severity": "Weak",
            "score_max": 40
        }
    },

    #Moderate passwords
    {
        "category": "Moderate",
        "name": "basic mix",
        "password": "helloWorld12",
        "expected": {
            "severity": "Moderate",
            "score_min": 40,
            "score_max": 70
        }
    },
    {
        "category": "Moderate",
        "name": "long but simple",
        "password": "thisisalongpassword",
        "expected": {
            "severity": "Moderate",
            "score_min": 40,
            "score_max": 70
        }
    },

    #Strong passwords
    {
        "category": "Strong",
        "name": "complex mix",
        "password": "College@Graduate#2026",
        "expected": {
            "severity": "Strong",
            "score_min": 70
        }
    },
    {
        "category": "Strong",
        "name": "long passphrase with symbols",
        "password": "PennsylvaniaStateUniversity!",
        "expected": {
            "severity": "Strong",
            "score_min": 70
        }
    },
    {
        "category": "Strong",
        "name": "completely random",
        "password": "XPfO$vdS914WS5",
        "expected": {
            "severity": "Strong",
            "score_min": 70
        }
    },

    #Breach tests (must exist in RockYou)
    {
        "category": "Breach",
        "name": "very common password",
        "password": "123456",
        "expected": {"breach_detected": "yes"}
    },
    {
        "category": "Breach",
        "name": "classic weak password",
        "password": "password",
        "expected": {"breach_detected": "yes"}
    },
    {
        "category": "Breach",
        "name": "keyboard pattern",
        "password": "qwerty",
        "expected": {"breach_detected": "yes"}
    },
]