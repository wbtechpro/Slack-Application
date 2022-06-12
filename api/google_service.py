import pytz
import httplib2
import json

from datetime import datetime

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery

UTC = pytz.utc
SCOPE=['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
spreadsheetId = '191hiA6AQt5VyZdJtyigWYwiLhFD-Nm5mY6QuCXH9D6c'
CREDENTIALS_DATA = {
  "type": "service_account",
  "project_id": "medium-data-extraction-323209",
  "private_key_id": "f5b0553461c81ab88cddcbfbc6b70565dea7d96d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC4jrl/LrP+2vQ8\nGw6nG5c3mrmfe0CB228C9qVLf3Yj9ArHiClWgsHhJt/Ei2BhfEUI8qWP1qIjrzBr\n3IGU6pSsUxnOq+6rFxxE0IO1ObE2th4okeNReP04GQa2jJJgzKS0DEuhOpH4c6OY\n72u8kVRugWFaUxRRo0AnvgELiG3yAm9Ezev+Mot2qI1zmYIblZnG8kyTqS1mRzin\nVT6AAP6OwUsrB1pKmBqW9FB6CKJxOryzu0n2xBUvw9wuaJj1Af/Anrr0b0chqByQ\nf5xesKZQkhsyKv0Gk5UiY75sjhfGiKXEdeu9PYrlpdXEmLbXiHc+pATK08WvpzZ9\nrnQKdvLjAgMBAAECggEAIAZEEdmcyiBcOQHI7R5QgwmKJC5S5zWYcb8yt4MKkPqL\n1EvAQI637cW9FnHI66GQqRjRub/YqrB/infc1GZQHgbdd4tGAtIjyZ0U/aFhKsk3\nOnr2IvEHn3BYRdzmmX1pJwTrKrLrGV2XibYhz7q4F+TDa9T2taPKQhsqO0IVMeUG\nXbeWwuZ6OkP4mUpyRLIBpuZ+fvZ4jhzg8BMXw2NpKMMaweilsiXSVAPnehb95XSG\nVvpktOxZCwQyGV0T1uPohO4ckrkP/YQ6roPTqSISlybIll230UZIgvgVvh80s51K\nS++FMzKU51IoJLp4Z6yb7R32LEESsyX8D0pOoMDFgQKBgQDymwzMx/kZbcfTrcCc\n6iWLbn31UQ8dMBaICl9jN6l2BzE2BBZYmN4iP6fwYMFzBNO+1C98xSQQV7rt6Cx8\nllqgzkorvdPL7dFyCkh+VIxD/y3y+AdLdEoV4/GyS5h7f/pWgfD8Nlhz6JSpFteA\nNq3iiFVHu6OfqOIL4pjKHpJhMwKBgQDCvzs2kVKiAyfMHR+ARWvzfdH0/MtrUycT\njUqu7Jqa5R1I/uJtmJ1TJ+JQHaJ97uoDSYNvM5UUQYpkMvvKhNa/i/qo8pYEdtPe\nx3El2hvV/8dktkK104XgpSybKWcBJ0PjiZ1P/qkd+CK+2RkSj8/26cVvTMvcdEAY\nv3/27oSHkQKBgQDWq/pkjiLOrISgu2PvtYTpXykX1NVB55ZYZI1JVyydYvnZqT44\nwXP17EvneUZUR5YyisFGb49c4rRm5gXPbJ/fIQsir4NlNRgbCBxjpN7FIF0BXRXf\nX5Ra0GvDb/8KcREMUUjzdAdK8Sfyg2LHchrlk+uaYOAFXERBbg3y86BlXwKBgQCI\nyWj92vT/dtftNkd6AUjhre5a9XSr3awEv6lFVEsDoQoAy4afFCLs1YbQXwBTFAyq\nYmg/IywDHkXmOylABi4QPHHDWSCl4hDO2adPvvLuTMnwo1QYAop2T44VLe97j+jP\nWUl1dpmywyckhbhmoTyhYXGby4UlQ0ICH//xoXbVAQKBgEu/wYUPwGDahhqYet41\ny2e6igFkyPUjV67arq7O1ZJ2pWZK8fk0vYUFWCjYmVeqFW0LxzGGm4F79RzIXXpb\neouAu/69x/iCTvYUcIAVoRQD7CJNtv4VQkolqrC+e6Mm1++NyfEghgZS2sNq0cGZ\neRZa5MK1v9EHc0v4xnZjAX2b\n-----END PRIVATE KEY-----\n",
  "client_email": "acc-509@medium-data-extraction-323209.iam.gserviceaccount.com",
  "client_id": "113744284089133795538",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/acc-509%40medium-data-extraction-323209.iam.gserviceaccount.com"
}

class GoogleSheetsService:
    """ Google sheets service for request data """

    def __init__(self, users_id):
        self.service = self._connect_service()
        self.users_id = users_id

    def _connect_service(self):
        """ cconect in google sheets service """
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(CREDENTIALS_DATA, SCOPE)  # Читаем ключи из файла
        httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
        return discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API

    def create_new_sheet(self, date):
        body = {
                'requests': [{
                    'addSheet': {
                        'properties': {
                            'title': str(date)
                        }
                    }
                }]
            }
        return self.service.spreadsheets().batchUpdate(spreadsheetId=spreadsheetId, body=body).execute()

    @property
    def _all_sheet_titles(self):
        sheet_metadata = self.service.spreadsheets().get(spreadsheetId=spreadsheetId).execute()
        sheets = sheet_metadata.get('sheets', '')
        return sheets

    def _write_users_new_sheet(self):
        date = datetime.today().date()
        body = {
            "valueInputOption": "USER_ENTERED",
            "data": [{
                "range": "{}!A1:Z1".format(str(date)),
                "majorDimension": "ROWS",
                "values": [self.users_id]}]}
        return self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body=body).execute()

    def check_have_today_date_list(self):
        """
             Проверяем имеется ли лист с сегодняшней датой в таблице и если нет, то создает
             В любом из возможных вариантах возвращает id таблицы для записи данных
        """
        sheets = self._all_sheet_titles
        date = datetime.today().date()
        sheet_titles = [sheet.get("properties", {}).get("title") for sheet in sheets]
        if str(date) not in sheet_titles:
            print('Данного листа с текущей датой нет, поэтому создадим новый')
            self.create_new_sheet(date)
            self._write_users_new_sheet()
        else:
            print('такой лист есть.')

    def write_users_time(self, data_time_users):
        date = datetime.today().date()
        body = {
            "valueInputOption": "USER_ENTERED",
            "data": [{
                "range": "{}!A2:Z2".format(str(date)),
                "majorDimension": "ROWS",
                "values": [data_time_users]}]}
        return self.service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, body=body).execute()

    def write_data(self, data_time_users):
        # Записываем данные
        self.check_have_today_date_list() # проверяем листы
        self.write_users_time(data_time_users) # записываем значения




