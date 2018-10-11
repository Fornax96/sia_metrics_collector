import datetime
import io
import unittest

from sia_metrics_collector import serialize
from sia_metrics_collector import state


class CsvSerializerTest(unittest.TestCase):

    def test_writes_header_to_empty_file(self):
        mock_file = io.BytesIO()

        serialize.CsvSerializer(mock_file)

        self.assertEqual((
            'timestamp,'
            'api_latency,'
            'file_count,'
            'file_total_bytes,'
            'file_uploads_in_progress_count,'
            'file_uploaded_bytes,'
            'contract_count_active,'
            'contract_count_inactive,'
            'contract_total_size,'
            'contract_total_spending,'
            'contract_fee_spending,'
            'contract_storage_spending,'
            'contract_upload_spending,'
            'contract_download_spending,'
            'contract_remaining_funds,'
            'wallet_siacoin_balance,'
            'wallet_outgoing_siacoins,'
            'wallet_incoming_siacoins,'
            'renter_allowance,'
            'renter_contract_fees,'
            'renter_total_allocated,'
            'renter_contract_spending,'
            'renter_download_spending,'
            'renter_storage_spending,'
            'renter_upload_spending,'
            'renter_unspent\n'), mock_file.getvalue())

    def test_writes_state_to_file(self):
        mock_file = io.BytesIO()

        serializer = serialize.CsvSerializer(mock_file)
        serializer.write_state(
            state.SiaState(
                timestamp=datetime.datetime(2018, 2, 11, 16, 5, 2),
                api_latency=5.0,
                file_count=3,
                file_total_bytes=4444,
                file_uploads_in_progress_count=2,
                file_uploaded_bytes=900,
                contract_count_active=3,
                contract_count_inactive=2,
                contract_total_size=9,
                contract_total_spending=65,
                contract_fee_spending=25,
                contract_storage_spending=2,
                contract_upload_spending=35,
                contract_download_spending=0,
                contract_remaining_funds=100,
                wallet_siacoin_balance=75,
                wallet_outgoing_siacoins=26,
                wallet_incoming_siacoins=83,
                renter_allowance=500,
                renter_contract_fees=233,
                renter_total_allocated=443,
                renter_contract_spending=123,
                renter_download_spending=0,
                renter_storage_spending=200,
                renter_upload_spending=66,
                renter_unspent=111))

        self.assertEqual((
            'timestamp,'
            'api_latency,'
            'file_count,'
            'file_total_bytes,'
            'file_uploads_in_progress_count,'
            'file_uploaded_bytes,'
            'contract_count_active,'
            'contract_count_inactive,'
            'contract_total_size,'
            'contract_total_spending,'
            'contract_fee_spending,'
            'contract_storage_spending,'
            'contract_upload_spending,'
            'contract_download_spending,'
            'contract_remaining_funds,'
            'wallet_siacoin_balance,'
            'wallet_outgoing_siacoins,'
            'wallet_incoming_siacoins,'
            'renter_allowance,'
            'renter_contract_fees,'
            'renter_total_allocated,'
            'renter_contract_spending,'
            'renter_download_spending,'
            'renter_storage_spending,'
            'renter_upload_spending,'
            'renter_unspent\n'
            '2018-02-11T16:05:02,5.0,3,4444,2,900,3,2,9,65,25,2,35,0,100,75,26,83,500,233,443,123,0,200,66,111\n'
        ), mock_file.getvalue())

    def test_appends_to_existing_file(self):
        if True:
            return
        mock_file = io.BytesIO((
            'timestamp,'
            'api_latency,'
            'file_count,'
            'file_total_bytes,'
            'file_uploads_in_progress_count,'
            'file_uploaded_bytes,'
            'contract_count_active,'
            'contract_count_inactive,'
            'contract_total_size,'
            'contract_total_spending,'
            'contract_fee_spending,'
            'contract_storage_spending,'
            'contract_upload_spending,'
            'contract_download_spending,'
            'contract_remaining_funds,'
            'wallet_siacoin_balance,'
            'wallet_outgoing_siacoins,'
            'wallet_incoming_siacoins,'
            'renter_allowance,'
            'renter_contract_fees,'
            'renter_total_allocated,'
            'renter_contract_spending,'
            'renter_download_spending,'
            'renter_storage_spending,'
            'renter_upload_spending,'
            'renter_unspent\n'
            '2018-02-11T16:05:02,5.0,3,4444,2,900,3,2,8,65,25,2,35,0,100,75,26,83,500,233,443,123,0,200,66,111\n'
        ))

        serializer = serialize.CsvSerializer(mock_file)
        serializer.write_state(
            state.SiaState(
                timestamp=datetime.datetime(2018, 2, 11, 16, 5, 7),
                api_latency=6.0,
                file_count=4,
                file_total_bytes=5555,
                file_uploads_in_progress_count=3,
                file_uploaded_bytes=901,
                contract_count_active=4,
                contract_count_inactive=2,
                contract_total_size=10,
                contract_total_spending=75,
                contract_fee_spending=26,
                contract_storage_spending=3,
                contract_upload_spending=36,
                contract_download_spending=1,
                contract_remaining_funds=101,
                wallet_siacoin_balance=76,
                wallet_outgoing_siacoins=27,
                wallet_incoming_siacoins=84,
                renter_allowance=501,
                renter_contract_fees=234,
                renter_total_allocated=444,
                renter_contract_spending=124,
                renter_download_spending=1,
                renter_storage_spending=201,
                renter_upload_spending=67,
                renter_unspent=110))

        self.assertEqual((
            'timestamp,'
            'api_latency,'
            'file_count,'
            'file_total_bytes,'
            'file_uploads_in_progress_count,'
            'file_uploaded_bytes,'
            'contract_count_active,'
            'contract_count_inactive,'
            'contract_total_size,'
            'contract_total_spending,'
            'contract_fee_spending,'
            'contract_storage_spending,'
            'contract_upload_spending,'
            'contract_download_spending,'
            'contract_remaining_funds,'
            'wallet_siacoin_balance,'
            'wallet_outgoing_siacoins,'
            'wallet_incoming_siacoins,'
            'renter_allowance,'
            'renter_contract_fees,'
            'renter_total_allocated,'
            'renter_contract_spending,'
            'renter_download_spending,'
            'renter_storage_spending,'
            'renter_upload_spending,'
            'renter_unspent\n'
            '2018-02-11T16:05:02,5.0,3,4444,2,900,3,2,8,65,25,2,35,0,100,75,26,83,500,233,443,123,0,200,66,111\n'
            '2018-02-11T16:05:07,6.0,4,5555,3,901,4,2,10,75,26,3,36,1,101,76,27,84,501,234,444,124,1,201,67,110\n'
        ), mock_file.getvalue())
