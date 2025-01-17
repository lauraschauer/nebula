import os
import sys
from pandas import to_datetime
from collections.abc import Iterable
from sklearn.metrics import roc_curve
import string
import torch
import random
import gc
import numpy as np
from torch import sigmoid

# supress UndefinedMetricWarning, which appears when a batch has only one class
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

def clear_cuda_cache():
    torch.cuda.empty_cache()
    gc.collect()


def get_tpr_at_fpr(true_labels, predicted_probs, fprNeeded):
        fpr, tpr, thresholds = roc_curve(true_labels, predicted_probs)
        if all(np.isnan(fpr)):
            return np.nan, np.nan
        else:
            tpr_at_fpr = tpr[fpr <= fprNeeded][-1]
            threshold_at_fpr = thresholds[fpr <= fprNeeded][-1]
            return tpr_at_fpr, threshold_at_fpr

def set_random_seed(seed_value):
    random.seed(seed_value) # Python
    np.random.seed(seed_value) # cpu vars
    torch.manual_seed(seed_value) # cpu  vars
    
    if torch.cuda.is_available(): 
        torch.cuda.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value) # gpu vars
        torch.backends.cudnn.deterministic = True  #needed
        torch.backends.cudnn.benchmark = False

def get_path(type="script"):
    idx = 1 if type == "notebook" else 0
    return os.path.dirname(os.path.realpath(sys.argv[idx]))

def get_alphanum_chars(s):
    return ''.join(filter(lambda x: x in string.ascii_letters + string.digits + string.punctuation, s))

def filterDictByKeys(dict, key_list):
    return {k: dict[k] for k in key_list if k in dict}

def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield 

def flattenList(l):
    return [item for sublist in l for item in sublist]

def dictToString(dictionary):
    return str(dictionary).replace(' ', '_').replace('\'', '').replace('{', '').replace('}', '').replace(':', '').replace(',', '').replace('[', '').replace(']', '')

def fix_random_seed(seed_value=1763):
    """Set seed for reproducibility."""
    import random
    import numpy as np
    import torch
    random.seed(seed_value)
    np.random.seed(seed_value)
    torch.manual_seed(seed_value)
    torch.cuda.manual_seed_all(seed_value)

def splitDataFrameTimeStampToChunks(df, timeFieldName='TimeStamp', chunkSize='5min'):
    df[timeFieldName] = to_datetime(df[timeFieldName])
    df[timeFieldName] = df[timeFieldName].dt.floor(chunkSize)
    return df

def isolationForestAnomalyDetctions(arr):
    from sklearn.ensemble import IsolationForest
    clf = IsolationForest(max_samples=100, random_state=42)
    clf.fit(arr)
    return clf.predict(arr)

def json_unnormalize(df, sep="."):
    """
    The opposite of json_normalize
    """
    result = []
    for _, row in df.iterrows():
        parsed_row = {}
        for col_label,v in row.items():
            keys = col_label.split(sep)

            current = parsed_row
            for i, k in enumerate(keys):
                if i==len(keys)-1:
                    current[k] = v
                else:
                    if k not in current.keys():
                        current[k] = {}
                    current = current[k]
        # save
        result.append(parsed_row)
    return result

def read_files_from_log(logfile=None, folder=".", pattern=".torch"):
    if logfile is None:
        logfile = [x for x in os.listdir(folder) if x.endswith(".log")][0]
    with open(logfile) as f:
        log = f.read()
    return [os.path.join(folder, "training_files", x.split(": ")[1]) for x in log.split("\n") if pattern in x]

def compute_score(model, x, verbose=True):
    logit = model(x)
    prob = sigmoid(logit)
    if verbose:
        print(f"\n[!!!] Probability of being malicious: {prob.item():.3f} | Logit: {logit.item():.3f}")
    return prob.item()
