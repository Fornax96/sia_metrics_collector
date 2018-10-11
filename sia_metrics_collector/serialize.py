import csv

# Constant for Python's file seek() function.
_FROM_FILE_END = 2


class CsvSerializer(object):
    """Serializes SiaState to a CSV file."""

    def __init__(self, csv_file):
        """Creates a serializer, wriiting to the given file.

        Args:
            csv_file: Output file to write CSV to. If file is empty,
                CsvSerializer will write a header row. Caller must open the file
                in either 'w' or 'r+' mode, as 'a' will not let us detect
                whether to write a header on Windows.
        """
        _seek_to_end_of_file(csv_file)
        is_empty_file = _is_empty_file(csv_file)
        self._csv_file = csv_file
        self._csv_writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                'timestamp',
                'api_latency',
                'file_count',
                'file_total_bytes',
                'file_uploads_in_progress_count',
                'file_uploaded_bytes',
                'contract_count_active',
                'contract_count_inactive',
                'contract_total_size',
                'contract_total_spending',
                'contract_fee_spending',
                'contract_storage_spending',
                'contract_upload_spending',
                'contract_download_spending',
                'contract_remaining_funds',
                'wallet_siacoin_balance',
                'wallet_outgoing_siacoins',
                'wallet_incoming_siacoins',
                'renter_allowance',
                'renter_contract_fees',
                'renter_total_allocated',
                'renter_contract_spending',
                'renter_download_spending',
                'renter_storage_spending',
                'renter_upload_spending',
                'renter_unspent',
            ],
            lineterminator='\n')
        if is_empty_file:
            self._csv_writer.writeheader()

    def write_state(self, state):
        self._csv_writer.writerow(_state_to_dict(state))
        self._csv_file.flush()


def _seek_to_end_of_file(file_handle):
    file_handle.seek(0, _FROM_FILE_END)


def _is_empty_file(file_handle):
    return file_handle.tell() == 0


def _state_to_dict(state):
    d = state.as_dict()
    d['timestamp'] = state.timestamp.strftime('%Y-%m-%dT%H:%M:%S')
    return d
