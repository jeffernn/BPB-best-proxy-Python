import customtkinter as ctk
from tkinter import filedialog, messagebox
import csv
import random
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import tempfile
import os
import uuid
import shutil
from urllib.parse import urlparse, parse_qs

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class IntegratedBPBTool(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("BPB节点全自动上传工具 By：Jeffern")
        self.geometry("720x650")
        self.resizable(False, False)
        self.configure(fg_color="#EAF6FC")

        # 初始化数据存储
        self.processed_urls = []
        self.filtered_urls = []
        self.active_drivers = []

        # 新增默认值
        self.default_subscriber_url = "dy.yomoh.ggff.net"
        self.default_proxy_id = "ProxyIP.Oracle.CMLiussss.net"
        self.default_upload_url = "https://ef7fa04a.python-aggregate-subscription.pages.dev/gotonews78910"

        # 初始化界面
        self.create_gui_components()

    def create_gui_components(self):
        # 顶部图标和标题
        self.icon_label = ctk.CTkLabel(
            self, text="(=^･ω･^=)",
            font=("Segoe UI", 22, "bold"),
            text_color="#003E7E"
        )
        self.icon_label.pack(pady=(15, 5))

        self.title_label = ctk.CTkLabel(
            self, text="BPB节点全自动上传工具",
            font=("Segoe UI", 16, "bold"),
            text_color="#003E7E"
        )
        self.title_label.pack(pady=(0, 15))

        # 主卡片容器
        self.card_frame = ctk.CTkFrame(
            self, corner_radius=20,
            fg_color="#FFFFFF",
            width=460, height=100
        )
        self.card_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # 步骤1：CSV处理
        self.create_csv_section(self.card_frame)
        # 新增步骤：配置设置
        self.create_config_section(self.card_frame)
        # 步骤2：筛选设置
        self.create_filter_section(self.card_frame)

        # 步骤3：状态显示
        self.create_status_section()

        # 全局进度条
        self.global_progress = ctk.CTkProgressBar(
            self, width=400,
            fg_color="#D1EAFD",
            progress_color="#0077B6"
        )
        self.global_progress.pack(pady=10)

        # 处理按钮
        self.process_btn = ctk.CTkButton(
            self, text="开始上传到服务器",
            command=self.start_full_process,
            width=220, height=40,
            font=("Segoe UI", 12, "bold"),
            fg_color="#4FC3F7", hover_color="#81D4FA",
            text_color="#003E7E", corner_radius=12
        )
        self.process_btn.pack(pady=5)

    def create_csv_section(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(frame, text="1. 选择CSV文件:").pack(side="left", padx=(0, 5))
        self.csv_path = ctk.StringVar()
        entry = ctk.CTkEntry(frame, textvariable=self.csv_path, width=250)
        entry.pack(side="left", padx=5)
        ctk.CTkButton(frame, text="浏览", width=60, command=self.select_csv).pack(side="left", padx=5)

    def create_config_section(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=10, padx=20, fill="x")

        configs = [
            ("①订阅器地址:", self.default_subscriber_url),
            ("②PROXYIP地址:", self.default_proxy_id),
            ("③上传服务器地址:", self.default_upload_url)
        ]

        for label_text, default_value in configs:
            config_sub_frame = ctk.CTkFrame(frame, fg_color="transparent")
            config_sub_frame.pack(pady=5, fill="x")
            label = ctk.CTkLabel(config_sub_frame, text=label_text)
            label.pack(side="left", padx=(0, 5))
            var = ctk.StringVar(value=default_value)
            entry = ctk.CTkEntry(config_sub_frame, textvariable=var, width=250)
            entry.pack(side="left", padx=5)

            if label_text == "①订阅器地址:":
                self.subscriber_url_var = var
            elif label_text == "②PROXYIP地址:":
                self.proxy_id_var = var
            elif label_text == "③上传服务器地址:":
                self.upload_url_var = var

    def create_filter_section(self, parent):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(pady=10, padx=20, fill="x")

        # 输出数量设置
        limit_frame = ctk.CTkFrame(frame, fg_color="transparent")
        limit_frame.pack(fill="x", pady=(0, 15))
        ctk.CTkLabel(limit_frame, text="2.上传的节点数:").pack(side="left", padx=(0, 5))
        self.limit_entry = ctk.CTkEntry(
            limit_frame, width=100,
            placeholder_text="若输入0则全部"
        )
        self.limit_entry.pack(side="left", padx=5)

        # 后缀选择
        ctk.CTkLabel(frame, text="选择所需上传的域名后缀:").pack(anchor="w", padx=5, pady=(0, 5))

        suffixes = [
            ('.com', False), ('.cn', False), ('.net', False),
            ('.org', False), ('us.kg', False), ('.edu', False),
            ('.me', False), ('.top', False), ('.ir', False),
            ('.cfd', False), ('.online', False), ('.cf', False),
            ('.xyz', False), ('.mn', False), ('.sbs', False),
            ('.cd.am', False), ('.pp.ua', False),
            ('.dev', False), ('.ink', False), ('.id', False),
            ('.hr', False), ('.eu', False), ('.be', False),
            ('.webside', False)
        ]

        self.suffix_vars = {}
        check_frame = ctk.CTkFrame(frame, fg_color="transparent")
        check_frame.pack(fill="both", expand=True, pady=5, padx=5)

        for i, (suffix, default) in enumerate(suffixes):
            var = ctk.BooleanVar(value=default)
            self.suffix_vars[suffix] = var
            cb = ctk.CTkCheckBox(
                check_frame, text=suffix, variable=var,
                text_color="#003E7E", checkbox_width=18, checkbox_height=18
            )
            cb.grid(row=i // 6, column=i % 6, sticky="w", padx=5, pady=2)

    def create_status_section(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=10, padx=20, fill="x")

        self.status_label = ctk.CTkLabel(
            frame, text="目前状态: 准备就绪",
            font=("Segoe UI", 12),
            text_color="#0077B6"
        )
        self.status_label.pack(anchor="w")

    def select_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_path.set(file_path)

    def start_full_process(self):
        self.process_btn.configure(state="disabled")
        threading.Thread(target=self.process_chain, daemon=True).start()

    def process_chain(self):
        try:
            self.update_status("正在处理CSV数据...", 0.2)
            if not self.process_csv():
                return

            self.update_status("正在筛选域名...", 0.5)
            if not self.filter_domains():
                return

            self.update_status("正在上传节点...", 0.8)
            self.auto_upload()

            self.update_status("服务器上传完成！", 1.0)
            messagebox.showinfo("完成", "节点已上传至服务器！")

        except Exception as e:
            messagebox.showerror("错误", f"处理链中断：{str(e)}")
        finally:
            self.process_btn.configure(state="normal")
            self.global_progress.set(0)
            self.cleanup_drivers()

    def process_csv(self):
        try:
            with open(self.csv_path.get(), 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                self.processed_urls = []

                for row in reader:
                    if not row or not row[0].strip():
                        continue

                    domain = row[0].strip().lower()
                    for prefix in ["https://", "http://", "\ufeff"]:
                        domain = domain.removeprefix(prefix)
                    domain = domain.split('/')[0].split(':')[0]

                    if "." in domain:
                        subscriber_url = self.subscriber_url_var.get().strip()
                        proxy_id = self.proxy_id_var.get().strip()
                        url = (f"https://{subscriber_url}/sub?uuid=89b3cbba-e6ac-485a-9481-976a0415eab9"
                               f"&encryption=none&security=tls&sni={domain}&fp=random&type=ws"
                               f"&host={domain}&path=%2Fproxyip%3D{proxy_id}")
                        self.processed_urls.append(url)

                if not self.processed_urls:
                    messagebox.showerror("错误", "CSV文件中未找到有效域名")
                    return False
                return True

        except Exception as e:
            messagebox.showerror("错误", f"CSV处理失败：{str(e)}")
            return False

    def filter_domains(self):
        try:
            limit = int(self.limit_entry.get() or 0)
            selected_suffixes = [s for s, v in self.suffix_vars.items() if v.get()]

            if not selected_suffixes:
                messagebox.showerror("错误", "请至少选择一个域名后缀")
                return False

            qualified = []
            for url in self.processed_urls:
                try:
                    parsed = urlparse(url)
                    host = parse_qs(parsed.query).get('host', [''])[0]
                    if any(host.endswith(suffix) for suffix in selected_suffixes):
                        qualified.append(url)
                except:
                    continue

            random.shuffle(qualified)
            self.filtered_urls = qualified[:limit] if limit > 0 else qualified

            if not self.filtered_urls:
                messagebox.showerror("错误", "没有符合筛选条件的域名")
                return False
            return True

        except Exception as e:
            messagebox.showerror("错误", f"筛选失败：{str(e)}")
            return False

    def auto_upload(self):
        driver = None
        user_data_dir = None
        try:
            user_data_dir = os.path.join(tempfile.gettempdir(), f"edge_profile_{uuid.uuid4().hex}")
            os.makedirs(user_data_dir, exist_ok=True)

            edge_options = Options()
            edge_options.add_argument("--headless")
            edge_options.add_argument(f"--user-data-dir={user_data_dir}")
            edge_options.add_argument("--disable-gpu")
            edge_options.add_argument("--no-sandbox")

            driver = webdriver.Edge(options=edge_options)
            self.active_drivers.append(driver)

            upload_url = self.upload_url_var.get().strip()
            driver.get(upload_url)
            time.sleep(3)

            textarea = driver.find_element(By.CSS_SELECTOR, "textarea.editor")
            textarea.clear()
            textarea.send_keys("\n".join(self.filtered_urls))

            driver.find_element(By.CSS_SELECTOR, "button.save-btn").click()
            time.sleep(5)

        except Exception as e:
            messagebox.showerror("错误", f"上传失败：{str(e)}")
        finally:
            self.cleanup_driver(driver, user_data_dir)

    def update_status(self, text, progress):
        self.status_label.configure(text=f"3. 状态: {text}")
        self.global_progress.set(progress)
        self.update_idletasks()

    def cleanup_driver(self, driver, user_data_dir):
        if driver:
            try:
                driver.quit()
            except:
                pass
        if user_data_dir and os.path.exists(user_data_dir):
            shutil.rmtree(user_data_dir, ignore_errors=True)

    def cleanup_drivers(self):
        for driver in self.active_drivers:
            self.cleanup_driver(driver, None)
        self.active_drivers.clear()

    def on_close(self):
        # 将清理操作放在单独的线程中执行
        threading.Thread(target=self._cleanup_and_close, daemon=True).start()

    def _cleanup_and_close(self):
        self.cleanup_drivers()
        self.destroy()


if __name__ == "__main__":
    app = IntegratedBPBTool()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
