import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# Read the data
df = pd.read_csv("data.csv")

# Summarize sales by department
summary = df.groupby("Department")["Sales"].sum().reset_index()

# Plotting sales chart
plt.figure(figsize=(6, 4))
plt.bar(summary["Department"], summary["Sales"], color="green")
plt.title("Total Sales by Department")
plt.xlabel("Department")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("sales_chart.png")
plt.close()

# Define PDF class
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Automated Sales Report", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_chart(self, image_path):
        self.image(image_path, x=30, w=150)
        self.ln(10)

    def add_table(self, data):
        self.set_font("Arial", size=10)
        # Manual column width (adjust as needed)
        col_widths = [60, 60]
        
        # Table header
        for i, column in enumerate(data.columns):
            self.cell(col_widths[i], 10, str(column), border=1)
        self.ln()

        # Table rows
        for index, row in data.iterrows():
            self.cell(col_widths[0], 10, str(row[0]), border=1)
            self.cell(col_widths[1], 10, str(row[1]), border=1)
            self.ln()

# Create and save PDF
pdf = PDF()
pdf.add_page()
pdf.add_chart("sales_chart.png")
pdf.add_table(summary)
pdf.output("sample_report.pdf")

print("Report generated: sample_report.pdf")
