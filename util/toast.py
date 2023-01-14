from win10toast import ToastNotifier
import time

def pc_toast(title, text, icon_path):
    toaster = ToastNotifier()
    time.sleep(1)  # 适当休息一下，避免出现提示秒弹的情况
    toaster.show_toast(title=f"{title}", msg=f"{text}", duration=10, threaded=True, icon_path=f"{icon_path}")
    while toaster.notification_active():  # toaster.notification_active()判断是否有活动通知显示
        time.sleep(0.005)

if __name__ == '__main__':
    pc_toast('eee')