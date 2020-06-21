import datetime
import logging
from urllib.parse import urljoin
import requests


def get_logger(logger_name):
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

    def __init__(self, username, password, account_number, logger=None):
        self.username = username
        self.password = password
        self.log = get_logger(self.__class__.__name__) if logger is None else logger
        self.account_number = account_number

    def send_request(self, prepared_request):
        session = requests.Session()
        response = session.send(request=prepared_request)

        try:
            return response.json()

        except Exception as e:
            self.log.error(e)

    def _request_authenticate(self):
        auth_end_point = "Auth/Authenticate"
        auth = {"username": self.username, "password": self.password}
        request = requests.Request("POST", urljoin(self.BASE_URL, auth_end_point), json=auth)

        request.headers["Content-Type"] = "application/json; charset=UTF-8"

        return request.prepare()

    def _request_data(self, access_token, start_date, end_date):
        transactions_end_point = "Account/GetAccountTransactions"

        request = requests.Request("GET", urljoin(self.BASE_URL, transactions_end_point))

        request.headers["Content-Type"] = "application/json; charset=UTF-8"
        request.headers["Authorization"] = f"Bearer {access_token}"
        request.params["accountKey"] = f"ACC_090-{self.account_number}"
        request.params["endDate"] = end_date
        request.params["startDate"] = start_date

        return request.prepare()

    def authenticate(self):
        return self.send_request(self._request_authenticate())

    def get_data(self, start_date=None, end_date=None):
        if not start_date:
            start_date = datetime.datetime.now() - datetime.timedelta(days=3 * 365)
        if not end_date:
            end_date = datetime.datetime.now()
        access_token = self.authenticate().get("l")

        transactions = []
        while end_date.year - start_date.year > 0:
            tmp_end_date = end_date.replace(year=start_date.year, month=12, day=31)

            transactions.extend(
                self.send_request(
                    self._request_data(
                        access_token,
                        start_date.strftime(self.DATETIME_FORMAT),
                        tmp_end_date.strftime(self.DATETIME_FORMAT),
                    )
                )
            )

            start_date = start_date.replace(year=start_date.year + 1, month=1, day=1)

        transactions.extend(
            self.send_request(
                self._request_data(
                    access_token, start_date.strftime(self.DATETIME_FORMAT), end_date.strftime(self.DATETIME_FORMAT)
                )
            )
        )

        return transactions
