import csv
import re
import pandas as pd

def chunks(arr, size):
	while arr:
		yield arr[:size]
		arr = arr[size:]

inp = open('BeckerVowelCorpus.csv', 'r', encoding = 'utf-8')
r = csv.reader(inp, delimiter = '\t')
header = next(r)
print(list(enumerate(header)))

columns = ['iso', 'lang', 'dialect', 'genetics', 'vowel',
		   'f1', 'f2', 'f3']
df_dic = { colname: [] for colname in columns }

for row in r:
	for c in chunks(row[13:97], 6):
		if len(c) < 6:
			continue
		if c[0]:
			f1 = c[2] if re.match(r'\d+', c[2]) else ''
			f2 = c[3] if re.match(r'\d+', c[3]) else ''
			f3 = c[4] if re.match(r'\d+', c[4]) else ''
			for k, v in [
				('iso', row[0]),
				('lang', row[1]),
				('dialect', row[2]),
				('genetics', row[3]),
				('vowel', c[0]),
				('f1', f1),
				('f2', f2),
				('f3', f3)
			]:
				df_dic[k].append(v)
	
formant_df = pd.DataFrame(df_dic)
formant_df = formant_df[columns]
formant_df.to_csv('becker_corpus.tsv', sep = '\t', index = False)