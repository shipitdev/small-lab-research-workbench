import unittest
from experiment import run_experiment


class ExperimentTest(unittest.TestCase):
    def test_counts_compression_overhead_and_keeps_raw_answers(self):
        calls = []
        def fake_call(system, prompt, limit):
            calls.append(prompt)
            return {"text": "short" if len(calls) == 1 else "Friday", "usage": {"prompt_tokens": 10, "completion_tokens": 2}, "seconds": 0.5}
        result = run_experiment("A long source", [{"question": "When?", "reference": "Friday"}], "test-model", fake_call)
        self.assertEqual(len(calls), 3)
        self.assertEqual(result["total_tokens_including_compression"], 36)
        self.assertEqual(result["runs"][0]["original"]["text"], "Friday")
        self.assertIn("Friday", result["runs"][0]["reference"])

    def test_invalid_dataset_fails_before_any_model_call(self):
        def forbidden(*args):
            self.fail("Must validate before spending credits")
        with self.assertRaises(ValueError):
            run_experiment("source", [{"question": ""}], "model", forbidden)


if __name__ == "__main__":
    unittest.main()
