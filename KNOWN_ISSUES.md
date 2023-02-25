# Known issues

## httpx.LocalProtocolError: Invalid input ConnectionInputs.RECV_WINDOW_UPDATE in state ConnectionState.CLOSED

<details>
  <summary>Logs with traceback</summary>

```log
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | 2023-02-25 03:53:40,053 - ERROR - Error while getting Updates: httpx.LocalProtocolError: Invalid input ConnectionInputs.RECV_WINDOW_UPDATE in state ConnectionState.CLOSED
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | 2023-02-25 03:53:40,054 - ERROR - Exception happened while polling for updates.
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | Traceback (most recent call last):
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/h2/connection.py", line 224, in process_input
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     func, target_state = self._transitions[(self.state, input_)]
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                          ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | KeyError: (<ConnectionState.CLOSED: 3>, <ConnectionInputs.RECV_WINDOW_UPDATE: 13>)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | During handling of the above exception, another exception occurred:
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | Traceback (most recent call last):
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/http2.py", line 112, in handle_async_request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     status, headers = await self._receive_response(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/http2.py", line 229, in _receive_response
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     event = await self._receive_stream_event(request, stream_id)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/http2.py", line 260, in _receive_stream_event
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     await self._receive_events(request, stream_id)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/http2.py", line 281, in _receive_events
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     events = await self._read_incoming_data(request)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/http2.py", line 343, in _read_incoming_data
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     events: typing.List[h2.events.Event] = self._h2_state.receive_data(data)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                                            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/h2/connection.py", line 1463, in receive_data
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     events.extend(self._receive_frame(frame))
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                   ^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/h2/connection.py", line 1487, in _receive_frame
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     frames, events = self._frame_dispatch_table[frame.__class__](frame)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/h2/connection.py", line 1728, in _receive_window_update_frame
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     events = self.state_machine.process_input(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/h2/connection.py", line 228, in process_input
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     raise ProtocolError(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | h2.exceptions.ProtocolError: Invalid input ConnectionInputs.RECV_WINDOW_UPDATE in state ConnectionState.CLOSED
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | During handling of the above exception, another exception occurred:
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | Traceback (most recent call last):
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 60, in map_httpcore_exceptions
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     yield
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 353, in handle_async_request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     resp = await self._pool.handle_async_request(req)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection_pool.py", line 253, in handle_async_request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     raise exc
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection_pool.py", line 237, in handle_async_request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     response = await connection.handle_async_request(request)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/connection.py", line 90, in handle_async_request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     return await self._connection.handle_async_request(request)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpcore/_async/http2.py", line 142, in handle_async_request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     raise LocalProtocolError(exc)  # pragma: nocover
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | httpcore.LocalProtocolError: Invalid input ConnectionInputs.RECV_WINDOW_UPDATE in state ConnectionState.CLOSED
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | The above exception was the direct cause of the following exception:
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | Traceback (most recent call last):
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/request/_httpxrequest.py", line 199, in do_request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     res = await self._client.request(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1533, in request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     return await self.send(request, auth=auth, follow_redirects=follow_redirects)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1620, in send
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     response = await self._send_handling_auth(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1648, in _send_handling_auth
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     response = await self._send_handling_redirects(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1685, in _send_handling_redirects
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     response = await self._send_single_request(request)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_client.py", line 1722, in _send_single_request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     response = await transport.handle_async_request(request)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 352, in handle_async_request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     with map_httpcore_exceptions():
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/contextlib.py", line 155, in __exit__
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     self.gen.throw(typ, value, traceback)
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/httpx/_transports/default.py", line 77, in map_httpcore_exceptions
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     raise mapped_exc(message) from exc
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | httpx.LocalProtocolError: Invalid input ConnectionInputs.RECV_WINDOW_UPDATE in state ConnectionState.CLOSED
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | The above exception was the direct cause of the following exception:
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | Traceback (most recent call last):
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/ext/_updater.py", line 607, in _network_loop_retry
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     if not await action_cb():
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |            ^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/ext/_updater.py", line 335, in polling_action_cb
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     raise exc
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/ext/_updater.py", line 320, in polling_action_cb
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     updates = await self.bot.get_updates(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |               ^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 524, in get_updates
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     updates = await super().get_updates(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |               ^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/_bot.py", line 331, in decorator
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     result = await func(*args, **kwargs)  # skipcq: PYL-E1102
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/_bot.py", line 3510, in get_updates
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     await self._post(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/_bot.py", line 419, in _post
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     return await self._do_post(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |            ^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/ext/_extbot.py", line 306, in _do_post
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     return await super()._do_post(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |            ^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/_bot.py", line 450, in _do_post
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     return await request.post(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |            ^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 165, in post
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     result = await self._request_wrapper(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 288, in _request_wrapper
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     raise exc
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/request/_baserequest.py", line 274, in _request_wrapper
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     code, payload = await self.do_request(
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |                     ^^^^^^^^^^^^^^^^^^^^^^
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |   File "/usr/local/lib/python3.11/site-packages/telegram/request/_httpxrequest.py", line 223, in do_request
gitlab-webhook-telegram-gitlab-webhook-telegram-1  |     raise NetworkError(f"httpx.{err.__class__.__name__}: {err}") from err
gitlab-webhook-telegram-gitlab-webhook-telegram-1  | telegram.error.NetworkError: httpx.LocalProtocolError: Invalid input ConnectionInputs.RECV_WINDOW_UPDATE in state ConnectionState.CLOSED
```

</details>

Issue link: https://github.com/python-telegram-bot/python-telegram-bot/issues/3556
