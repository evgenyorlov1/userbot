import logging

from telethon import TelegramClient

import handlers
from argsparse_extra import MergeAction
from manager import Manager, NewMessage
from persistence import load_session_file, save_before_term
from settings import API_HASH, API_ID, NOU_LIST, USERBOT_NAME, USER_PASSWORD, USER_PHONE

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('telethon').setLevel(logging.WARNING)
logging.getLogger('PIL').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

save_before_term()
load_session_file()


def setup(client: TelegramClient):
    m = Manager(client)

    m.add_handler(handlers.handle_help, NewMessage(cmd='', outgoing=True, parser=m.parser))

    with m.add_command('e', "evaluate expression", handlers.calculator) as p:
        p.add_argument('expression', action=MergeAction)

    with m.add_command('s', "find and replace", handlers.sub) as p:
        p.add_argument('a', help='what to replace')
        p.add_argument('b', help='with what replace')

    with m.add_command('t', "timer", handlers.timer) as p:
        p.add_argument('time', help='time is seconds')
        p.add_argument('-m', dest='message', help='message to show after time is up')

    with m.add_command('g', "google search", handlers.google) as p:
        p.add_argument('query', help='query to search', action=MergeAction)
        p.add_argument('-i', dest='image', action='store_true', help='image search')
        p.add_argument('-l', dest='let_me', action='store_true', help='"let me google for you"')

    with m.add_command('m', "magic moon loop", handlers.magic) as p:
        p.add_argument('text', action=MergeAction)
        p.add_argument('-c', dest='count', type=int, default=3, help='number of loops')
        p.add_argument('-w', dest='wide', action='store_true', help='use wide text')

    with m.add_command('mar', "marquee loop", handlers.marquee) as p:
        p.add_argument('text', action=MergeAction)
        p.add_argument('-c', dest='count', type=int, default=3, help='number of loops')

    with m.add_command('h', "highlight text/code block", handlers.highlight_code) as p:
        p.add_argument('text', action=MergeAction)
        p.add_argument('-l', dest='lang', help="programming language")
        p.add_argument('-c', dest='carbon', action='store_true', help="add carbon link")
        p.add_argument('--ln', dest='line_numbers', action='store_true', help="show line numbers")

    with m.add_command('loop_desc', "loop random description", handlers.loop_description):
        pass

    # no u
    nou_pattern = "|".join(NOU_LIST)
    nou_pattern = f'^.*({nou_pattern}).*$'
    m.add_handler(handlers.nou, NewMessage(pattern=nou_pattern))

    m.register_handlers()


def main():
    client = TelegramClient(USERBOT_NAME, API_ID, API_HASH)
    client.parse_mode = 'md'

    logger.info("setting up...")
    setup(client)

    logger.info("starting...")
    client.start(phone=USER_PHONE, password=USER_PASSWORD)
    client.run_until_disconnected()


if __name__ == '__main__':
    main()
