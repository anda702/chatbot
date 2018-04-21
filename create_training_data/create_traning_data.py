import sqlite3
import pandas as pd
from datetime import datetime

time_frames = ['2015-05']

for time_frame in time_frames:
    connection = sqlite3.connect('{}.db'.format(time_frame))
    cursor = connection.cursor()
    limit = 5000
    last_unix = 0
    current_length = limit
    counter = 0
    test_done = False
    while current_length == limit:
        df = pd.read_sql(
            "SELECT * FROM parent_reply WHERE unix > {} AND parent NOT NULL AND score > 0 ORDER BY unix ASC LIMIT {}".format(last_unix, limit), connection)
        last_unix = df.tail(1)['unix'].values[0]
        current_length = len(df)
        if not test_done:
            with open("test.from", 'a', encoding='utf8') as f:
                for content in df['parent'].values:
                    f.write(content + '\n')
            with open("test.to", 'a', encoding='utf8') as f:
                for content in df['comment'].values:
                    f.write(content + '\n')
            test_done = True
        else:
            with open("train.from", 'a', encoding='utf8') as f:
                for content in df['parent'].values:
                    f.write(content + '\n')
            with open("train.to", 'a', encoding='utf8') as f:
                for content in df['comment'].values:
                    f.write(content + '\n')
        counter +=1
        if counter % 20 == 0:
            print(counter*limit, 'rows completed @ {}'.format(str(datetime.now())))
