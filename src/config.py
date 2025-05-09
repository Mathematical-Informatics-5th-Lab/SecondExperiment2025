class Config:
    """
    Configuration class for the application.
    """
    WIDTH, HEIGHT = 800, 600
    FRAME_RATE = 60
    CHECK_INTERVAL = 3.0  # 定期チェック間隔（秒）
    WAIT_TIME = 2.0       # 判定時に静止して評価を出す時間（秒）
    REPEAT_COUNT = 5
    THRESHOLD = 0.1       # 成功条件の閾値