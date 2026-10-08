#!/usr/bin/env python3
"""Summarize labeled noul judgments. Never enable an automatic decision policy."""
import argparse,json,math
from pathlib import Path
from judge import number,Invalid

def evaluate(rows,false_max=.1,true_min=.9):
 number(false_max);number(true_min)
 if false_max>=true_min or not isinstance(rows,list) or not rows:raise Invalid('records and separated thresholds required')
 ids=set();known=[];unknown=0
 for row in rows:
  if not isinstance(row,dict) or not isinstance(row.get('id'),str) or not row['id'] or row['id'] in ids:raise Invalid('unique record IDs required')
  ids.add(row['id']);p=number(row.get('p_true'));y=row.get('label')
  if y is None:unknown+=1;continue
  if type(y) is not bool:raise Invalid('label must be true, false or null')
  known.append((p,y))
 if not known:raise Invalid('at least one labeled record required')
 tp=fp=tn=fn=review=0
 for p,y in known:
  if p>=true_min:
   if y:tp+=1
   else:fp+=1
  elif p<=false_max:
   if y:fn+=1
   else:tn+=1
  else:review+=1
 n=len(known);auto=tp+fp+tn+fn
 bins=[];ece=0
 for i in range(10):
  bucket=[(p,y) for p,y in known if i/10<=p<(i+1)/10 or (i==9 and p==1)]
  if not bucket:continue
  mean=sum(p for p,y in bucket)/len(bucket);rate=sum(y for p,y in bucket)/len(bucket);ece+=len(bucket)/n*abs(mean-rate)
  bins.append({'lower':i/10,'upper':(i+1)/10,'n':len(bucket),'mean_p':mean,'positive_rate':rate})
 return {'labeled_count':n,'unknown_label_count':unknown,'automatic_count':auto,'review_count':review,'review_rate':review/n,'confusion_resolved_only':{'tp':tp,'fp':fp,'tn':tn,'fn':fn},'precision_resolved_only':tp/(tp+fp) if tp+fp else None,'recall_resolved_only':tp/(tp+fn) if tp+fn else None,'positive_capture_all_labeled':tp/sum(y for p,y in known) if any(y for p,y in known) else None,'automatic_error_rate':(fp+fn)/auto if auto else None,'brier_score':sum((p-int(y))**2 for p,y in known)/n,'ece_10_bins':ece,'bins':bins,'thresholds':{'false_max':false_max,'true_min':true_min},'calibrated':False,'notes':['Descriptive sample metrics only; no proof of domain accuracy or statistical certification.','Unknown labels are excluded, not converted to false. Separate development and holdout data; report population and selection bias.','This script never enables a policy. Require domain review and a bound, expiring calibration record.']}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);ap.add_argument('--output');ap.add_argument('--false-max',type=float,default=.1);ap.add_argument('--true-min',type=float,default=.9);a=ap.parse_args()
 try:r=evaluate(json.loads(Path(a.input).read_text()),a.false_max,a.true_min)
 except (OSError,ValueError,TypeError):r={'status':'review','reason':'invalid_evaluation_data'}
 s=json.dumps(r,ensure_ascii=False,indent=2)
 if a.output:Path(a.output).write_text(s)
 else:print(s)
if __name__=='__main__':main()
