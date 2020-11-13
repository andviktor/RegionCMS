from django.contrib import admin

from .models import Topvisor, Site, Region, Template, Chunk, Page, Placeholder

# Сайты
class SiteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'domain')
    actions = None

admin.site.register(Site, SiteAdmin)

# Регионы
class RegionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'site')
    list_filter = ('site__title',)

admin.site.register(Region, RegionAdmin)

# Шаблоны
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'site')
    list_filter = ('site__title',)

admin.site.register(Template, TemplateAdmin)

# Чанки
class ChunkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'site')
    list_filter = ('site__title',)

admin.site.register(Chunk, ChunkAdmin)

# Страницы
class PageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'site', 'parent')
    list_filter = ('site__title',)

admin.site.register(Page, PageAdmin)

# Плейсхолдеры
class PlaceholderAdmin(admin.ModelAdmin):
    #readonly_fields = ('uniqcodes','uniqwords',)
    list_display = ('__str__', 'page')
    list_filter = ('page__site__title','page__title',)

admin.site.register(Placeholder, PlaceholderAdmin)

# Топвизоры (настройки для сайтов)
class TopvisorAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'site', 'userid', 'apikey', 'keywords', 'scheduleday', 'schedulehour')

admin.site.register(Topvisor, TopvisorAdmin)