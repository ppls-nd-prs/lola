# LoLa
This repository contains the necessary code for the research *Beyond Translation: An Evaluatory Study of LogicLLaMA's Performance for Natural Language Inference*.

Dictionaries for evaluation can be obtained by running the notebook Dictionary-Creator (https://colab.research.google.com/drive/17aHKSSeDpQvHjzoGQdrKQVbO1sCNwjkX?usp=sharing) either directly or one can copy it to their own Google Drive to edit and customize for alternative datasets.

The dictionaries containing the direct translation from LogicLLaMA for this research can be found in the folder <code>dictionaries</code>.

It is possible to obtain dictionaries with the lexical modifications researched to boost performance. These can be created by running the code in <code>modify_dicts.ipynb</code>. Make sure the new dictionaries are saved in the <code>mod_dictionaries</code> folder. 

Now the evaluation of the LogicLLaMA translations can be performed by running
<code>python get_preds.py</code> with the proper arguments (see code for argument specification). Evaluation files will be created either in the <code>evaluations</code> or in the <code>mod_evaluations</code> folder, depending on whether a modified dictionary was used.

Finally, the confusion matrices for the evaluations can be computed by running <code>python get_conf_mats.py [filename]</code>.




