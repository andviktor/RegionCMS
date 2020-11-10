from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Site, Region, Template, Chunk, Page, Placeholder
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.core import management
from io import StringIO

# build
def build_site(request, site_id):
    site = Site.objects.get(pk=site_id)
    out = StringIO()
    management.call_command('buildsite', site.title, stdout=out)
    site.log = str(out.getvalue())
    site.save(update_fields=['log'])
    return redirect('site-detail', pk=site.pk)

# upload
def upload_site(request, site_id):
    site = Site.objects.get(pk=site_id)
    out = StringIO()
    management.call_command('uploadsite', site.title, stdout=out)
    site.log = str(out.getvalue())
    site.save(update_fields=['log'])
    return redirect('site-detail', pk=site.pk)

# site
class SiteCreate(generic.CreateView):
    model = Site
    fields = ['title', 'domain', 'ssl', 'hosting', 'ftp_host', 'ftp_user', 'ftp_password', 'robots', 'favicon']
    template_name = 'forms/site_form.html'

class SiteUpdate(generic.UpdateView):
    model = Site
    fields = ['title', 'domain', 'ssl', 'hosting', 'ftp_host', 'ftp_user', 'ftp_password', 'robots', 'favicon']
    template_name = 'forms/site_form.html'

class SiteListView(generic.ListView):
    model = Site
    template_name = 'lists/site_list.html'

class SiteDetailView(generic.DetailView):
    model = Site
    template_name = 'details/site_detail.html'

# region
class RegionCreate(generic.CreateView):
    model = Region
    fields = ['title', 'main_region', 'padeji', 'alias', 'phone', 'email', 'address']
    template_name = 'forms/region_form.html'
    def form_valid(self, form):
         site = Site.objects.get(pk=self.kwargs['site_id'])
         form.instance.site = site
         return super(RegionCreate, self).form_valid(form)
    def get_success_url(self):
        return reverse('region-list', kwargs={'site_id': self.object.site.pk})

class RegionListView(generic.ListView):
    model = Region
    context_object_name = 'region_list'
    
    template_name = 'lists/region_list.html'

    def get_queryset(self):
        return Region.objects.filter(
            site=self.kwargs['site_id']
        ).order_by(
            'title'
        )
    
    def get_site_id(self):
        return self.kwargs['site_id']

class RegionUpdate(generic.UpdateView):
    model = Region
    fields = ['title', 'main_region', 'padeji', 'alias', 'phone', 'email', 'address']
    template_name = 'forms/region_form.html'
    def get_success_url(self):
        return reverse('region-list', kwargs={'site_id': self.object.site.pk})

class RegionDelete(generic.DeleteView):
    model = Region
    template_name = 'forms/region_confirm_delete.html'
    def get_success_url(self):
        return reverse('region-list', kwargs={'site_id': self.object.site.pk})

# template
class TemplateCreate(generic.CreateView):
    model = Template
    fields = ['site', 'title', 'html']
    template_name = 'forms/template_form.html'
    def form_valid(self, form):
         site = Site.objects.get(pk=self.kwargs['site_id'])
         form.instance.site = site
         return super(TemplateCreate, self).form_valid(form)
    def get_success_url(self):
        return reverse('site-detail', kwargs={'pk': self.object.site.pk})

class TemplateUpdate(generic.UpdateView):
    model = Template
    fields = ['site', 'title', 'html']
    template_name = 'forms/template_form.html'
    def get_success_url(self):
        return reverse('site-detail', kwargs={'pk': self.object.site.pk})

class TemplateDelete(generic.DeleteView):
    model = Template
    template_name = 'forms/template_confirm_delete.html'
    def get_success_url(self):
        return reverse('site-detail', kwargs={'pk': self.object.site.pk})

# chunk
class ChunkCreate(generic.CreateView):
    model = Chunk
    fields = ['site', 'title', 'html']
    template_name = 'forms/chunk_form.html'
    def form_valid(self, form):
         site = Site.objects.get(pk=self.kwargs['site_id'])
         form.instance.site = site
         return super(ChunkCreate, self).form_valid(form)
    def get_success_url(self):
        return reverse('site-detail', kwargs={'pk': self.object.site.pk})

class ChunkUpdate(generic.UpdateView):
    model = Chunk
    fields = ['site', 'title', 'html']
    template_name = 'forms/chunk_form.html'
    def get_success_url(self):
        return reverse('site-detail', kwargs={'pk': self.object.site.pk})

class ChunkDelete(generic.DeleteView):
    model = Chunk
    template_name = 'forms/chunk_confirm_delete.html'
    def get_success_url(self):
        return reverse('site-detail', kwargs={'pk': self.object.site.pk})

# page
class PageCreate(generic.CreateView):
    model = Page
    fields = ['site', 'title', 'alias', 'parent', 'template', 'metatitle', 'metadescription', 'sitemap_priority']
    template_name = 'forms/page_form.html'
    def form_valid(self, form):
         site = Site.objects.get(pk=self.kwargs['site_id'])
         form.instance.site = site
         return super(PageCreate, self).form_valid(form)
    def get_success_url(self):
        return reverse('site-detail', kwargs={'pk': self.object.site.pk})

class PageUpdate(generic.UpdateView):
    model = Page
    fields = ['site', 'title', 'alias', 'parent', 'template', 'metatitle', 'metadescription', 'sitemap_priority']
    template_name = 'forms/page_form.html'
    def get_success_url(self):
        return reverse('site-detail', kwargs={'pk': self.object.site.pk})

class PageDelete(generic.DeleteView):
    model = Page
    template_name = 'forms/page_confirm_delete.html'
    def get_success_url(self):
        return reverse('site-detail', kwargs={'pk': self.object.site.pk})

# placeholder
class PlaceholderCreate(generic.CreateView):
    model = Placeholder
    fields = ['page', 'title', 'html', 'uniqenable']
    template_name = 'forms/placeholder_form.html'
    def form_valid(self, form):
         page = Page.objects.get(pk=self.kwargs['page_id'])
         form.instance.page = page
         return super(PlaceholderCreate, self).form_valid(form)
    def get_success_url(self):
        return reverse('page-edit', kwargs={'pk': self.object.page.pk})

class PlaceholderUpdate(generic.UpdateView):
    model = Placeholder
    fields = ['page', 'title', 'html', 'uniqenable']
    template_name = 'forms/placeholder_form.html'
    def get_success_url(self):
        return reverse('page-edit', kwargs={'pk': self.object.page.pk})

class PlaceholderDelete(generic.DeleteView):
    model = Placeholder
    template_name = 'forms/placeholder_confirm_delete.html'
    def get_success_url(self):
        return reverse('page-edit', kwargs={'pk': self.object.page.pk})