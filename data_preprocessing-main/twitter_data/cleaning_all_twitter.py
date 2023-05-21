from mpi4py import MPI
import nltk
from nltk.corpus import stopwords
import json
import ijson
import re
from decimal import Decimal
from tqdm import tqdm
import decimal
from textblob import TextBlob

nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# word lemmatize
def lemmatize(word):
    lemmatizer = nltk.stem.wordnet.WordNetLemmatizer()
    lemma = lemmatizer.lemmatize(word, 'v')
    if lemma == word:
        lemma = lemmatizer.lemmatize(word, 'n')
    return lemma

def preprocess_text(text):
    #remove the @
    text=re.sub(r'\s?@\w+', '', text)
    url_pattern = re.compile(r'http\S+')
    text=url_pattern.sub('', text)
    #keep the letters
    text =re.sub(r'[^A-Za-z\s]', '', text)
    #lower the letters
    text = text.lower()
    tokens = nltk.word_tokenize(text)
    #remove the stop words
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]
    tokens = [lemmatize(token) for token in tokens]
    #remove the punctuation
    tokens = [token for token in tokens if token.isalnum()]
    preprocessed_text = " ".join(tokens)
    return preprocessed_text

def sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    polarity = sentiment.polarity
    if polarity > 0:
        sentiment_label = "Positive"
    elif polarity < 0:
        sentiment_label = "Negative"
    else:
        sentiment_label = "Neutral"
    return sentiment_label,polarity

def decimal_to_float(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: decimal_to_float(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_float(v) for v in obj]
    else:
        return obj

def process_twitter_data(rank, size, twitter_file, output_file_path):
    city_ls=['Sydney','Melbourne','Brisbane','Adelaide','Perth','Hobart','Darwin','Australian Capital Territory']
    city_set = set(city_ls)
    with open(twitter_file, "rb") as f:
        with open(f"{output_file_path}_{rank}.json", "a") as output_file:
            output_file.write('[\n')
            count = 0
            for index, item in tqdm(enumerate(ijson.items(f, 'rows.item.doc'))):
                if index % size == rank:
                    if "includes" in item and "places" in item["includes"] and "full_name" in item["includes"]["places"][0]:
                        location_ls = item['includes']['places'][0]['full_name'].split(',')
                        location_set=set(location_ls)
                        location=location_set.intersection(city_set)
                        if len(location)>0:
                            location=list(location)[0]
                            _id = item.get('_id')
                            create_time = item.get('data').get('created_at').split('.')[0].split(':')[0].split('T')
                            create_day=create_time[0].replace('-','')
                            month=int(create_day[4:6])
                            create_hour=int(create_time[1])
                            if create_hour>=0 and create_hour<=12:
                                time_quantum='morning'
                            elif create_hour>12 and create_hour<=18:
                                time_quantum='afternoon'
                            else:
                                time_quantum='night'
                            lang = item.get('data').get('lang')
                            text = item.get('data').get('text')
                            sentiment_label, polarity = sentiment_analysis(text)
                            text_tokens = preprocess_text(text).split(' ')
                            new_dict = {
                                '_id': _id,
                                'month': month,
                                'time_quantum': time_quantum,
                                'text': text,
                                'text_tokens': text_tokens,
                                'lang': lang,
                                'geo': location,
                                'sentiment_label': sentiment_label,
                                'polarity': polarity
                            }
                            if count > 0:
                                output_file.write(',\n')
                            json.dump(decimal_to_float(new_dict), output_file)
                            count += 1
            output_file.write('\n]')

def combine_files(num_files, output_file_name):
    combined_data = []
    for i in range(num_files):
        with open(f'twitter_geo_{i}.json', 'r') as file:
            data = json.load(file)
            combined_data.extend(data)

    with open(output_file_name, 'w') as output_file:
        json.dump(combined_data, output_file)


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()
    twitter_file = 'twitter-huge.json'
    output_file_path = 'twitter_geo'
    process_twitter_data(rank, size, twitter_file, output_file_path)
    comm.Barrier()  # Synchronize all processes

    if rank == 0:  # Only the root process (rank 0) should run the combine_files function
        output_file_name = 'all_twitter.json'
        combine_files(8, output_file_name)

if __name__ == '__main__':
    main()
