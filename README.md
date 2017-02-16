# Text-Mining
Exploring a Text-Mining Approach as Rapid Prototyping Tool for Formative-Assessment Development in Problem-Based Learning Environments.

# How to Use extractDTM_computeCosineValues.py
## Note: requires NLTK, NUMPY, and SCIPY packages
## Note: extractDTM_computeCosineValues.py has been written in Python 2.7, it might not run in Python 3 versions

python extractDTM_computeCosineValues.py input_path, output_path, title

### Argument definition
'input_path' is a folder path with text documents (i.e., '.txt' files)

'output_path' is a folder path where csv files will be written with output matrices

'title' is a string with a label/identifier for the text documents (e.g., 'pre' or 'post')

### Output
extractDTM_computeCosineValues.py retrieves two matrices: (1) a document-term matrix of norm i,j where rows (i) are documents and columns (j) are terms, 
and (2) a pairwise cosine similarity values matrix of norm k (a symmetric matrix), where k is the number of text documents

# How to Use tm2.py
## Note: requires NLTK and NUMPY packages
## Note: tm2.py has been written in Python 2.7, it might not run in Python 3 versions. For Python 3 use tm2_3.py

python tm2.py 'input_folder' 'output_folder'

### Argument definition
'input_folder' is the folder path to the three folders called "pre", "during", and "post"

'output_folder' is the folder path where you want to save the csv files with the dtm matrices per each folder (i.e., pre, during, post)

### Output
tm2.py retrieves three document-term matrices for text documents inside "pre", "during", and "post" folders
