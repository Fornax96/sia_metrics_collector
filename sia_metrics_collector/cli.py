"""Functions to support printing messages to the console."""

import datetime
import logging

logger = logging.getLogger(__name__)


def print_header():
    print """
time     latency uploaded  #c  tot $     fees $    store $   u/l $     d/l $
-------- ------- --------- --- --------- --------- --------- --------- ---------
""".strip()


def print_state(state):
    try:
        print _make_console_string(state)
    except Exception as e:
        logger.error('Failed to print to console: %s', e.message)
        return ''


def _make_console_string(state):
    return ('{timestamp} {api_latency:5d}ms {file_uploaded_bytes}'
            ' {contract_count}'
            ' {contract_total_spending}'
            ' {renter_contract_fees}'
            ' {renter_storage_spending} {renter_upload_spending} {renter_download_spending}').format(
                timestamp=_format_timestamp(state),
                api_latency=int(state.api_latency),
                file_uploaded_bytes=_format_bytes(state.file_uploaded_bytes),
                contract_count=_format_contract_count(state.contract_count),
                contract_total_spending=_format_hastings(state.contract_total_spending),
                renter_contract_fees=_format_hastings(state.renter_contract_fees),
                renter_storage_spending=_format_hastings(state.renter_storage_spending),
                renter_upload_spending=_format_hastings(state.renter_upload_spending),
                renter_download_spending=_format_hastings(state.renter_download_spending))


def _format_timestamp(state):
    # Show start of poll, for more regular timestamps.
    return (state.timestamp - datetime.timedelta(milliseconds=state.api_latency)
           ).strftime('%H:%M:%S')


def _format_hastings(hastings):
    if hastings is None:
        return '  -  '
    unit_pairs = [(-27, 'KS'), (-24, 'SC'), (-21, 'mS')]
    for magnitude, suffix in unit_pairs:
        if float(hastings) * pow(10, magnitude) >= 1.0:
            return ('%3.3f%s' % ((float(hastings) * pow(10, magnitude)),
                                 suffix)).rjust(9)
    return '0SC'.rjust(9)


def _format_contract_count(contract_count):
    if contract_count is None:
        return '-  '
    return ('%d' % contract_count).rjust(3)


def _format_bytes(b):
    if b is None:
        return '  - '
    unit_pairs = [(40, 'T'), (30, 'G'), (20, 'M'), (10, 'K'), (0, 'B')]
    for magnitude, suffix in unit_pairs:
        if b >= pow(2, magnitude):
            return ('%4.3f%s' % ((float(b) / pow(2, magnitude)),
                                 suffix)).rjust(9)
    return '0'.rjust(9)
