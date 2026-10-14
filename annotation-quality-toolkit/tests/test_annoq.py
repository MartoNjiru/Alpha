import unittest
from annoq import fleiss_kappa, krippendorff_alpha_nominal, pairwise_agreement, majority_vote, gold_accuracy, flag_annotators


class TestAgreement(unittest.TestCase):
    def test_perfect_agreement(self):
        items = [{"a": "x", "b": "x"}, {"a": "y", "b": "y"}]
        self.assertAlmostEqual(fleiss_kappa(items), 1.0)
        self.assertAlmostEqual(krippendorff_alpha_nominal(items), 1.0)
        self.assertEqual(pairwise_agreement(items), 1.0)

    def test_fleiss_wikipedia_example(self):
        # Classic Fleiss (1971) style table: 10 items, 14 raters, 5 categories -> kappa 0.210
        table = [[0,0,0,0,14],[0,2,6,4,2],[0,0,3,5,6],[0,3,9,2,0],[2,2,8,1,1],
                 [7,7,0,0,0],[3,2,6,3,0],[2,5,3,2,2],[6,5,2,1,0],[0,2,2,3,7]]
        items = []
        for row in table:
            labels = [c for c, n in enumerate(row) for _ in range(n)]
            items.append({f"r{i}": l for i, l in enumerate(labels)})
        self.assertAlmostEqual(fleiss_kappa(items), 0.210, places=3)

    def test_alpha_handles_missing(self):
        items = [{"a": 1, "b": 1}, {"a": 2, "b": 2, "c": 2}, {"b": 3}]
        self.assertAlmostEqual(krippendorff_alpha_nominal(items), 1.0)

    def test_disagreement_is_low(self):
        items = [{"a": "x", "b": "y"}, {"a": "y", "b": "x"}]
        self.assertLess(krippendorff_alpha_nominal(items), 0)


class TestAggregate(unittest.TestCase):
    def test_majority_and_weights(self):
        self.assertEqual(majority_vote({"a": "x", "b": "x", "c": "y"}), ("x", 2 / 3))
        self.assertEqual(majority_vote({"a": "x", "b": "y"}, {"b": 3})[0], "y")

    def test_gold_and_flags(self):
        items = [{"a": "x", "b": "y"}, {"a": "z", "b": "z"}]
        acc = gold_accuracy(items, {0: "x", 1: "z"})
        self.assertEqual(acc, {"a": 1.0, "b": 0.5})
        self.assertEqual(flag_annotators(acc, 0.8), ["b"])


if __name__ == "__main__":
    unittest.main()
