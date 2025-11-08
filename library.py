
import json
import pandas as pd
import numpy as np
def init_params(instance):
    # On load le json
    with open(instance, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Ici on récupère toutes les compétences existantes et on en fait un dict de correspondance avec leur valeur numérique dans les matrices    
    qualifications={}
    i=0
    for q in sorted(data["qualifications"]):
        qualifications[q] = i
        i += 1   
    #On récupère les params généraux de l'instance
    h= data["horizon"]
    qualif_nb = len(data["qualifications"])
    staff_nb = len(data["staff"])
    project_nb = len(data["jobs"])
    # On crée la matrice de compétences de chaque membre du staff
    C = []
    for s in range(staff_nb):
        qualifs = data["staff"][s]["qualifications"]
        C.append([0]*qualif_nb)
        for q in qualifs:
            C[s][qualifications[q]]=1
    # La matrice des gains pour chaque projet complété
    CA = [data["jobs"][j]["gain"] for j in range(len(data["jobs"]))]
    # La matrice des besoins par compétences de chaque projet
    N = []
    for j in range(len(data["jobs"])):
        N.append([0]*qualif_nb)
        for q in data["jobs"][j]["working_days_per_qualification"].keys():
            N[j][qualifications[q]]=data["jobs"][j]["working_days_per_qualification"][q]
    # La matrice des congés de chaque membre du staff
    G =[[1]*h for _  in range(staff_nb)]
    for s in range(staff_nb):
        for g in data["staff"][s]["vacations"]:
            G[s][g-1] = 0
    # La matrice des noms de chaque membre du staff
    names = [staff["name"] for staff in data["staff"]]
    # La matrice des deadlines de chaques projets
    D = [[0]*h for _ in range(project_nb)]
    for j in range(project_nb):
        D[j][data["jobs"][j]["due_date"]-1]=1
    # La matrice des pénalités de retards
    R=[data["jobs"][j]["daily_penalty"] for j in range(project_nb)]

    return(h,qualif_nb,staff_nb,project_nb,np.array(C),np.array(CA),np.array(N),np.array(G),np.array(D),np.array(R),names)