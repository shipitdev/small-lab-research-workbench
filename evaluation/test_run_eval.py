import unittest
import json
from unittest.mock import patch
from email.message import Message

from run_eval import _call, compression_metrics, score_answer


class EvaluationMetricsTest(unittest.TestCase):
    def test_request_provenance_excludes_credentials(self):
        import io
        response = io.BytesIO(json.dumps({"id": "response-1", "model": "fixed-model", "choices": [{"finish_reason": "stop", "message": {"content": "answer"}}], "usage": {"prompt_tokens": 10, "completion_tokens": 2}}).encode())
        response.headers = Message()
        response.headers["x-request-id"] = "request-1"
        with patch("run_eval.request.urlopen", return_value=response):
            result = _call("https://inference.do-ai.run/v1/chat/completions", "secret-test-key", "fixed-model", "instruction", "context", 1024)
        self.assertEqual(result["provider_request_id"], "request-1")
        self.assertEqual(result["request"]["messages"][1]["content"], "context")
        self.assertNotIn("secret-test-key", json.dumps(result))

    def test_compression_metrics_use_model_prompt_tokens(self):
        result = compression_metrics(100, 60)

        self.assertEqual(result["original_prompt_tokens"], 100)
        self.assertEqual(result["compressed_prompt_tokens"], 60)
        self.assertEqual(result["prompt_token_reduction"], 40)
        self.assertEqual(result["prompt_token_reduction_ratio"], 0.4)

    def test_reference_score_keeps_numbers_and_not_found_alignment_visible(self):
        reference = "Not found / cannot be calculated. Sensor B is 45 mA."
        answer = "Not found; cannot be calculated. Sensor B is 45 mA."

        result = score_answer(answer, reference)

        self.assertEqual(result["not_found_alignment"], 1)
        self.assertIn("45", result["reference_markers_present"])
        self.assertEqual(result["reference_marker_recall"], 1.0)


if __name__ == "__main__":
    unittest.main()
