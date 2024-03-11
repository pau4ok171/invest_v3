from django.template.defaultfilters import register


@register.filter(name='get_dict_value')
def get_dict_value(d, key):
    try:
        return d[key]
    except KeyError:
        return 'n/a'
