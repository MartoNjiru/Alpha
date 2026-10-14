import unittest
from mteval import sentence_bleu, corpus_bleu, chrf, ter


class TestMetrics(unittest.TestCase):
    def test_identical_scores_perfect(self):
        s = "Lake Nakuru has many flamingos."
        self.assertAlmostEqual(corpus_bleu([s], [[s]]), 100.0)
        self.assertAlmostEqual(chrf(s, s), 100.0)
        self.assertEqual(ter(s, s), 0.0)

    def test_unrelated_scores_low(self):
        self.assertEqual(corpus_bleu(["apples oranges bananas pears"], [["the cat sat down"]]), 0.0)
        self.assertLess(chrf("xyz", "the cat"), 10)

    def test_ordering(self):
        ref = "It rained heavily last night."
        good, bad = "It rained heavily last night", "Rain fell a lot yesterday."
        self.assertGreater(sentence_bleu(good, ref), sentence_bleu(bad, ref))
        self.assertGreater(chrf(good, ref), chrf(bad, ref))
        self.assertLess(ter(good, ref), ter(bad, ref))

    def test_brevity_penalty(self):
        ref = "please help me carry this heavy load today"
        self.assertLess(sentence_bleu("please help me", ref), sentence_bleu("please help me carry this heavy load", ref))

    def test_multiple_references(self):
        self.assertGreater(sentence_bleu("the kids are playing", ["the children are playing", "the kids are playing"]), 99)


if __name__ == "__main__":
    unittest.main()
