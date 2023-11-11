from typing import List, Any

import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host="localhost", port=6379, password=None)
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


@cache
def find_by_tags(tags: str) -> list[str | None]:
    print(f"Find by {tags}")
    result = []
    tags = tags.lower().strip().split(',')
    for i in tags:
        for quote in Quote.objects(tags=i):
            result.append(quote.to_mongo().to_dict()["quote"].encode("utf-8"))
    return result


COMMANDS = {
    'name': find_by_author,
    'tag': find_by_tag,
    'tags': find_by_tags
}


def command_parser(message: str):
    try:
        command, data = message.lower().split(':')
    except ValueError as error:
        return f'Error: {error}'
    if command.strip() in COMMANDS.keys():
        return COMMANDS.get(command.strip())(data.strip())
    else:
        return 'Wrong command! Try again'


def main():
    while True:
        input_message = input('\nInput command: ')
        if input_message.lower() == 'exit':
            break
        print(command_parser(input_message))


if __name__ == '__main__':
    main()

