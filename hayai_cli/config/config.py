import yaml
import functools
from pathlib import Path
from sys import platform
from sys import exit as sys_exit

class SysNotFoundError(Exception):
    pass

class Config:
    def __init__(self):
        self._config_file, self._yaml_conf = Config._read_config()
        
        if not self._yaml_conf:
            self._yaml_conf = {}

    @property
    def _hayai_cli_folder(self):
        return Path(Path(__file__).parent)

    @property
    def download_folder_path(self):
        return self._get_path_value(
            "download_folder_path", self._hayai_cli_folder / "download"
        )

    @property
    def player_path(self):
        return self._get_value("player_path", "mpv", str)

    @property
    def mpv_commandline_options(self):
        return self._get_value("mpv_commandline_options", ["--keep-open=no"], list)

    @property
    def vlc_commandline_options(self):
        return self._get_value("vlc_commandline_options", [], list)

    @property
    def ffmpeg_ts_to_mp4(self):
        return self._get_value("ffmpeg_ts_to_mp4", False, bool)


    @property
    def anime_types(self):
        return self._get_value("anime_types", list(["sub", "dub"]), list)

    def _get_path_value(self, key: str, fallback: Path) -> Path:
        path = self._get_value(key, fallback, str)
        try:
            return Path(path).expanduser()
        except:
            return fallback

    def _get_value(self, key: str, fallback, typ: object):
        value = self._yaml_conf.get(key, fallback)
        if isinstance(value, typ): #pyright: ignore
            return value

        return fallback

    def _create_config(self):
        try:
            self._get_config_path().mkdir(exist_ok=True, parents=True)
            config_options = {}
            # generate config based on attrs and default values of config class
            for attribute, value in Config.__dict__.items():
                if attribute.startswith("_"):
                    continue

                if isinstance(value, property):
                    val = self.__getattribute__(attribute)
                    config_options[attribute] = (
                        str(val) if isinstance(val, Path) else val
                    )
            self._config_file.touch()
            with open(self._config_file, "w") as file:
                yaml.dump(
                    yaml.dump(config_options, file, indent=4, default_flow_style=False)
                )
        except PermissionError as e:
            print(f"Failed to create config file: {repr(e)}")
            sys_exit(1)
    
    @staticmethod
    @functools.lru_cache
    def _read_config():
        config_file = Config._get_config_path() / "config.yaml"
        try:
            with config_file.open("r") as conf:
                yaml_conf = yaml.safe_load(conf)
        except FileNotFoundError:
            # There is no config file, create one
            yaml_conf = {}
        
        return config_file, yaml_conf


    @staticmethod
    def _get_config_path() -> Path:
        linux_path = Path().home() / ".config" / "hayai-cli"
        windows_path = Path().home() / "AppData" / "Local" / "hayai-cli"
        macos_path = Path().home() / ".config" / "hayai-cli"

        if platform == "linux":
            return linux_path
        elif platform == "darwin":
            return macos_path
        elif platform == "win32":
            return windows_path
        else:
            raise SysNotFoundError(platform)

