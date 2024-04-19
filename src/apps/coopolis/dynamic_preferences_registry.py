from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.types import FilePreference

from apps.coopolis.storage_backends import PublicMediaStorage

customization = Section("customization")


@global_preferences_registry.register
class SiteLogo(FilePreference):
    section = customization
    name = "Logotip"
    default = ""
    required = True

    def get_file_storage(self):
        return PublicMediaStorage()
