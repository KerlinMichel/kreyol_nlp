import os
import requests
from urllib.parse import urlparse


# TODO: using __file__ is bad practice
_CORPUS_CACHE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../corpuses')
)

def handle_corpus_src(src,
                      title_of_text_src,
                      use_corpus_cache: bool,
                      copus_cache_file_extension: str,
                      text_encoding = 'utf-8'):
    corpus_cache_file_name = f'{title_of_text_src}.{copus_cache_file_extension}'
    # TODO: using __file__ is bad practice
    corpus_cache_file_path = os.path.join(_CORPUS_CACHE_DIR, corpus_cache_file_name)

    if use_corpus_cache and os.path.exists(corpus_cache_file_path):
        with open(corpus_cache_file_path, 'rb') as corpus_cache_file:
            return corpus_cache_file.read().decode(encoding=text_encoding)

    if type(src) is str and urlparse(src).scheme.lower() in ['http', 'https']:
        response = requests.get(src)
        response.raise_for_status()
        if use_corpus_cache and not os.path.exists(corpus_cache_file_path):
            with open(corpus_cache_file_path, 'wb+') as corpus_cache_file:
                corpus_cache_file.write(requests.get(src).content)
        return requests.get(src).content.decode(encoding=text_encoding)

def parse_group_lines(text: str,
                      group_size: int,
                      group_separator: str = '\n\n',
                      line_separator: str = '\n') -> tuple:
    groups = text.strip().split(group_separator)

    parsed_groups = []
    for group in groups:
        lines_in_group = group.strip().split(line_separator)
        if len(lines_in_group) != group_size:
            raise ValueError(f'Failed to parse {group}')
        lines_in_group = map(str.strip, lines_in_group)
        parsed_groups.append(tuple(lines_in_group))

    return tuple(parsed_groups)