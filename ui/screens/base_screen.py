class BaseScreen:
    def __init__(self):
        pass

    def handle_events(self, events):
        """
        Xử lý input
        Return:
            - None (không đổi màn)
            - "GAME", "MENU", "PAUSE"... (đổi màn)
        """
        return None

    def update(self):
        """
        Update trạng thái (KHÔNG chứa logic game lớn)
        """
        pass

    def draw(self, screen):
        """
        Vẽ lên màn hình
        """
        pass