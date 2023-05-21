from mpi4py import MPI
import json
import ijson
from decimal import Decimal
from tqdm import tqdm


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
    education_ls = ['school', 'college', 'university', 'study', 'student', 'teacher', 'tech', 'education', 'course',
                    'learn', 'class', 'homework', 'assignment', 'exam', 'test', 'grade', 'degree', 'diploma', 'master',
                    'bachelor', 'phd', 'scholarship', 'research', 'academy', 'academic', 'campus', 'tuition', 'tutor',
                    'lecture', 'professor', 'classroom', 'lab', 'laboratory', 'library', 'book', 'textbook', 'notebook',
                    'note', 'paper', 'essay', 'thesis', 'dissertation', 'project']
    art_ls = ['art', 'paint', 'sing', 'dance', 'music', 'film', 'show', 'movie', 'artist', 'dancer', 'cinema', 'design',
              'photo', 'picture', 'actor', 'story', 'theater', 'theatre', 'poem', 'poetry', 'poet', 'song', 'singer',
              'band', 'album', 'concert', 'performance', 'exhibition', 'gallery', 'museum', 'creative', 'creativity',
              'creative', 'art', 'creative', 'artist', 'creative', 'work', 'creative', 'industry']
    technology_ls = ['technology', 'tech', 'computer', 'software', 'hardware', 'data', 'internet', 'network', 'program',
                     'code', 'developer', 'coding', 'programming', 'algorithm', 'app', 'application', 'website', 'web',
                     'digital', 'device', 'smartphone', 'mobile', 'phone', 'laptop', 'tablet', 'ipad', 'iphone',
                     'camera', 'robot', 'machine', 'artificial', 'intelligence', 'ai', 'virtual', 'reality', 'vr',
                     'augment', 'ar', 'cloud', 'blockchain', 'cyber', 'security', 'hacker', 'hack', 'privacy',
                     'encryption', 'data', 'science', 'big', 'data', 'analytics', 'database', 'server', 'cloud']
    finance_ls = ['finance', 'financial', 'bank', 'account', 'money', 'cash', 'wealth', 'rich', 'poor', 'stock',
                  'market', 'investment', 'investor', 'invest', 'trading', 'trade', 'trader', 'stock', 'market',
                  'stock', 'exchange', 'stock', 'broker', 'fund', 'gold', 'silver', 'asset', 'currency', 'banking',
                  'banker', 'interest']
    education_set=set(education_ls)
    art_set=set(art_ls)
    technology_set=set(technology_ls)
    finance_set=set(finance_ls)
    with open(twitter_file, "rb") as f:
        with open(f"{output_file_path}_{rank}.json", "a") as output_file:
            output_file.write('[\n')
            count = 0
            for index, item in tqdm(enumerate(ijson.items(f, 'item'))):
                if index % size == rank:
                    lang = item.get('lang')
                    geo = item.get('geo')
                    _id = item.get('_id')
                    month = item.get('month')
                    time_quantum = item.get('time_quantum')
                    text = item.get('text')
                    text_tokens = item.get('text_tokens')
                    sentiment_label = item.get('sentiment_label')
                    polarity = item.get('polarity')
                    if lang == 'en':
                        if len(education_set.intersection(set(text_tokens))) > 0:
                            job_type = 'education'
                        elif len(art_set.intersection(set(text_tokens))) > 0:
                            job_type = 'art'
                        elif len(technology_set.intersection(set(text_tokens))) > 0:
                            job_type = 'technology'
                        elif len(finance_set.intersection(set(text_tokens))) > 0:
                            job_type = 'finance'
                        else:
                            job_type = ''
                        if job_type != '':
                            new_dict = {
                                '_id': _id,
                                'month': month,
                                'time_quantum': time_quantum,
                                'text': text,
                                'text_tokens': text_tokens,
                                'geo': geo,
                                'job_type': job_type,
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
        with open(f'industry_twiiter_{i}.json', 'r') as file:
            data = json.load(file)
            combined_data.extend(data)

    with open(output_file_name, 'w') as output_file:
        json.dump(combined_data, output_file)


def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    twitter_file = 'general_twitter.json'
    output_file_path = 'industry_twiiter'

    process_twitter_data(rank, size, twitter_file, output_file_path)
    comm.Barrier()  # Synchronize all processes

    if rank == 0:  # Only the root process (rank 0) should run the combine_files function
        output_file_name = 'industry_twiiter.json'
        combine_files(8, output_file_name)


if __name__ == '__main__':
    main()
