from tornado.gen import coroutine
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError as SocketClosedError
from tornado.tcpserver import TCPServer as BaseTCPServer

TCP_MAX_LENGTH = 1024


class Connection(object):
    _last_send: bytes
    clients = set()

    def __init__(self, stream, address, protocol):
        Connection.clients.add(self)
        self._stream = stream
        self._address = address
        self._protocol = protocol()
        self._stream.set_close_callback(self.on_close)
        self.read_message()
        print("A new client has connected the server.", address)

    def on_close(self):
        print("A client has disconnect the server.", self._address)
        Connection.clients.remove(self)

    def read_message(self):
        self._stream.read_bytes(TCP_MAX_LENGTH, self.read_messages_handle, partial=True)
        # self._stream.read_until('\n', self.broadcast_messages)

    def send_message(self, data):
        self._last_send = data
        try:
            self._stream.write(data, self.send_messages_handle)
        except SocketClosedError:
            # todo 判断连接是否断开，如果未断开则断开连接
            pass

    @coroutine
    def read_messages_handle(self, data):
        self.read_message()
        yield self.log_messages('read', data)
        if self._protocol:
            data = yield self._protocol.handle(data)
            self.send_message(data)

    @coroutine
    def send_messages_handle(self):
        yield self.log_messages('send', self._last_send)

    @coroutine
    def log_messages(self, ty, data):
        print("{} {}:{}".format(self._address, ty, data))


class TCPServer(BaseTCPServer):
    _protocol = None

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, protocol):
        if not hasattr(protocol, 'handle'):
            raise AttributeError("object has no attribute 'handle'")
        self._protocol = protocol

    def handle_stream(self, stream, address):
        print("New connection :", address, stream)
        Connection(stream, address, self._protocol)
        print("connection num is:", len(Connection.clients))

    def run_forever(self, port):
        """

        :type port: int
        :param port: 监听端口
        :return:
        """
        self.listen(port)
        IOLoop.instance().start()


if __name__ == '__main__':
    print("Server start ......")
    server = TCPServer()
    server.run_forever(8000)
