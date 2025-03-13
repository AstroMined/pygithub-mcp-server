# Unit Test Deprecation Plan

## These unit tests should be replaced with integration tests

These tests use mocking, which has proven to be brittle and unreliable in this environment.
See ADR-002 for more details.

- tests/unit/converters/common/test_pagination_unit.py
- tests/unit/operations/*
- tests/unit/tools

## These unit tests should be considered for deprecation

These tests use mocking in a cleaner way, but integration tests would likely be more effective by testing the real objects.
Replace with intergration tests where possible.

- tests/unit/converters/issues/*
- tests/unit/converters/repositories/*
- tests/unit/converters/users/*
- tests/unit/utils/test_environment.py
