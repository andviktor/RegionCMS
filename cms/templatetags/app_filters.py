from django import template
from cms.models import Page

register = template.Library()

# Common

# sorting queryset
@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

# For Pages

# get parent page
@register.filter(name='get_parent_page')
def get_parent_page(id):
    parent_page = Page.objects.get(pk=id)
    return parent_page

# get list of child pages
@register.filter(name='get_child_pages')
def get_child_pages(id):
    child_pages = Page.objects.filter(parent=id)
    return child_pages

