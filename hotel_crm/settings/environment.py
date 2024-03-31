import os

import environ

env = environ.Env(DEBUG=(bool, False), ALLOWED_HOSTS=(list, []))

current_path = environ.Path(__file__) - 1
site_root = current_path - 2
env_file = site_root('.env')

if os.path.exists(env_file):
    env.read_env(env_file)
