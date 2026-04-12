import threading
import time

class ReusableWorker(threading.Thread):
    # 增加 args, kwargs 接收参数
    def __init__(self, task_func, args=(), kwargs=None, interval=1):
        super().__init__()
        self.daemon = True
        self.running = True
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs or {}
        self.interval = interval
        self.cond = threading.Condition()
        self.paused = False

    def run(self):
        print("✅ 线程已启动")
        while self.running:
            # 暂停逻辑：如果 paused=True，线程会卡住等待
            with self.cond:
                while self.paused:
                    self.cond.wait()  # 线程休眠，不占CPU

            # 执行任务
            self.task_func(*self.args, **self.kwargs)
            time.sleep(self.interval)

        print("🛑 线程已彻底停止")

    # 暂停
    def pause(self):
        with self.cond:
            self.paused = True
        time.sleep(0.5)
        print("⏸️  线程已暂停")

    # 继续
    def resume(self):
        with self.cond:
            self.paused = False
            self.cond.notify()  # 唤醒线程
        print("▶️  线程已继续运行")

    # 彻底停止
    def stop(self):
        with self.cond:
            self.running = False
            self.paused = False
            self.cond.notify()  # 唤醒后退出
