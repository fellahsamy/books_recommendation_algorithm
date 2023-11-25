import sqlite3
import pandas as pd

cnn = sqlite3.connect('books.db')
books_df = pd.read_csv('processed_books.csv',delimiter="|")
books_df = books_df.drop(columns="id")
var ="isbn|title|author|year|publisher|image_m|image_l|mean_rating|count_rating|reco_1|reco_2|reco_3|reco_4|reco_5|reco_6|reco_7|reco_8|reco_9|reco_10"
var = var.split("|")
books_df.columns = var
books_df.to_sql(name="books", con=cnn, index = False)


