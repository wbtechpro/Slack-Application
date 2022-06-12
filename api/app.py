import multiprocessing

from flask import Flask, Response
from flask import jsonify, request

from models import ListenWebsocket


dev_mode = False
app = Flask(__name__)


def kill_process():
    for children_process in multiprocessing.active_children():
        p = children_process
        p.kill()

@app.route('/', methods=['POST'])
def head() -> Response:
    """ main page """
    content = request.get_json(silent=True)
    key = content.get('key', '')
    persons_id = content.get('persons_id', '')
    if key == "3h4k13j4521412j3h1fh18s141@4h214h142@!h314h31":
        kill_process() # Очищаем дочерние процессы

        url_websocket_wbt = "https://slack.com/api/rtm.connect?pretty=1&Content-type =application/x-www-form-urlencoded"
        url_websocket_nova = "https://slack.com/api/rtm.connect?pretty=1&Content-type =application/x-www-form-urlencoded"
        bearer_token_wbt = 'xoxb-3762656355-3648818890261-3VMgZC28qkJXlIiMR08bL7sQ'
        bearer_token_nova = 'xoxb-3762656355-3648818890261-3VMgZC28qkJXlIiMR08bL7sQ'
        listen_websocket_wbt = ListenWebsocket(persons_id, url_websocket_wbt, bearer_token_wbt)
        listen_websocket_nova = ListenWebsocket(persons_id, url_websocket_nova, bearer_token_nova)
        wbt_process = multiprocessing.Process(target=listen_websocket_wbt.listen_websocket, args=(),
                                               name="listen_websocket")
        nova_process = multiprocessing.Process(target=listen_websocket_nova.listen_websocket, args=(),
                                               name="listen_websocket")
        wbt_process.start()
        nova_process.start()
        return jsonify("200")

    return jsonify("403")


if __name__ == '__main__':
    """ run multiprocessing app flask """
    app.run(host='0.0.0.0', port=5006, debug=True, use_reloader=False)