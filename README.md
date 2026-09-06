# Medical Data Validator

A small Python tool that validates a list of patient medical records against a
fixed schema — checking required fields, correct data types, and simple
formatting rules (ID prefixes, minimum age, allowed gender values, and so on).

This is a good first step in any data pipeline: catching malformed or
inconsistent records *before* they get fed into analysis or a machine
learning model.

## What it checks

For each record, the validator confirms:

| Field            | Rule                                                            |
|-------------------|------------------------------------------------------------------|
| `patient_id`      | String matching the pattern `P<digits>` (case-insensitive)      |
| `age`             | Integer, `>= 18`                                                 |
| `gender`          | String, one of `male` / `female` (case-insensitive)              |
| `diagnosis`       | String, or `None`                                                |
| `medications`     | List of strings (can be empty)                                   |
| `last_visit_id`   | String matching the pattern `V<digits>` (case-insensitive)       |

A dataset is only considered valid if:
1. It's a `list` or `tuple`.
2. Every item in it is a `dict`.
3. Every dict has **exactly** the six fields above (no missing or extra keys).
4. Every field in every record passes its individual rule.

## Project structure

```
medical-data-validator/
├── validator.py           # Core validation logic
├── example.py              # Sample data + demo run
├── tests/
│   └── test_validator.py   # Test suite (pytest)
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

## Installation

```bash
git clone https://github.com/<your-username>/medical-data-validator.git
cd medical-data-validator
pip install -r requirements.txt   # only needed to run the tests
```

No external libraries are required to run the validator itself — it only
uses Python's standard library (`re`).

## Usage

```python
from validator import validate

records = [
    {
        'patient_id': 'P1001',
        'age': 34,
        'gender': 'Female',
        'diagnosis': 'Hypertension',
        'medications': ['Lisinopril'],
        'last_visit_id': 'V2301',
    },
]

validate(records)
# -> prints "Valid format." and returns True
```

Or just run the included demo:

```bash
python example.py
```

### Example: catching a bad record

```python
from validator import validate

bad_records = [
    {
        'patient_id': 'X999',       # wrong prefix
        'age': 10,                  # under 18
        'gender': 'unknown',        # not male/female
        'diagnosis': 'Flu',
        'medications': ['Tylenol'],
        'last_visit_id': 'V1',
    }
]

validate(bad_records)
```

Output:

```
Invalid record at position 0: invalid field(s) ['patient_id', 'age', 'gender'] in {...}.
```

## Running the tests

```bash
pytest
```

## Known limitations / next steps

This is a learning project, so it's intentionally simple. Some ideas for
extending it:

- Return structured error objects instead of printing to stdout, so callers
  can handle validation failures programmatically.
- Support configurable schemas instead of a hard-coded field list.
- Add CLI support to validate records from a CSV/JSON file.
- Add logging instead of `print()`.

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for
details.
