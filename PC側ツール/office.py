#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""キノコ商事 勤務記録ヘルパー
Claude Code / Codex が作業状況を書き込むためのコマンド。
office-status.json(現在の状態)と office-history.jsonl(全履歴)を更新する。

使い方:
  python office.py mission "LPの改修"
  python office.py set dig working "競合LPを調査"
  python office.py set dig done "調査完了"
  python office.py set kuro error "承認待ち: デプロイ"
  python office.py log dig "掘ってくる"
  python office.py reset

担当ID: judge=統括・裁定 / han=タスク分解・進行 / owl=設計・仕様 /
        zeni=コスト・モデル選択 / dig=調査・検索 / kuro=点検・原因調査 /
        niko=報告・要約 / new=実装
status: idle / working / done / error
"""
import json, sys, os, datetime

BASE = os.path.dirname(os.path.abspath(__file__))
STATUS = os.path.join(BASE, "..", "office", "office-status.json")
HISTORY = os.path.join(BASE, "..", "office", "office-history.jsonl")
IDS = ["judge","han","owl","zeni","dig","kuro","niko","new"]

def now(): return datetime.datetime.now()

def load():
    if os.path.exists(STATUS):
        try:
            with open(STATUS, encoding="utf-8") as f: return json.load(f)
        except Exception: pass
    return {"mission":"", "employees":{i:{"status":"idle","task":""} for i in IDS}, "log":[]}

def save(d):
    d.setdefault("employees", {})
    for i in IDS: d["employees"].setdefault(i, {"status":"idle","task":""})
    d["log"] = d.get("log", [])[-30:]
    tmp = STATUS + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    os.replace(tmp, STATUS)
    with open(HISTORY, "a", encoding="utf-8") as f:
        f.write(json.dumps({"t": now().isoformat(timespec="seconds"), "data": d},
                           ensure_ascii=False) + "\n")

def main():
    a = sys.argv[1:]
    if not a:
        print(__doc__); return
    d = load()
    cmd = a[0]
    if cmd == "mission" and len(a) >= 2:
        d["mission"] = a[1]
        d["log"].append({"time": now().strftime("%H:%M"), "who":"judge",
                         "msg": f"ミッション受理: {a[1]}"})
    elif cmd == "set" and len(a) >= 3:
        who, st = a[1], a[2]
        task = a[3] if len(a) > 3 else ""
        if who not in IDS: sys.exit(f"unknown id: {who} (use: {','.join(IDS)})")
        if st not in ("idle","working","done","error"): sys.exit("status must be idle/working/done/error")
        d["employees"][who] = {"status": st, "task": task}
        label = {"working":"開始","done":"完了","error":"承認待ち","idle":"待機"}[st]
        d["log"].append({"time": now().strftime("%H:%M"), "who": who,
                         "msg": f"[{label}] {task}" if task else f"[{label}]",
                         **({"err": True} if st=="error" else {})})
    elif cmd == "log" and len(a) >= 3:
        d["log"].append({"time": now().strftime("%H:%M"), "who": a[1], "msg": a[2]})
    elif cmd == "reset":
        d = {"mission":"", "employees":{i:{"status":"idle","task":""} for i in IDS}, "log":[]}
    else:
        print(__doc__); sys.exit(1)
    save(d)
    print("ok")

if __name__ == "__main__":
    main()
