from django import template

register = template.Library()
@register.simple_tag(takes_context=True)
def param_replace(context, path='', **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    if path:
        new_url = path + '?' + d.urlencode()
    else:
        new_url = d.urlencode()
    return new_url
