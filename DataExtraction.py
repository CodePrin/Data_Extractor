# Check the package_requirements.txt

'''Importing packages'''
from bs4 import BeautifulSoup
import nltk
from nltk import RegexpTokenizer, sent_tokenize
nltk.download('punkt')
import pandas as pd
import requests
import re
import os


'''Current file location'''
current_file_path = os.path.join(os.path.dirname(__file__))
os.chdir(current_file_path)
# print(current_file_path)


'''File location for StopWordsFile.'''
StopWords_Auditor = 'StopWordsFile/StopWords_Auditor.txt'
StopWords_Currencies = 'StopWordsFile/StopWords_Currencies.txt'
StopWords_DatesAndNumbers = 'StopWordsFile/StopWords_DatesAndNumbers.txt'
StopWords_Generic = 'StopWordsFile/StopWords_Generic.txt'
StopWords_GenericLong = 'StopWordsFile/StopWords_GenericLong.txt'
StopWords_Geographic = 'StopWordsFile/StopWords_Geographic.txt'
StopWords_Names = 'StopWordsFile/StopWords_Names.txt'

PositiveWords_File = 'MasterDictionary/positive-words.txt'
NegativeWords_File = 'MasterDictionary/negative-words.txt'


# This code will help in loading all the records of the dataset when any command will be run to output the dataframe.
pd.options.display.max_rows = 10000000
pd.options.display.max_columns = 10000000


'''Loading the dataset containing url's.'''
current_file_path = os.path.join(os.path.dirname(__file__))
input_table = pd.read_excel(f"{current_file_path}\input.xlsx")
# print(input_table)


'''Loading positive words.'''
with open(PositiveWords_File, 'r') as positive_file:
    PositiveWords = positive_file.read().lower()
positive_words_list = PositiveWords.split('\n')
# print(positive_words_list)


'''Loading negative words.'''
with open(NegativeWords_File, 'r') as negative_file:
    NegativeWords = negative_file.read().lower()
negative_words_list = NegativeWords.split('\n')
# # print(negative_words_list)


'''Loading stop words file to retrieve StopWords_Auditor.'''
with open(StopWords_Auditor ,'r') as stop_words_auditor:
    StopWordsAuditor = stop_words_auditor.read().lower()
stop_words_auditor_list = StopWordsAuditor.split('\n')
# print(stop_words_auditor_list)


'''Loading stop words file to retrieve StopWords_Currencies.'''
with open(StopWords_Currencies ,'r') as stop_words_currencies:
    StopWordsCurrencies = stop_words_currencies.read().lower()

stop_words_currencies_list = StopWordsCurrencies.replace("|", "").split()

stop_words_currencies_list.remove('(former')
stop_words_currencies_list.remove('yug.')
stop_words_currencies_list.remove('rep.)')

stop_words_currencies_list[17:19] = [' '.join(stop_words_currencies_list[17:19])]  # Joined into "costa rica".
stop_words_currencies_list[29:33] = [' '.join(stop_words_currencies_list[29:33])]  # Joined into "sao tom and principe".
stop_words_currencies_list[35:37] = [' '.join(stop_words_currencies_list[35:37])]  # Joined into "cape verde".
stop_words_currencies_list[47:49] = [' '.join(stop_words_currencies_list[47:49])]  # Joined into "netherlands antilles".
stop_words_currencies_list[51:54] = [' '.join(stop_words_currencies_list[51:54])]  # Joined into "papua new guinea".
stop_words_currencies_list[54:56] = [' '.join(stop_words_currencies_list[54:56])]  # Joined into "konvertibilna marka".
stop_words_currencies_list[57:59] = [' '.join(stop_words_currencies_list[57:59])]  # Joined into "czech republic".
stop_words_currencies_list[81:83] = [' '.join(stop_words_currencies_list[81:83])]  # Joined into "sierra leone".
stop_words_currencies_list[102:104] = [' '.join(stop_words_currencies_list[102:104])]  # Joined into "new lira".
stop_words_currencies_list[104:106] = [' '.join(stop_words_currencies_list[104:106])]  # Joined into "new sheqel".
stop_words_currencies_list[108:110] = [' '.join(stop_words_currencies_list[108:110])]  # Joined into "nuevo sol".
stop_words_currencies_list[123:125] = [' '.join(stop_words_currencies_list[123:125])]  # Joined into "south africa".
stop_words_currencies_list[135:137] = [' '.join(stop_words_currencies_list[135:137])]  # Joined into "saudi arabia".
stop_words_currencies_list[152:155] = [' '.join(stop_words_currencies_list[152:155])]  # Joined into "special drawing rights".
stop_words_currencies_list[153:156] = [' '.join(stop_words_currencies_list[153:156])]  # Joined into "international monetary funds".
stop_words_currencies_list[157:159] = [' '.join(stop_words_currencies_list[157:159])]  # Joined into "western samoa".
stop_words_currencies_list[165:167] = [' '.join(stop_words_currencies_list[165:167])]  # Joined into "korea, south".

unwanted_elements_in_currencies = []

for i in range(1, 170, 2):
    unwanted_elements_in_currencies.append(stop_words_currencies_list[i])
for j in unwanted_elements_in_currencies:
    stop_words_currencies_list.remove(j)

# print(stop_words_currencies_list)


'''Loading stop words file to retrieve StopWords_DatesAndNumbers.'''
with open(StopWords_DatesAndNumbers ,'r') as stop_words_dates_and_numbers:
    StopWordsDatesAndNumbers = stop_words_dates_and_numbers.read().lower()
stop_words_dates_and_numbers_list = StopWordsDatesAndNumbers.replace("|", "").split()

stop_words_dates_and_numbers_list.remove('denominations')
stop_words_dates_and_numbers_list.remove('time')
stop_words_dates_and_numbers_list.remove('related')
stop_words_dates_and_numbers_list.remove('calendar')
stop_words_dates_and_numbers_list.remove('numbers')
stop_words_dates_and_numbers_list.remove('roman')
stop_words_dates_and_numbers_list.remove('numerals')
# print(stop_words_dates_and_numbers_list)


'''Loading stop words file to retrieve StopWords_Generic.'''
with open(StopWords_Generic ,'r') as stop_words_generic:
    StopWordsGeneric = stop_words_generic.read().lower()
stop_words_generic_list = StopWordsGeneric.split('\n')
# print(stop_words_generic_list)


'''Loading stop words file to retrieve StopWords_GenericLong.'''
with open(StopWords_GenericLong ,'r') as stop_words_generic_long:
    StopWordsGenericLong = stop_words_generic_long.read().lower()
stop_words_generic_long_list = StopWordsGenericLong.split('\n')

unwanted_elements_in_generic_long = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

for element in unwanted_elements_in_generic_long:
    if element in stop_words_generic_long_list:
        stop_words_generic_long_list.remove(element)
# print(stop_words_generic_long_list)


'''Merging all stop words in single all_stop_words_list.'''
all_stop_words_list = stop_words_auditor_list + stop_words_currencies_list + stop_words_currencies_list + stop_words_dates_and_numbers_list + stop_words_generic_list + stop_words_generic_long_list
# print(all_stop_words_list)


'''Make a tokenizing function to extract data that is not in all_stop_words_list.'''
def tokenizer(text):
    text = text.lower()
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)  # Extracts all the data from the content and generate it in form of separated words in form of a list.
    filtered_words = list(filter(lambda token: token not in all_stop_words_list, tokens))
    return filtered_words
# print(tokenizer(content))


'''To calculate how many positive words are present in the content.'''
def positive_score_counter(text):
  positive_words = 0
  filtered_phrase = tokenizer(text)  
  for word in filtered_phrase:
    if word in positive_words_list:
       positive_words += 1
  return positive_words
# print(positive_score_counter(content))


'''To calculate how many negative words are present in the content.'''
def negative_score_counter(text):
  negative_words=0
  tokenphrase = tokenizer(text)  
  for word in tokenphrase :
    if word in negative_words_list:
       negative_words += 1
  return negative_words
# print(negative_score_counter(content))


'''To calculate polarity score.'''
def polarity_score_counter(positive_score , negative_score) :
  return (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
# print(polarity_score_counter(positive_score_counter(content), negative_score_counter(content)))


'''To calculate total word count of the content.'''
def total_word_counter(text):
    tokens = tokenizer(text)
    return len(tokens)
# print(total_word_counter(content))


'''To calculate subjectivity score.'''
def subjectivity_score_counter(positive_score , negative_score, total_word_count) :
  return (positive_score - negative_score) / ((total_word_count) + 0.000001)
# print(subjectivity_score_counter(positive_score_counter(content), negative_score_counter(content), total_word_counter(content)))


'''To print the the number of sentences in the content.'''
def sentence_counter(text):
    sentence_counts = len(sent_tokenize(text))
    return sentence_counts
# print(sentence_counter(content))


'''To calculate average sentence length of the content.'''
def avg_sentence_len(text):
    word_count = total_word_counter(text)
    sentence_count = sentence_counter(text)
    if sentence_count > 0 : 
        average_sentence_length = word_count / sentence_count
    return round(average_sentence_length)
# print(avg_sentence_len(content))


'''To calculate complex words of the content.'''
def complex_word_counter(text):
    tokens = tokenizer(text)
    complex_Words = 0
    
    for word in tokens:
        vowels = 0
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w == 'a' or w == 'e' or w == 'i' or w == 'o' or w == 'u'):
                    vowels += 1
            if(vowels > 2):
                complex_Words += 1

    return complex_Words
# print(complex_word_counter(content))


'''To calculate syllable count per word.'''
def syllable_counter(text):
    filtered_phrase = tokenizer(text)
    vowels = 0
    
    for word in filtered_phrase:        
        if word.endswith(('es','ed')):
            pass
        else:
            for w in word:
                if(w == 'a' or w == 'e' or w == 'i' or w == 'o' or w == 'u'):
                    vowels += 1
    return vowels
# print(syllable_counter(content))


'''To calculate personal pronouns.'''
def personal_pronoun_counter(text):
    pronounRegex = re.compile(r'I|we|my|ours|us',re.I)
    pronouns = pronounRegex.findall(text)
    pronouns_count = len(pronouns)
    return pronouns_count
# print(personal_pronoun_counter(content))


'''To calculate average word length.'''
def avg_word_len_counter(text):
    filtered_phrase = tokenizer(text)
    total_characters = 0

    for word in filtered_phrase:
            for char in word:
                 total_characters += 1

    return total_characters
# print(avg_word_len_counter(content))


'''Function for generating a dataframe having analysis report.'''
def data_analysis(input_table):
    x = {
         'URL_ID': [],
         'URL': [],
         'POSITIVE SCORE': [],
         'NEGATIVE SCORE': [],
         'POLARITY SCORE': [],
         'SUBJECTIVITY SCORE': [],
         'AVG SENTENCE LENGTH': [],
         'PERCENTAGE OF COMPLEX WORDS': [],
         'FOG INDEX': [],
         'AVG NUMBER OF WORDS PER SENTENCE': [],
         'COMPLEX WORD COUNT': [],
         'WORD COUNT': [],
         'SYLLABLE PER WORD': [],
         'PERSONAL PRONOUNS': [],
         'AVG WORD LENGTH': [],
         }

    url_id = input_table['URL_ID']
    x['URL_ID'] = url_id

    for url in input_table['URL']:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        data = soup.find(attrs = { 'class' : 'td-post-content'})
        x['URL'].append(url)

        if data:
            content = data.get_text()
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines.
            content = '\n'.join(chunk for chunk in chunks if chunk)

            positive_score = positive_score_counter(content)
            x['POSITIVE SCORE'].append(positive_score)

            negative_score = negative_score_counter(content)
            x['NEGATIVE SCORE'].append(negative_score)

            polarity_score = polarity_score_counter(positive_score, negative_score)
            x['POLARITY SCORE'].append(polarity_score)

            subjectivity_score = subjectivity_score_counter(positive_score, negative_score, total_word_counter(content))
            x['SUBJECTIVITY SCORE'].append(subjectivity_score)

            average_sentence_length = avg_sentence_len(content)
            x['AVG SENTENCE LENGTH'].append(average_sentence_length)

            percentage_complex_words = complex_word_counter(content) / total_word_counter(content)
            x['PERCENTAGE OF COMPLEX WORDS'].append(percentage_complex_words)

            fog_index = 0.4*(avg_sentence_len(content) + percentage_complex_words)
            x['FOG INDEX'].append(fog_index)

            avg_words_per_sentence = total_word_counter(content) / sentence_counter(content)
            x['AVG NUMBER OF WORDS PER SENTENCE'].append(avg_words_per_sentence)

            complex_words = complex_word_counter(content)
            x['COMPLEX WORD COUNT'].append(complex_words)

            total_content_words = total_word_counter(content)
            x['WORD COUNT'].append(total_content_words)

            syllable_count = syllable_counter(content)
            x['SYLLABLE PER WORD'].append(syllable_count)

            pronoun_count = personal_pronoun_counter(content)
            x['PERSONAL PRONOUNS'].append(pronoun_count)

            avg_word_len_count = avg_word_len_counter(content)
            x['AVG WORD LENGTH'].append(avg_word_len_count)

        else:
            x['POSITIVE SCORE'].append('Cannot open URL.')
            x['NEGATIVE SCORE'].append('Cannot open URL.')
            x['POLARITY SCORE'].append('Cannot open URL.')
            x['SUBJECTIVITY SCORE'].append('Cannot open URL.')
            x['AVG SENTENCE LENGTH'].append('Cannot open URL.')
            x['PERCENTAGE OF COMPLEX WORDS'].append('Cannot open URL.')
            x['FOG INDEX'].append('Cannot open URL.')
            x['AVG NUMBER OF WORDS PER SENTENCE'].append('Cannot open URL.')
            x['COMPLEX WORD COUNT'].append('Cannot open URL.')
            x['WORD COUNT'].append('Cannot open URL.')
            x['SYLLABLE PER WORD'].append('Cannot open URL.')
            x['PERSONAL PRONOUNS'].append('Cannot open URL.')
            x['AVG WORD LENGTH'].append('Cannot open URL.')

    df = pd.DataFrame(x)

    return df


'''Function that extracts the title and content from the url's article and then saving it in a text file with URL_ID as it's file name.'''
def title_and_content_extraction():
    os.mkdir('./Articles')  # './' is denoted as current working directory.
    for url in input_table['URL']:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        data = soup.find(attrs = { 'class' : 'td-post-content'})

        if data:
            content = data.get_text()
            lines = (line.strip() for line in content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines.
            content = '\n'.join(chunk for chunk in chunks if chunk)
            title = soup.find("title").get_text()

            url_id = input_table.loc[input_table['URL'] == url, 'URL_ID'].iloc[0]

            with open(f".\Articles\{url_id}.txt", "a", encoding = 'utf-8') as f:
                print(title, '\n', file=f)
                print(content, file=f)
                 
        else:
            print('Content not found for this particular url:', {url})

# print(title_and_content_extraction())


'''Generating a excel sheet consisting the dataframe of analysis.'''
data = data_analysis(input_table)
data.to_excel("Output Data Structure.xlsx")


'''Generating separate files for the url's article consisting only the title and content. Then saving it in a text file with URL_ID as it's file name'''
title_and_content_extraction()
