import unittest
from evaluate import evaluate
from judge import Invalid
class EvaluationTests(unittest.TestCase):
 def test_perfect(self):
  r=evaluate([{'id':'a','p_true':1,'label':True},{'id':'b','p_true':0,'label':False}]);self.assertEqual(r['brier_score'],0);self.assertEqual(r['automatic_error_rate'],0);self.assertFalse(r['calibrated'])
 def test_review_and_unknown(self):
  r=evaluate([{'id':'a','p_true':.5,'label':True},{'id':'b','p_true':.9,'label':None}]);self.assertEqual(r['review_rate'],1);self.assertEqual(r['unknown_label_count'],1);self.assertEqual(r['positive_capture_all_labeled'],0);self.assertIsNone(r['automatic_error_rate'])
 def test_confusion(self):
  r=evaluate([{'id':'a','p_true':.95,'label':False},{'id':'b','p_true':.05,'label':True}]);self.assertEqual(r['confusion_resolved_only'],{'tp':0,'fp':1,'tn':0,'fn':1});self.assertEqual(r['automatic_error_rate'],1)
 def test_duplicate(self):
  with self.assertRaises(Invalid):evaluate([{'id':'a','p_true':.2,'label':True}]*2)
 def test_non_boolean(self):
  with self.assertRaises(Invalid):evaluate([{'id':'a','p_true':.2,'label':1}])
 def test_nan(self):
  with self.assertRaises(Invalid):evaluate([{'id':'a','p_true':float('nan'),'label':True}])
if __name__=='__main__':unittest.main()
