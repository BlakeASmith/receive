import requests
import receive
import logging
import threading


async def test_receive():

    @receive.get_request("/callback", port=3000, host="localhost")
    async def get_code(request):
        return request.query["code"]

    future = await get_code()

    def make_request():
        response = requests.get("http://localhost:3000/callback?code=test")
        logging.info(response.text)

    thread = threading.Thread(target=make_request)
    thread.daemon = True
    thread.start()

    code = await future

    assert code == "test"
