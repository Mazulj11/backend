# algorithm.py
from operator import itemgetter
import numpy as np
from datetime import datetime

def run_algorithm(init_set, kriterij_1, gr_vrijednost, file_skup_content, file_emboss_content):
    start_time = datetime.now()

    total_prot = []
    linije_za_ispis = []

    # Učitavanje proteina iz file_skup_content
    lines1 = file_skup_content.strip().splitlines()
    for i in range(len(lines1)):
        rbroj = i
        l1 = lines1[i].strip().split('\t')
        ulli = [rbroj] + l1
        linije_za_ispis.append(ulli)
        chain = l1[0].strip()
        dulj = int(l1[1])
        ntm = int(l1[2])
        res = l1[3].strip('0')
        if res not in ('N-APP', 'N-ANG'):
            res = float(res)
        exp_met = l1[4]
        tip = l1[15]
        seq = l1[15]
        total_prot.append([rbroj, chain, dulj, ntm, res, exp_met, tip, seq])

    # Odabir skupa proteina
    select_prot = []
    x = n = em = e = s = f = 0
    if init_set == '1212':
        R = 100
        for prot in total_prot:
            res, method = prot[4], prot[5]
            if (isinstance(res, float) and res <= R) or res in ('N-ANG', 'N-APP'):
                if method == 'X-RAY':
                    x += 1; select_prot.append(prot)
                elif method == 'S-NMR':
                    n += 1; select_prot.append(prot)
                elif method == 'E-MIC':
                    em += 1; select_prot.append(prot)
                elif method == 'E-CRY':
                    e += 1; select_prot.append(prot)
                elif method == 'SSNMR':
                    s += 1; select_prot.append(prot)
                elif method == 'F-DIF':
                    f += 1; select_prot.append(prot)
    elif init_set == '907':
        R = 1.5
        for prot in total_prot:
            res, method = prot[4], prot[5]
            if (isinstance(res, float) and res <= R) or res in ('N-ANG', 'N-APP'):
                if method == 'X-RAY':
                    x += 1; select_prot.append(prot)
                elif method == 'S-NMR':
                    n += 1; select_prot.append(prot)
    else:
        return {"error": "Neispravan init_set"}

    # Kriterij
    if kriterij_1.lower() == 'ident':
        kol_krit = 2
    elif kriterij_1.lower() == 'sim':
        kol_krit = 3
    else:
        return {"error": "Neispravan kriterij"}

    # Učitavanje emboss file-a
    lines2 = file_emboss_content.strip().splitlines()
    ulazne_linije = []
    for line in lines2:
        lp1 = line.strip().split('\t')
        ulazne_linije.append([
            lp1[0].strip(), lp1[1].strip(),
            float(lp1[2].strip()), float(lp1[3].strip())
        ])

    # Filtriranje po pragu
    linije = [
        lin for lin in ulazne_linije
        if lin[kol_krit] >= gr_vrijednost
        and any(lin[0]==x[1] for x in select_prot)
        and any(lin[1]==x[1] for x in select_prot)
    ]

    # Kreiranje matrice
    mat = np.zeros((len(select_prot), len(select_prot)), dtype=int)
    for lin in linije:
        for i, p in enumerate(select_prot):
            if lin[1] == p[1]:
                for j, k in enumerate(select_prot):
                    if lin[0] == k[1]:
                        mat[i][j] = 1

    # Broj TM segmenata ukupno
    total_tm = sum(p[3] for p in select_prot)

    # Prosječna duljina sekvence
    avg_length = round(sum(p[2] for p in select_prot) / len(select_prot), 2) if select_prot else 0

    # Prosječan broj TM segmenata
    avg_tm = round(total_tm / len(select_prot), 2) if select_prot else 0

    # Sve pdb kodove
    all_pdb_codes = [p[1] for p in select_prot]

    # Prvih 3 sekvence (skraćeno)
    first_seqs = [p[7][:50] + '...' if len(p[7]) > 50 else p[7] for p in select_prot[:3]]

    # Statistika matrice
    num_ones = int(np.sum(mat))
    density = round(num_ones / (mat.shape[0] * mat.shape[1]), 4) if mat.size > 0 else 0

    end_time = datetime.now()
    trajanje = str(end_time - start_time)

    return {
        "trajanje": trajanje,
        "broj_proteina": len(select_prot),
        "dimenzija_matrice": f"{mat.shape[0]}x{mat.shape[1]}",
        "prvih_5_proteina": all_pdb_codes[:5],
        "total_tm": total_tm,
        "avg_length": avg_length,
        "avg_tm": avg_tm,
        "num_ones_in_matrix": num_ones,
        "matrix_density": density,
        "first_sequences": first_seqs,
        "all_pdb_codes": all_pdb_codes
    }
