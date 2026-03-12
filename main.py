import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
from report_engine import process_csv
from exporters.excel_exporter import export_excel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from exporters.pdf_exporter import export_pdf


class CSVReportApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # данные для отчётов
        self.df = None
        self.summary_data = None
        self.country_sales = None
        self.selected_file = None

        # окно
        self.title("CSV Business & E-commerce Report Generator")
        self.geometry("900x700")

        # icon
        try:
            self.iconbitmap("assets/icon.ico")
        except:
            pass

        # UI
        self.setup_ui()

    def setup_ui(self):

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # ---------- HEADER ----------
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", pady=10)

        try:
            logo = Image.open("assets/logo.png")
            self.logo_image = ctk.CTkImage(logo, size=(50, 50))

            logo_label = ctk.CTkLabel(header_frame, image=self.logo_image, text="")
            logo_label.pack(side="left", padx=10)

        except:
            logo_label = ctk.CTkLabel(header_frame, text="TM", font=("Arial", 26, "bold"))
            logo_label.pack(side="left", padx=10)

        title_label = ctk.CTkLabel(
            header_frame,
            text="CSV Business & E-commerce Report Generator",
            font=("Arial", 20, "bold")
        )
        title_label.pack(side="left", padx=10)

        # ---------- BUTTONS ----------

        select_btn = ctk.CTkButton(
            main_frame,
            text="Select CSV File",
            command=self.select_csv
        )
        select_btn.pack(pady=10)

        process_btn = ctk.CTkButton(
            main_frame,
            text="Process Data",
            command=self.process_data
        )
        process_btn.pack(pady=10)

        export_frame = ctk.CTkFrame(main_frame)
        export_frame.pack(pady=15)

        excel_btn = ctk.CTkButton(
            export_frame,
            text="Export Excel Report",
            command=self.export_excel
        )
        excel_btn.pack(side="left", padx=10)

        pdf_btn = ctk.CTkButton(
            export_frame,
            text="Export PDF Report",
            command=self.export_pdf
        )
        pdf_btn.pack(side="left", padx=10)

        # ---------- LOG ----------

        log_label = ctk.CTkLabel(main_frame, text="LOG")
        log_label.pack(pady=(20, 5))

        self.log_box = ctk.CTkTextbox(main_frame, height=120)
        self.log_box.pack(fill="x", pady=5)

# added==
# CHART FRAME
        self.chart_frame = ctk.CTkFrame(main_frame, height=350)
        self.chart_frame.pack(fill="both", expand=True, pady=10)


    def log(self, message):
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")

    def select_csv(self):

        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )

        if file_path:
            self.selected_file = file_path
            self.log(f"CSV selected: {file_path}")

    def process_data(self):

        if not self.selected_file:
            self.log("Please select a CSV file first.")
            return

        try:
            self.log("Processing CSV data...")

            df, summary_data, country_sales = process_csv(self.selected_file)

            self.df = df
            self.summary_data = summary_data
            self.country_sales = country_sales

            self.log(f"Total Orders: {summary_data['orders']}")
            self.log(f"Total Revenue: {summary_data['revenue']:.2f}")
            self.log(f"Average Order Value: {summary_data['avg_order']:.2f}")

            self.log("Data processing completed.")
            self.draw_chart()
        except Exception as e:
            self.log(f"Error: {e}")
            

    def export_excel(self):

        if self.df is None:
            self.log("Please process data first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Excel Report"
        )

        if not file_path:
            return

        try:
            export_excel(
                self.df,
                self.summary_data,
                self.country_sales,
                file_path
            )

            self.log(f"Excel report saved: {file_path}")

        except Exception as e:
            self.log(f"Excel export error: {e}")



    def draw_chart(self):

        if self.country_sales is None:
            return

        countries = self.country_sales.index
        values = self.country_sales.values

        fig, ax = plt.subplots(figsize=(5.5,3))

        ax.bar(countries, values)

        ax.set_title("Revenue by Country")
        ax.set_xlabel("Country")
        ax.set_ylabel("Revenue")

        ax.tick_params(axis='x', rotation=0)

        ax.grid(axis="y", linestyle="--", alpha=0.4)

        plt.subplots_adjust(bottom=0.25, top=0.88)
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)










    def export_pdf(self):

        if self.df is None:
            self.log("Please process data first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF Report"
    )

        if not file_path:
            return
       
        try:

            export_pdf(
                self.summary_data,
                self.country_sales,
                file_path
        )

            self.log(f"PDF report saved: {file_path}")

        except Exception as e:
            self.log(f"PDF export error: {e}")


if __name__ == "__main__":

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = CSVReportApp()
    app.mainloop()