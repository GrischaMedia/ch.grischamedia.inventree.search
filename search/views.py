from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from plugin.registry import registry


@method_decorator(login_required, name='dispatch')
@method_decorator(permission_required("part.view_part", raise_exception=True), name='dispatch')
class SearchView(TemplateView):
    template_name = "search/search.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['request'] = self.request
        ctx["plugin_title"] = "Suche"
        ctx["csrf_token"] = get_token(self.request)
        
        plugin = registry.get_plugin("search")
        if plugin:
            ctx["plugin_version"] = plugin.VERSION
        else:
            ctx["plugin_version"] = ""
        
        return ctx


@login_required
@permission_required("part.view_part", raise_exception=True)
def search(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error": "method_not_allowed"}, status=405)

    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"results": []})

    from django.db.models import Q

    results = []
    query_lower = query.lower()

    # Search in parts
    from part.models import Part

    parts = Part.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(IPN__icontains=query)
    ).select_related("category")[:50]

    for part in parts:
        results.append({
            "type": "part",
            "id": part.pk,
            "name": part.name,
            "description": getattr(part, "description", "")[:100] if hasattr(part, "description") else "",
            "ipn": getattr(part, "IPN", ""),
            "url": part.get_absolute_url() if hasattr(part, "get_absolute_url") else None,
            "category": part.category.name if part.category else "",
        })

    return JsonResponse({"results": results})

