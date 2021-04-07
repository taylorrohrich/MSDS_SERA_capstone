# =============================================================================
# File: DocSim_class.py
# Author: Ashley, David, Kip, Latifa
# Functions:
#   init: (defining the class object)
#       input: dataframe: data,
#              string: text, name of the column in data that contains text as a single string
#       Additional features:
#           factors: defined in preprocessing function. Retreived in getFeatureName function
#           vectorized_documents: defined in preprocessing function. Retreived in getFeatureName function
#           similarity_scores: defined in doc_sim function. Retreived in getSimalarityScore function
#   preprocessing:
#       input: optional boolean parameters: remove_stopwords, stem, tfidf, LSA. Default False
#              optional list of additional stopwords: filler_words. Default empty list
#              optional int number of LSA topics: lsa_n_components. Default 2
#       output: Returns a dataframe with an additional column "cleaned_vectorized_document"
#           that contains the preprocessed and vectorized documents.
#       Note: Preprocessing does not change the dataframe used in defining the class.
#               It returns a copy of the preprocessed dataframe and saves the list of words
#               corresponding to the word vectors to the object.
#   get_feature_names:
#       input: None
#       output: Returns the list of words that corresponds to the numeric vectors
#   get_preprocessed_text:
#       input: None
#       output: Returns the series 'clean_processed_text'.
# ============================================================================= 
#%%
# Standard Library Modules
import os
import re
import string
import datetime

#Related 3rd Party Modules
import nltk
# nltk.download('wordnet')
# nltk.download('stopwords')
# nltk.data.path.append('/app')
import pandas
import numpy
import scipy
import string
#nltk.data.path = os.getcwd()
#sklearn does not automatically import its subpackages
import sklearn
import sklearn.metrics
import sklearn.decomposition
import sklearn.feature_extraction
#%%
# DocSim Class
class DocSim: #defining the class
    """
    Parameters
    ----------
    data : dataframe
        Dataframe where one column contains the text from the documents.
    skill : String
        Specify the name of the column that contains the skill information.
    study : String
        Specify the name of the column that contains the study information.
    doc_type : String
        Specify the name of the column that contains the document type.
        e.g. "script" or "transcript"
    text : String
        Specify the name of the column that contains the document text.
    """

    def __init__(self, data, skill, study, doc_type, doc_id, text):

        # Initialize the attributes
        self.data = data
        self.doc_id = doc_id
        self.skill = skill
        self.study = study
        self.doc_type = doc_type
        self.text = text


        # The column of preprocessed numeric vectors 
        self.vectorized_documents = "Apply function 'preprocessing' before \
                'get_preprocessed_text' to get the column 'clean_vectorized_document'" 
            
        # The word vector corresponding to the numeric vector 
        self.tfidf_factors = "Apply function 'preprocessing' before \
                'get_tfidf_feature_names' to get the feature names associated \
                with the numeric vectors in 'clean_vectorized_document'"
        
        self.lsa_factors = "Apply function 'preprocessing' before \
                'get_lsa_feature_names' to get the feature names associated \
                with the numeric vectors in 'clean_vectorized_document'"
        
        # Check if column name specified is correct
        if self.text not in self.data.columns:
            raise SystemExit(f"Incorrect 'text' used. \
                Cannot find {self.text} in data")

        if self.skill not in self.data.columns:
            raise SystemExit(f"Incorrect 'skill' used. \
                Cannot find {self.skill} in data")

        if self.study not in self.data.columns:
            raise SystemExit(f"Incorrect 'study' used. \
                Cannot find {self.study} in data")
        
        if self.doc_type not in self.data.columns:
            raise SystemExit(f"Incorrect 'doc_type' used. \
                Cannot find {self.doc_type} in data")
    
    # clean and convert text to numeric vector
    def preprocessing(self,
                      remove_stopwords = False, 
                      filler_words = [], 
                      stem = False,
                      lemm = False, 
                      tfidf = False, 
                      tfidf_level = 'skill', 
                      lsa = False, 
                      lsa_n_components = 2,
                      ngram = 1):
        """
        Parameters
        ----------
        remove_stopwords : Boolean, optional
            Remove stopwords and punctuation from the Natural Language Toolkit's
            (NLTK) pre-specified list. The default is False.
        filler_words : List of strings, optional
            Specify any additional stop words to be removed. The default is [].
        stem : Boolean, optional
            Replace all word derivatives with a single stem. The default is False.
        tfidf : Boolean, optional
            Weight each word frequency using term frequency–inverse document 
            frequency (tf-idf) weighting. The default is False.
        tfidf_level: string, ['full', 'study', 'skill', 'document']
            Specify the level of hierarchy to apply tf-idf
        lsa : Boolean, optional
            Apply the dimentionality reduction technique Latent Semantic 
            Analysis (LSA). 
            The default is False.
        lsa_n_components : Int, optional
            The number of topics in the output data. The default is 2.
        Returns
        -------
        df : Dataframe
            A copy data with an additional column containing the preprocessed 
            and vectorized documents.
                
        Package Dependencies
        ------
        nltk
        string
        sklearn
        """

        # Make a copy of the data
        df = self.data.copy()
            
        # Isolate text column as lowercase
        text = self.data[self.text].str.lower()
    
        # Define a set of stopwords
        if remove_stopwords:
            filler_words = set(nltk.corpus.stopwords.words('english')).\
                union(set(string.punctuation), set(filler_words))
        
        # Define stopwords as None 
        else:
            filler_words = None

        # Stem and remove stopwords that are in filler_words
        if stem:
            if filler_words == None:
                filler_words = [filler_words]
            # Tokenize
            text = text.apply(lambda x: nltk.tokenize.casual.casual_tokenize(x)) 
            
            # Remove stopwords and stem
            text = text.apply(lambda x: [nltk.stem.SnowballStemmer('english').\
                                        stem(item) for item in x \
                                        if item not in filler_words])
            
            # Combine
            text = text.apply(lambda x: ' '.join([item for item in x]))
            
            # Prevent removing stop words twice
            filler_words = None
        
        # Lemmantize and remove stopwords that are in filler_words
        elif lemm:
            
            if filler_words == None:
                filler_words = [filler_words]
            
            # Set up the lemmatizer
            wnl = nltk.stem.WordNetLemmatizer()
            text = text.apply(lambda x: nltk.tokenize.casual.casual_tokenize(x)) 

            # remove stopwords and lemmatize
            text = text.apply(lambda x: [wnl.lemmatize(item) for item in x \
                                        if item not in filler_words])

            text = text.apply(lambda x: ' '.join([item for item in x]))
            
            # Prevent removing stop words twice
            filler_words = None 

        # Vectorize the text: using tf-idf weights 
        if tfidf:
            
            # Handle different level of TF-IDF
            if tfidf_level == 'full':
                # Tfidf Vectorizer
                vectorizer = sklearn.feature_extraction.text.\
                    TfidfVectorizer(lowercase = True, stop_words = filler_words)
                vectors = vectorizer.fit_transform(text.tolist())
                
                # Save feature names
                self.tfidf_factors = [('full', vectorizer.get_feature_names())]
            
            # TF-IDF at the Skill Level
            elif tfidf_level == 'skill':
                df = df.sort_values(self.skill)
                vectors = self.tfidf_preprocessing(level = self.skill, 
                                                   filler_words = filler_words,
                                                   text = text)
            # TF-IDF at the Study Level
            elif tfidf_level == 'study':                
                df = df.sort_values(self.study)
                vectors = self.tfidf_preprocessing(level = self.study, 
                                                   filler_words = filler_words,
                                                   text = text)
            # TF-IDF at the Document Level
            elif tfidf_level == 'document':                
                df = df.sort_values(self.doc_id)
                vectors = self.tfidf_preprocessing(level = self.doc_id, 
                                                   filler_words = filler_words,
                                                   text = text)
        
        # If tf-idf is not enabled, vectorize the text using word counts
        else:
            # Count vectorize
            vectorizer = sklearn.feature_extraction.text.\
                    CountVectorizer(lowercase = True, stop_words = filler_words)
            vectors = vectorizer.fit_transform(text.tolist())
            
            # Save feature names
            self.tfidf_factors = [('full', vectorizer.get_feature_names())]
        
        # Apply LSA using the vectorized text
        if lsa:
            # Check if the number of LSA components is >= the number of features
            if lsa_n_components >= min([len(self.tfidf_factors[x][1]) \
                                        for x in range(0, len(self.tfidf_factors))]):
               
                raise SystemExit("lsa_n_components is too large for this set of documents.\
                                  lsa_n_components must be less than " + 
                                  str(min([len(self.tfidf_factors[x][1]) 
                                      for x in range(0, len(self.tfidf_factors))])))
            
            # Rename the vectors
            vectorized_text = vectors
            
            # Define the LSA function
            lsa_function = sklearn.decomposition.TruncatedSVD( \
                n_components = lsa_n_components, random_state = 100)
            
            # Convert text to vectors
            vectors = lsa_function.fit_transform(vectorized_text).tolist()
            
            # Define list of topic numbers
            self.lsa_factors = ['topic ' + str(i) for i in range(1, lsa_n_components + 1)]
            
            # Save the vectorized documents to the class
            self.vectorized_documents = vectors
            df["cleaned_vectorized_document"] = vectors
            
            return df
        
        # Append preprocessed text to the dataframe and return  
        denselist = vectors.todense().tolist()

        # # Save the vectorized documents to the class
        self.vectorized_documents = denselist
        df["cleaned_vectorized_document"] = denselist

        return df

    def tfidf_preprocessing(self, level, text, filler_words):
        """
        Apply TF-IDF at different level of hierarchy
        
        Parameters
        ----------
        level: string
            Column name of the level of hierarchy in self.data
        text: Pandas Series 
            A Pandas series of raw text for each document
        filler_words: list
            A list of filler words to be removed from TF-IDF process
        """
        # Get all unique words for mapping
        vectorizer = sklearn.feature_extraction.text.\
                CountVectorizer(lowercase = True, stop_words = filler_words)
        vectors = vectorizer.fit_transform(text.tolist())
        
        # Save feature names as a dictionary of Data Frame
        unique_words = vectorizer.get_feature_names()
        df_all = pandas.DataFrame(index = unique_words)

        # Write the text back to self.data and sort by skill
        #   so that the ordering is correct
        self.data = self.data.sort_values(level)
        self.data[self.text] = text

        # Create empty list to store results
        vectors = list()
        self.tfidf_factors = list()

        for index in self.data[level].unique():                  

            # Extract the raw text for this study group
            tmp_text = self.data.loc[
                self.data[level] == index, [self.doc_id, self.text]]

            # Train and Fit TF-IDF 
            vectorizer = sklearn.feature_extraction.text.\
                TfidfVectorizer(lowercase = True, 
                                stop_words = filler_words)
            tmp_vectors = vectorizer.fit_transform(
                tmp_text[self.text].tolist())

            # Get the TF-IDF weights and feature names
            tmp_weights = tmp_vectors.todense().tolist()
            tmp_factors = vectorizer.get_feature_names()

            # Store weights as a data frame
            df_tmp = pandas.DataFrame(numpy.transpose(tmp_weights), 
                                      index = tmp_factors)
            
            # Match with all unique words for identical structure
            vectors += df_all \
                        .join(df_tmp, how = "left") \
                        .fillna(0) \
                        .to_numpy() \
                        .T \
                        .tolist()

            # Store features
            self.tfidf_factors += [(index, tmp_factors)]

        # Convert vectors back to sparse matrix
        return scipy.sparse.csr_matrix(vectors)

    # Get the series containing the vectorized documents
    def get_preprocessed_text(self):
        """
        Get the series containing the vectorized documents
        """
        return self.vectorized_documents
    
    # Get the features names for the numeric vector
    def get_tfidf_feature_names(self):
        """
        Get the features names for the tfidf feature names
        """
        return self.tfidf_factors

    def get_lsa_feature_names(self):
        """
        Get the features names for the lsa feature names
        """
        return self.lsa_factors

    def get_skill(self):
        """
        Get the series containing the unique skills
        """
        return self.data[self.skill].unique()

    def get_doc_type(self):
        """
        Get the series containing the unique document type
        """
        return self.data[self.doc_type].unique()
    
    def get_study(self, skill_id = []):
        """
        Get the series containing the unique study information by skill
        
        Parameters
        ----------
        skill_id: list
            Put in the skill id that you want to look at.
        """
        if len(skill_id) == 0:
            skill_id = self.get_skill()

        return self.data[self.data[self.skill] \
                  .isin(skill_id)][self.study].unique()

    def check_preprocessing_input(self,
                                  remove_stopwords, 
                                  filler_words, 
                                  stem, 
                                  lemm,
                                  tfidf, 
                                  tfidf_level,
                                  lsa, 
                                  lsa_n_components,
                                  ngram):

        # Check if the method is coded correctly
        # if method not in ('cosine'):
        #    raise SystemExit("Incorrect 'method' used. Use 'cosine'")
        
        # Check preprocessing settings: 
        if remove_stopwords not in (True, False):
            raise SystemExit("Incorrect 'remove_stopwords' used. \
                Use True or False")
        if stem not in (True, False):
            raise SystemExit("Incorrect 'stem' used. Use True or False")
        if lemm not in (True, False):
            raise SystemExit("Incorrect 'lemm' used. Use True or False")
        if stem and lemm:
            raise SystemExit("Stemmed text may not also be lemmatized.")
        if tfidf not in (True, False):
            raise SystemExit("Incorrect 'tfidf' used. Use True or False")
        if tfidf_level not in ('full', 'skill', 'study', 'document'):
            raise SystemExit("Incorrect 'tfidf_level' used. Use \
                'full', 'skill', 'study' or 'document'. ")
        if lsa not in (True, False):
            raise SystemExit("Incorrect 'lsa' used. Use True or False")
        if type(lsa_n_components) is not int:
            raise SystemExit("Incorrect 'LSA_n_components' used. \
                LSA_n_components must be an integer")
        elif lsa_n_components < 2:
            raise SystemExit("Incorrect 'LSA_n_components' used. \
                Set LSA_n_components as an int that is greater than or equal to 2")

    def create_sparse_matrix(self, data, col = 'cleaned_vectorized_document'):
        """
        Convert the vectorized column to a sparse matrix
           A sparse matrix is a matrix that majority of the elements are zero.
           To save memory space and tos increase computational efficiency, we 
           convert the vectorized column to a sparse matrix to improve the 
           performance.
          
        `cleaned_vectorized_document` is the column generated by the 
           preprocessing() function above. It is the reserved column name that
           specifies the output of preprocessing.
        
        Parameter 
        ----------
        data: Data Frame 
            Data Frame object that contains the column of the vectorized text
        col: String
            Column name of the column that contains vectorized text
        """
        return scipy.sparse.csr_matrix([i for i in data[col]])

    # Scenario #1: Normal 
    def normal_comparison(self, 
                          method = 'cosine', 
                          remove_stopwords = False, 
                          filler_words = [], 
                          stem = False, 
                          lemm = False,
                          tfidf = False, 
                          tfidf_level = 'skill', 
                          lsa = False, 
                          lsa_n_components = 2,
                          ngram = 1):
        
        """
        Get the cosine similarity between each transcripts to the benchmark
            script for each skills
        """

        # Check Input Value                  
        self.check_preprocessing_input(remove_stopwords = remove_stopwords, 
                                       filler_words = filler_words,
                                       stem = stem, 
                                       lemm = lemm,
                                       tfidf = tfidf,
                                       tfidf_level = tfidf_level, 
                                       lsa = lsa,
                                       lsa_n_components = lsa_n_components,
                                       ngram = ngram)

        # NLP Preprocessing: 
        self.document_matrix = self.preprocessing(remove_stopwords = remove_stopwords, 
                                                  filler_words = filler_words,
                                                  stem = stem, 
                                                  lemm = lemm,
                                                  tfidf = tfidf,
                                                  tfidf_level = tfidf_level, 
                                                  lsa = lsa,
                                                  lsa_n_components = lsa_n_components,
                                                  ngram = ngram)
        # Sufficiency Check
        if self.document_matrix.empty:
            raise SystemExit("Insufficient data to process.")      
        
        # Collect the transcripts and sort by skill
        transcript = self.document_matrix.\
            loc[self.document_matrix[self.doc_type] == 'transcript'].\
            sort_values(self.skill)

        # Calculate the Similarity Score
        if method == 'cosine':

            # Create an empty list to store the similarity scores
            similarity_score = numpy.array([])

            # iterate over different skills
            for skills in self.get_skill():
                
                # Extract the script for this skill
                tmp_script = self.document_matrix.\
                    loc[(self.document_matrix[self.doc_type] == 'script') & \
                        (self.document_matrix[self.skill] == skills)]
                
                # Extract the transcript for this skill
                tmp_transcript = transcript.\
                    loc[self.document_matrix[self.skill] == skills]

                # Calculate the similarity score and store it
                similarity_score = numpy.concatenate([similarity_score,  
                    sklearn.metrics.pairwise.\
                    cosine_similarity(self.create_sparse_matrix(tmp_script),
                                      self.create_sparse_matrix(tmp_transcript),
                                      dense_output = True). \
                    reshape(1, -1)[0]])

            # Write the similarity score back to the orignial DF
            transcript['similarity_score'] = \
                similarity_score.reshape(-1, 1) #.round(6)

            # Return the output data frame
            return(transcript)


    # Scenario #2: Pairwise 
    def pairwise_comparison(self, 
                            method = 'cosine', 
                            remove_stopwords = False, 
                            filler_words = [], 
                            stem = False, 
                            lemm = False,
                            tfidf = False, 
                            tfidf_level = 'skill',
                            lsa = False, 
                            lsa_n_components = 2,
                            ngram = 1):
        """
        Get the cosine similarity among each transcripts within skills
        """
        # Check Input Value                  
        self.check_preprocessing_input(remove_stopwords = remove_stopwords, 
                                       filler_words = filler_words,
                                       stem = stem, 
                                       lemm = lemm,
                                       tfidf = tfidf,
                                       tfidf_level = tfidf_level, 
                                       lsa = lsa,
                                       lsa_n_components = lsa_n_components,
                                       ngram = ngram)

        # NLP Preprocessing: 
        self.document_matrix = self.preprocessing(remove_stopwords = remove_stopwords, 
                                                  filler_words = filler_words,
                                                  stem = stem, 
                                                  lemm = lemm,
                                                  tfidf = tfidf,
                                                  tfidf_level = tfidf_level, 
                                                  lsa = lsa,
                                                  lsa_n_components = lsa_n_components,
                                                  ngram = ngram)
        # Sufficiency Check
        if self.document_matrix.empty:
            raise SystemExit("Insufficient data to process.")      
        
        # Collect the transcripts and sort by skill
        transcript = self.document_matrix.\
            loc[self.document_matrix[self.doc_type] == 'transcript'].\
            sort_values(self.skill)

        # Calculate the Similarity Score
        if method == 'cosine':

            # Create an empty list to store the similarity scores
            similarity_score = numpy.array([])   

            # iterate over different skills
            for skills in self.get_skill():
                
                # Extract the transcript for this skill
                tmp_transcript = transcript.\
                    loc[self.document_matrix[self.skill] == skills]

                # Calculate the similarity score and store it
                # Steps: 
                # 1. Calculate the pairwise similarity
                # 2. Apply the average function along the axis 0
                # 3. Store the values within similarity_score array
                similarity_score = numpy.concatenate([similarity_score,  
                    numpy.apply_along_axis(lambda x: (sum(x) - 1) / (len(x) - 1), 
                    0, sklearn.metrics.pairwise.cosine_similarity(
                        X = self.create_sparse_matrix(tmp_transcript),
                        dense_output = True))])

            # Write the similarity score back to the orignial DF
            transcript['similarity_score'] = \
                similarity_score.reshape(-1, 1) #.round(6)
            
            # Return the output data frame
            return(transcript)

    # Scenario 3
    def within_study_normal_average(self, 
                                    method = 'cosine', 
                                    remove_stopwords = False, 
                                    filler_words = [], 
                                    stem = False, 
                                    lemm = False,
                                    tfidf = False, 
                                    tfidf_level = 'skill',
                                    lsa = False, 
                                    lsa_n_components = 2,
                                    ngram = 1):
        """
        Get the average similarity score for each study 
        """

        output = self.normal_comparison(method = method, 
                                        remove_stopwords = remove_stopwords, 
                                        filler_words = filler_words, 
                                        stem = stem, 
                                        lemm = lemm,
                                        tfidf = tfidf, 
                                        tfidf_level = tfidf_level, 
                                        lsa = lsa, 
                                        lsa_n_components = lsa_n_components,
                                        ngram = ngram)

        return output[[self.study, 'similarity_score']].\
               groupby([self.study]).\
               mean().\
               reset_index()


    # Scenario 4
    def across_study_normal_average(self, 
                                    method = 'cosine', 
                                    remove_stopwords = False, 
                                    filler_words = [], 
                                    stem = False, 
                                    lemm = False,
                                    tfidf = False, 
                                    tfidf_level = 'skill',
                                    lsa = False, 
                                    lsa_n_components = 2,
                                    ngram = 1):
        """
        Get the average similarity score for each study 
        """
        # Check Input Value                  
        self.check_preprocessing_input(remove_stopwords = remove_stopwords, 
                                       filler_words = filler_words,
                                       stem = stem, 
                                       lemm = lemm,
                                       tfidf = tfidf,
                                       tfidf_level = tfidf_level, 
                                       lsa = lsa,
                                       lsa_n_components = lsa_n_components,
                                       ngram = ngram)

        # NLP Preprocessing: 
        self.document_matrix = self.preprocessing(remove_stopwords = remove_stopwords, 
                                                  filler_words = filler_words,
                                                  stem = stem, 
                                                  lemm = lemm,
                                                  tfidf = tfidf,
                                                  tfidf_level = tfidf_level, 
                                                  lsa = lsa,
                                                  lsa_n_components = lsa_n_components,
                                                  ngram = ngram)
        
        # Remove non-transcripts, sort by skill, study
        tmp_data = self.document_matrix.copy().\
            loc[self.document_matrix[self.doc_type] == 'transcript'].\
            sort_values([self.skill, self.study])

        # Create an empty list to store the similarity scores
        similarity_score = list()

        # iterate over different skills
        for skills in self.get_skill():

            # Within each skill, iterate over different study
            for studies in self.get_study(skill_id = [skills]):
                
                # doc_type = 'script' will have nan for study
                if pandas.isnull(studies):
                    pass
                else: 
                    # tmp_script will be the study we want to compare
                    tmp_script = tmp_data.\
                        loc[(tmp_data[self.skill] == skills) & 
                            (tmp_data[self.study] == studies)]. \
                        reset_index()

                    # tmp_transcript will be all other studies within the skill
                    tmp_transcript = tmp_data.\
                        loc[(tmp_data[self.skill] == skills) & 
                            (tmp_data[self.study] != studies)].\
                        reset_index() 
                    
                    # Iterate over each transcripts
                    for index, _ in tmp_script.iterrows():
                        similarity_score += [sklearn.metrics.pairwise.cosine_similarity(
                                self.create_sparse_matrix(tmp_script.iloc[index,]),
                                self.create_sparse_matrix(tmp_transcript),
                                dense_output = True).mean()] # Average of all tmp_transcripts

        # Write the similarity score back to the orignial DF
        tmp_data['similarity_score'] = numpy.asarray(similarity_score).\
            reshape(-1, 1) #.round(6)

        # Return the output data frame
        return(tmp_data)
    
class PreprocessCorpusText:
    """
    Parameters
    ----------
    source_dir : String
        Maybe either:
            Directory address containing .txt files of corpus documents.
        Or:
            Dataframe where each row contains the text of a corpus document.
    """
    def collect_directory(self, source_dir, recursive=False):
        """
        Extract each line of each file in a directory [source_dir] 
            of text documents. Return a single dataframe of 
            labeled lines from documents.
            """

        # columns of final DF output
        dfcolumns=['doc_id', 'source_dir', 'subdir', 'filename', \
                "collected", "rtlen", "rawtext"]
        collect_df = pandas.DataFrame()
        # if seeking recursive search, look in all subfolders as default
        # otherwise, return first result of os.walk(), i.e. base folder only 
        src_dir = os.walk(source_dir)
        if not recursive:
            src_dir = next(src_dir)

        # enumerate all files in given directory
        f = [os.path.join(root, name) \
                for root, _, files in os.walk(source_dir) \
                for name in files if ".txt" in name]
        print(f)
        if not f:
            raise SystemExit("The target directory must contain .txt files.")

        # for each text file identified, extract text lines
        for i, file in enumerate(f):
            #open source file
            # sometimes problems with utf-8 or latin-1 encodings, 
            # cp1252 appeared to work consistently
            with open(file, encoding="cp1252") as f:
                #remove all non-ascii characters by encoding ascii 
                # then decode again
                # strip lines of extra whitespace
                lines = [line.encode("ascii", "ignore")\
                    .decode().rstrip('\n') for line in f]
            # create dataframe of lines to modify
            df = pandas.DataFrame(lines,columns=["rawtext"])
            # strip any remaining extremity whitespace
            df['rawtext'] = df['rawtext'].str.strip()
            # add line length
            df['rtlen'] = df.rawtext.str.len()
            # remove any zero length or NA lines
            df = df[df.rtlen > 0]
            df = df.dropna()

            # add incrementing ID per file
            df['doc_id'] = i
            #fs = file.split("\\")[-3:]
            splitpath = list(os.path.split(file))
            splitpath[0] = splitpath[0].replace(source_dir, "")
            splitpath = [source_dir] + splitpath
            df[['source_dir', 'subdir', 'filename']] = splitpath
            #df['dir_path'], df['filename']
            df['collected'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df = df[dfcolumns]
            #df['dir_path'] = 
            # df = df.assign(**{'parentdir1':fs[0], 
            #         'parentdir2':fs[1], 
            #         'filename':fs[2]})
                    
            collect_df = collect_df.append(df)
        
        collect_df['line_id'] = collect_df.index
        #print(collect_df)
        return collect_df

    def explode_lines(self, col_name):
        """
        Given a column named [col_name] containing line breaks, 
        explode the dataset so that every single line is a separate row. 
        returns new instance of the class object
        """
        if col_name not in self.df.columns:
            raise SystemExit("Input [col_name] must be a column in this dataset.")

        # remove unhelpful \r character
        obj = self.copy()
        obj.df = obj.df.replace("\r", "")
        #  separate multi-line text to individual rows
        obj.df[col_name] = obj.df[col_name].str.split("\n")
        obj.df = obj.df.explode(col_name)
        # clean up any resulting empty rows 
        obj.df = obj.df.dropna(subset=[col_name])
        return obj

    def copy(self):
        """ 
        create a new instance of PreprocessCorpusText,
        with the same data as this instance
        """
        return PreprocessCorpusText(self.df, text=self.curr_txt)

    def __init__(self, data_source, recursive=False, text=None): #, directory=None, document_dataframe=None

        validentry = "Some data source must be added, either a directory of txt files, or an existing Pandas dataframe of documents."
        if isinstance(data_source, pandas.DataFrame):
            if not text:
                raise SystemExit("This class requires input dataframes to" + \
                    " specify the column containing document" + \
                    " text with [text].")
            self.df = data_source.copy()
            cols_check = {'doc_id': self.df.index,
                'source_dir': pandas.NA,
                'subdir': pandas.NA,
                'filename': pandas.NA,
                'collected': datetime.datetime.now()\
                    .strftime('%Y-%m-%d %H:%M:%S'),
                'rawtext': self.df[text]
                }
            checkcols = self.df.columns
            for cc in cols_check.keys():
                if cc not in checkcols:
                    self.df[cc] = cols_check[cc]
            self.curr_txt = text
            self.data_sources = "dataframe"
        elif os.path.isdir(str(data_source)):
            self.data_sources = data_source
            self.df = self.collect_directory(data_source, recursive)
            self.curr_txt = "rawtext"
        else:
            raise SystemExit(validentry)

        self.__name__ = "PreprocessCorpusText"

    def group_by_speaker(self, speaker):
        """
        Returns dataframe where text has been joined by speaker.
        Accepts source [dataframe], 
        and column names for speaker [speaker],
        text to be concatenated [text], 
        and ID to identify each unique document [doc_id].
        returns new instance of the class object
        """

        obj = self.copy()

        stablecols = ["doc_id", "source_dir", "subdir", \
            "filename", "collected", speaker]

        #select columns not abstractable to documents, remove duplicates
        limdf = self.df.copy()
        limdf = limdf[["doc_id", "period", 
                    "filename", "collected"]].drop_duplicates()

        errmsg = "[speaker] must all be a column name in the given dataset"
        if not isinstance(speaker, str) or \
            speaker not in obj.df.columns: 
            raise SystemExit(errmsg)
        if not isinstance(obj.df, pandas.DataFrame):
            raise SystemExit(errmsg)
        print(obj.curr_txt)
        # concatenate text by speaker
        speak_red = obj.df.groupby([speaker, "doc_id"])\
            [obj.curr_txt].apply(' '.join).reset_index()

        obj.df = pandas.merge(limdf, speak_red, \
            how="inner", on="doc_id")

        print("Speaker names extracted")
        return obj
        
    def extr(self, x, pattern, mult):
        """
        Function for Pandas Apply vectorizing. 
        Extract from src text [x] to add to a separate column 
        if any match of the given regex [pattern]. 
        If [mult]=True then extract multiple regex pattern group matches.
        """
        if not x or x is numpy.nan:
            return numpy.nan
        out = re.findall(pattern, x)
        if not out: #exit if no matches at all
            return numpy.nan
        if type(out[0]) == tuple:
            out = [x.strip() for x in list(out[0]) if x]
        elif len(out) > 1:
            out = [x.strip() for x in out if x]
        if not out: #exit if matches are all empty
            return numpy.nan
        if type(out) == list and not mult:
            out = out[0]
        return out

    def add_col_from_extract(self, df1, colfrom, newcolname, regex, \
            mult=False, from_prev_row=False):
        """
        Return the original given dataframe [df1] with a 
        new column [newcolname] created from matches returned from 
        the given regex pattern [regex] applied to a src column [colfrom]. 
        If [mult]=True, returns list of all matches, not just first.
        If from_prev_row, returns [regex] match from previous instead of 
        current row.
        returns new instance of the class object
        """

        # obj = self.copy()
        # df1 = obj.df
        # colfrom = self.curr_txt
        # create empty column
        df1[newcolname] = numpy.nan

        # if shifting, use shift function inside where equals [shift_equals]
        if from_prev_row:
            df1['prevrow'] = df1[colfrom].shift(1, axis = 0)
            df1[newcolname] = df1.apply( \
                lambda x: self.extr(x['prevrow'], regex, mult), axis=1)
            # df1[newcolname] = numpy.where( \
            #     df1[colfrom].shift(1, axis = 0) == regex,
            #     df1[colfrom], numpy.nan)
            # remove extracted text from src column
            df1[colfrom] = numpy.where(~df1[newcolname].isnull(), "",df1[colfrom])
            df1 = df1.drop(columns=["prevrow"])
        else:
        # otherwise, add regex match to new column
            df1[newcolname] = df1[colfrom].apply( \
                lambda x: self.extr(x, regex, mult))
            # remove extracted text from src column
            df1[colfrom] = df1[colfrom].apply(lambda x: \
                re.sub(regex, "", x).strip())

        # clean up beginning/end of reduced src column
        df1[colfrom] = df1[colfrom].str.lstrip(": ").str.strip()
        df1[colfrom] = df1[colfrom].str.lstrip("-")
        # return output 
        print(f"{newcolname} extracted into a new column")
        return df1

    def addumn(self, colname, contents):
        """
        Add a new column to the dataset, named [colname],
        and the values should be [contents].
        If [contents] is a string and the name of an existing column,
        copy existing column [contents] to the new column. 
        """
        if isinstance(contents, str) and contents in self.df.columns:
            self.df[colname] = self.df[contents].copy()
        else:
            self.df[colname] = contents

    def new_text_column(self, new_text_name):
        """
        create a new column of text to process named [new_text_name],
        automatically updates internal text col tracking
        returns new instance of the class object
        """
        obj = self.copy()
        obj.addumn(new_text_name, obj.curr_txt)
        obj.curr_txt = new_text_name
        return obj

    def join_dataset(self, newdf, join_on, assign_text):
        """
        join current dataset with new dataset [newdf],
        assuming inner join,
        join on the column named [join_on] which must exist
            in both datasets
        for the benefit of the object, 
            set column named [assign_text] as text analysis target
        returns new instance of the class object
        """
        obj = self.copy()
        obj.df = pandas.merge(obj.df, newdf, 
            how="inner", on=join_on)
        obj.curr_txt = assign_text
        return obj

    # convert timestamp to numeric second counter
    def colon_delim_timestamp_to_second(self, x):
        """
        Apply vectorizer function, accepts raw text like timestamp,
        returns number of hours, minutes, and seconds converted to 
        a single numeric seconds value.
        """
        if pandas.isna(x): #if nothing here, return null
            return numpy.nan

        # get numeric timestamp matches
        nums = re.findall(r"(\d\d)?\:?(\d\d)\:(\d\d)",x)
        if not nums: #if no matches, return null
            return numpy.nan
        
        # convert regex match outcome into list of integers
        secs = 0
        incr = 0
        for num in range(len(list(nums[0])), -1, -1):
            #aggregate time values moving backward from 0, 
            #increase multiple by order of 60 as time in seconds
            if num:
                secs += int(num) * (incr * 60) 
                incr += 1
        return secs

    def regex_replace_from_dict(self, reg_dict):
        """ 
        Accepts dictionary where each key is a regex group to find
        and each value is what should replace the found group.
        returns new instance of the class object
        """
        obj = self.copy()
        obj.df[obj.curr_txt] = obj.df[obj.curr_txt].replace(reg_dict,
            regex=True)
        return obj

    def __str__(self):
        
        join_me = {"Document Source": self.data_sources,
            "Count of Documents": self.df.doc_id.nunique(),
            "Top 10 rows": self.df.to_string(maxwidth=33,
                justify="right",
                max_rows=10,
                show_dimensions=True)
        }
        return '\n'+'\n\n'.join( \
            ['\t'+k+"\n"+str(r) for k,r in join_me.items()])

    def SERA_clean_text(self, src_corpus_df=None):
        obj = self.copy()
        
        """Apply functions above to clean up raw_corpus content."""
        if not src_corpus_df:
            df = obj.df
        else:
            df = src_corpus_df.copy()
        
        # remove unhelpful \r character
        df = df.replace("\r", "")
        #  separate multi-line text to individual rows
        df['rawtext'] = df['rawtext'].str.split("\n")
        df = df.explode('rawtext')
        # clean up any resulting empty rows 
        df = df.dropna(subset=['rawtext'])
        # print(df)
        df.columns = ["doc_id", "filedir", "period", 
            "filename", "collected", "txtlen", "rawtext", "line_id"] 
        #"file_index","script_impl", "src", 
            #"linkrow", "linkid", "linkskill", "linkcoach"]

        # # extract period and document text, remove filedir
        # df[['period', 'document']] = df.apply(lambda x: \
        #     x['filedir'].split("\\")[-2:], \
        #     axis='columns', result_type='expand')
        df = df.drop(["filedir"], axis=1)

        # incrementally process raw text in duplicate column
        df['text'] = df['rawtext'].values
        obj.curr_txt = "text"
        # extract otter service notes
        # do this first to ensure - 1 - is captured 
        # before leading dash removed
        df = self.add_col_from_extract(df, 'text', \
            'otter_notes', r"(Transcribed by https\:\/\/otter\.ai|\- \d* \-)")
        
        # replace typos and unhelpful strings
        replacements = {r"(00\:\,00:)": "00:00:",
                        r"(\:\:)": ":",
                        r"(Colleen \& Respondent)": "Colleen",
                        r"(\s{2,})": " ",
                        #r"(Speaker )\d": "Speaker",
                        r"(\–)": "-",
                        "(•)": "-",
                        r"( \- )": " ",
                        r"(’)": "'",
                        r"(see that as\:)": "see that as",
                        r"([Aa]ll? ?righty?)": "alright",
                        r"([Mm]+?\-?hm+)": "mhmm"}
        df['text'] = df['text'].replace(replacements, regex=True)

        # extract datetimes, convert to python datetime
        df = self.add_col_from_extract(df, 'text', \
            'date_time', \
            r"([A-Z][a-z]{,5}, \d{,2}\/\d{,2}(?:\s*\d{,2}:\d\d" \
                +r"\s?(?:A|P)M)?\s?(?:- \d{,2}:\d\d)?)")

        # add timestamp col and remove from text
        df = self.add_col_from_extract(df, 'text', \
            'speaker', r"^(?:([^\d:\[\]\n]*) \d\d\:\d\d" \
                + r"|[\[\]\d\: ]* ([\w ]{,25}?)\: |([\w ]*)\: )")

        # in some files, utterances by single speaker broke into multiple lines
        # where an utterance is not yet labeled by speaker,
        # fill down the last identified speaker
        df["speaker"] = df["speaker"].fillna(method='ffill')

        # extract character markers, unknown purpose/interpretation
        df = self.add_col_from_extract(df, 'text', \
            'char_marker', r"^([\d\_a-zC]{8,}(?:\_Transcript)?(?: - )?(?:\d*)?)")

        # extract timestamp values
        df = self.add_col_from_extract(df, 'text', \
            'timestamp', r"(\[?[\d\d\:]{5,}]?)")

        # # extract time in seconds
        # df['seconds'] = df['timestamp'].apply(lambda x: \
        #     colon_delim_timestamp_to_second(x))

        # extract audio notes in brackets
        df = self.add_col_from_extract(df, 'text', \
            'audio_note', r"(\[.*?\])", mult=True)

        # extract audio filename in format *.mp4
        df = self.add_col_from_extract(df, 'text', \
            'audio_file', r"([^\s]*\.mp4)$")
        df = self.add_col_from_extract(df, 'text', \
            'summary_keywords', "", from_prev_row=True)
            #shift_equals="SUMMARY KEYWORDS")
        df = self.add_col_from_extract(df, 'text', \
            'speakers', "", from_prev_row=True)
            #, shift_equals="SPEAKERS")

        removeus = ["SUMMARY","KEYWORDS","SPEAKERS", r"\[unintelligible"]
        for ru in removeus:
            df['text'] = df['text'].replace(ru, "", regex=True)
            df['text'] = df['text'].apply(lambda x: 
                str(x).strip())
        print("Raw corpus text has been cleaned.")
        obj.df = df
        return obj

# if __name__ == "__main__":

#     #%%
#     # =============================================================================
#     # Example
#     # =============================================================================
#     # Testing / Usage
#     documents = pandas.DataFrame({'id':[1,2,3,4,5],\
#                                   'text':['this is the first','this is the second','this is the third','this is the fourth','this is the fifth'],\
#                                   'text2':["He is a good dog.","The dog is too lazy.","That is a brown cat.","The cat is very active.","I have brown cat and dog."],
#                                   'id2':['1a','2a','3a','4a','5a']}) # create instance

#     # def __init__(self, data_A_ideal, A_text, A_match,
#     #     data_B_compare, B_text, B_match, grouping=None):
#     # #define objects
#     # doc1 = DocSim(documents.copy(), A_text='text', A_match='id', \
#     #     data_B_compare=documents, B_text='text2', B_match='id')
#     # doc2 = DocSim(documents.copy(), A_text='text2', A_match='id', \
#     #     data_B_compare=documents, B_text='text2', B_match='id')

#     doc1 = DocSim(documents, "text")
#     doc2 = DocSim(documents, "text2")
#     #%%
#     #get feature names
#     print(doc1.get_feature_names())
#     #%%
#     #get vectorized test
#     print(doc1.get_preprocessed_text())
#     #%%
#     #preprocessing
#     print(doc1.preprocessing(remove_stopwords = True, stem = True, \
#                                 tfidf = False, lsa=False))

#     #get feature names
#     print(doc1.get_feature_names())
#     #get vectorized text
#     print(doc1.get_preprocessed_text())
#     #%%
#     #preprocessing
#     print(doc2.preprocessing(remove_stopwords = True, stem = True, \
#                                 tfidf = True, lsa = True, lsa_n_components = 4))
#     #%%
#     #get feature names
#     print(doc2.get_feature_names())


#     # %%
#     print(doc2.doc_sim(mode = 'pairwise', 
#                     method = 'cosine', 
#                     remove_stopwords = True, 
#                     stem = True, 
#                     tfidf = True, 
#                     lsa = True, 
#                     lsa_n_components = 4))
#     # %% Negaive Cosine Similarities...

#     print(doc2.doc_sim(mode = 'normal', 
#                     method = 'cosine', 
#                     remove_stopwords = True, 
#                     stem = True, 
#                     tfidf = True, 
#                     lsa = True, 
#                     lsa_n_components = 4))
