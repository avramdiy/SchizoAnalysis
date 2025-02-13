from flask import Flask, render_template_string
import pandas as pd
import os

app = Flask(__name__)

# File path for the dataset
data_path = r'C:\Users\Ev\Desktop\TRG Week 11\schizophrenia_dataset.csv'

# Ensure the file exists
if not os.path.exists(data_path):
    raise FileNotFoundError(f"The file at {data_path} does not exist.")

@app.route('/')
def display_dataframe():
    # Load the data into a pandas dataframe
    try:
        df = pd.read_csv(data_path)
        # Rename columns from Turkish to English
        df.rename(columns={
            'Hasta_ID': 'Patient_ID',
            'Yaş': 'Age',
            'Cinsiyet': 'Gender',
            'Eğitim_Seviyesi': 'Education',
            'Medeni_Durum': 'Marital_Status',
            'Meslek': 'Occupation',
            'Gelir_Düzeyi': 'Income',
            'Yaşadığı_Yer': 'Live_Area',
            'Tanı': 'Diagnosis',
            'Hastalık_Süresi': 'Disease_Duration',
            'Hastaneye_Yatış_Sayısı': 'Hospitalizations',
            'Ailede_Şizofreni_Öyküsü': 'Family_History',
            'Madde_Kullanımı': 'Substance_Use',
            'İntihar_Girişimi': 'Suicide_Attempt',
            'Pozitif_Semptom_Skoru': 'Positive_Symptom_Score',
            'Negatif_Semptom_Skoru': 'Negative_Symptom_Score',
            'GAF_Skoru': 'GAF',
            'Sosyal_Destek': 'Social_Support',
            'Stres_Faktörleri': 'Stress_Factors',
            'İlaç_Uyumu': 'Medication_Adherence'
        }, inplace=True)
        # Drop the Patient_ID column
        df.drop(columns=['Patient_ID'], inplace=True)
    except Exception as e:
        return f"Error loading CSV file: {e}"

    # Convert dataframe to raw HTML
    html_table = df.to_html(index=False, classes='table table-striped', border=0)

    # Render the HTML
    html_template = f"""<!DOCTYPE html>
    <html>
    <head>
        <title>DataFrame Viewer</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            .table th, .table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            .table th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Schizophrenia Dataset</h1>
        {html_table}
    </body>
    </html>"""
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True)
