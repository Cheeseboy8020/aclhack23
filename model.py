import stable_baselines3
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback
import os
import numpy as np
from stable_baselines3.common.monitor import load_results
from stable_baselines3.common.results_plotter import ts2xy

from gymenv import PiratesEnv


class SaveOnBestTrainingRewardCallback(BaseCallback):
    """
    Callback for saving a model (the check is done every ``check_freq`` steps)
    based on the training reward (in practice, we recommend using ``EvalCallback``).

    :param check_freq:
    :param log_dir: Path to the folder where the model will be saved.
      It must contains the file created by the ``Monitor`` wrapper.
    :param verbose: Verbosity level: 0 for no output, 1 for info messages, 2 for debug messages
    """
    def __init__(self, check_freq: int, log_dir: str, verbose: int = 1):
        super(SaveOnBestTrainingRewardCallback, self).__init__(verbose)
        self.check_freq = check_freq
        self.log_dir = log_dir
        self.save_path = "pirate_model"
        self.best_mean_reward = -np.inf

    def _init_callback(self) -> None:
        pass

    def _on_step(self) -> bool:
        self.model.save(self.save_path)
        return True


env = PiratesEnv('human')
print(stable_baselines3.common.utils.get_device(device='auto'))

model = PPO('MlpPolicy', env)
model.save("pirate_model")
callback = SaveOnBestTrainingRewardCallback(check_freq=100, log_dir="logs/")
model.learn(total_timesteps=100000000, progress_bar=True, callback=callback)
model.save("pirate_model")