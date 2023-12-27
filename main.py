#
# Final Project
#
# Text Model
#
# Computer Science 111
#
import math

def clean_text(txt):
    """takes string of text txt as a parameter and returns a list
    containing the words in tdxt after its been cleaned"""
    low_txt = txt.lower()
    result = low_txt.split()
    final = []
    for word in result:
        for symbol in """.,?"'!;:""":
            word = word.replace(symbol, "")
        final += [word]
    return final

def stem(s):
    """accepts a string as param and return the stem"""
    res_str = ""

    if len(s) <= 3:
        return s
    
    if "ing" == s[-3:]:
        if len(s) > 4:
            if s[-4] == s[-5]:
                res_str = s[:-4]
                return res_str
        else:
            res_str = s[:-3]
            return res_str

    elif "ers" == s[-3:]:
        res_str = s[:-3]
        return res_str
    
    elif "es" == s[-2:] or "er" == s[-2:]:
        res_str = s[:-2]
        return res_str
    
    elif "e" == s[-1:]:
        res_str = s[:-1]
        return res_str
    
    elif "ly" == s[-2:]:
        res_str = s[:-2]
        return res_str
    
    elif "y" == s[-1]:
        res_str = s[:-1] + "i"
        return res_str
    
    elif "s" == s[-1]:
        res_str = s[:-1]
        return res_str

    elif "al" == s[-2:]:
        res_str = s[:-2]
        return res_str

    elif "ied" == s[-3:] or "ies" == s[-3:]:
        res_str = s[:-3] + "i"
        return res_str

    else:
        return s

def compare_dictionaries(d1, d2):
    """take two feature dictionaries d1 and d2 as inputs, and
    it should compute and retunr thier long similarities score"""
    if d1 == {}:
        return -50
    
    score = 0
    total = 0
    for item in d1:
        total += d1[item]

    for word in d2:
        if word in d1:
            score += math.log(d1[word] / total) * d2[word]
        else:
            score += math.log(0.5 / total) * d2[word]

    return score

    

class TextModel():
    """data type for text model"""
    def __init__(self, model_name):
        """constructing a TextModel object by accepting
        string as name"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuations = {}

    def __repr__(self):
        """returns a string which include the name of the
        model as well as the size of the dictionaries
        for each features of the text"""
        s = "text model name: " + self.name + "\n"
        s += "  number of words: " + str(len(self.words)) + "\n"
        s += "  number of word lengths: " + str(len(self.word_lengths)) + "\n"
        s += "  number of stems: " + str(len(self.stems)) + "\n"
        s += "  number of sentence lengths: " + str(len(self.sentence_lengths)) + "\n"
        s += "  puncutations: " + str(len(self.punctuations)) + "\n"
        return s

    def add_string(self, s):
        """adds string of text s to the model by argumenting the feature
        dictionaries defined in the constructor"""
        word_list = clean_text(s)
        word_not_cleaned = s.split()
        sentence_split = s.split(""".?!""")

        for current_word in word_list:
            if current_word not in self.words:
                self.words[current_word] = 1
            else:
                self.words[current_word] += 1
                
            if len(current_word) not in self.word_lengths:
                self.word_lengths[len(current_word)] = 1
            else:
                self.word_lengths[len(current_word)] += 1

            if stem(current_word) not in self.stems:
                self.stems[stem(current_word)] = 1
            else:
                self.stems[stem(current_word)] += 1
        
        sentence_count = 0
        
        for word in word_not_cleaned:
            sentence_count += 1
            if "." in word or "?" in word or "!" in word:
                if sentence_count not in self.sentence_lengths:
                    self.sentence_lengths[sentence_count] = 1
                else:
                    self.sentence_lengths[sentence_count] += 1
                sentence_count = 0
            
            if "." not in self.punctuations:
                self.punctuations["."] = 1
            elif "." in self.punctuations:
                self.punctuations["."] += 1

            if "?" not in self.punctuations:
                self.punctuations["?"] = 1
            elif "?" in self.punctuations:
                self.punctuations["?"] += 1

            if "," not in self.punctuations:
                self.punctuations[","] = 1
            elif "," in self.punctuations:
                self.punctuations["?"] += 1

            if '"' not in self.punctuations:
                self.punctuations['"'] = 1
            elif '"' in self.punctuations:
                self.punctuations['"'] += 1

            if "'" not in self.punctuations:
                self.punctuations["'"] = 1
            elif "'" not in self.punctuations:
                self.punctuations["'"] += 1

            if "!" not in self.punctuations:
                self.punctuations["!"] = 1
            elif "!" in self.punctuations:
                self.punctuations["!"] = 1

            if ";" not in self.punctuations:
                self.punctuations[";"] = 1
            elif ";" in self.punctuations:
                self.punctuations[";"] += 1

            if ":" not in self.punctuations:
                self.punctuations[":"] = 1
            elif ":" in self.punctuations:
                self.punctuations[":"] += 1

        
    def add_file(self, filename):
        """adds all the text in the file identified by the filename
        to the model"""
        f = open(filename, "r", encoding="utf8", errors="ignore")
        text = f.read()
        result = self.add_string(text)
        return result

    def save_model(self):
        """saves the TextModel object self by writing its various feature
        dictionaries to file. There will be on file written for each feature
        dictionary"""
        
        word_name = self.name + "_words"
        length_name = self.name + "_word_lengths"
        stems_name = self.name + "_stems"
        sentence_name = self.name + "_sentence_lengths"
        punctuation_name = self.name + "_punctuations"

        f_w = open(word_name, "w")
        f_w.write(str(self.words))
        f_w.close()

        f_l = open(length_name, "w")
        f_l.write(str(self.word_lengths))
        f_l.close()

        f_s = open(stems_name, "w")
        f_s.write(str(self.stems))
        f_s.close()

        f_sent = open(sentence_name, "w")
        f_sent.write(str(self.sentence_lengths))
        f_sent.close()

        f_punc = open(punctuation_name, "w")
        f_punc.write(str(self.punctuations))
        f_punc.close()

    def read_model(self):
        """reads the stores dict for TextModel and assigns them to the
        attributes of the called TextModel"""

        word_name = self.name + "_words"
        length_name = self.name + "_word_lengths"
        stems_name = self.name + "_stems"
        sentence_name = self.name + "_sentence_lengths"
        punctuation_name = self.name + "_punctuations"

        f_w = open(word_name, "r")
        w_str = f_w.read()
        f_w.close()
        self.words = dict(eval(w_str))

        f_l = open(length_name, "r")
        l_str = f_l.read()
        f_w.close()
        self.word_lengths = dict(eval(l_str))

        f_s = open(stems_name, "r")
        s_str = f_s.read()
        f_s.close()
        self.stems = dict(eval(s_str))

        f_sent = open(sentence_name, "r")
        sent_str = f_sent.read()
        f_sent.close()
        self.sentence_lengths = dict(eval(sent_str))

        f_punc = open(punctuation_name, "r")
        punc_str = f_punc.read()
        f_punc.close()
        self.punctuations = dict(eval(punc_str))

    def similarity_scores(self, other):
        """computes and return a list of log similarity scores
        measuring the similarity of self and other"""
        similar_list = []
        
        word_score = compare_dictionaries(other.words, self.words)
        similar_list += [word_score]
        
        w_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        similar_list += [w_length_score]

        s_score = compare_dictionaries(other.stems, self.stems)
        similar_list += [s_score]

        s_length_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        similar_list += [s_length_score]

        punc_score = compare_dictionaries(other.punctuations, self.punctuations)
        similar_list += [punc_score]

        return similar_list

    def classify(self, source1, source2):
        """compares the TextModel object self to two other "source" TextModel objects
        and determines which of these other TextModels is the more likely source of
        the called textModel"""
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)

        print("scores for " + source1.name + ":" + str(scores1))
        print("scores for " + source2.name + ":" + str(scores2))

        total_1 = 0
        total_2 = 0

        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                total_1 += 1
            elif scores2[i] > scores1[i]:
                total_2 += 1

        if total_1 > total_2:
            print(self.name + " is more likely to have come from " + source1.name)
        else:
            print(self.name + " is more likely to have come from " + source2.name)



def test():
    """test final code"""
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
        
        
# Copy and paste the following function into finalproject.py
# at the bottom of the file, *outside* of the TextModel class.
def run_tests():
    """to test with txt documents"""
    source1 = TextModel('reuters')
    source1.add_file('reuters_articles.txt')

    source2 = TextModel('ap')
    source2.add_file('ap_articles.txt')

    new1 = TextModel('cnn')
    new1.add_file('cnn_articles.txt')
    new1.classify(source1, source2)

    # Add code for three other new models below.
    source1 = TextModel('reuters')
    source1.add_file('reuters_articles.txt')

    source2 = TextModel('ap')
    source2.add_file('ap_articles.txt')

    new1 = TextModel('yahoo')
    new1.add_file('yahoo_articles.txt')
    new1.classify(source1, source2)

    #---
    source1 = TextModel('reuters')
    source1.add_file('reuters_articles.txt')

    source2 = TextModel('ap')
    source2.add_file('ap_articles.txt')

    new1 = TextModel('nyt')
    new1.add_file('nyt_articles.txt')
    new1.classify(source1, source2)

    #---
    source1 = TextModel('reuters')
    source1.add_file('reuters_articles.txt')

    source2 = TextModel('ap')
    source2.add_file('ap_articles.txt')

    new1 = TextModel('bbc')
    new1.add_file('bbc_articles.txt')
    new1.classify(source1, source2)
    

