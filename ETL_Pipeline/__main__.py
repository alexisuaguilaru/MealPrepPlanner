import asyncio
import logging

from .Mains import MainExtraction , MainLoad

from .Logger import ColorFormatter

_logger = logging.getLogger(' ETL Pipeline ')
_logger.propagate = False
    
handler_cli = logging.StreamHandler()
handler_cli.setFormatter(ColorFormatter())
_logger.addHandler(handler_cli)

logging.basicConfig(level = logging.INFO)

if __name__ == '__main__':
    _logger.info('No issues with imports')
    
    # MainExtraction(_logger)

    MainLoad(_logger)

    _logger.info('No issues found')