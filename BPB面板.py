import customtkinter as ctk
from tkinter import filedialog, messagebox
import csv
import os

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class DomainProcessorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BPB节点处理工具 By Jeffern")
        self.geometry("500x350")
        self.resizable(False, False)
        self.configure(fg_color="#EAF6FC")  # 主背景色

        # 图标
        self.icon_label = ctk.CTkLabel(
            self,
            text="(=^･ω･^=)",
            font=("Segoe UI", 22, "bold"),
            text_color="#003E7E"
        )
        self.icon_label.pack(pady=(10, 0))

        # 主标题
        self.title_label = ctk.CTkLabel(
            self,
            text="CSV域名处理工具",
            font=("Segoe UI", 16, "bold"),
            text_color="#003E7E"
        )
        self.title_label.pack(pady=(0, 5))

        # 卡片容器
        self.card_frame = ctk.CTkFrame(
            self,
            corner_radius=16,
            fg_color="#FFFFFF",
            width=440,
            height=180
        )
        self.card_frame.pack(pady=10)

        # CSV文件选择
        self.csv_button = ctk.CTkButton(
            self.card_frame,
            text="选择CSV文件",
            command=self.select_csv,
            width=180,
            height=32,
            font=("Segoe UI", 12),
            fg_color="#4FC3F7",
            hover_color="#81D4FA",
            text_color="#003E7E"
        )
        self.csv_button.place(x=20, y=20)

        self.csv_entry = ctk.CTkEntry(
            self.card_frame,
            width=220,
            height=32,
            font=("Segoe UI", 12)
        )
        self.csv_entry.place(x=210, y=20)

        # 输出文件选择
        self.output_button = ctk.CTkButton(
            self.card_frame,
            text="保存位置",
            command=self.select_output,
            width=180,
            height=32,
            font=("Segoe UI", 12),
            fg_color="#4FC3F7",
            hover_color="#81D4FA",
            text_color="#003E7E"
        )
        self.output_button.place(x=20, y=70)

        self.output_entry = ctk.CTkEntry(
            self.card_frame,
            width=220,
            height=32,
            font=("Segoe UI", 12)
        )
        self.output_entry.place(x=210, y=70)

        # 状态显示
        self.status_label = ctk.CTkLabel(
            self.card_frame,
            text="准备就绪",
            font=("Segoe UI", 12),
            text_color="#0077B6"
        )
        self.status_label.place(x=20, y=120)

        # 进度条
        self.progress = ctk.CTkProgressBar(
            self.card_frame,
            width=400,
            height=6,
            fg_color="#D1EAFD",
            progress_color="#0077B6"
        )
        self.progress.set(0)
        self.progress.place(x=20, y=150)

        # 处理按钮
        self.process_btn = ctk.CTkButton(
            self,
            text="开始转换",
            command=self.start_process,
            width=220,
            height=40,
            font=("Segoe UI", 12, "bold"),
            fg_color="#4FC3F7",
            hover_color="#81D4FA",
            text_color="#003E7E",
            corner_radius=12
        )
        self.process_btn.pack(pady=(5, 0))

    def update_status(self, text, progress=0):
        self.status_label.configure(text=text)
        self.progress.set(progress)
        self.update_idletasks()

    def select_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.csv_entry.delete(0, "end")
            self.csv_entry.insert(0, file_path)

    def select_output(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")],
            initialfile="BPB泄露节点"
        )
        if file_path:
            self.output_entry.delete(0, "end")
            self.output_entry.insert(0, file_path)

    def start_process(self):
        csv_file = self.csv_entry.get()
        output_file = self.output_entry.get()

        if not csv_file or not output_file:
            messagebox.showerror("错误", "请先选择CSV文件和输出路径！")
            return

        self.process_btn.configure(state="disabled")
        self.update_status("正在处理数据...", 0.3)

        try:
            with open(csv_file, 'r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                results = []

                for row in reader:
                    if not row or not row[0].strip():
                        continue

                    domain = row[0].strip().lower()
                    for prefix in ["https://", "http://", "\ufeff"]:
                        domain = domain.removeprefix(prefix)
                    domain = domain.split('/')[0].split(':')[0]

                    if "." in domain:
                        url = (
                            f"https://dy.yomoh.ggff.net/sub?uuid=89b3cbba-e6ac-485a-9481-976a0415eab9&"
                            f"encryption=none&security=tls&sni={domain}&fp=random&type=ws&"
                            f"host={domain}&path=%2Fproxyip%3DProxyIP.Oracle.CMLiussss.net"
                        )
                        results.append(url)

                self.update_status("正在保存文件...", 0.8)
                with open(output_file, 'w', encoding='utf-8') as out_file:
                    out_file.write('\n'.join(results))

                self.update_status("处理完成", 1.0)
                messagebox.showinfo("完成", f"成功生成 {len(results)} 条记录")

        except Exception as e:
            messagebox.showerror("错误", f"处理失败：\n{str(e)}")
            self.update_status("发生错误", 0)

        self.process_btn.configure(state="normal")
        self.progress.set(0)


if __name__ == "__main__":
    app = DomainProcessorApp()
    app.mainloop()
