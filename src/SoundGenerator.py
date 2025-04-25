import numpy as np
import sounddevice
import random

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
        self.rate = 48000
        self.param_names = []
        self.params = {}

    def play(self,params:dict[str, float]) -> None:
        '''
        音を再生するメソッド

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

    def play(self, params:dict[str, float]) -> None:
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
        x = (1.+0.4*np.sin(2.*np.pi*am*t))*np.array([pulse(2.*np.pi*freq*t_, dutycycle) for t_ in t])
        # x = Distortion(x, distortion)

        sounddevice.play(x, samplerate=self.rate)
        sounddevice.wait()


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

    def play(self, params:dict[str, float]) -> None:
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
        x = (1.+0.4*np.sin(2.*np.pi*am*t))*np.sin(2.*np.pi*(freq+fm*np.sin(2.*np.pi*1200*t))*t)

        sounddevice.play(x, samplerate=self.rate)
        sounddevice.wait()

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

    def play(self, param:float) -> None:
        '''
        音を再生するメソッド
        Parameters
        ----------
        param : float
            音のパラメータの値 (0.0~1.0)
        '''
        self.sound_gen.play({self.param_name: param})

if __name__ == "__main__":
    # Example usage
    sound_gen = RandomSoundGen()
    sound_gen.sound_gen.duration=0.5
    for i in range(11):
        sound_gen.play(param=i/10.)
