import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

# 设置外观风格
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class TXTNodeUploaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BPB节点自动上传工具 By Jeffern")
        self.geometry("500x320")
        self.resizable(False, False)
        self.configure(fg_color="#EAF6FC")  # 主背景色

        # 图标小猫头像（模拟 Clash 风格）
        self.icon_label = ctk.CTkLabel(self, text="(=^･ω･^=)", font=("Segoe UI", 22, "bold"), text_color="#003E7E")
        self.icon_label.pack(pady=(10, 0))

        # 主标题
        self.title_label = ctk.CTkLabel(self, text="BPB节点自动上传工具", font=("Segoe UI", 16, "bold"),
                                        text_color="#003E7E")
        self.title_label.pack(pady=(0, 5))

        # 卡片容器
        self.card_frame = ctk.CTkFrame(self, corner_radius=16, fg_color="#FFFFFF", width=440, height=120)
        self.card_frame.pack(pady=10)

        # 状态标签（显示当前步骤）
        self.status_label = ctk.CTkLabel(self.card_frame, text="准备就绪", font=("Segoe UI", 13), text_color="#003E7E")
        self.status_label.place(relx=0.5, rely=0.3, anchor="center")

        # 进度条
        self.progress = ctk.CTkProgressBar(self.card_frame, width=320)
        self.progress.place(relx=0.5, rely=0.6, anchor="center")
        self.progress.set(0)
        self.progress.configure(fg_color="#D1EAFD", progress_color="#0077B6")

        # 开始上传按钮
        self.start_button = ctk.CTkButton(
            self,
            text="选择 TXT 文件并上传节点",
            command=self.start_thread,
            width=220,
            height=40,
            font=("Segoe UI", 12, "bold"),
            fg_color="#4FC3F7",
            hover_color="#81D4FA",
            text_color="#003E7E",
            corner_radius=12
        )
        self.start_button.pack(pady=(10, 5))

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_status(self, text, progress_value):
        """更新状态标签和进度条"""
        self.status_label.configure(text=text)
        self.progress.set(progress_value)
        self.update_idletasks()

    def start_thread(self):
        """在子线程中启动数据处理，避免阻塞 GUI"""
        self.start_button.configure(state="disabled")
        threading.Thread(target=self.process_data).start()

    def process_data(self):
        try:
            # 步骤 1：选择 TXT 文件
            self.update_status("正在获取 TXT 文件数据...", 0.125)
            filepath = filedialog.askopenfilename(
                title="选择 TXT 文件",
                filetypes=[("TXT 文件", "*.txt"), ("所有文件", "*.*")]
            )
            if not filepath:
                self.update_status("未选择文件", 0)
                self.start_button.configure(state="normal")
                return
            time.sleep(0.5)  # 模拟等待

            # 步骤 2：读取 TXT 数据
            self.update_status("正在读取 TXT 数据...", 0.25)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            if not content:
                messagebox.showwarning("警告", "TXT 文件为空")
                self.update_status("TXT 文件为空", 0)
                self.start_button.configure(state="normal")
                return

            # 步骤 3：准备上传数据
            self.update_status("准备上传数据...", 0.5)
            upload_data = content

            # 步骤 4：连接节点服务器
            self.update_status("正在连接节点服务器...", 0.625)
            edge_options = Options()
            edge_options.add_argument("--headless")
            edge_options.use_chromium = True
            driver = webdriver.Edge(options=edge_options)

            # 步骤 5：提交节点数据
            self.update_status("正在提交节点数据...", 0.75)
            target_url = "https://newss.newss.cc.ua/gotonews78910"
            driver.get(target_url)
            time.sleep(3)

            textarea = driver.find_element(By.CSS_SELECTOR, "textarea.editor")
            textarea.clear()
            textarea.send_keys(upload_data)

            # 步骤 6：保存提交
            self.update_status("正在保存提交...", 0.875)
            save_button = driver.find_element(By.CSS_SELECTOR, "button.save-btn")
            save_button.click()
            time.sleep(5)

            driver.quit()
            # 完成上传
            self.update_status("完成上传！", 1.0)
            self.after(0, lambda: messagebox.showinfo("成功", "节点数据上传完成"))

        except Exception as e:
            self.after(0, lambda: messagebox.showerror("错误", f"发生错误: {e}"))
            self.update_status("发生错误", 0)

        self.start_button.configure(state="normal")

    def on_close(self):
        self.destroy()


if __name__ == '__main__':
    app = TXTNodeUploaderApp()
    app.mainloop()
