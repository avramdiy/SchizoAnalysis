from flask import Flask, render_template_string
import pandas as pd
import os
import matplotlib.pyplot as plt
import io
import base64

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

@app.route('/group_bar_chart')
def grouped_bar_chart():
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

        # Group data for the chart
        chart_data = df.groupby(['Gender', 'Education', 'Diagnosis']).size().reset_index(name='Count')
        pivot_table = chart_data.pivot(index=['Gender', 'Education'], columns='Diagnosis', values='Count').fillna(0)
        pivot_table.columns = ['Not Schizo', 'Schizo']
        pivot_table = pivot_table.astype(int)

        # Plot the grouped bar chart
        ax = pivot_table.plot(kind='bar', stacked=False, figsize=(10, 6), color=['skyblue', 'salmon'])
        plt.title('Diagnosis by Gender and Education', fontsize=16)
        plt.xlabel('(Gender, Education)', fontsize=12)
        plt.ylabel('Count', fontsize=12)
        plt.xticks(rotation=45, fontsize=10)
        plt.legend(title='Diagnosis', fontsize=10)
        plt.tight_layout()

        # Save the plot to a BytesIO object
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        # Render the plot in HTML
        html_template = f"""<!DOCTYPE html>
        <html>
        <head>
            <title>Diagnosis Chart</title>
        </head>
        <body>
            <h1>Grouped Bar Chart</h1>
            <img src="data:image/png;base64,{plot_url}" alt="Chart">
        </body>
        </html>"""
        return render_template_string(html_template)

    except Exception as e:
        return f"Error generating chart: {e}"

if __name__ == '__main__':
    app.run(debug=True)
