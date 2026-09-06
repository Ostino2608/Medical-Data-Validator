"""
Medical record validator.

Checks a list of patient record dictionaries against a fixed schema:
required fields, correct types, and simple format rules (ID prefixes,
minimum age, allowed gender values, etc.).
"""

import re

REQUIRED_FIELDS = {
    'patient_id',
    'age',
    'gender',
    'diagnosis',
    'medications',
    'last_visit_id',
}


def find_invalid_fields(patient_id, age, gender, diagnosis, medications, last_visit_id):
    """
    Check a single record's fields against the validation rules.

    Returns a list of field names that failed validation. An empty
    list means the record is valid.
    """
    constraints = {
        'patient_id': isinstance(patient_id, str)
        and re.fullmatch(r'p\d+', patient_id, re.IGNORECASE) is not None,
        'age': isinstance(age, int) and age >= 18,
        'gender': isinstance(gender, str) and gender.lower() in ('male', 'female'),
        'diagnosis': isinstance(diagnosis, str) or diagnosis is None,
        'medications': isinstance(medications, list)
        and all(isinstance(item, str) for item in medications),
        'last_visit_id': isinstance(last_visit_id, str)
        and re.fullmatch(r'v\d+', last_visit_id, re.IGNORECASE) is not None,
    }
    return [field for field, is_valid in constraints.items() if not is_valid]


def validate(data):
    """
    Validate a list (or tuple) of medical record dictionaries.

    Prints a message for every problem found and returns True only if
    every record in `data` is well-formed and passes all field checks.
    """
    if not isinstance(data, (list, tuple)):
        print('Invalid format: expected a list or tuple.')
        return False

    is_invalid = False

    for index, record in enumerate(data):
        if not isinstance(record, dict):
            print(f'Invalid format: expected a dictionary at position {index}.')
            is_invalid = True
            continue

        if set(record.keys()) != REQUIRED_FIELDS:
            print(
                f'Invalid format: {record} at position {index} has missing '
                'and/or unexpected keys.'
            )
            is_invalid = True
            continue

        invalid_fields = find_invalid_fields(**record)
        if invalid_fields:
            print(
                f'Invalid record at position {index}: invalid field(s) '
                f'{invalid_fields} in {record}.'
            )
            is_invalid = True

    if is_invalid:
        return False

    print('Valid format.')
    return True
