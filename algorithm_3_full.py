def run_algorithm_full(sequences, kriterij_1, prag):
    """
    sequences: lista dict-ova: [{'id': '2w2e_A', 'sequence': 'MPDIENQA...'}, ...]
    kriterij_1: 'ident' ili 'sim'
    prag: float ili int
    """
    from datetime import datetime
    import numpy as np

    start_time = datetime.now()

    broj_proteina = len(sequences)

    # Npr. dummy matrica s random vrijednostima > za demo
    mat = np.random.randint(0, 2, size=(broj_proteina, broj_proteina))

    # Broj jedinica i gustoća
    num_ones = int(np.sum(mat))
    density = round(num_ones / (mat.shape[0] * mat.shape[1]), 4) if mat.size > 0 else 0

    # Prosječna duljina sekvence
    avg_length = round(sum(len(s['sequence']) for s in sequences) / broj_proteina, 2) if broj_proteina else 0

    trajanje = str(datetime.now() - start_time)

    return {
        "trajanje": trajanje,
        "broj_proteina": broj_proteina,
        "dimenzija_matrice": f"{mat.shape[0]}x{mat.shape[1]}",
        "num_ones_in_matrix": num_ones,
        "matrix_density": density,
        "avg_length": avg_length,
        "first_ids": [s['id'] for s in sequences[:5]],
        "first_sequences": [s['sequence'][:50]+'...' if len(s['sequence'])>50 else s['sequence'] for s in sequences[:3]]
    }
