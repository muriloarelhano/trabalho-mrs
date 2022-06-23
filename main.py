from gitter.processing.parallel import parallelize
import pandas as pd
import multiprocessing as mp

from gitter.preprocessing.messages import apply_messages_pre_processing, process_messages
from gitter.processing.sentence import apply_sentimental_analysis
from gitter.scraper import GitterScraper

if __name__ == '__main__':

    try:
        scraper = GitterScraper(
            "62fe76c279230fbd70415c924fef5d1b26f1aec7", "555f74e315522ed4b3e0ce42"
        )
        messages = scraper.get_messages(20, 20)

    except ValueError:
        print(f'Error with gitter API')

    # Create Dataframe
    remove_columns = ["text", "status", "v", "editedAt",
                      "threadMessageCount", "readBy", "unread"]

    messages_df = pd.DataFrame(process_messages(messages)).drop(
        columns=remove_columns, errors="ignore")

    messages_df.rename(columns={'html': 'sentence'}, inplace=True)

    print(messages_df.head(5))

    n_cpu = mp.cpu_count() - 1

    print('Init apply_messages_pre_processing: ')
    messages_df = parallelize(
        messages_df, apply_messages_pre_processing, n_cpu)

    # messages_df.to_csv('./data/dataset.csv', index=False)

    # messages_df = pd.read_csv('./data/dataset.csv', )
    # print(messages_df.head(5))

    # print('Init apply_sentimental_analysis: ')
    # result_df = parallelize(messages_df, apply_sentimental_analysis, n_cpu)

    # result_df.to_csv('./data/result_dataset.csv', index=False)

    # print(result_df.head(20))
