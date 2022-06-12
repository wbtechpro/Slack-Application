import time
import json
import datetime
import requests
import zoneinfo
from websocket import create_connection
from google_service import GoogleSheetsService

class Users:

    def __init__(self, user):
        self.user = user
        self.time_work_day = 0 # время дневного онлайн в слаке преобразуем в float
        self.active = 'away' # активность по умолчанию
        self.start_active_day = datetime.datetime.now()  # время активности по умолчанию
        self.start_away_day = datetime.datetime.now()  # время в офлайне по умолчанию

    def __str__(self):
        return self.user

    def calculate_time_online(self):
        time = self.start_away_day - self.start_active_day
        self.time_work_day += time.total_seconds() # время в секундах


class ListenWebsocket:
    """
        class for listen socket, where check status users and send notificate,
        if 4 users in a hour have status away
    """

    def __init__(self, persons_id, url_websocket, bearer_token):
        self.persons_id = persons_id
        self.time_begin_work = datetime.datetime.now()
        self.url_get_websocket = url_websocket
        self.bearer_token = bearer_token
        self.users_obj_work_time_day = []
        self.zone = zoneinfo.ZoneInfo("Europe/Moscow")
        self.current_date = datetime.datetime.today().date()  # текущая дата по умолчанию

    def get_websocket(self):
        """ get websocket from service """
        headers = {'Authorization': 'Bearer {}'.format(self.bearer_token)}
        response = requests.request("GET", self.url_get_websocket, headers=headers, data={})
        content = response.json()
        return content['url']

    def _send_notificate_if_active_and_list_3(self, user_id):
        """ send notificate when status person active and len list 3"""
        user = {"user": user_id}
        payload = json.dumps(user)
        headers = {'Content-Type': 'application/json'}
        return requests.request("POST", self.url_notificate_if_active_and_list_3, headers=headers, data=payload)

    def get_ws(self, persons_id):
        """ get ws """
        websocket_url = self.get_websocket()
        ws = create_connection(websocket_url)
        time.sleep(1)
        ws.send(json.dumps({

            "type": "presence_sub",
            "ids": persons_id

        }))
        return ws

    def _convert_name_users_in_time_for_write_to_sheet(self):
        """
            Конвертируем все id во время, которое пользователи онлайн в слаке
        """
        list_time_for_write = [] # список времени, упорядоченный как в документе для записи для каждого пользователя
        for user_id in self.persons_id:
            for users_obj in self.users_obj_work_time_day:
                if user_id == users_obj.user:
                    time_work_day = str(datetime.timedelta(seconds=users_obj.time_work_day)) # конвертируем время с секунд
                    list_time_for_write.append(time_work_day) # Записываем
        return list_time_for_write


    def _check_status_for_calculate_online(self, presence, user):
        """
            Проверка для подсчета человека онлайна в день
        """
        user_obj = self._get_item_users_work_day(user)
        if presence == 'active':
            user_obj.active = presence # ставим статус active
            user_obj.start_active_day = datetime.datetime.now() # ставим время когда он начал становится активным
        elif presence == 'away':
            user_obj.active = presence # ставим статус away
            user_obj.start_away_day = datetime.datetime.now()  # ставим время когда он начал становится офлайн
            user_obj.calculate_time_online() # запускаем функцию для подсчета времени
            list_time_for_write = self._convert_name_users_in_time_for_write_to_sheet()
            # Подключаемся к GoogleSheetsService и записываем значения
            service = GoogleSheetsService(self.persons_id)
            service.write_data(list_time_for_write) # Пока что будем записывать каждый раз когда у нас человек уйдет в away

    def create_obj_users(self, persons_id):
        for person_id in persons_id:
            user_obj = Users(person_id)
            self.users_obj_work_time_day.append(user_obj)

    def _get_item_users_work_day(self, user):
        user = [i for i in self.users_obj_work_time_day if i.__str__() == user] # поиск обьекта среди списка обьектов
        return user[0]

    def _reset_users_work_day_time(self):
        for user in self.users_obj_work_time_day:
            user.time_work_day = 0

    def check_current_date(self):
        today_date = datetime.datetime.today().date()
        if today_date != self.current_date:
            print('дата сменилась с {}, на {}'.format(today_date, self.current_date))
            self.current_date = today_date
            self._reset_users_work_day_time()

    def check_status(self, ws):
        """
            check all status and filter
        """
        for i, event in enumerate(ws):
            self.check_current_date() # При прослушивании сокета проверяет дату

            service = GoogleSheetsService(self.persons_id)
            list_time_for_write = self._convert_name_users_in_time_for_write_to_sheet()
            service.write_data(list_time_for_write)  # Записываем данные нового дня

            data = json.loads(event)
            event_type = data.get('type', '')
            now_time = datetime.datetime.now()
            now_time_date = str(datetime.datetime.today().date())
            current_time = now_time.strftime("%H:%M:%S")
            print("Date - {}, Current Time - {}".format(now_time_date, current_time))
            if event_type == 'presence_change' and i > len(self.persons_id) and self.work_time:
                presence = data.get('presence', '')
                user = data.get('user', '')
                print('presence - {}, user - {}'.format(presence, user))
                self._check_status_for_calculate_online(presence, user)

    def listen_websocket(self):
        """
            Start cicle for listen socket
        """
        self.create_obj_users(self.persons_id)
        while True:
            try:
                print('success start')
                ws = self.get_ws(self.persons_id)
                self.check_status(ws)
            except:
                print('error or connect close, we reloading service')
                time.sleep(10)





