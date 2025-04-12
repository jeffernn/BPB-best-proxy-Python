import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import tempfile
import os
import uuid
import shutil
import glob

# 设置外观风格
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class TXTNodeUploaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BPB节点自动上传工具 By Jeffern")
        self.geometry("500x320")
        self.resizable(False, False)
        self.configure(fg_color="#EAF6FC")

        # GUI组件初始化
        self.icon_label = ctk.CTkLabel(self, text="(=^･ω･^=)", font=("Segoe UI", 22, "bold"), text_color="#003E7E")
        self.icon_label.pack(pady=(10, 0))

        self.title_label = ctk.CTkLabel(self, text="BPB节点自动上传工具", font=("Segoe UI", 16, "bold"),
                                        text_color="#003E7E")
        self.title_label.pack(pady=(0, 5))

        self.card_frame = ctk.CTkFrame(self, corner_radius=16, fg_color="#FFFFFF", width=440, height=120)
        self.card_frame.pack(pady=10)

        self.status_label = ctk.CTkLabel(self.card_frame, text="准备就绪", font=("Segoe UI", 13), text_color="#003E7E")
        self.status_label.place(relx=0.5, rely=0.3, anchor="center")

        self.progress = ctk.CTkProgressBar(self.card_frame, width=320)
        self.progress.place(relx=0.5, rely=0.6, anchor="center")
        self.progress.set(0)
        self.progress.configure(fg_color="#D1EAFD", progress_color="#0077B6")

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
        self.active_drivers = []

    def update_status(self, text, progress_value):
        self.status_label.configure(text=text)
        self.progress.set(progress_value)
        self.update_idletasks()

    def start_thread(self):
        self.start_button.configure(state="disabled")
        threading.Thread(target=self.process_data, daemon=True).start()

    def process_data(self):
        driver = None
        user_data_dir = None
        try:
            # 生成唯一临时目录
            user_data_dir = os.path.join(tempfile.gettempdir(), f"edge_profile_{uuid.uuid4().hex}")
            os.makedirs(user_data_dir, exist_ok=True)

            # 文件选择
            self.update_status("正在获取 TXT 文件数据...", 0.125)
            filepath = filedialog.askopenfilename(filetypes=[("TXT 文件", "*.txt")])
            if not filepath:
                self.update_status("未选择文件", 0)
                return

            # 读取文件
            self.update_status("正在读取 TXT 数据...", 0.25)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            if not content:
                messagebox.showwarning("警告", "TXT 文件为空")
                self.update_status("TXT 文件为空", 0)
                return

            # 浏览器配置
            edge_options = Options()
            edge_options.add_argument("--headless")
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            edge_options.add_argument(f"--user-data-dir={user_data_dir}")

            # 启动浏览器
            self.update_status("正在连接节点服务器...", 0.625)
            driver = webdriver.Edge(options=edge_options)
            self.active_drivers.append(driver)

            # 页面操作
            driver.get("https://ef7fa04a.python-aggregate-subscription.pages.dev/gotonews78910")
            time.sleep(3)
            textarea = driver.find_element(By.CSS_SELECTOR, "textarea.editor")
            textarea.clear()
            textarea.send_keys(content)

            driver.find_element(By.CSS_SELECTOR, "button.save-btn").click()
            time.sleep(5)

            self.update_status("完成上传！", 1.0)
            messagebox.showinfo("成功", "节点数据上传完成")

        except Exception as e:
            messagebox.showerror("错误", f"发生错误: {str(e)}")
            self.update_status("发生错误", 0)
        finally:
            if driver:
                driver.quit()
                if driver in self.active_drivers:
                    self.active_drivers.remove(driver)
            if user_data_dir and os.path.exists(user_data_dir):
                try:
                    shutil.rmtree(user_data_dir, ignore_errors=True)
                except Exception as e:
                    print(f"清理临时目录出错: {e}")
            self.start_button.configure(state="normal")

    def on_close(self):
        threading.Thread(target=self.cleanup_resources, daemon=True).start()
        self.destroy()

    def cleanup_resources(self):
        for driver in list(self.active_drivers):
            try:
                driver.quit()
            except Exception as e:
                print(f"清理驱动时出错: {e}")
        self.active_drivers.clear()

        temp_dir = os.path.join(tempfile.gettempdir(), "edge_profile_*")
        for dir_path in glob.glob(temp_dir):
            try:
                shutil.rmtree(dir_path, ignore_errors=True)
            except Exception as e:
                print(f"清理临时目录出错: {e}")


if __name__ == '__main__':
    app = TXTNodeUploaderApp()
    app.mainloop()
