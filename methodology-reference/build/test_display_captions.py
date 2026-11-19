import unittest
from display_captions import audit, number_displays


class CaptionTests(unittest.TestCase):
    def test_authored_and_generated_tables_and_figures(self):
        source = '<h2>Candidate evidence</h2><table><tr><th>Situation</th><th>Action</th></tr></table><table><caption>Reported costs <a href="source">and source</a></caption></table><figure><svg></svg><figcaption>Evidence to accepted mapping.</figcaption></figure>'
        rendered = number_displays(source, 'Synthesis')
        self.assertIn('<caption>Table 1. Candidate evidence: Situation, Action</caption>', rendered)
        self.assertIn('<caption>Table 2. Reported costs <a href="source">and source</a></caption>', rendered)
        self.assertIn('<figcaption>Figure 1. Evidence to accepted mapping.</figcaption>', rendered)
        self.assertEqual(audit(rendered), [])
        self.assertEqual(number_displays(rendered, 'Synthesis'), rendered)

    def test_missing_or_duplicate_captions_fail_audit(self):
        for html in ['<table></table>', '<table><caption>Table 1.</caption></table>', '<figure><figcaption>Caption without number</figcaption></figure>', '<table><caption>Table 1. First</caption><caption>Table 1. Second</caption></table>']:
            self.assertTrue(audit(html))
        with self.assertRaisesRegex(ValueError, 'Figure without'):
            number_displays('<figure><svg></svg></figure>', 'Method')

    def test_sequences_restart_per_page_and_preserve_source_numbers(self):
        self.assertIn('Table 1. Source Table 4', number_displays('<table><caption>Source Table 4</caption></table>', 'Sources'))
        self.assertIn('Table 1.', number_displays('<table><tr><th>Unit</th></tr></table>', 'Costs'))
