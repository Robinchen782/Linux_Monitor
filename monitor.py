import pickle
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import psutil
import tkinter as tk
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from tkinter import filedialog


# 获取当前CPU使用率
def get_cpu():
    return psutil.cpu_percent()

# 获取当前内存使用率
def get_mem():
    return psutil.virtual_memory().percent

class Monitor:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        
        # 设置横坐标时间戳格式
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        self.var = tk.IntVar()
        self.stop = False
        self.now = 0

        self.data_load = None
        self.print_load = False

        # 获取程序开始时间
        self.start_time = datetime.now()

        # 设置曲线横坐标
        plt.xlim([self.start_time, self.start_time + timedelta(seconds=60)])

        # 创建性能参数按钮
        self.cpu_button = tk.Radiobutton(text="CPU", variable=self.var, value=1, width=10, indicatoron=False)
        self.mem_button = tk.Radiobutton(text="Memory", variable=self.var, value=2, width=10, indicatoron=False)
        self.disk_button = tk.Radiobutton(text="Disk", variable=self.var, value=3, width=10, indicatoron=False)
        self.net_button = tk.Radiobutton(text="Net", variable=self.var, value=4, width=10, indicatoron=False)
        
        # 创建控制按钮
        self.clear_button = tk.Button(text='Clear', command=self.on_click_clear, width=6)
        self.stop_button = tk.Button(text='Stop', command=self.on_click_stop, width=6)
        self.save_button = tk.Button(text='Save', command=self.save_data, width=6)
        self.load_button = tk.Button(text='Load', command=self.load_data, width=6)
        self.real_time_button = tk.Button(text='Monitor', command=self.real_time, width=6)

        # 放置按钮
        self.cpu_button.place(x=0, y=0)
        self.mem_button.place(x=85, y=0)
        self.disk_button.place(x=2 * 85, y=0)
        self.net_button.place(x=3 * 85, y=0)
        
        self.clear_button.place(x=0, y=300)
        self.stop_button.place(x=0, y=325)
        self.save_button.place(x=0, y=350)
        self.load_button.place(x=0, y=375)
        self.real_time_button.place(x=0, y=400)

        # 获取初始的网络 IO 统计信息
        self.prev_net_io_counters = psutil.net_io_counters()

        # 获取初始的磁盘 IO 统计信息
        self.prev_disk_io_counters = psutil.disk_io_counters()

        # 定义存储性能参数数据的字典
        self.data = {"cpu": [], "mem": [], "disk": [], "net": [], "time": []}

    
    def get_disk(self):
        # 获取当前磁盘I/O计数
        new_counters = psutil.disk_io_counters()

        # 计算先前值和当前值之间的差值
        diff = new_counters.write_bytes - self.prev_disk_io_counters.write_bytes

        # 更新磁盘I/O计数
        self.prev_disk_io_counters = new_counters

        # 转换为 MB/s
        return diff / (1024 * 1024)

    def get_net(self):
        # 获取当前网络I/O计数
        new_counters = psutil.net_io_counters()

        # 计算先前值和当前值之间的差值
        diff = new_counters.bytes_sent - self.prev_net_io_counters.bytes_sent

        # 更新网络I/O计数
        self.prev_net_io_counters = new_counters

        # 转换为 KB/s
        return diff / 1024

    # 实时更新函数
    def update(self, frame):
        # 获取当前时间
        self.now = datetime.now()

        # 更新缓存
        if not self.stop:
            self.data["time"].append(self.now)
            self.data["cpu"].append(get_cpu())
            self.data["mem"].append(get_mem())
            self.data["disk"].append(self.get_disk())
            self.data["net"].append(self.get_net())
        else:
            self.data["time"].append(self.now)
            self.data["cpu"].append(self.data["cpu"][-1])
            self.data["mem"].append(self.data["mem"][-1])
            self.data["disk"].append(self.data["disk"][-1])
            self.data["net"].append(self.data["net"][-1])

        # 清除先前图像
        plt.clf()

        # 获取当前性能参数类型（单选按钮值）
        selected = self.var.get()

        # 加载数据模式
        if self.print_load:
            plt.xlim([self.data_load["time"][0], self.data_load["time"][-1]])

            # 绘制对应性能参数曲线
            if selected == 1:
                plt.plot(self.data_load["time"], self.data_load["cpu"], color='red')
                plt.title("CPU Usage(%)")
                plt.ylim([0, 100])
            elif selected == 2:
                plt.plot(self.data_load["time"], self.data_load["mem"], color='green')
                plt.title("Memory Usage(%)")
                plt.ylim([0, 100])
            elif selected == 3:
                plt.plot(self.data_load["time"], self.data_load["disk"], color='blue')
                plt.title("Disk Usage(MB/s)")
            elif selected == 4:
                plt.plot(self.data_load["time"], self.data_load["net"], color='yellow')
                plt.title("Network Usage(KB/s)")
            else:
                plt.plot(self.data_load["time"], self.data_load["cpu"], color='red')
                plt.title("CPU Usage(%)")
                plt.ylim([0, 100])

        # 实时监测模式
        else:
            # 设置曲线横坐标
            if (self.now - self.start_time) < timedelta(seconds=60):
                plt.xlim([self.start_time, self.start_time + timedelta(seconds=60)])
            else:
                plt.xlim([self.now - timedelta(seconds=60), self.now])

            # 绘制对应性能参数曲线
            if selected == 1:
                plt.plot(self.data["time"], self.data["cpu"], color='red')
                plt.title("CPU Usage(%)")
                plt.ylim([0, 100])
            elif selected == 2:
                plt.plot(self.data["time"], self.data["mem"], color='green')
                plt.title("Memory Usage(%)")
                plt.ylim([0, 100])
            elif selected == 3:
                plt.plot(self.data["time"], self.data["disk"], color='blue')
                plt.title("Disk Usage(MB/s)")
            elif selected == 4:
                plt.plot(self.data["time"], self.data["net"], color='yellow')
                plt.title("Network Usage(KB/s)")
            else:
                plt.plot(self.data["time"], self.data["cpu"], color='red')
                plt.title("CPU Usage(%)")
                plt.ylim([0, 100])

    # Clear按钮回调函数
    def on_click_clear(self):
        # 清除缓存数据
        self.data["time"] = []
        self.data["cpu"] = []
        self.data["mem"] = []
        self.data["disk"] = []
        self.data["net"] = []

    # Stop按钮回调函数
    def on_click_stop(self):
        if self.stop:
            self.stop = False
        else:
            self.stop = True

    # Save按钮回调函数
    def save_data(self):
        # 保存数据到文件
        # with open('data.pkl', 'wb') as f:
        #     pickle.dump(self.data, f)

        # 弹出文件保存对话框，选择保存路径和文件名称
        file_path = filedialog.asksaveasfilename(defaultextension=".pkl")

        # 如果用户选择了文件，则保存数据到文件中
        if file_path:
            with open(file_path, 'wb') as f:
                pickle.dump(self.data, f)

    # Load按钮回调函数
    def load_data(self):
        # self.print_load = True
        # # 从文件中读取数据
        # with open('data.pkl', 'rb') as f:
        #     self.data_load = pickle.load(f)

        # 弹出文件打开对话框，选择要读取的文件
        file_path = filedialog.askopenfilename()

        # 如果用户选择了文件，则从文件中读取数据
        if file_path:
            with open(file_path, 'rb') as f:
                self.data_load = pickle.load(f)
                self.print_load = True

    # Monitor按钮回调函数
    def real_time(self):
        self.print_load = False


# 定义Monitor对象
monitor = Monitor()

# 实现动态更新曲线图
ani = FuncAnimation(monitor.fig, monitor.update, interval=1000, save_count=1000)

# 定义图像窗口标题
manager = plt.get_current_fig_manager()
manager.set_window_title('Linux Monitor')

# 绘制曲线
plt.show()
