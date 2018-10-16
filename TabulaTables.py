import tabula
import os
import pandas as pd

folder = 'C:/Users/Joe/Documents/GISRealEstateProject/CushmanWakefield_vacancy_cap_NOI/Atlanta/'
paths = [folder + fn for fn in os.listdir(folder) if fn.endswith('.pdf')]
for path in paths:
    df = tabula.read_pdf(path, encoding = 'utf-8', pages = 'all', area = [29.75,43.509,819.613,464.472], nospreadsheet = True)
    path = path.replace('pdf', 'csv')
    df.to_csv(path, index = False)

