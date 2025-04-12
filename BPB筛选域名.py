import customtkinter as ctk
from tkinter import filedialog, messagebox
import re
import os
from urllib.parse import urlparse, parse_qs
import threading

# 设置外观风格
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class DomainExtractorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("域名筛选工具 - By Jeffern")
        self.geometry("500x625")
        self.resizable(False, False)
        self.configure(fg_color="#EAF6FC")

        # 图标标签
        self.icon_label = ctk.CTkLabel(self, text="(=^･ω･^=)",
                                       font=("Segoe UI", 22, "bold"),
                                       text_color="#003E7E")
        self.icon_label.pack(pady=(10, 0))

        # 主标题
        self.title_label = ctk.CTkLabel(self,
                                        text="域名筛选工具",
                                        font=("Segoe UI", 16, "bold"),
                                        text_color="#003E7E")
        self.title_label.pack(pady=(0, 5))

        # 卡片容器
        self.card_frame = ctk.CTkFrame(self, corner_radius=16,
                                       fg_color="#FFFFFF", width=455, height=450)
        self.card_frame.pack(pady=10)

        # 初始化界面组件
        self.create_file_selector()  # 文件选择
        self.create_output_limit()  # 输出限制
        self.create_suffix_selector()  # 后缀选择

        # 进度条
        self.progress = ctk.CTkProgressBar(self.card_frame, width=320)
        self.progress.place(relx=0.5, rely=0.95, anchor="center")
        self.progress.set(0)
        self.progress.configure(fg_color="#D1EAFD", progress_color="#0077B6")

        # 处理按钮
        self.start_button = ctk.CTkButton(
            self,
            text="开始处理",
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

    def create_file_selector(self):
        """创建文件选择组件"""
        frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        frame.place(relx=0.5, rely=0.1, anchor="n", relwidth=0.9)

        self.input_path = ctk.StringVar()

        ctk.CTkLabel(frame, text="选择输入文件:",
                     font=("Segoe UI", 12)).pack(side="left")
        entry = ctk.CTkEntry(frame, textvariable=self.input_path, width=200)
        entry.pack(side="left", padx=5)
        ctk.CTkButton(frame, text="浏览", width=60,
                      command=self.select_input_file).pack(side="left")

    def create_output_limit(self):
        """创建输出限制组件"""
        frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        frame.place(relx=0.5, rely=0.2, anchor="n", relwidth=0.9)

        ctk.CTkLabel(frame, text="输出条数设置:",
                     font=("Segoe UI", 12)).pack(side="left")

        self.entry_limit = ctk.CTkEntry(frame,
                                        width=100,
                                        placeholder_text="0表示全部")
        self.entry_limit.pack(side="left", padx=5)

    def create_suffix_selector(self):
        """创建后缀选择组件"""
        frame = ctk.CTkFrame(self.card_frame, fg_color="transparent")
        frame.place(relx=0.5, rely=0.3, anchor="n", relwidth=0.9)

        ctk.CTkLabel(frame, text="选择域名后缀:",
                     font=("Segoe UI", 12)).pack(anchor="w")

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

        check_frame = ctk.CTkFrame(frame, fg_color="transparent")
        check_frame.pack(fill="both", expand=True, pady=5)

        cols = 4
        self.suffix_vars = {}
        for i, (suffix, default) in enumerate(suffixes):
            var = ctk.BooleanVar(value=default)
            self.suffix_vars[suffix] = var
            cb = ctk.CTkCheckBox(check_frame,
                                 text=suffix,
                                 variable=var,
                                 text_color="#003E7E",
                                 checkbox_width=18,
                                 checkbox_height=18)
            cb.grid(row=i // cols, column=i % cols, sticky="w", padx=5, pady=2)

    def select_input_file(self):
        """处理文件选择"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            self.input_path.set(file_path)

    def start_thread(self):
        """启动处理线程"""
        self.start_button.configure(state="disabled")
        threading.Thread(target=self.process_file).start()

    def update_progress(self, value):
        """更新进度条"""
        self.progress.set(value)
        self.update_idletasks()

    def process_file(self):
        """主要处理逻辑"""
        try:
            # 验证输出限制
            try:
                limit = int(self.entry_limit.get() or 0)
                if limit < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("错误", "请输入有效的正整数（0表示全部）")
                return

            # 验证输入文件
            if not self.input_path.get():
                messagebox.showerror("错误", "请先选择输入文件")
                return

            # 读取文件
            try:
                with open(self.input_path.get(), "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                messagebox.showerror("错误", f"文件读取失败: {str(e)}")
                return

            # 处理URL
            url_pattern = re.compile(r'https?://\S+')
            url_matches = url_pattern.findall(content)
            selected_suffixes = [s for s, v in self.suffix_vars.items() if v.get()]

            results = []
            for idx, url in enumerate(url_matches):
                try:
                    parsed = urlparse(url)
                    query = parse_qs(parsed.query)
                    if 'host' not in query:
                        continue

                    host = query['host'][0]
                    if any(host.endswith(suffix) for suffix in selected_suffixes):
                        results.append(url)

                    # 更新进度
                    self.update_progress((idx + 1) / len(url_matches) * 0.7)

                    # 达到限制数量提前退出
                    if limit > 0 and len(results) >= limit:
                        break

                except Exception as e:
                    print(f"解析失败: {url} - {str(e)}")

            # 保存结果
            save_dir = filedialog.askdirectory(title="选择保存目录")
            if not save_dir:
                return

            save_path = os.path.join(save_dir, "BPB面板筛选节点.txt")
            if os.path.exists(save_path):
                overwrite = messagebox.askyesno("确认", "目标文件已存在，是否覆盖？")
                if not overwrite:
                    return

            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(results[:limit] if limit > 0 else results))
                messagebox.showinfo("完成", f"成功导出 {len(results)} 条完整URL到\n{save_path}")
            except Exception as e:
                messagebox.showerror("错误", f"文件保存失败: {str(e)}")

        except Exception as e:
            messagebox.showerror("错误", f"处理过程中发生错误: {str(e)}")
        finally:
            self.start_button.configure(state="normal")
            self.update_progress(0)

    def on_close(self):
        """关闭窗口事件处理"""
        self.destroy()


if __name__ == "__main__":
    app = DomainExtractorApp()
    app.mainloop()
