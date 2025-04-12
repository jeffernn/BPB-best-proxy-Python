import re
import requests
from tkinter import *
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

def fetch_and_save_ips():
    url = "https://ip.164746.xyz/ipTop10.html"
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        ip_elements = soup.find_all(text=ip_pattern)

        ips = []
        for element in ip_elements:
            matches = ip_pattern.findall(element)
            ips.extend(matches)

        if not ips:
            messagebox.showwarning("警告", "未找到任何IP地址")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="保存优选IP文件",
            initialfile="网页获取优选IP.txt"
        )

        if not save_path:
            return

        with open(save_path, 'w', encoding='utf-8') as file:
            for i, ip in enumerate(ips, start=1):
                file.write(f"{ip} #Jeffern优选节点{i}\n")

        messagebox.showinfo("成功", f"已成功保存{len(ips)}个优选IP")

    except Exception as e:
        messagebox.showerror("错误", f"获取或保存IP时出错:\n{str(e)}")

# 按钮动画效果函数
def on_enter(e):
    fetch_button['background'] = '#A7C7E7'  # 鼠标悬停时的颜色
    fetch_button['font'] = ('微软雅黑', 12, 'bold')  # 加粗
    fetch_button.config(relief=RAISED)  # 悬停时按钮凸起

def on_leave(e):
    fetch_button['background'] = '#B0E0E6'  # 鼠标离开时的颜色
    fetch_button['font'] = ('微软雅黑', 12)  # 恢复普通字体
    fetch_button.config(relief=FLAT)  # 恢复扁平样式

# 创建GUI界面
root = Tk()
root.title("Jeffern优选IP获取工具")
root.geometry("400x200")

# 设置窗口图标（可选）
try:
    root.iconbitmap(default='icon.ico')
except:
    pass

# 设置背景颜色为更淡的蓝色
root.configure(bg='#F0F8FF')  # AliceBlue颜色，非常淡的蓝色

# 标题标签
title_label = Label(
    root,
    text="Jeffern优选IP获取工具",
    font=("微软雅黑", 16, "bold"),
    bg='#F0F8FF',
    fg='#333'
)
title_label.pack(pady=(20, 10))

# 说明标签
desc_label = Label(
    root,
    text="点击下方按钮获取并保存优选IP",
    font=("微软雅黑", 10),
    bg='#F0F8FF',
    fg='#666'
)
desc_label.pack(pady=(0, 20))

# 获取按钮 - 使用更柔和的蓝色并添加动画效果
fetch_button = Button(
    root,
    text="开始获取",
    command=fetch_and_save_ips,
    font=("微软雅黑", 12),
    bg='#B0E0E6',  # PowderBlue颜色，柔和的蓝色
    fg='#333',    # 深灰色文字
    activebackground='#A7C7E7',  # 点击时颜色
    activeforeground='#333',    # 点击时文字颜色
    padx=20,
    pady=5,
    relief=FLAT,
    bd=0,  # 无边框
    highlightthickness=0  # 无高亮边框
)
fetch_button.pack()

# 绑定鼠标事件实现动画效果
fetch_button.bind("<Enter>", on_enter)
fetch_button.bind("<Leave>", on_leave)

# 版权信息
copyright_label = Label(
    root,
    text="© 2025 Jeffern",
    font=("微软雅黑", 8),
    bg='#F0F8FF',
    fg='#666'
)
copyright_label.pack(side=BOTTOM, pady=10)

root.mainloop()