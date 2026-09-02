from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    if dictionary is None:
        return None
    return dictionary.get(key)


@register.filter
def elided_page_range(paginator, current_page):
    if paginator is None:
        return []

    try:
        page_range = paginator.get_elided_page_range(
            current_page or 1,
            on_each_side=1,
            on_ends=1,
        )
    except TypeError:
        page_range = paginator.page_range

    result = []
    for item in page_range:
        item_text = str(item)
        if item_text in {"...", "…", "…"}:
            result.append("...")
        else:
            result.append(int(item) if str(item).isdigit() else item)
    return result