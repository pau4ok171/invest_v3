import datetime
from datetime import timedelta

import decouple
from tinkoff.invest import (
    Client,
    RequestError,
    InstrumentIdType,
    InstrumentResponse,
    GetDividendsResponse,
    GetAssetFundamentalsResponse,
    GetAssetFundamentalsRequest,
)
from pprint import pprint

from tinkoff.invest.schemas import GetAssetReportsRequest
from tinkoff.invest.utils import now

TOKEN_API = decouple.config('TINKOFF_KEY')
COMPANY_UID = 'e6123145-9665-43e0-8413-cd61b8aa9b13'


def main():
    try:
        with Client(TOKEN_API) as client:
            execute(client)
    except RequestError as e:
        print(f'[ERROR]: {e}')


def execute(client):
    # main information about instrument
    instrument: InstrumentResponse = client.instruments.get_instrument_by(
        id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID,
        id=COMPANY_UID
    )
    # pprint(instrument)

    # Список дивидендов
    dividends: GetDividendsResponse = client.instruments.get_dividends(
        instrument_id=COMPANY_UID,
        from_=datetime.datetime.utcnow() - timedelta(days=365*30),
        to=datetime.datetime.utcnow(),
    )
    pprint(dividends)

    # fundamentals data
    # fundamentals_request = GetAssetFundamentalsRequest(
    #     assets=[COMPANY_UID]
    # )
    # fundamentals: GetAssetFundamentalsResponse = client.instruments.get_asset_fundamentals(fundamentals_request)
    # pprint(fundamentals)

    # reports_request = GetAssetReportsRequest(
    #     instrument_id=COMPANY_UID,
    #     from_=now() - timedelta(days=120),
    #     to=now()
    # )
    # reports = client.instruments.get_asset_reports(reports_request)
    # pprint(reports)

    # forecast = client.instruments.get_forecast_by(instrument_id=COMPANY_UID)
    # pprint(forecast)


if __name__ == '__main__':
    main()
