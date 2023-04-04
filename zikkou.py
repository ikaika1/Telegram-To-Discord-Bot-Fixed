import time
import subprocess

def task():
    # 実行したいpyファイルを指定
    subprocess.run(["python", "forwardgram.py"])

def main():
    while True:
        task()
        time.sleep(60)

if __name__ == '__main__':
    main()