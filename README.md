# tap-tester
Integration testing framework for Singer taps.

[NOTE: This is a big work in progress, but all are encouraged to give it a try, dig in and leave feedback as it is in development. Good luck! Hope you like it!]

**See `tests/test_standard_tests.py` for a usage example of the standard canary test.**

## To Document:

1. StandardTests usage example
2. BaseTest subclassing requirements and example
  - E.g., "You must implement these things because..." for things like `config_environment`
3. Purpose for the library
4. Contribution and Vision
  - Should be clean interface
  - Should use standards for cross-platform Python (e.g., use os.linesep instead of `\n`, and so on.
5. Testing advice (what makes a good tap-tester test?)

## Basic Test Writing Standards (Don'ts)

1. Don't import the tap code directly. This is meant to be true black-box integration testing, and importing a client library muddies that up, and may actually make a test ineffective.
2. Don't create or delete data, these should be generic, and should rely on data that already exists to test the tap's features. This is not always possible, but should be for those who are interested in the tap.
