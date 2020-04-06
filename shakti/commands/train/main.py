from shakti.utils.utilities import get_train_dir
from shakti.utils.constants import CPU, GPU, TRAIN_ERROR


def train(model_type, hardware_type=GPU, **kwargs):
    try:
        train_dir = get_train_dir()
    except:
        raise Exception(TRAIN_ERROR)
