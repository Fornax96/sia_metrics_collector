import recordtype
import datetime
import json
import logging

import pysia

logger = logging.getLogger(__name__)


def make_builder(sia_hostname, sia_port):
    """Makes a Builder using production mode defaults."""
    return Builder(pysia.Sia(sia_hostname, sia_port), datetime.datetime.utcnow)


"""Represents a set of Sia metrics at a moment in time.

Note that the timestamp is *roughly* the time these metrics were collected.
It's accurate to within a few seconds, but shouldn't be trusted beyond that,
as different metrics come from different API calls made sequentially, each
with a small amount of latency.

Fields:
    timestamp: Time at which the metrics were collected.
    api_latency: Time (in milliseconds) it took for Sia to respond to
        all API calls.
    file_count: Number of files known to Sia (either partially or
        fully uploaded).
    file_total_bytes: Total size of all files files known to Sia. Not
        all bytes have necessarily been uploaded to Sia yet.
    file_uploads_in_progress_count: Number of uploads currently in progress.
    file_uploaded_bytes: Total number of bytes that have been uploaded
    contract_count_active: Number of active Sia contracts.
    contract_count_inactive: Number of inactive Sia contracts.
    contract_total_size: Total size of all Sia contracts (this should be
        equal to file_uploaded_bytes, but the data come from different
        sources).
        across all files.
    contract_total_spending: Total amount of money (in hastings) spent
        on storage contracts.
    contract_fee_spending: Total amount of money (in hastings) spent on
        contract fees.
    contract_storage_spending: Total amount of money (in hastings) spent on
        storage.
    contract_upload_spending: Total amount of money (in hastings) spent on
        upload bandwidth.
    contract_download_spending: Total amount of money (in hastings) spent on
        download bandwidth.
    contract_remaining_funds: Total amount of money (in hastings) that remain
        unspent across all contracts.
    wallet_siacoin_balance: Current wallet balance of Siacoins (in
        hastings).
    wallet_outgoing_siacoins: Unconfirmed outgoing Siacoins (in hastings).
    wallet_incoming_siacoins: Unconfirmed incoming Siacoins (in hastings).
    renter_allowance: Total renter allowance in hastings.
    renter_contract_fees: Total amount of money spent on fees in hastings.
    renter_total_allocated: Total amount of money the renter has put into
        contracts in hastings.
    renter_contract_spending: Total amount of money spent on contracts in
        hastings.
    renter_download_spending: Total amount of money spent on downloads in
        hastings.
    renter_storage_spending: Total amount of money spent on storage in hastings.
    renter_upload_spending: Total amount of money spent on uploads in hastings.
    renter_unspent: Amount of money the renter hasn't spent yet in hastings.
"""
SiaState = recordtype.recordtype(
    'SiaState', [
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
    default=None)
SiaState.as_dict = SiaState._asdict


class Builder(object):
    """Builds a SiaState object by querying the Sia API."""

    def __init__(self, sia_api, time_fn):
        """Creates a new Builder instance.

        Args:
            sia_api: An implementation of the Sia client API.
            time_fn: A function that returns the current time.
        """
        self._sia_api = sia_api
        self._time_fn = time_fn

    def build(self):
        """Builds a SiaState object representing the current state of Sia."""
        state = SiaState()
        queries_start_time = self._time_fn()
        state_population_fns = (self._populate_contract_metrics,
                                self._populate_file_metrics,
                                self._populate_wallet_metrics,
                                self._populate_renter_metrics,
                                self._populate_timestamp)
        for fn in state_population_fns:
            try:
                fn(state)
            except Exception as e:
                logging.error('Error when calling %s: %s', fn.__name__,
                              e.message)
                continue
        state.api_latency = (
            self._time_fn() - queries_start_time).total_seconds() * 1000.0
        return state

    def _populate_timestamp(self, state):
        state.timestamp = self._time_fn()

    def _populate_contract_metrics(self, state):
        response = self._sia_api.get_renter_contracts()
        if not response or not response.has_key(u'activecontracts'):
            logger.error('Failed to query contracts information: %s',
                         json.dumps(response))
            return

        active_contracts = response[u'activecontracts']
        inactive_contracts = response[u'inactivecontracts']
        state.contract_count_active = len(active_contracts)
        state.contract_count_inactive = len(inactive_contracts)
        state.contract_total_size = 0
        state.contract_total_spending = 0
        state.contract_fee_spending = 0
        state.contract_storage_spending = 0
        state.contract_upload_spending = 0
        state.contract_download_spending = 0
        state.contract_remaining_funds = 0
        for contract in active_contracts + inactive_contracts:
            state.contract_total_size += long(contract[u'size'])
            state.contract_total_spending += long(contract[u'totalcost'])
            state.contract_fee_spending += long(contract[u'fees'])
            state.contract_storage_spending += long(contract[u'StorageSpending'])
            state.contract_upload_spending += long(contract[u'uploadspending'])
            state.contract_download_spending += long(contract[u'downloadspending'])
            state.contract_remaining_funds += long(contract[u'renterfunds'])

    def _populate_file_metrics(self, state):
        response = self._sia_api.get_renter_files()
        if not response or not response.has_key(u'files'):
            logger.error('Failed to query file information: %s',
                         json.dumps(response))
            return
        files = response[u'files']
        state.file_count = 0
        state.file_total_bytes = 0
        state.file_uploaded_bytes = 0
        state.file_uploads_in_progress_count = 0
        if not files:
            return
        for f in files:
            state.file_count += 1
            state.file_total_bytes += long(f[u'filesize']) * (f[u'uploadprogress'] / 100.0)
            state.file_uploaded_bytes += f[u'uploadedbytes']
            if f[u'uploadprogress'] < 100:
                state.file_uploads_in_progress_count += 1

    def _populate_wallet_metrics(self, state):
        response = self._sia_api.get_wallet()
        if not response or not response.has_key(u'confirmedsiacoinbalance'):
            logger.error('Failed to query wallet information: %s',
                         json.dumps(response))
            return
        state.wallet_siacoin_balance = long(response[u'confirmedsiacoinbalance'])
        state.wallet_outgoing_siacoins = long(response[u'unconfirmedoutgoingsiacoins'])
        state.wallet_incoming_siacoins = long(response[u'unconfirmedincomingsiacoins'])

    def _populate_renter_metrics(self, state):
        response = self._sia_api.get_renter()
        if not response or not response.has_key(u'financialmetrics'):
            logger.error('Failed to query renter information: %s',
                         json.dumps(response))
            return
        financialmetrics = response[u'financialmetrics']
        state.renter_allowance = response[u'settings'][u'allowance'][u'funds']
        state.renter_contract_fees = financialmetrics[u'contractfees']
        state.renter_total_allocated = financialmetrics[u'totalallocated']
        state.renter_contract_spending = financialmetrics[u'contractspending']
        state.renter_download_spending = financialmetrics[u'downloadspending']
        state.renter_storage_spending = financialmetrics[u'storagespending']
        state.renter_upload_spending = financialmetrics[u'uploadspending']
        state.renter_unspent = financialmetrics[u'unspent']
