class MissingOrganizers(Exception):
    """The polls report is based in Organizers and no Organizer exists."""

    def __init__(self, message="'organizer' data missing."):
        super().__init__(message)


class AxisDoesNotExistException(Exception):
    """Trying to resolve the title of an axis that does not exist in settings."""
