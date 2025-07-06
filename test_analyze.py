import requests

url = "http://127.0.0.1:8000/analyze"

# Prilagodi putanje!
files = {
    "file_skup": open("./ULAZ_SKUP_N1212.txt", "rb"),
    "file_emboss": open("./ULAZ_OPM_PDB_EMBOSS_OUT.txt", "rb"),
}

data = {
    "init_set": "1212",
    "kriterij": "ident",
    "prag": "20"
}

response = requests.post(url, data=data, files=files)

print("Status code:", response.status_code)
print("Response JSON:")
print(response.json())
