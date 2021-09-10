from django.conf import settings

import happybase


class HBaseClient:
    conn = None

    @classmethod
    def get_connection(cls):
        # singleton: if there's a connection exist. use the connection
        if cls.conn:
            return cls.conn
        cls.conn = happybase.Connection(settings.HBASE_HOST)
        return cls.conn
