#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""記録の自動push: office-status.json / office-history.jsonl が変わるたびに
git commit & push して、iPhone側のアプリに反映させる。
使い方: リポジトリ内で  python sync.py   (止めるまで動き続けます)"""
import os, time, subprocess

BASE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(BASE, ".."))
FILES = ["office/office-status.json", "office/office-history.jsonl"]

def mtimes():
    return tuple(os.path.getmtime(os.path.join(REPO, f)) if os.path.exists(os.path.join(REPO, f)) else 0
                 for f in FILES)

def push():
    try:
        subprocess.run(["git", "add"] + FILES, cwd=REPO, capture_output=True)
        r = subprocess.run(["git", "commit", "-m", "office: 勤務記録更新"], cwd=REPO, capture_output=True, text=True)
        if "nothing to commit" in (r.stdout + r.stderr):
            return
        subprocess.run(["git", "push"], cwd=REPO, capture_output=True)
        print(time.strftime("%H:%M:%S"), "pushed")
    except Exception as e:
        print("push error:", e)

print("勤務記録の自動同期を開始しました(Ctrl+Cで終了)")
last = mtimes()
while True:
    time.sleep(15)
    cur = mtimes()
    if cur != last:
        last = cur
        push()
