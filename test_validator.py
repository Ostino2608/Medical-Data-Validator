"""
Basic tests for validator.py.

Run with:
    pytest
"""

import sys
from pathlib import Path

# Allow running pytest from the project root without installing the package.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from validator import validate, find_invalid_fields  # noqa: E402


VALID_RECORD = {
    'patient_id': 'P1001',
    'age': 34,
    'gender': 'Female',
    'diagnosis': 'Hypertension',
    'medications': ['Lisinopril'],
    'last_visit_id': 'V2301',
}


def test_valid_dataset_returns_true(capsys):
    assert validate([VALID_RECORD]) is True
    assert 'Valid format.' in capsys.readouterr().out


def test_non_list_input_is_rejected():
    assert validate({'not': 'a list'}) is False
    assert validate('a string') is False


def test_record_that_is_not_a_dict_is_rejected():
    assert validate(['not a dict']) is False


def test_missing_keys_are_rejected():
    incomplete = {k: v for k, v in VALID_RECORD.items() if k != 'age'}
    assert validate([incomplete]) is False


def test_extra_keys_are_rejected():
    extra = dict(VALID_RECORD, extra_field='oops')
    assert validate([extra]) is False


def test_underage_patient_is_invalid():
    minor = dict(VALID_RECORD, age=15)
    assert validate([minor]) is False


def test_bad_gender_is_invalid():
    bad_gender = dict(VALID_RECORD, gender='unknown')
    assert validate([bad_gender]) is False


def test_bad_patient_id_format_is_invalid():
    bad_id = dict(VALID_RECORD, patient_id='X1001')
    assert validate([bad_id]) is False


def test_bad_last_visit_id_format_is_invalid():
    bad_visit = dict(VALID_RECORD, last_visit_id='X2301')
    assert validate([bad_visit]) is False


def test_medications_must_be_a_list_of_strings():
    bad_meds = dict(VALID_RECORD, medications='Lisinopril')
    assert validate([bad_meds]) is False


def test_diagnosis_can_be_none():
    no_diagnosis = dict(VALID_RECORD, diagnosis=None)
    assert validate([no_diagnosis]) is True


def test_find_invalid_fields_reports_each_bad_field():
    invalid = find_invalid_fields(
        patient_id='bad',
        age=10,
        gender='x',
        diagnosis=123,
        medications='not a list',
        last_visit_id='bad',
    )
    assert set(invalid) == {
        'patient_id',
        'age',
        'gender',
        'diagnosis',
        'medications',
        'last_visit_id',
    }
