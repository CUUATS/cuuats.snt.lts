# base classs of LTS
import pandas as pd
import numpy as np


def calculate_score(score, crits):
    if (not isinstance(score, pd.DataFrame)) and \
       (not isinstance(score, pd.Series)):
        raise TypeError(
            'df argument must be a pandas DataFrame of Series object')

    if isinstance(score, pd.DataFrame):
        assert len(crits) == 2
    elif isinstance(score, pd.Series):
        assert len(crits) == 1

    for crit in crits:
        score.index = crit[1]
        score = score.loc[crit[0]]
    assert isinstance(score, np.int64)
    return score
