"""Category support for Vojtux customizations add-on."""

from pyanaconda.ui import Category
from pyanaconda.ui.gui import GUIObject

__all__ = ["VojtuxCategory"]


class VojtuxCategory(Category, GUIObject):
    """Category for Vojtux accessibility customizations."""

    displayTitle = "Vojtux"
    sortOrder = 100

    def __init__(self, storage, payload):
        GUIObject.__init__(self, storage, payload)
        self.title = "Vojtux"

    def initialize(self):
        pass

    def refresh(self):
        pass
