#!/usr/bin/env python3
"""Deterministic scenario arithmetic; does not certify evidence or execute payments."""
import argparse,json
from pathlib import Path
def integer(value,nonnegative=False):
 if type(value) is not int or (nonnegative and value<0):raise ValueError('integer amounts and days required')
 return value
def calculate(job):
 if not isinstance(job,dict) or not isinstance(job.get('currency'),str) or not job['currency']:raise ValueError('currency required')
 if job.get('basis') not in ('actual','scenario'):raise ValueError('actual or scenario basis required')
 opening=integer(job['opening_cash'],True);reserve=integer(job['reserved_cash'],True);deadline=integer(job['deadline_day'],True)
 rows=job['events']
 if not isinstance(rows,list):raise ValueError('events list required')
 seen=set();events=[]
 for e in rows:
  if not isinstance(e,dict) or not isinstance(e.get('id'),str) or not e['id'] or e['id'] in seen:raise ValueError('unique event IDs required')
  seen.add(e['id']);day=integer(e['day'],True);seq=integer(e['sequence'],True);amount=integer(e['amount'])
  if (day,seq) in [(x['day'],x['sequence']) for x in events]:raise ValueError('event order must be unique')
  events.append(dict(e,day=day,sequence=seq,amount=amount))
 cash=opening;minimum=cash-reserve;cash_at_deadline=opening;receipts=0;trace=[]
 for e in sorted(events,key=lambda x:(x['day'],x['sequence'])):
  cash+=e['amount'];available=cash-reserve;minimum=min(minimum,available)
  if e['day']<=deadline:
   cash_at_deadline=cash
   if e['amount']>0:receipts+=e['amount']
  trace.append(dict(e,cash=cash,available_cash=available))
 return {'status':'calculated','currency':job['currency'],'basis':job['basis'],'opening_cash':opening,'reserved_cash':reserve,'deadline_day':deadline,'positive_receipts_by_deadline':receipts,'cash_at_deadline':cash_at_deadline,'available_cash_at_deadline':cash_at_deadline-reserve,'closing_cash':cash,'minimum_available_cash':minimum,'additional_cash_required':max(0,-minimum),'schedule_fundable_from_opening_cash':minimum>=0,'trace':trace,'note':'Arithmetic of supplied ledger only. Positive receipts are not necessarily sales. Scenario output is not realized cash or an authorized spending limit.'}
def main():
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);a=p.parse_args()
 try:r=calculate(json.loads(Path(a.input).read_text()))
 except (ValueError,TypeError,KeyError,OSError):r={'status':'review','reason':'invalid_or_missing_ledger_input'}
 print(json.dumps(r,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
