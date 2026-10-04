import datetime
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from codex_scan import select_pending
from fetch_jobtech import normalize_hit
class DatesTest(unittest.TestCase):
 def test_window_and_priority(self):
  jobs={str(i):dict(link=str(i),publication_date=date,status='new') for i,date in enumerate(['2026-10-04T10:00:00','2026-10-01','2026-09-20','2026-08-01',''])}
  jobs['5']=dict(link='5',publication_date='2026-10-03',status='applied')
  jobs['6']=dict(link='6',publication_date='2026-10-03',status='new',application_deadline='2026-10-02')
  jobs['7']=dict(link='7',publication_date='2026-10-03',status='new',score=80)
  today=datetime.date(2026,10,4)
  self.assertEqual([j['link'] for j in select_pending(jobs,7,20,today)],['0','1'])
  self.assertEqual([j['link'] for j in select_pending(jobs,30,20,today)],['0','1','2'])
  self.assertEqual(len(select_pending(jobs,30,1,today)),1)
 def test_normalized_dates(self):
  j=normalize_hit({'id':'1','publication_date':'2026-10-04','application_deadline':'2026-10-20'})
  self.assertEqual(j['publication_date'],'2026-10-04')
  self.assertEqual(j['application_deadline'],'2026-10-20')
