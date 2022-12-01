# Project Nebula

<!-- scaled image from web -->
<center><img src="https://cdn.eso.org/images/screen/eso1205ec.jpg" width="400"></center>

## Modelling

- `modeling/language_model`: code for self-supervised learning from system logs
- `modeling/tradition_nlp`: code for traditional NLP modeling of bash process titles
- `modeling/tokenizer`: code for tokenizing bash process titles with sentencePiece

## To Be Done

### `auditd` commandLine dataset for dowstream tasks

- generate augmented reverse shells as malicious samples: (a) train -- one set of reverse shell binaries (b) val -- another binaries
- random split of unique legitimate commands to train/val
- A/B tests:
  - test with traditional pipeline and different tokenizers: (1) sentencePiece (2) wordPiece (3) wordPunct
  - (TF-IDF | HashingVectorizer) vs FastText
  
### Contextual embeddings

- adjust preprocessing:
  - remove artificial separator
  - include only the minimal set of fields
  - `fasttext`: any chance to use sentencePiece tokenizer instead of default one?

- `fasttext` intrinstic evaluation: `get_nearest_neighbors()` | `get_analogies()`  
  see: <https://fasttext.cc/docs/en/unsupervised-tutorial.html#nearest-neighbor-queries>

- downstream tasks for malicious classification
  - *Speakeasy reports*: define pipeline for emulation logs from Quo.Vadis
  - *Windows logs*:
    - using public repos with Windows telemetry:  
  (a) mordor (redirects here: <https://github.com/OTRF/Security-Datasets>)  
  (b) <https://github.com/sbousseaden/EVTX-ATTACK-SAMPLES>  
  (c) <https://github.com/NextronSystems/evtx-baseline>  
    - ask for `attackbot` data on windows?
  - *Linux logs*:
    - using logs from pentest machines?
    - simulate your own TTPs in validation environments?
      - automate it?

- `fasttext` A/B tests with default hyperparameters:
  - `fasttext` MAX_LINE_SIZE analysis?
    - is it a problem at all? if yes -- limit size:
      - chunk smaller windows -- 5 min vs 1 min
      - chunk the same window to multiple inputs
  - sequence of vectors (`get_word_vector()`) vs `get_sentence_vector()`
  - `fasttext` hyperparameter tests: epochs, dimension, ngrams, etc.
  - modeling -- embeddings:
    - with trainable from scratch, random initialization
    - pre-trained `fasttext` model, frozen (not updated)
    - pre-trained `fasttext` model, but updated during supervised phase
  - modeling -- model:
    - LSTM
    - attention: (1) tranformer (2) reformer
      > (a) use the same time for training, e.g. one day  
      > (b) plot mean epoch time with boxplots

## Done

- test speeds (DONE in `_auditd_b_preprocess.ipynb`)
  - ~~any ways to optimize pandas involvement?~~
    - ~~replace pandas whatsoever -- do plain `json` or `koalas`?~~
    - ~~what takes the most time -- loading? groupby?~~
- write pipeline for fastText training
  - check tokenization
    - ~~Will it be a problem that title after tokenization will screw number of tokens in single event?~~ YES
    - ~~Try with different column separator, e.g. `\s,` pr `\s,\s` (if `,` makes incorrect tokens)?~~  
      See `utils.contants.FIELD_SEPARATOR`, settled on `" , "`
  intrinstic evalution:
  - network events tokens are close by?
  - ~~anomaly detection on red team host~~ see `_auditd_c_fasttext.ipynb`
- ~~consider unification of pre-processing to represent same/similar data as Sysmon/Speakeasy/(what Win telemetry uses Vanquish)?~~  
  Sort of done -- removed all non-essential stuff, left only fields, that can be replicated in case of Sysmon. See `utils.contants.AUDITD_FIELDS`
- ~~check what telemetry we have on Windows machines~~  
  Standard structure, but unusual EventIDs...
