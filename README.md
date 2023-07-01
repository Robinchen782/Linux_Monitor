# Linux_Monitor
使用Python简单实现Linux性能监视器

## **1.使用文档**

### **概述**

Linux Monitor是一个基于psutil库和matplotlib库的Linux系统性能监测程序，可以实时显示Linux系统的CPU、内存、磁盘和网络的使用情况，并提供保存和加载监测数据的功能。使用GUI界面和曲线图的形式直观地展示系统监测信息，帮助用户了解系统的性能和资源利用情况。

### **环境要求**

在使用 Linux Monitor 之前，需确保满足以下环境要求：

1. 安装 Python 3.x。

2. 安装以下 Python 库：pickle、matplotlib、psutil 和 tkinter。

### **功能说明**

1. 实时监测：实时显示 CPU 使用率、内存使用率、磁盘传输速度和网络传输速度等性能参数曲线图。支持通过标签选择显示的性能参数。

2. 数据保存和加载：可以将一段时间内的监测数据保存到文件，并在需要时加载已保存的数据进行回顾和分析。

3. 提供清除数据和暂停记录的功能。

### **程序实现**

1. 定义Monitor类。
   - 构造函数：创建一个图形窗口和一个坐标轴对象，用于显示性能参数曲线图。通过 tkinter库创建一组性能参数单选按钮和控制按钮，并设置它们的位置和相关的事件处理函数。定义并初始化相关参数和标志位。最后定义存储性能参数数据的字典。
   - 实现性能参数监测函数get_cpu()、get_mem()、get_disk()和get_net()，其中使用psutil库获取系统的监测数据，包括CPU利用率、内存利用率、磁盘IO和网络IO等。
   - 实现各个控制按钮Clear、Stop、Save、Load和Monitor按钮的回调函数。
   - 实现更新函数update()，其中通过性能参数监测函数更新缓存，再通过性能参数单选按钮获取当前参数类型，最后根据当前模式（加载数据模式或实时监测模式）绘制对应曲线。

2. 程序主体
   - 首先创建Monitor对象monitor，再通过FuncAnimation实现动态更新曲线图。关于FuncAnimation函数，其以图像对象monitor.fig、实时更新函数monitor.update为参数，并以interval=1000将monitor设置为每秒监测并记录性能参数一次。

### **使用方法**

1. 运行程序：
   - 打开终端或命令行，并进入包含程序文件的目录。
   - 执行以下命令来运行程序：

```
python monitor.py
```

2. 界面介绍：

   - 左上方的单选按钮用于选择要显示的性能参数曲线，包括
     - CPU 按钮：显示 CPU 使用率曲线。
     - Memory 按钮：显示内存使用率曲线。
     - Disk 按钮：显示磁盘传输速度曲线。
     - Net 按钮：显示网络传输速度曲线。

   - 左下角的按钮为功能按钮，包括
     - Clear 按钮：清除存储缓存中的所有数据，同时清除已绘制曲线。
     - Stop 按钮：暂停或继续实时数据更新。
     - Save 按钮：将存储缓存中的监测数据保存到文件，由用户确定保存路径及文件名称。
     - Load 按钮：由用户选择文件，并从文件中加载已保存的监测数据，显示在曲线绘制界面上。
     - Monitor按钮：显示实时性能参数曲线。

   - 绘图区域将显示所选性能参数的曲线（实时或加载）。

3. 数据保存和加载：

   - 保存数据：

     单击 Save 按钮，选择保存路径，对文件进行命名如”data.pkl”，以将当前存储缓存中的数据保存到文件中。

   - 加载数据：

     单击 Load 按钮，选择之前已保存的文件以加载监控数据。

     加载数据后，将在曲线绘制界面中进行显示，以便进行回顾和比较分析。

4. 实时监控：
   - 默认情况下，程序以实时监控模式启动，显示CPU使用情况的曲线。
   - 实时监控将显示最近一分钟的数据曲线，且每秒更新一次数据和曲线
   - 当点击不同的性能参数按钮时，程序将根据选择更新曲线的显示。
   - 当点击Load按钮加载并显示先前数据后，可以点击Monitor按钮重新回到实时监测模式。

5. 其他操作：
   - 点击"Clear"按钮将清除缓存数据和已绘制曲线，重新开始绘制曲线。
   - 点击"Stop"按钮将暂停数据更新，当前数据将保持不变。再次点击可继续实时数据更新。

6. 关闭程序：
   - 关闭程序窗口或按下Ctrl+C键停止程序的执行。
