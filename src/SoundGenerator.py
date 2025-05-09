import numpy as np
import random
import pyaudio
import struct
import threading
import pygame


class SoundGen:
    """
    音を生成するための基底クラス

    Attributes
    ----------
    duration : float
        音の長さ(秒)
    rate : int
        サンプリングレート
    param_names : list[str]
        音のパラメータの名前
    params : dict[str, float]
        音のパラメータの値
    """

    def __init__(self) -> None:
        self.duration = 1.0
        self.rate = 44100
        self.param_names = []
        self.params = {}
        self.amplitude = 0.3  # 振幅を0.3に調整
        self.buffer_size = 1024  # バッファサイズを1024に増加
        self.phase = 0.0  # 基本位相
        self.am_phase = 0.0  # AM変調の位相
        self.fm_phase = 0.0  # FM変調の位相
        self.last_am_freq = 0.0  # 前回のAM周波数を保存

    def reset_phase(self) -> None:
        """位相をリセット"""
        self.phase = 0.0
        self.am_phase = 0.0
        self.fm_phase = 0.0
        self.last_am_freq = 0.0

    def generate_buffer(self, params: dict[str, float]) -> np.ndarray:
        """
        バッファサイズ分の音声データを生成するメソッド

        Parameters
        ----------
        params : dict[str, float]
            音のパラメータの値

        Returns
        -------
        np.ndarray
            生成された音声データ
        """
        pass


class PulseGen(SoundGen):
    """
    パルス音を生成するクラス
    Attributes
    ----------
    duration : float
        音の長さ(秒)
    rate : int
        サンプリングレート
    param_names : list[str]
        音のパラメータの名前
    params : dict[str, float]
        音のパラメータの値
    """

    def __init__(self) -> None:
        super().__init__()
        self.param_names = ["frequency", "dutycycle", "AM"]
        self.params = {
            "frequency": 0.5,
            "dutycycle": 0.0,
            "AM": 0.0,
        }
        self.last_freq = 220.0  # 前回の周波数を保存

    def reset_phase(self, initial_params: dict[str, float] | None = None) -> None:
        """位相をリセット

        Parameters
        ----------
        initial_params : dict[str, float] | None, optional
            初期パラメータ。指定しない場合はデフォルト値を使用
        """
        super().reset_phase()
        if initial_params is not None and "frequency" in initial_params:
            freq = 220 * (4 ** initial_params["frequency"])
            self.last_freq = freq
        else:
            self.last_freq = 440.0

    def generate_buffer(self, params: dict[str, float]) -> np.ndarray:
        # パラメータを更新
        for key in params:
            if key in self.params:
                self.params[key] = params[key]

        # パラメータを計算
        freq = 220 * (4 ** self.params["frequency"])
        dutycycle = 0.5 + 0.45 * self.params["dutycycle"]
        am = 10 * (2 ** self.params["AM"] - 1)

        # 周波数の変化を滑らかにする
        freq = self.last_freq + (freq - self.last_freq) * 0.1
        self.last_freq = freq

        # 時間配列を生成
        x = np.arange(self.buffer_size)
        phase_increment = 2.0 * np.pi * freq / self.rate
        t = self.phase + phase_increment * x
        t = t - np.trunc(t / (2.0 * np.pi)) * (2.0 * np.pi)  # 位相を0-2πの範囲に正規化
        t = t / (2.0 * np.pi)  # 位相を0-1の範囲に変換

        # パルス波を生成
        wave = np.where(t < dutycycle, 1.0, -1.0)

        # AM変調を適用
        if am != 0:
            am_freq = am
            am_phase_increment = 2.0 * np.pi * am_freq / self.rate
            am_phase = self.am_phase + am_phase_increment * x
            am_envelope = 1.0 + 0.3 * np.sin(am_phase)
            wave = wave * am_envelope
            self.am_phase += am_phase_increment * self.buffer_size
            self.last_am_freq = am_freq

        # 位相を更新
        self.phase += phase_increment * self.buffer_size
        self.phase = self.phase % (2.0 * np.pi)  # 位相を0-2πの範囲に保持

        return wave * self.amplitude


class SineGen(SoundGen):
    """
    サイン波音を生成するクラス
    Attributes
    ----------
    duration : float
        音の長さ(秒)
    rate : int
        サンプリングレート
    param_names : list[str]
        音のパラメータの名前
    params : dict[str, float]
        音のパラメータの値
    """

    def __init__(self) -> None:
        super().__init__()
        self.param_names = ["frequency", "FM", "AM"]
        self.params = {
            "frequency": 0.5,
            "FM": 0.0,
            "AM": 0.0,
        }
        self.last_freq = 440.0  # 前回の周波数を保存
        self.mod_freq = 1200.0  # 変調波の周波数（1200Hz）
        self.phase = 0.0  # 基本位相
        self.mod_phase = 0.0  # 変調波の位相
        self.am_phase = 0.0  # AM変調の位相
        self.amplitude = 1.0  # 振幅を1.0に増加

    def reset_phase(self, initial_params: dict[str, float] | None = None) -> None:
        """位相をリセット

        Parameters
        ----------
        initial_params : dict[str, float] | None, optional
            初期パラメータ。指定しない場合はデフォルト値を使用
        """
        super().reset_phase()
        if initial_params is not None and "frequency" in initial_params:
            freq = 220 * (4 ** initial_params["frequency"])
            self.last_freq = freq
        else:
            self.last_freq = 440.0
        self.phase = 0.0
        self.mod_phase = 0.0
        self.am_phase = 0.0

    def generate_buffer(self, params: dict[str, float]) -> np.ndarray:
        # パラメータを更新
        for key in params:
            if key in self.params:
                self.params[key] = params[key]

        # パラメータを計算
        target_freq = 220 * (
            4 ** self.params["frequency"]
        )  # frequencyが0のとき220Hz、1のとき880Hz
        fm = self.params["FM"]  # FMの強度
        am = 10 * (2 ** self.params["AM"] - 1)

        # 周波数の変化を滑らかにする
        freq = self.last_freq + (target_freq - self.last_freq) * 0.1
        self.last_freq = freq

        # 時間配列を生成
        x = np.arange(self.buffer_size)
        t = x / self.rate  # 時間配列

        # 波形を生成
        if abs(fm) <= 0.001:  # FM変調なし
            # 基本波形のみを生成
            phase_increment = 2.0 * np.pi * freq / self.rate
            phase = self.phase + phase_increment * x
            wave = np.sin(phase)
            self.phase += phase_increment * self.buffer_size
            self.phase = self.phase % (2.0 * np.pi)
        else:  # FM変調あり
            # 変調波の位相を計算
            mod_phase_increment = 2.0 * np.pi * self.mod_freq / self.rate
            mod_phase = self.mod_phase + mod_phase_increment * x
            mod_wave = np.sin(mod_phase)
            self.mod_phase += mod_phase_increment * self.buffer_size
            self.mod_phase = self.mod_phase % (2.0 * np.pi)

            # 搬送波の位相を計算（FM変調を適用）
            phase_increment = 2.0 * np.pi * freq / self.rate
            phase = self.phase + phase_increment * x
            carrier_phase = phase + fm * mod_wave
            wave = np.sin(carrier_phase)
            self.phase += phase_increment * self.buffer_size
            self.phase = self.phase % (2.0 * np.pi)

        # AM変調を適用
        if abs(am) > 0.001:  # AM変調あり
            am_phase_increment = 2.0 * np.pi * am / self.rate
            am_phase = self.am_phase + am_phase_increment * x
            am_envelope = 1.0 + 0.3 * np.sin(am_phase)
            wave = wave * am_envelope
            self.am_phase += am_phase_increment * self.buffer_size
            self.am_phase = self.am_phase % (2.0 * np.pi)

        return wave * self.amplitude


class RandomSoundGen:
    """
    ランダムな音を生成するクラス
    Attributes
    ----------
    sound_name : str
        音の名前
    sound_gen : SoundGen
        SoundGenのサブクラスのインスタンス
    param_name : str
        音のパラメータの名前
    """

    def __init__(self) -> None:
        sound_gen_list = [
            "PulseGen",
            "SineGen",
        ]
        self.sound_name = random.choice(sound_gen_list)
        if self.sound_name == "PulseGen":
            self.sound_gen = PulseGen()
        elif self.sound_name == "SineGen":
            self.sound_gen = SineGen()
        else:
            raise ValueError("Invalid sound generator name")
        self.param_name = random.choice(self.sound_gen.param_names)

    def generate(self, param: float) -> pygame.mixer.Sound:
        """
        音を生成するメソッド
        Parameters
        ----------
        param : float
            音のパラメータの値 (0.0~1.0)
        """
        return self.sound_gen.generate({self.param_name: param})

    def set_sample_rate(self, rate: int) -> None:
        """
        サンプリングレートを設定するメソッド
        Parameters
        ----------
        rate : int
            サンプリングレート
        """
        self.sound_gen.rate = rate

    def get_sample_rate(self) -> int:
        """
        サンプリングレートを取得するメソッド
        Returns
        -------
        int
            サンプリングレート
        """
        return self.sound_gen.rate

    def set_duration(self, duration: float) -> None:
        """
        音の長さを設定するメソッド
        Parameters
        ----------
        duration : float
            音の長さ(秒)
        """
        self.sound_gen.duration = duration


class ContinuousSoundPlayer:
    def __init__(self, sound_gen: SoundGen) -> None:
        self.sound_gen = sound_gen
        self.running = False
        self.current_params = sound_gen.params.copy()
        self.target_params = sound_gen.params.copy()
        self.interpolation_speed = 0.1  # 補間速度を調整
        self.audio_thread = None
        self.p = None
        self.stream = None

    def start(self, initial_params: dict[str, float] | None = None) -> None:
        """音声再生を開始

        Parameters
        ----------
        initial_params : dict[str, float] | None, optional
            初期パラメータ。指定しない場合はsound_genのデフォルト値を使用
        """
        self.running = True
        self.sound_gen.reset_phase(
            initial_params
        )  # 開始時に位相をリセット（初期パラメータを渡す）

        # 初期パラメータを設定
        if initial_params is not None:
            for key in initial_params:
                if key in self.current_params:
                    self.current_params[key] = initial_params[key]
                    self.target_params[key] = initial_params[key]

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sound_gen.rate,
            output=True,
            frames_per_buffer=self.sound_gen.buffer_size,
        )
        self.audio_thread = threading.Thread(target=self._audio_loop)
        self.audio_thread.daemon = True
        self.audio_thread.start()

    def stop(self) -> None:
        """音声再生を停止"""
        self.running = False
        if self.audio_thread:
            self.audio_thread.join()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.p:
            self.p.terminate()
        self.sound_gen.reset_phase()  # 停止時に位相をリセット

    def update_params(self, params: dict[str, float]) -> None:
        """パラメータを更新（指定されたパラメータのみ）"""
        for key in params:
            if key in self.target_params:
                self.target_params[key] = params[key]
                # 現在値も即座に更新（補間を避ける）
                self.current_params[key] = params[key]

    def _audio_loop(self) -> None:
        """音声生成と再生のループ"""
        while self.running:
            try:
                # パラメータの補間
                for key in self.current_params:
                    self.current_params[key] += (
                        self.target_params[key] - self.current_params[key]
                    ) * self.interpolation_speed

                # 音声データを生成
                wave = self.sound_gen.generate_buffer(self.current_params)

                # 音声データを再生
                self.stream.write(wave.astype(np.float32).tobytes())

            except Exception as e:
                print(f"Error in audio loop: {e}")
                self.running = False  # エラーが発生したら停止


class RandomSoundPlayer:
    def __init__(self) -> None:
        self.sound_gen = RandomSoundGen()
        self.player = ContinuousSoundPlayer(self.sound_gen.sound_gen)
        self.param_name = self.sound_gen.param_name

    def start(self, param: float | None = None) -> None:
        """音声再生を開始"""
        self.player.start({self.param_name: param})

    def stop(self) -> None:
        """音声再生を停止"""
        self.player.stop()

    def update_param(self, value: float) -> None:
        """パラメータを更新

        Parameters
        ----------
        value : float
            パラメータの値 (0.0~1.0)
        """
        self.player.update_params({self.param_name: value})

    def get_sound_info(self) -> tuple[str, str]:
        """音源の情報を取得

        Returns
        -------
        tuple[str, str]
            (音源名, パラメータ名)
        """
        return self.sound_gen.sound_name, self.param_name


if __name__ == "__main__":
    # ランダムな音源とパラメータでプレイヤーを作成
    player = RandomSoundPlayer()

    # 音源情報を表示
    sound_name, param_name = player.get_sound_info()
    print(f"音源: {sound_name}")
    print(f"パラメータ: {param_name}")

    # 音声再生を開始
    player.start(0.0)  # 最初のパラメータは指定しなくても良いが、指定することを推奨

    try:
        # パラメータを徐々に変更
        for i in range(101):
            player.update_param(i / 100.0)  # 0.0~1.0の範囲でパラメータを変更
            pygame.time.delay(50)  # 50ミリ秒待機
    except KeyboardInterrupt:
        pass
    finally:
        player.stop()
