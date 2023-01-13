from gym.envs.registration import register

register(
    id='pig-v0',
    entry_point='pig.envs:SushiGoEnv',
)

