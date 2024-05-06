from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

from apps.coopolis.s3_files_utils import generate_presigned_url


def db_backup_download_view(request):
    formatted_date = timezone.now().strftime("%y%m%d")
    backup_file = f"server.backup/{formatted_date}/0000.postgress.sql"
    file_url = generate_presigned_url(backup_file)
    if file_url:
        return HttpResponseRedirect(file_url)
    return HttpResponse(
        f"Unable to generate the presigned url for the file {file_url}.",
        status=500,
    )
