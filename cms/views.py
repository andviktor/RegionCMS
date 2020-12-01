from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Topvisor, Site, Region, Template, Chunk, Page, Placeholder
from django.views import generic
from django.urls import reverse_lazy, reverse
from django.core import management
from io import StringIO
from requests import post
import json
import datetime

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

# services
def create_topvisor(request, site_id):
    try:
        site = Site.objects.get(pk=site_id)
        topvisor = Topvisor(site=site)
        topvisor.save()
        site.log = "Топвизор подключен."
    except:
        site = Site.objects.get(pk=site_id)
        site.log = "Ошибка при создании Топвизора."
    site.save(update_fields=['log'])
    return redirect('site-detail', pk=site.pk)

def export_topvisor(request, topvisor_id):
    topvisor = Topvisor.objects.get(pk=topvisor_id)
    site = Site.objects.get(pk=topvisor.site.pk)
    regions = list(Region.objects.filter(site=site).order_by('-title'))
    log = ''
    region_log ='Назначение регионов:\n'
    header_apikey = 'bearer '+topvisor.apikey
    create_project_request_headers = {
        'Content-type':'application/json',
        'User-Id':topvisor.userid,
        'Authorization':header_apikey
    }
    for region in regions:
        try:
            region_site_link = 'http'
            if site.ssl:
                region_site_link += 's'
            region_site_link += '://'
            if not region.main_region:
                region_site_link += region.alias + '.'
            region_site_link += site.domain
            
            create_project_request_data = {
                'url':region_site_link,
                'name':region.title
            }
            create_project_request = post('https://api.topvisor.com/v2/json/add/projects_2/projects', headers=create_project_request_headers, data = json.dumps(create_project_request_data))

            log += 'Проект для г. ' + region.title + ' создан\n'
        except:
            log += '(!) Ошибка проекта для г. ' + region.title + '\n'

    try:        
        get_projects_request_data = {
            'fields':['name']
        }
        get_projects_request = post('https://api.topvisor.com/v2/json/get/projects_2/projects', headers=create_project_request_headers, data= json.dumps(get_projects_request_data))
        get_projects_request_json = get_projects_request.json()
        for project in get_projects_request_json['result']:

            # Получаем данные региона
            get_region_data_request_data = {
                'searcher':0,
                'search':project['name'],
                'limit':1
            }
            get_region_data_request = post('https://api.topvisor.com/v2/json/get/mod_common/regions', headers=create_project_request_headers, data = json.dumps(get_region_data_request_data))
            get_region_data_request_result = get_region_data_request.json()

            # Яндекс
            add_searcher_request_data = {
                'project_id':project['id'],
                'searcher_key':0
            }
            add_searcher_request = post('https://api.topvisor.com/v2/json/add/positions_2/searchers', headers=create_project_request_headers, data = json.dumps(add_searcher_request_data))
            
            # Google            
            add_searcher_request_data = {
                'project_id':project['id'],
                'searcher_key':1
            }
            add_searcher_request = post('https://api.topvisor.com/v2/json/add/positions_2/searchers', headers=create_project_request_headers, data = json.dumps(add_searcher_request_data))

            # Добавляем регионы
            for set_region in get_region_data_request_result['result']:
                add_region_data_request_data = {
                    'project_id':project['id'],
                    'searcher_key':0,
                    'region_key':set_region['id']
                }
                add_region_data_request = post('https://api.topvisor.com/v2/json/add/positions_2/searchers_regions', headers=create_project_request_headers, data = json.dumps(add_region_data_request_data))
                add_region_data_request_data = {
                    'project_id':project['id'],
                    'searcher_key':1,
                    'region_key':set_region['id']
                }
                add_region_data_request = post('https://api.topvisor.com/v2/json/add/positions_2/searchers_regions', headers=create_project_request_headers, data = json.dumps(add_region_data_request_data))
                region_log += project['name']+' : '+set_region['name']+'\n'

            # Добавляем фразы
            keywords = topvisor.keywords.replace('\r',' ')
            region_keywords = ''
            for keyword in keywords.split('\n'):
                region_keywords += '\n'+keyword+' '+project['name']
            add_keywords_data_request_data = {
                'project_id':project['id'],
                'keywords':'name\n'+keywords+region_keywords
            }
            add_keywords_data_request = post('https://api.topvisor.com/v2/json/add/keywords_2/keywords/import', headers=create_project_request_headers, data = json.dumps(add_keywords_data_request_data))
            
            # Добавляем расписание
            add_schedule_data_request_data = {
                'type':'positions_go',
                'target_id':project['id'],
                'schedule':[{
                    'times':[{
                        'hour':topvisor.schedulehour,
                        'minute':15
                    }],
                    'days':[topvisor.scheduleday]
                }]
            }
            add_schedule_data_request = post('https://api.topvisor.com/v2/json/edit/schedule_2', headers=create_project_request_headers, data = json.dumps(add_schedule_data_request_data))
            

    except:
        log += '(!) Ошибка получения списка проектов.'


    site.log = log + '\n----------\n' + region_log
    site.save(update_fields=['log'])
    return redirect('site-detail', pk=topvisor.site.pk)

def clear_topvisor(request, topvisor_id):
    topvisor = Topvisor.objects.get(pk=topvisor_id)
    site = Site.objects.get(pk=topvisor.site.pk)
    try:        
        header_apikey = 'bearer '+topvisor.apikey
        create_project_request_headers = {
            'Content-type':'application/json',
            'User-Id':topvisor.userid,
            'Authorization':header_apikey
        }
        create_project_request_data = {
            "filters":[{
                "name":"name",
                "operator":"NOT_EQUALS",
                "values": [""]
            },]
        }
        create_project_request = post('https://api.topvisor.com/v2/json/del/projects_2/projects', headers=create_project_request_headers, data = json.dumps(create_project_request_data))

        site.log = "Все проекты Топвизор успешно удалены."
        
    except:
        site.log = "Ошибка при удалении проектов Топвизор."

    site.save(update_fields=['log'])
    return redirect('site-detail', pk=topvisor.site.pk)

class TopvisorUpdate(generic.UpdateView):
    model = Topvisor
    fields = ['userid', 'apikey', 'keywords', 'scheduleday', 'schedulehour']
    template_name = 'forms/services/topvisor_form.html'
    def get_success_url(self):
        return reverse('topvisor-edit', kwargs={'pk': self.object.pk})


# Analytics

def AnalyticsTopvisorPositions(request, topvisor_id):
    topvisor = Topvisor.objects.get(pk=topvisor_id)
    template = 'details/services/topvisor/positions.html'

    def get_positions(topvisor):
        result_html = ''
        result_html += '<table class="table table-hover"><tr><td rowspan="1">Регион</td><td colspan="5">Яндекс</td><td></td><td colspan="5">Google</td></tr>'
        result_html += '<tr><td rowspan="1"></td><td>1-3</td><td>1-10</td><td>11-30</td><td>31-100</td><td>100+</td><td></td><td>1-3</td><td>1-10</td><td>11-30</td><td>31-100</td><td>100+</td></tr>'
        header_apikey = 'bearer '+topvisor.apikey
        get_positions_request_headers = {
            'Content-type':'application/json',
            'User-Id':topvisor.userid,
            'Authorization':header_apikey
        }
        get_projects_request_data = {
            'fields':['name'],
            'show_site_stat':1,
            'show_searchers_and_regions':1
        }
        get_projects_request = post('https://api.topvisor.com/v2/json/get/projects_2/projects', headers=get_positions_request_headers, data= json.dumps(get_projects_request_data))
        get_projects_request_json = get_projects_request.json()
        
        today = datetime.date.today()
        monthago = str(today - datetime.timedelta(weeks=4))
        today = str(today)

        for project in get_projects_request_json['result']:
            # if project['name'] != 'Саранск':
            #     continue
            print(project['name'])
            result_html += '<tr><td>'+project['name']+'</td>'
            for searcher in project['searchers']:
                if searcher['regions'][0]['name'] == project['name'] and searcher['searcher'] == 0:
                    yandex_region_key = searcher['regions'][0]['index']
                if searcher['regions'][0]['name'] == project['name'] and searcher['searcher'] == 1:
                    google_region_key = searcher['regions'][0]['index']
            # yandex
            get_positions_request_data = {
                'project_id':project['id'],
                'region_index':yandex_region_key,
                'dates':[today,monthago],
                'show_tops':1
            }
            get_positions_data_request = post('https://api.topvisor.com/v2/json/get/positions_2/summary', headers=get_positions_request_headers, data = json.dumps(get_positions_request_data))
            get_positions_data_request_result = get_positions_data_request.json()
            
            phrases_total = get_positions_data_request_result['result']['tops'][1]['1_10']+get_positions_data_request_result['result']['tops'][1]['11_30']+get_positions_data_request_result['result']['tops'][1]['31_50']+get_positions_data_request_result['result']['tops'][1]['51_100']+get_positions_data_request_result['result']['tops'][1]['101_10000']
            
            dynamics = {}
            
            dynamics['1_3'] = ' ('+str(get_positions_data_request_result['result']['tops_dynamics']['1_3'])+')' if get_positions_data_request_result['result']['tops_dynamics']['1_3'] != 0 else ''
            dynamics['1_10'] = ' ('+str(get_positions_data_request_result['result']['tops_dynamics']['1_10'])+')' if get_positions_data_request_result['result']['tops_dynamics']['1_10'] != 0 else ''
            dynamics['11_30'] = ' ('+str(get_positions_data_request_result['result']['tops_dynamics']['11_30'])+')' if get_positions_data_request_result['result']['tops_dynamics']['11_30'] != 0 else ''
            dynamics['31_100'] = ' ('+str(get_positions_data_request_result['result']['tops_dynamics']['31_50']+get_positions_data_request_result['result']['tops_dynamics']['51_100'])+')' if (get_positions_data_request_result['result']['tops_dynamics']['31_50']+get_positions_data_request_result['result']['tops_dynamics']['51_100']) != 0 else ''
            dynamics['101_10000'] = ' ('+str(get_positions_data_request_result['result']['tops_dynamics']['101_10000'])+')' if get_positions_data_request_result['result']['tops_dynamics']['101_10000'] != 0 else ''

            td_color_opacity_1_3 = get_positions_data_request_result['result']['tops'][1]['1_3']/phrases_total
            td_color_opacity_1_10 = get_positions_data_request_result['result']['tops'][1]['1_10']/phrases_total
            td_color_opacity_11_30 = get_positions_data_request_result['result']['tops'][1]['11_30']/phrases_total
            td_color_opacity_31_100 = (get_positions_data_request_result['result']['tops'][1]['31_50']+get_positions_data_request_result['result']['tops'][1]['51_100'])/phrases_total
            td_color_opacity_101_10000 = get_positions_data_request_result['result']['tops'][1]['101_10000']/phrases_total

            result_html += '<td style="background-color: rgba(0,255,0,'+str(td_color_opacity_1_3)+')">'+str(get_positions_data_request_result['result']['tops'][1]['1_3'])+dynamics['1_3']+'</td>'
            result_html += '<td style="background-color: rgba(0,255,0,'+str(td_color_opacity_1_10)+')">'+str(get_positions_data_request_result['result']['tops'][1]['1_10'])+dynamics['1_10']+'</td>'
            result_html += '<td style="background-color: rgba(0,255,0,'+str(td_color_opacity_11_30)+')">'+str(get_positions_data_request_result['result']['tops'][1]['11_30'])+dynamics['11_30']+'</td>'
            result_html += '<td style="background-color: rgba(0,255,0,'+str(td_color_opacity_31_100)+')">'+str(get_positions_data_request_result['result']['tops'][1]['31_50']+get_positions_data_request_result['result']['tops'][1]['51_100'])+dynamics['31_100']+'</td>'
            result_html += '<td style="background-color: rgba(255,0,0,'+str(td_color_opacity_101_10000)+')">'+str(get_positions_data_request_result['result']['tops'][1]['101_10000'])+dynamics['101_10000']+'</td><td></td>'
            
            # google
            get_positions_request_data = {
                'project_id':project['id'],
                'region_index':google_region_key,
                'dates':[today,monthago],
                'show_tops':1
            }
            get_positions_data_request = post('https://api.topvisor.com/v2/json/get/positions_2/summary', headers=get_positions_request_headers, data = json.dumps(get_positions_request_data))
            get_positions_data_request_result = get_positions_data_request.json()

            dynamics['1_3'] = ' ('+str(get_positions_data_request_result['result']['tops_dynamics']['1_3'])+')' if get_positions_data_request_result['result']['tops_dynamics']['1_3'] != 0 else ''
            dynamics['1_10'] = ' ('+str(get_positions_data_request_result['result']['tops_dynamics']['1_10'])+')' if get_positions_data_request_result['result']['tops_dynamics']['1_10'] != 0 else ''
            dynamics['11_30'] = ' ('+str(get_positions_data_request_result['result']['tops_dynamics']['11_30'])+')' if get_positions_data_request_result['result']['tops_dynamics']['11_30'] != 0 else ''
            dynamics['31_100'] = ' ('+str(get_positions_data_request_result['result']['tops_dynamics']['31_50']+get_positions_data_request_result['result']['tops_dynamics']['51_100'])+')' if (get_positions_data_request_result['result']['tops_dynamics']['31_50']+get_positions_data_request_result['result']['tops_dynamics']['51_100']) != 0 else ''
            dynamics['101_10000'] = ' ('+str(get_positions_data_request_result['result']['tops_dynamics']['101_10000'])+')' if get_positions_data_request_result['result']['tops_dynamics']['101_10000'] != 0 else ''

            td_color_opacity_1_3 = get_positions_data_request_result['result']['tops'][1]['1_3']/phrases_total
            td_color_opacity_1_10 = get_positions_data_request_result['result']['tops'][1]['1_10']/phrases_total
            td_color_opacity_11_30 = get_positions_data_request_result['result']['tops'][1]['11_30']/phrases_total
            td_color_opacity_31_100 = (get_positions_data_request_result['result']['tops'][1]['31_50']+get_positions_data_request_result['result']['tops'][1]['51_100'])/phrases_total
            td_color_opacity_101_10000 = get_positions_data_request_result['result']['tops'][1]['101_10000']/phrases_total

            result_html += '<td style="background-color: rgba(0,255,0,'+str(td_color_opacity_1_3)+')">'+str(get_positions_data_request_result['result']['tops'][1]['1_3'])+dynamics['1_3']+'</td>'
            result_html += '<td style="background-color: rgba(0,255,0,'+str(td_color_opacity_1_10)+')">'+str(get_positions_data_request_result['result']['tops'][1]['1_10'])+dynamics['1_10']+'</td>'
            result_html += '<td style="background-color: rgba(0,255,0,'+str(td_color_opacity_11_30)+')">'+str(get_positions_data_request_result['result']['tops'][1]['11_30'])+dynamics['11_30']+'</td>'
            result_html += '<td style="background-color: rgba(0,255,0,'+str(td_color_opacity_31_100)+')">'+str(get_positions_data_request_result['result']['tops'][1]['31_50']+get_positions_data_request_result['result']['tops'][1]['51_100'])+dynamics['31_100']+'</td>'
            result_html += '<td style="background-color: rgba(255,0,0,'+str(td_color_opacity_101_10000)+')">'+str(get_positions_data_request_result['result']['tops'][1]['101_10000'])+dynamics['101_10000']+'</td><td></td>'
            
            # print(yandex_region_key)
            # print(google_region_key)
            #print(get_positions_data_request_result)
            #break
            result_html += '</tr>'

        result_html += '</table>'
        return result_html

    context = {
        "topvisor" : topvisor,
        "positions" : get_positions(topvisor)
    }
    
    return render(request, template, context)