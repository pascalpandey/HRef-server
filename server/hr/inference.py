from build import vectorizer, model, reducer_1, reducer_2, cluster_model
from utils import full_parse, get_keywords
import pandas as pd


def process(applicant_path):
    keywords = get_keywords(applicant_path)[:5]
    new_applicant = full_parse(keywords, vectorizer)
    applicant_score = model.predict(new_applicant)
    
    applicant_red = reducer_1.transform(new_applicant)
    applicant_red = pd.DataFrame(applicant_red, columns=['PCA1', 'PCA2'])
    applicant_red = pd.concat([applicant_red, applicant_score], axis=1)

    applicant_red = reducer_2.transform(applicant_red)
    applicant_red = pd.DataFrame(applicant_red, columns=['x', 'y'])

    applicant_red['clusters'] = cluster_model.transform(applicant_red)
    applicant_red = pd.concat([applicant_red, applicant_score], axis=1)

    res={'x': applicant_red.iloc[0,0], 'y':applicant_red.loc[0,1], 
         'cluster':applicant_red.loc[0,2], 'score':applicant_red.loc[0,3],
         'keywords':keywords}

    return res