from sys import maxsize

from py_stringsimjoin.index.index import Index


class SizeIndex(Index):
    def __init__(self, table, index_attr, tokenizer):
        self.table = table
        self.index_attr = index_attr
        self.tokenizer = tokenizer
        self.index = None
        self.min_length = maxsize
        self.max_length = 0
        super(self.__class__, self).__init__()

    def build(self, cache_empty_records=True):
        self.index = {}
        empty_records = []
        row_id = 0
        for row in self.table:
            index_string = row[self.index_attr]
            num_tokens = len(self.tokenizer.tokenize(index_string))

            if num_tokens < self.min_length:
                self.min_length = num_tokens

            if num_tokens > self.max_length:
                self.max_length = num_tokens

            if cache_empty_records and num_tokens == 0:
                empty_records.append(row_id)
           
            if num_tokens == 0:
                row_id += 1
                continue
 
            if self.index.get(num_tokens) is None:
                self.index[num_tokens] = []

            self.index.get(num_tokens).append(row_id)

            row_id += 1  

        return {'empty_records': empty_records}

    def probe(self, num_tokens):
        return self.index.get(num_tokens, [])
