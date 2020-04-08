import json
import logging
import time
import uuid
import requests


from jcapi.devices.factory import get_jiachang_device

url = "http://nlu.jiachang8.com/homeassistant/skill"

_LOGGER = logging.getLogger(__name__)


class JcSession:
    devices = []
    accessToken = ""


SESSION = JcSession()


class JiachangApi:
    def init(self, username, password, hicid):
        SESSION.username = username
        SESSION.password = password
        SESSION.token = self.get_mac_address()
        SESSION.hicid = hicid

        if username is None or password is None:
            return None
        else:
            self.refresh_token()
            self.discover_devices()
            return SESSION.devices

    def get_mac_address(self):
        mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
        return "".join([mac[e:e+2] for e in range(0,11,2)])

    def poll_devices_update(self):
        return self.discover_devices()

    def refresh_token(self):
        pass

    def discovery(self):
        response = self._request("Discovery", "discovery")
        if response and response["header"]["code"] == "SUCCESS":
            return response["payload"]["devices"]
        return None

    def discover_devices(self):
        devices = self.discovery()
        if not devices:
            return None
        SESSION.devices = []
        for device in devices:
            SESSION.devices.extend(get_jiachang_device(device, self))
        return devices

    def get_devices_by_type(self, dev_type):
        device_list = []
        for device in SESSION.devices:
            if device.dev_type() == dev_type:
                device_list.append(device)

    def get_all_devices(self):
        return SESSION.devices

    def get_device_by_id(self, dev_id):
        for device in SESSION.devices:
            if device.object_id() == dev_id:
                return device
        return None

    def device_control(self, devId, action, param=None, namespace="control"):
        if param is None:
            param = {}
        response = self._request(action, namespace, devId, param)
        if response and response["header"]["code"] == "SUCCESS":
            success = True
        else:
            success = False
        return success, response

    def _request(self, name, namespace, devId=None, payload={}):
        headers = {"Content-Type": "application/json"}
        header = {"name": name, "namespace": namespace, "payloadVersion": 1}
        payload["accessToken"] = SESSION.accessToken
        if namespace != "discovery":
            payload["devId"] = devId
        data = {"header": header, "payload": payload}
        response = requests.post(url, json=data)
        if not response.ok:
            _LOGGER.warning(
                "request error, status code is %d, device %s",
                response.status_code,
                devId,
            )
            return
        response_json = response.json()
        if response_json["header"]["code"] != "SUCCESS":
            _LOGGER.debug(
                "control device error, error code is " + response_json["header"]["code"]
            )
        return response_json


class JicAPIException(Exception):
    pass


