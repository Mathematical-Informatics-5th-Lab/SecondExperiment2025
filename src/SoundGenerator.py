import numpy as np
import random
import pygame  # type: ignore

class SoundGen:
    '''
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
    '''
    def __init__(self) -> None:
        self.duration = 1.0
        self.rate = 44100
        self.param_names = []
        self.params = {}
        self.amplitude = 22000
        self.t_start = 0.0

    def generate(self,params:dict[str, float]) -> pygame.mixer.Sound:
        '''
        音を生成するメソッド

        Parameters
        ----------
        params : dict[str, float]
            音のパラメータの値
        '''
        pass

class PulseGen(SoundGen):
    '''
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
    '''
    def __init__(self) -> None:
        super().__init__()
        self.param_names = ['frequency', 'dutycycle', 'AM']
        self.params = {
            'frequency': 0.5,
            'dutycycle': 0.0,
            'AM': 0.0,
        }
        self.phase = 0.0
        self.AM_phase = 0.0

    def generate(self, params:dict[str, float]) -> pygame.mixer.Sound:
        # update parameters
        for key in params:
            if key in self.params:
                self.params[key] = params[key]
        # parameters
        freq = 220*(4**self.params['frequency'])
        dutycycle = 0.95*np.log2(self.params['dutycycle']+1)
        am = 20*(2**self.params['AM']-1)
        # distortion = self.params['distortion']

        def pulse(phi:float, dutycycle:float) -> float:
            # normalize phi to [0, 2*pi]
            phi = phi % (2.*np.pi)
            # create pulse
            if phi < 2.*np.pi*(1+dutycycle)/2.:
                return 0.5
            else:
                return -0.5
        t = np.linspace(0., self.duration, int(self.rate*self.duration))
        waveform = self.amplitude*(1.+0.4*np.sin(2.*np.pi*am*t+self.AM_phase))*np.array([pulse(2.*np.pi*freq*t_+self.phase, dutycycle) for t_ in t])
        self.phase += 2.*np.pi*freq*self.duration
        self.AM_phase += 2.*np.pi*am*self.duration
        # x = Distortion(x, distortion)
        waveform = waveform.astype(np.int16)
        waveform_stereo = np.column_stack((waveform, waveform))
        sound = pygame.sndarray.make_sound(waveform_stereo)
        return sound

class SineGen(SoundGen):
    '''
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
    '''
    def __init__(self) -> None:
        super().__init__()
        self.param_names = ['frequency', 'FM', 'AM']
        self.params = {
            'frequency': 0.5,
            'FM': 0.0,
            'AM': 0.0,
            # 'distortion': 0.0,
        }
        self.phase = 0.0
        self.FM_phase = 0.0
        self.AM_phase = 0.0

    def generate(self, params:dict[str, float]) -> pygame.mixer.Sound:
        # update parameters
        for key in params:
            if key in self.params:
                self.params[key] = params[key]
        # parameters
        freq = 220*(4**self.params['frequency'])
        fm = 1.*self.params['FM']
        am = 20*(2**self.params['AM']-1)
        # distortion = self.params['distortion']

        t = np.linspace(0., self.duration, int(self.rate*self.duration))
        waveform = self.amplitude*(1.+0.4*np.sin(2.*np.pi*am*t+self.AM_phase))*np.sin(2.*np.pi*(freq+fm*np.sin(2.*np.pi*1200*t+self.FM_phase))*t+self.phase)
        self.phase += 2.*np.pi*freq*self.duration
        self.FM_phase += 2.*np.pi*fm*self.duration
        self.AM_phase += 2.*np.pi*am*self.duration
        # x = Distortion(x, distortion)
        waveform = waveform.astype(np.int16)
        waveform_stereo = np.column_stack((waveform, waveform))
        sound = pygame.sndarray.make_sound(waveform_stereo)
        return sound

class RandomSoundGen():
    '''
    ランダムな音を生成するクラス
    Attributes
    ----------
    sound_name : str
        音の名前
    sound_gen : SoundGen
        SoundGenのサブクラスのインスタンス
    param_name : str
        音のパラメータの名前
    '''
    def __init__(self) -> None:
        sound_gen_list = [
            'PulseGen',
            'SineGen',
        ]
        self.sound_name = random.choice(sound_gen_list)
        if self.sound_name == 'PulseGen':
            self.sound_gen = PulseGen()
        elif self.sound_name == 'SineGen':
            self.sound_gen = SineGen()
        else:
            raise ValueError("Invalid sound generator name")
        self.param_name = random.choice(self.sound_gen.param_names)

    def generate(self, param:float) -> pygame.mixer.Sound:
        '''
        音を生成するメソッド
        Parameters
        ----------
        param : float
            音のパラメータの値 (0.0~1.0)
        '''
        return self.sound_gen.generate({self.param_name: param})

    def set_sample_rate(self, rate:int) -> None:
        '''
        サンプリングレートを設定するメソッド
        Parameters
        ----------
        rate : int
            サンプリングレート
        '''
        self.sound_gen.rate = rate

    def get_sample_rate(self) -> int:
        '''
        サンプリングレートを取得するメソッド
        Returns
        -------
        int
            サンプリングレート
        '''
        return self.sound_gen.rate

    def set_duration(self, duration:float) -> None:
        '''
        音の長さを設定するメソッド
        Parameters
        ----------
        duration : float
            音の長さ(秒)
        '''
        self.sound_gen.duration = duration

if __name__ == "__main__":
    # Example usage
    sound_gen = RandomSoundGen() # ランダムな音を生成するクラスのインスタンスを作成
    sound_gen.set_duration(0.1) # 音の長さを0.5秒に設定

    pygame.mixer.pre_init(frequency=sound_gen.get_sample_rate(), size=-16, channels=2) # サンプリングレートを設定
    pygame.init() # pygameの初期化

    print(f"sound_name: {sound_gen.sound_name}")
    print(f"param_name: {sound_gen.param_name}")
    for i in range(101):
        sound = sound_gen.generate(param=i/100.) # 音のパラメータの値を0.0~1.0の範囲で生成
        sound.play() # 音を再生
        pygame.time.delay(100) # 600ミリ秒待機
