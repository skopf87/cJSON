#!/usr/bin/env python3
"""Reproduce the frozen cJSON develop-base PR validation."""
from pathlib import Path
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,datetime
HERE=Path(__file__).resolve().parent

def run(args):subprocess.run(list(map(str,args)),check=True,timeout=240)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--stage',choices=['screen','validate'],default='validate');p.add_argument('--prepare-only',action='store_true');a=p.parse_args()
 if hasattr(os,'sched_getaffinity') and 0 not in os.sched_getaffinity(0):raise SystemExit('Frozen protocol requires CPU 0; record a new protocol to change affinity.')
 work=Path(tempfile.mkdtemp(prefix='cjson-develop-pr-'))
 for name in ['configs','framework','benchmarks','fixtures','patches']:shutil.copytree(HERE/name,work/name)
 cfg=json.loads((work/'configs/C03PR.json').read_text());manifest=json.loads((work/'configs/C03PR.v1.frozen.json').read_text())
 for name,sha in manifest.items():
  if hashlib.sha256((work/name).read_bytes()).hexdigest()!=sha:raise SystemExit('Frozen evaluator mismatch: '+name)
 src=work/'repos/cJSON';src.parent.mkdir()
 run(['git','clone','--depth','1',cfg['repository'],src])
 run(['git','-C',src,'fetch','--depth','1','origin',cfg['upstream_commit']]);run(['git','-C',src,'checkout','--detach',cfg['upstream_commit']])
 run(['git','-C',src,'apply','--check',work/'patches/pr.patch'])
 print('Verified evaluator and pinned upstream:',work,flush=True)
 if a.prepare_only:return
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 run([sys.executable,work/'framework/lab.py','baseline','C03PR','--id','baseline-'+stamp])
 run([sys.executable,work/'framework/lab.py','trial','C03PR','--id','trial-'+stamp,'--patch',work/'patches/pr.patch','--hypothesis','Reproduce cJSON develop-base PR validation','--stage',a.stage,'--upstream','--no-promote'])
 print('New raw measurements:',work/'results',flush=True)
if __name__=='__main__':main()
