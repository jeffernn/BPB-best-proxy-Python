import csv
import tkinter as tk
from tkinter import filedialog, messagebox


def process_file():
    try:
        filepath = filedialog.askopenfilename(
            title="选择CSV文件",
            filetypes=[("CSV文件", "*.csv"), ("所有文件", "*.*")]
        )
        if not filepath:
            return

        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = [row for row in reader if row]  # 读取所有非空行

            # 检查是否有数据
            if not rows:
                messagebox.showwarning("警告", "CSV文件为空")
                return

            # 查找下载速度列的索引
            header = rows[0]
            try:
                speed_col = header.index("下载速度 (MB/s)")
            except ValueError:
                try:
                    speed_col = header.index("下载速度")
                except ValueError:
                    messagebox.showerror("错误", "未找到下载速度列")
                    return

            # 处理数据行（跳过标题行）
            data = []
            for row in rows[1:]:
                if len(row) > speed_col and row[0].strip():  # 确保有足够列且IP不为空
                    try:
                        speed = float(row[speed_col])
                        if speed > 0:  # 只保留下载速度>0的IP
                            data.append(row[0])
                    except ValueError:
                        continue  # 跳过无法转换为数字的行

        result = [f"{item}#Jeffern优选节点{i + 1}" for i, item in enumerate(data)]

        save_path = filedialog.asksaveasfilename(
            title="保存结果",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialfile="优选IP.txt"
        )
        if not save_path:
            return

        with open(save_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result))

        messagebox.showinfo("成功", f"已成功导出{len(result)}条Cloudflare优选IP\n文件名为：优选IP")
    except Exception as e:
        messagebox.showerror("错误", f"处理失败: {e}")


# 创建GUI界面
root = tk.Tk()
root.title("Cloudflare优选IP转换器 by:Jeffern")
root.geometry("400x180")
root.resizable(False, False)
root.configure(bg='#e6f2ff')

# 主框架
main_frame = tk.Frame(root, bg='#e6f2ff')
main_frame.pack(expand=True, fill='both', padx=20, pady=20)

# 标题
title_label = tk.Label(
    main_frame,
    text="优选IP处理",
    font=('Arial', 20, 'bold'),
    bg='#e6f2ff',
    fg='#2c5282'
)
title_label.pack(pady=(10, 20))

# 处理按钮
process_btn = tk.Button(
    main_frame,
    text="选取CSV文件",
    command=process_file,
    bg='#4a90d9',
    fg='white',
    activebackground='#7fb8e6',
    activeforeground='white',
    font=('Arial', 10),
    relief='raised',
    borderwidth=0,
    padx=20,
    pady=5
)
process_btn.pack(pady=10)

# 添加悬停效果
process_btn.bind("<Enter>", lambda e: process_btn.config(bg='#7fb8e6'))
process_btn.bind("<Leave>", lambda e: process_btn.config(bg='#4a90d9'))

root.mainloop()