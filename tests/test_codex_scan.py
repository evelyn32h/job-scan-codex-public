import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from codex_scan import eligibility, validate
from results_io import merge,filter_pending
class PipelineTest(unittest.TestCase):
    def test_visa_and_clearance_kept(self):
        for text in ['We do not offer visa sponsorship.', 'Security clearance required.', 'Must have unrestricted right to work in Sweden.', 'Swedish citizenship is preferred.', 'Swedish citizenship is not required.']:
            self.assertFalse(eligibility(text)[0],text)
    def test_citizenship_required(self):
        for text in ['You must be a Swedish citizen.', 'EU/EEA citizenship is required.', 'Krav på svenskt medborgarskap.']:
            self.assertTrue(eligibility(text)[0],text)
    def test_schema_unknown_duplicate(self):
        batch=[{'link':'a'},{'link':'b'}]
        rows=[dict(link='a',score=80,lane='AI',reason='matches/gaps')]*2
        with self.assertRaises(ValueError): validate({'jobs':rows},batch,['AI'])
        rows=[dict(link='x',score=80,lane='AI',reason='x')]
        with self.assertRaises(ValueError): validate({'jobs':rows},[{'link':'a'}],['AI'])
    def test_status_and_pending(self):
        existing={'a':dict(link='a',status='applied',first_seen='old',score=75),'b':dict(link='b',status='new')}
        out=merge(existing,[dict(link='a',score=80)],set(),'today')
        self.assertEqual(out['a']['status'],'applied')
        self.assertEqual(out['a']['first_seen'],'old')
        self.assertEqual([j['link'] for j in filter_pending(out)],['b'])
if __name__=='__main__': unittest.main()
