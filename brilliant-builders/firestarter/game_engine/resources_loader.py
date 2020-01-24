import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from firestarter.game_engine.sprite import SpriteConfig

from kivy.core.image import Image as CoreImage
from kivy.logger import Logger

import toml

RESOURCE_DIR = (Path('.') / 'firestarter' / 'resources').absolute()
RESOURCE_TYPES = ['sprites']


def load_sprite(folder_path: Path, sp: str) -> Optional[SpriteConfig]:
    if sp.rsplit('.', 1)[-1] != 'png':
        return  # It is probably a config file, not loading it

    config_file = (folder_path / sp.rsplit('.', 1)[0]).as_posix() + '_config.toml'
    sp_path = folder_path / sp

    if not os.path.exists(config_file):
        Logger.error(f"Engine: No configuration file found for {sp}, not loading it.")
        return

    texture = CoreImage(sp_path.as_posix()).texture
    texture.mag_filter = 'nearest'

    with open(config_file) as f:
        config_dict = toml.load(f)

    config = SpriteConfig(
        sp_path,
        texture,
        config_dict['size'],
        len(config_dict['animation']),
        [an['length'] for an in config_dict['animation']]
    )
    return config


def load_resources() -> List[Dict[str, Any]]:
    """Generate a list of loaded resources."""
    loaded_resources_list = []

    for rtype in RESOURCE_TYPES:
        loaded_resources = {}
        resource_dir_path = RESOURCE_DIR / rtype

        for resource in os.listdir(resource_dir_path):
            Logger.debug(f"Engine: Loading {resource_dir_path / resource}")
            loaded = LOADER_MAPPING[rtype](resource_dir_path, resource)
            if loaded:
                loaded_resources[resource.rsplit('.', 1)[0]] = loaded

        loaded_resources_list.append(loaded_resources)
    return loaded_resources_list


LOADER_MAPPING = {
    'sprites': load_sprite
}
