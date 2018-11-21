import requests

def request_patch(slf, *args, **kwargs):
    print("Fix called")
    timeout = kwargs.pop('timeout', 2)
    return slf.request_orig(*args, **kwargs, timeout=timeout)

setattr(requests.sessions.Session, 'request_orig', requests.sessions.Session.request)
requests.sessions.Session.request = request_patch

