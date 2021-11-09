from django.urls import resolve


def path_name(request):
    path_name = resolve(request.path).url_name
    return {'path_name': path_name}
