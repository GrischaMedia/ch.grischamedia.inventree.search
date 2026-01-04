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
        ctx["csrf_token"] = get_token(self.request)
        
        plugin = registry.get_plugin("gm-search")
        if plugin:
            ctx["plugin_version"] = plugin.VERSION
            # Header-Titel aus Settings holen
            try:
                header_title = plugin.get_setting("HEADER_TITLE", backup_value="Suche")
                ctx["header_title"] = header_title or "Suche"
            except Exception:
                ctx["header_title"] = "Suche"
            # Card-Titel aus Settings holen
            try:
                card_title = plugin.get_setting("CARD_TITLE", backup_value="Suche")
                ctx["card_title"] = card_title or "Suche"
            except Exception:
                ctx["card_title"] = "Suche"
        else:
            ctx["plugin_version"] = ""
            ctx["header_title"] = "Suche"
            ctx["card_title"] = "Suche"
        
        return ctx


@login_required
@permission_required("part.view_part", raise_exception=True)
def search(request: HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error": "method_not_allowed"}, status=405)

    plugin = registry.get_plugin("gm-search")
    if not plugin:
        return JsonResponse({"error": "plugin_not_loaded"}, status=500)

    enable_search = bool(plugin.get_setting("ENABLE_ADVANCED_SEARCH", backup_value=True))
    if not enable_search:
        return JsonResponse(
            {"error": "search_disabled", "detail": "Plugin setting ENABLE_ADVANCED_SEARCH is disabled"},
            status=400,
        )

    query = request.GET.get("q", "").strip()
    if not query:
        return JsonResponse({"results": []})

    from django.db.models import Q

    results = []
    query_lower = query.lower()

    # Search in parts
    from part.models import Part
    from stock.models import StockItem
    from django.db.models import Sum

    parts = Part.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(IPN__icontains=query)
    ).select_related("category")[:50]

    for part in parts:
        # Lagerort und Stückanzahl holen
        stock_items = StockItem.objects.filter(part=part)
        total_quantity = stock_items.aggregate(total=Sum('quantity'))['total'] or 0
        
        # Ersten Lagerort finden (oder alle sammeln)
        locations = []
        for stock_item in stock_items[:5]:  # Maximal 5 Lagerorte anzeigen
            if stock_item.location:
                try:
                    location_path = stock_item.location.pathstring
                except AttributeError:
                    location_path = stock_item.location.name
                locations.append(location_path)
        
        location_text = ", ".join(locations) if locations else "Kein Lagerort"
        if len(stock_items) > 5:
            location_text += f" (+{len(stock_items) - 5} weitere)"
        
        results.append({
            "type": "part",
            "id": part.pk,
            "name": part.name,
            "description": getattr(part, "description", "")[:100] if hasattr(part, "description") else "",
            "ipn": getattr(part, "IPN", ""),
            "url": part.get_absolute_url() if hasattr(part, "get_absolute_url") else None,
            "category": part.category.name if part.category else "",
            "location": location_text,
            "quantity": float(total_quantity),
        })

    return JsonResponse({"results": results})

