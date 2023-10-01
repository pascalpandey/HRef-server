from hr.build import vectorizer, model, reducer_1, reducer_2, cluster_model
from hr.utils import full_parse, get_keywords
import pandas as pd
import os

def process(applicant_path):
    res =[]

    for dir in os.listdir(applicant_path):
        print(f"Doing dir {len(res)+1}")
        keywords = get_keywords(applicant_path+'/'+dir)[:5]
        new_applicant = full_parse(keywords, vectorizer)
        print("predicting")
        print(new_applicant)
        applicant_score = model.predict(new_applicant)
        applicant_score = pd.DataFrame(applicant_score, columns=['average'])

        applicant_red = reducer_1.transform(new_applicant)
        applicant_red = pd.DataFrame(applicant_red, columns=['PCA1', 'PCA2'])
        applicant_red = pd.concat([applicant_red, applicant_score], axis=1)

        applicant_red = reducer_2.transform(applicant_red)
        applicant_red = pd.DataFrame(applicant_red, columns=['x', 'y'])

        applicant_red['clusters'] = cluster_model.predict(applicant_red)
        applicant_red = pd.concat([applicant_red, applicant_score], axis=1)

        applicant={'x': applicant_red.iloc[0,0], 'y':applicant_red.iloc[0,1], 
            'color':applicant_red.iloc[0,2], 'score':applicant_red.iloc[0,3],
            'keywords':keywords}

        res.append(applicant)
      

    return res