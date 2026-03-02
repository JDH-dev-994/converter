import pdfplumber
import json
import os
import re

def extract_text_from_pdf(pdf_path):
    full_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n\n"
    return full_text

def split_text_into_paragraphs(text):
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)  # заменяет одиночные разрывы строк на пробел
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def convert_pdf_to_json(pdf_path, output_folder):
    text = extract_text_from_pdf(pdf_path)
    file_name = os.path.basename(pdf_path)
    data = {
        "file_name": file_name,
        "paragraphs": split_text_into_paragraphs(text)
    }
    json_path = os.path.join(output_folder, file_name.replace(".pdf", ".json"))
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Created {json_path}")

def convert_folder(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Получаем все файлы с расширением .pdf в папке
    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
    total = len(files)
    print(f"found {total} PDF files to convert.")

    # Проходим по всем файлам
    for idx, file in enumerate(files, start=1):
        pdf_path = os.path.join(folder_path, file)
        print(f"[{idx}/{total}] converting {file}...")
        convert_pdf_to_json(pdf_path, output_folder)

    print("=== finish ===")

