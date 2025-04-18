from apps.coopolis.models.general import Customization
from apps.coopolis.templatetags.my_tag_library import external_static


def global_context(request):

    context = {
        # **settings.GLOBAL_CONTEXT,
        **get_customization_context(),
        **projects_menu_context(request),
    }
    return context


def get_customization_context():
    obj = Customization()
    objs = Customization.objects.all()
    if len(objs) > 0:
        obj = objs[0]
    return {
        "customization": {
            "logo": get_customization_or_external_static(
                obj,
                "logo",
                "logo.png",
            ),
            "signatures_pdf_footer": get_customization_or_external_static(
                obj,
                "signatures_pdf_footer",
                "peu_signatures_pdf.png",
            )
        }
    }


def get_customization_or_external_static(obj, field_name, file_name):
    """
    Aquesta funció s'ha d'eliminar en un futur un cop tots els ateneus
    tinguin el logo posat al model de personalització.
    """
    try:
        customization_image = getattr(obj, field_name)
        return customization_image.url
    except (AttributeError, ValueError):
        return external_static(f"/{file_name}")


def projects_menu_context(request):
    user_projects = None
    if request.user.is_authenticated and request.user.projects.count() > 0:
        user_projects = request.user.projects.all()
    return {"user_projects": user_projects}
