import sqlite3
class QuotescrapePipeline(object):
    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = sqlite3.connect("quotes.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS quotes_tb""")
        self.curr.execute("""create table quotes_tb(
            quote text,
            author text,
            tags text
        )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""insert into quotes_tb values(?,?,?)""",(
            item['quote'],
            item['author'],
            item['tags'][0]
        ))
        self.conn.commit()
        
