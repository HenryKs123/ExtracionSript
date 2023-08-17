import re
import json
import os
from unidecode import unidecode  # Importa la función unidecode

def clean_json_data(data):
    cleaned_data = data.copy()
    for key, value in cleaned_data.items():
        if isinstance(value, str):
            cleaned_data[key] = unidecode(value)
    return cleaned_data

def extract_especificacion_codes(textoAnotaciones):
    especificacion_codes = []
    for anotacion in textoAnotaciones:
        match = re.search(r'ESPECIFICACION: (\d{3,5})', anotacion)
        if match:
            especificacion_codes.append(match.group(1))
    return especificacion_codes

def process_json_file(filename):
    with open(filename, "r") as json_file:
        data = json.load(json_file)

    # Limpia los caracteres especiales en el diccionario
    cleaned_data = clean_json_data(data)

    especificacion_codes = extract_especificacion_codes(cleaned_data["textoAnotaciones"])

    for code in especificacion_codes:
        print("Código de especificación:", code)

def replace_special_character(input_filename, output_filename):
    with open(input_filename, "r", encoding="utf-8") as input_file:
        content = input_file.read()

    # Reemplaza el carácter especial "�" por "n"
    cleaned_content = content.replace("�", "n")

    with open(output_filename, "w", encoding="utf-8") as output_file:
        output_file.write(cleaned_content)

def main():
    json_files = [file for file in os.listdir() if file.endswith(".json")]

    for json_file in json_files:
        print("Procesando archivo:", json_file)
        process_json_file(json_file)
        print("-" * 30)
        
        # Reemplaza el carácter especial en el archivo JSON
        replace_special_character(json_file, "temp.json")
        os.remove(json_file)
        os.rename("temp.json", json_file)

if __name__ == "__main__":
    main()