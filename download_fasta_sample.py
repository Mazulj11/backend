import requests
import random
from Bio import SeqIO

# URL za UniProt reviewed Homo sapiens proteinske sekvence (možeš promijeniti organism)
URL = "https://rest.uniprot.org/uniprotkb/stream?compressed=false&format=fasta&query=reviewed:true+AND+organism_id:9606"

OUTPUT_FILE = "all_sequences.fasta"
SAMPLE_FILE = "sequences.fasta"
SAMPLE_SIZE = 25000

print("➡️  Preuzimam FASTA dataset s UniProt...")
response = requests.get(URL, stream=True)
response.raise_for_status()

with open(OUTPUT_FILE, "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)

print(f"✅ Preuzeto u datoteku: {OUTPUT_FILE}")

# Parsiramo FASTA i nasumično biramo 25k sekvenci
print("🔍 Parsiram FASTA i biram nasumičnih 25k sekvenci...")
records = list(SeqIO.parse(OUTPUT_FILE, "fasta"))

if len(records) < SAMPLE_SIZE:
    print(f"⚠️ Samo {len(records)} sekvenci dostupno, spremam sve.")
    sample_records = records
else:
    sample_records = random.sample(records, SAMPLE_SIZE)

SeqIO.write(sample_records, SAMPLE_FILE, "fasta")
print(f"✅ Spremio {len(sample_records)} sekvenci u {SAMPLE_FILE}")
