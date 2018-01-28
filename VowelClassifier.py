import json
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier, KDTree
from cgi import parse_qs, escape

def l2m(l):
    return np.array(l).reshape(1, -1)

def analyse_formants(f1, f2, f3, start_response):
    if f3 is None:
        f1 = float(f1); f2 = float(f2)
        newdata = l2m([f1, f2])
        result = two_formant_classifier.predict(newdata)[0]
        _, ind = two_formant_tree.query(newdata, k = 7)
        table = df.iloc[ind[0],np.isin(df.columns, ['lang', 'vowel', 'f1', 'f2', 'f3'])].to_dict()
        table['predicted_vowel'] = result
    else:
        f1 = float(f1); f2 = float(f2); f3 = float(f3)
        newdata = l2m([f1, f2, f3])
        result = three_formant_classifier.predict(newdata)[0]
        _, ind = three_formant_tree.query(newdata, k = 7)
        table = df.iloc[ind[0],np.isin(df.columns, ['lang', 'vowel', 'f1', 'f2', 'f3'])].to_dict()
        table['predicted_vowel'] = result
    response_body = (json.dumps(table)).encode()
    status = '200 OK'
    response_headers = [
    ('Content-Type', 'application/json'),
    ('Access-Control-Allow-Origin', '*'),
    ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body]

def app(environ, start_response):
    d = parse_qs(environ['QUERY_STRING'])
    if (not 'f1' in d) and (not 'f2' in d):
        response_body = ('First two formants not specified').encode()
        status = '400 BAD REQUEST'
        response_headers = [
        ('Content-Type', 'text/html'),
        ('Access-Control-Allow-Origin', '*'),
        ('Content-Length', str(len(response_body)))
        ]
        start_response(status, response_headers)
        return [response_body]
    if 'f3' in d:
        return analyse_formants(d['f1'][0], d['f2'][0], d['f3'][0], start_response)
    else:
        return analyse_formants(d['f1'][0], d['f2'][0], None, start_response)

df = pd.read_csv('becker_train_data.csv', sep = '\t')
d = df
for colname in ['f1', 'f2', 'f3']:
    # Filling the NAs with average values for the same vowel
    d[colname].fillna(d.groupby('vowel')[colname].transform('mean'), inplace=True)

two_formant_tree = KDTree(d[['f1', 'f2']])
two_formant_classifier = KNeighborsClassifier(7)
two_formant_classifier.fit(X = d[['f1', 'f2']], y = d['vowel'])

three_formant_tree = KDTree(d[['f1', 'f2', 'f3']])
three_formant_classifier = KNeighborsClassifier(7)
three_formant_classifier.fit(X = d[['f1', 'f2', 'f3']], y = d['vowel'])