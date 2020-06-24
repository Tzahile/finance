import datetime
from datetime import datetime as dt
import logging
from logging import Logger
from typing import List, Dict
from urllib.parse import urljoin
import requests
from requests import PreparedRequest, Response


def get_logger(logger_name: str) -> Logger:
    logger = logging.getLogger(logger_name)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s %(levelname)s: %(message)s [in %(filename)s:%(lineno)d]")
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    return logger


class PsagotCollector:
    BASE_URL = "https://sparkpsagot.ordernet.co.il/api/"
    DATETIME_FORMAT = "%Y-%m-%dT%H:00:00.000Z"

    def __init__(self, username: str, password: str, account_number: str, logger: Logger = None):
        self.username = username
        self.password = password
        self.log = logger or get_logger(self.__class__.__name__)
        self.account_number = account_number

    @staticmethod
    def send_request(prepared_request: PreparedRequest) -> Response:
        session = requests.Session()
        return session.send(request=prepared_request)

    def _request_authenticate(self) -> PreparedRequest:
        auth_end_point = "Auth/Authenticate"
        auth = {"username": self.username, "password": self.password}
        request = requests.Request("POST", urljoin(self.BASE_URL, auth_end_point), json=auth)

        request.headers["Content-Type"] = "application/json; charset=UTF-8"

        return request.prepare()

    def _request_data(self, access_token: str, start_date: str, end_date: str) -> PreparedRequest:
        transactions_end_point = "Account/GetAccountTransactions"

        request = requests.Request("GET", urljoin(self.BASE_URL, transactions_end_point))

        request.headers["Content-Type"] = "application/json; charset=UTF-8"
        request.headers["Authorization"] = f"Bearer {access_token}"
        request.params["accountKey"] = f"ACC_090-{self.account_number}"
        request.params["endDate"] = end_date
        request.params["startDate"] = start_date

        return request.prepare()

    def authenticate(self) -> Dict[str, str]:
        return self.send_request(self._request_authenticate()).json()

    def get_data(self, start_date: dt = None, end_date: dt = None) -> List[Dict[str, str]]:
        if not start_date:
            start_date = dt.now() - datetime.timedelta(days=3 * 365)
        if not end_date:
            end_date = dt.now()
        access_token = self.authenticate().get("l")
        if access_token is None:
            raise AttributeError("Authentication response is invalid")

        transactions: List[Dict[str, str]] = []
        while end_date.year - start_date.year > 0:
            tmp_end_date = end_date.replace(year=start_date.year, month=12, day=31)

            transactions.extend(
                self.send_request(
                    self._request_data(
                        access_token,
                        start_date.strftime(self.DATETIME_FORMAT),
                        tmp_end_date.strftime(self.DATETIME_FORMAT),
                    )
                ).json()
            )

            start_date = start_date.replace(year=start_date.year + 1, month=1, day=1)

        transactions.extend(
            self.send_request(
                self._request_data(
                    access_token, start_date.strftime(self.DATETIME_FORMAT), end_date.strftime(self.DATETIME_FORMAT)
                )
            ).json()
        )

        return transactions
