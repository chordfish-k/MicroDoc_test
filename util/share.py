import enum


class ObjectManager:

    __objDict__ = {}
    
    @staticmethod
    def set(name: str, obj):
        """
        对象存储
        """
        ObjectManager.__objDict__[name] = obj

    @staticmethod
    def get(name: str):
        """
        取得对象
        """
        obj = ObjectManager.__objDict__[name]
        return obj if obj else None
    
        
