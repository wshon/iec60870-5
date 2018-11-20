from tornado import gen


class IEC101(object):
    """

    """

    @gen.coroutine
    def handle(self, data):
        """

        :param data:
        :return:
        """
        if data == b'None':
            return None
        yield gen.sleep(5)
        data = b'iec101:' + data
        return data

    pass
