class MissingOrganizers(Exception):
    """The polls report is based in Organizers and no Organizer exists."""


class AxisDoesNotExistException(Exception):
    """Trying to resolve the title of an axis that does not exist in settings."""
