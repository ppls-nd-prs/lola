# LoLa
This repository contains the necessary code for the research *Beyond Translation: An Evaluatory Study of LogicLLaMA's Performance for Natural Language Inference*.

Dictionaries containing the FOL translation as predicted by the LogicLLaMA model can be obtained by running the notebook Dictionary-Creator (https://colab.research.google.com/drive/17aHKSSeDpQvHjzoGQdrKQVbO1sCNwjkX?usp=sharing). The notebook can be either run directly or one can copy it to their own Google Drive to edit and customize for alternative datasets. For backup purposes, Dictionary-Creator outputs small subsets of the full dictionary for the SICK and FraCaS datasets. These dictionaries can be merged by customizing and running the code in <code>merge_dictionaries.py</code>. <br>
The dictionaries containing the direct translation from LogicLLaMA for this research can be found in the folder <code>dictionaries</code>.

It is possible to obtain dictionaries with the lexical modifications researched to boost performance. These can be created by running the code in <code>modify_dicts.ipynb</code>. Make sure the new dictionaries are saved in the <code>mod_dictionaries</code> folder. <br>
The dictionaries containing the modified translations for this research can be found in the folder <code>mod_dictionaries</code>.

Now the evaluation of the LogicLLaMA translations can be performed by running
<code>get_preds.py</code> with the proper arguments (see code and below for argument specification). Evaluation files will be created either in the <code>evaluations</code> or in the <code>mod_evaluations</code> folder, depending on whether a modified dictionary was used. <br>
The evaluations for this research can be found in these folders as well.

Finally, the confusion matrices for the evaluations can be computed by running <code>get_conf_mats.py</code>. <br>
The confusion matrices for this research can be found in both evaluation folders and are marked with "[metrics]" at the end of the file name.  

### Specifics for various files
Here we specify how to run various files.
Depending on the file, you can pass the desired arguments when running the file, or you will need to edit the file itself. For files where you can pass various arguments, below we list all necessary arguments. To run them, fill in the <code>*arguments*</code> with your desired values. 

---
#### <code>merge_dictionaries.py</code>: <br>
Edit values of <code>directory</code> and <code>out_filename</code> in the file itself and run without arguments. 

---
#### <code>modify_dicts.ipynb</code>: <br>
Follow the examples in the notebook to create a new dictionary with your desired modifications. 

---

#### <code>get_preds.py</code>: <br>
Run in command line with: <code>python</code> <code>get_preds.py</code> <code>*Data-set*</code> <code>*modification-id*</code> <code>*lexical-knowledge*</code>

<code>*Data-set*</code>: name of any file in (a folder in) the <code>datasets</code> folder <br>
<code>*modification-id*</code>: see <code>README.md</code> in the <code>mod_dictionaries</code> folder. <br>
<code>*lexical-knowledge*</code>: use "True" if you want the prover to use lexical knowledge when making the predictions, otherwise use "False".

---

#### <code>get_conf_mats.py</code>: <br>
Run in command line with: <code>python</code> <code>get_conf_mats.py</code> <code>*File name*</code> 

<code>*File name*</code>: file path of any CSV evaluations file.

