import time
import subprocess as sp

def run_subprocess(e):
    proc = sp.Popen(["python", "forwardgram.py", e], stdout = sp.PIPE, stderr = sp.PIPE)
    return proc

proc = run_subprocess("")
while True:
    ecode = proc.poll()
    if ecode is None:  # サブプロセスが実行中
        time.sleep(2)
    else:              # サブプロセス終了
        for line in proc.stdout.readlines():
            print (line.decode(encoding="cp932"), end="")  # utf-8だと全角文字でエラーになる（Windows）

        if ecode == 0: # 正常終了
            e = ""
        else:          # 異常終了
            e = proc.stderr.readlines()[-1].decode()
        proc = run_subprocess(e)
