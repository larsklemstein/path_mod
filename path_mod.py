#!/usr/bin/env python3

"""
Perform several $PATH modifications

"""

# bugs and hints: lrsklemstein@gmail.com

import argparse
import logging
import logging.config
import os
import re
import sys

from typing import Any, Dict, List

__log_level_default = logging.INFO


def main() -> None:
    setup = get_prog_setup_or_exit_with_usage()

    init_logging(setup)
    logger = logging.getLogger(__name__)

    try:
        sys.exit(run(setup))
    except Exception:
        logger.critical("Abort, rc=3", exc_info=True)
        sys.exit(3)


def get_prog_setup_or_exit_with_usage() -> Dict[str, Any]:
    parser = argparse.ArgumentParser(
                description=get_prog_doc(),
                formatter_class=argparse.RawTextHelpFormatter,
            )

    parser.add_argument('--path', help='the path to be modified (default: $PATH)')

    log_group = parser.add_mutually_exclusive_group()

    log_group.add_argument(
        '--debug', action='store_true',
        help='enable debug log level',
    )

    log_group.add_argument(
        '--log_cfg', dest='log_cfg',
        help='optional logging cfg in ini format',
    )

    subparsers = parser.add_subparsers(dest='subparser_name')
    subparsers.required = True

    _asp = subparsers.add_parser

    parser_unify = _asp('unify', help='delete redundant entries (keep order)')

    parser_filter = _asp('filter', help='filter out entries specified by regex')
    parser_filter.add_argument('regex', help='regex to specify the entry to be filtered out')

    parser_filter.add_argument(
        '--lazy', action='store_true',
        help='regex does not need to be anchored at the beginning'
    )

    parser_reorder = _asp('reorder', help='reorder entry by spec')
    parser_reorder.add_argument(
        'spec', help=(
            'The reorder definition(s), seperated by ;. '
            'Each definition consists of a regex (describing the path item) '
            'and a command which describes the action. '
            'Both are seperated through a :. '
            'Allowed actions are '
            '1=move entry to the first pos., $=move entry to the last pos, '
            '<REGEX=move entry before the first item matching REGEX, '
            '>REGEX=move entry behind the last item matching REGEX.'
            'Examples: "/opt/bin/java:1" (move entry to the end); '
            '"/opt/bin/java:<.*openjdk" '
            '(move entry before the open jdk path entry)'
        )
    )

    args = vars(parser.parse_args())
    args = {k: '' if v is None else v for k, v in args.items()}

    if args['path'] == '':
        args['path'] = os.environ['PATH']

    return args


def get_prog_doc() -> str:
    doc_str = sys.modules['__main__'].__doc__

    if doc_str is not None:
        return doc_str.strip()
    else:
        return '<???>'


def init_logging(setup: Dict[str, Any]) -> None:
    """Creates either a logger by cfg file or a default instance
    with given log level by arg --log_level (otherwise irgnored)
    """
    if setup['log_cfg'] == '':
        if setup['debug']:
            level = logging.DEBUG
            format = '%(levelname)s - %(message)s'
        else:
            level = __log_level_default
            format = '%(message)s'

        logging.basicConfig(level=level, format=format)
    else:
        logging.config.fileConfig(setup['log_cfg'])


def run(setup: Dict[str, Any]) -> int:
    logger = logging.getLogger(__name__)

    cmd = setup['subparser_name']
    logger.debug(f'run() got cmd "{cmd}"')

    path_items = setup['path'].split(':')
    path_items_new = list()

    if cmd == 'filter':
        run_filter(setup, path_items, path_items_new)
    elif cmd == 'unify':
        run_unify(setup, path_items, path_items_new)
    elif cmd == 'reorder':
        run_reorder(setup, path_items, path_items_new)
    else:
        raise NotImplementedError(f'sub command "{cmd}"')

    path_new = ':'.join(path_items_new)
    print(path_new)


def run_filter(
        setup: Dict[str, any],
        path_items: List[str], path_items_new: List[str]):
    logger = logging.getLogger(__name__)

    pattern = re.compile(setup['regex'])

    filter = pattern.search if setup['lazy'] else pattern.match

    for n, e in enumerate(path_items, start=1):
        if not filter(e):
            path_items_new.append(e)
            logger.debug(f'+{e}')
        else:
            logger.debug(f'-{e}')


def run_unify(
        setup: Dict[str, any],
        path_items: List[str], path_items_new: List[str]):
    logger = logging.getLogger(__name__)

    for n, e in enumerate(path_items, start=1):
        if not e in path_items_new:
            path_items_new.append(e)
            logger.debug(f'+{e}')
        else:
            logger.debug(f'-{e}')


def run_reorder(
        setup: Dict[str, any],
        path_items: List[str], path_items_new: List[str]):
    logger = logging.getLogger(__name__)


if __name__ == '__main__':
    main()