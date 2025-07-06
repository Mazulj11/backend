from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from algorithm_3 import run_algorithm
from algorithm_3_full import run_algorithm_full

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.post("/analyze")
# async def analyze(
#     init_set: str = Form(...),
#     kriterij: str = Form(...),
#     prag: int = Form(...),
#     file_skup: UploadFile = File(...),
#     file_emboss: UploadFile = File(...)
# ):
#     skup_content = (await file_skup.read()).decode('utf-8')
#     emboss_content = (await file_emboss.read()).decode('utf-8')

#     rezultat = run_algorithm(init_set, kriterij, prag, skup_content, emboss_content)

#     return JSONResponse(content={"status": "success", "result": rezultat})

@app.post("/analyze")
async def analyze(
    criteri: str = Form(...),
    limit: float = Form(...),
    text_input: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    sequences = []

    if text_input:
        sequences += parse_fasta(text_input)
    if file:
        content = (await file.read()).decode('utf-8')
        sequences += parse_fasta(content)

    if not sequences:
        return JSONResponse(content={"error": "Nema sekvenci!"})

    rezultat = run_algorithm_full(sequences, criteri, limit)

    return JSONResponse(content={"status": "success", "result": rezultat})


def parse_fasta(fasta_string):
    sequences = []
    current_id = None
    current_seq = []
    for line in fasta_string.strip().splitlines():
        line = line.strip()
        if line.startswith('>'):
            if current_id:
                sequences.append({'id': current_id, 'sequence': ''.join(current_seq)})
            current_id = line[1:]
            current_seq = []
        else:
            current_seq.append(line)
    if current_id:
        sequences.append({'id': current_id, 'sequence': ''.join(current_seq)})
    return sequences