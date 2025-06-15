import pandas as pd
from fpdf import FPDF
import os
from pathlib import Path

#  Function to read data from CSV file
def read_data(file_path):
    try:
        file_path = file_path.strip().strip('"')  # Clean up input
        data = pd.read_csv(file_path)
        return data
    except FileNotFoundError:
        print(" File not found. Please check the path.")
        return None
    except Exception as e:
        print(f" Error reading file: {e}")
        return None

# Analyze the data
def analyze_data(data):
    summary = {
        "Total Entries": len(data),
        "Columns": data.columns.tolist(),
        "Mean of Numeric Columns": data.select_dtypes(include='number').mean().round(2).to_dict(),
        "Missing Values": data.isnull().sum().to_dict()
    }
    return summary

# Define the PDF report class
class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Data Analysis Report', border=0, ln=1, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=1)
        self.set_font('Arial', '', 11)
        if isinstance(content, dict):
            for key, value in content.items():
                self.cell(0, 10, f'{key}: {value}', ln=1)
        elif isinstance(content, list):
            for item in content:
                self.cell(0, 10, f'- {item}', ln=1)
        else:
            self.cell(0, 10, str(content), ln=1)
        self.ln(5)

# Generate the PDF report, you can add more section based on need 
def generate_pdf_report(summary, output_path):
    pdf = PDFReport()
    pdf.add_page()
    pdf.add_section('Summary', summary)
    pdf.add_section('Mean of Numeric Columns', summary['Mean of Numeric Columns'])
    pdf.add_section('Missing Values', summary['Missing Values'])
    pdf.output(output_path)
    return output_path

# Main function, takes the input path and saves the file in desktop
def main():
    file_path = input(" Enter the path to your CSV file: ").strip().strip('"')
    data = read_data(file_path)

    if data is not None:
        summary = analyze_data(data)

        # Get user's desktop path
        desktop_path = Path.home() / "Desktop"

        # Use original file name for the report
        base_name = Path(file_path).stem
        output_filename = f"{base_name}_analysis_report.pdf"
        output_path = desktop_path / output_filename

        # Generate report
        final_path = generate_pdf_report(summary, str(output_path))
        print(f"\n Report successfully generated at: {final_path}")

if __name__ == "__main__":
    main()
