"""D-Bus service for Vojtux customizations add-on."""

import sys

from pyanaconda.dbus import DBus
from pyanaconda.modules.boss.module_manager.start_modules import StartModuleTask


def main():
    """Start the Vojtux customizations service."""
    from pyanaconda.modules.common.base import Service
    from pyanaconda.modules.common.constants.services import ADDONS
    from pyanaconda.addons import AddonData

    service = Service()
    service.run()


if __name__ == "__main__":
    main()
