class CountShiftException(Exception):

    def __init__(self, msg = "Уже существует открытая смена. Чтобы открыть новую закройте активную"):
        self.msg = msg

    def __repr__(self):
        return f"{self.__class__.__name__}: {self.msg}"
