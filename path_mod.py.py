#!/usr/bin/env python3

"""
Perform sever $PATH modifications

"""

# bugs and hints: lrsklemstein@gmail.com

import argparse
import logging
import logging.config
import sys

from typing import Any, Dict, Callable  # , List, Tuple

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
    _asp = subparsers.add_parser

    parser_unique = _asp('unique', help='delete redundant entries (keep order)')

    parser_filter = _asp('filter', help='filter out entries specified by regex')
    parser_filter.add_argument('regex', help='regex to specify the entry to be filtered out')

    parser_filter = _asp('reorder', help='reorder entry by spec')
    parser_filter.add_argument('entry', help='the $PATH entry to be reordered')
    parser_filter.add_argument('pos', help=(
        'position description where to move to, must follow the pattern: '
        '{{before|after} ENTRY|(first|last)}'
    ))

    args = vars(parser.parse_args())
    args = {k: '' if v is None else v for k, v in args.items()}

    return args


def runner_unique(setup: Dict[str, any]) -> int:
    print('unique')
    return 0


def runner_filter(setup: Dict[str, any]) -> int:
    print('filter')
    return 0


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

    #
    # this is the entry point for what your program actually does...
    #

    logger.info('Done something...')

    return 0


if __name__ == '__main__':
    main()
