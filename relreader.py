import re

import relations


def generate_relation(table_description):
    relation_name, column_descriptions = re.match(r"(\w+)\((.*)\)", table_description[0]).groups()
    columns = []
    if column_descriptions:
        for column_description in column_descriptions.split(","):
            column_description_words = column_description.split()
            if column_description_words[-1] == "K":
                column_is_part_of_key = True
                del (column_description_words[-1])
            columns.append(relations.Column(
                is_part_of_key=check_if_item_exists_and_remove_it(column_description_words, "K"),
                nullable=check_if_item_exists_and_remove_it(column_description_words, "NULL"),
                unique=check_if_item_exists_and_remove_it(column_description_words, "UN"),
                name=column_description_words[0],
                type=column_description_words[1] if len(column_description_words) >= 2 else ""
            ))


def check_if_item_exists_and_remove_it(list, item):
    if item in list:
        list.remove(item)
        return True
    return False


class Reader:
    def __init__(self, file_name):
        self.file_name = file_name

    def read(self):
        relations = []
        for table_description in self.read_table_descriptions():
            relations.append(generate_relation(table_description))

    def read_table_descriptions(self):
        with open(self.file_name) as file_stream:
            lines = file_stream.read().splitlines()
            table_descriptions = []
            first_line_regex = re.compile(r"(\w+\(.*\))")
            assert first_line_regex.match(lines[0]), "la première ligne doit décrire une table"
            for line in lines:
                if first_line_regex.match(line):
                    table_descriptions.append([])
                table_descriptions[-1].append(line)
            return table_descriptions
