# LLM-as-a-Judge Learning Project

This project builds a production-oriented LLM judge one small step at a time.

## Step 1: evaluation contract

The initial judge evaluates an AI answer against a question and supplied reference
information. It scores correctness, relevance, completeness, and clarity from 1 to
5. The application calculates the final `PASS` or `FAIL` decision.

An answer passes when:

- its weighted score is at least `3.5`;
- correctness is at least `3`; and
- relevance is at least `3`.

The judge must not use model identity, response length alone, personal style
preferences, cost, or latency in its decision.

Run the Step 1 tests:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

Azure integration and the judge prompt intentionally belong to later steps.
