from SQLiteAdapter import SQLiteAdapter

class DBFacade(object):
    """
    Facade that retrieve the right database adapter.
    """
    def __init__(self):
        pass
    def getInstance(self, dbName, dbType):
        if dbType == "sqlite":
            return SQLiteAdapter(dbName)
        else:
            raise Exception("The adapter is not available. Requested adapter: %s", dbName )

