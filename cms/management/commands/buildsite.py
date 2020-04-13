from django.core.management.base import BaseCommand, CommandError
from cms.models import Site, Chunk, Page
from ftplib import FTP
import re, os, sys, random, json, datetime, zipfile, shutil

class Command(BaseCommand):
    help = 'Print current site title'

    # Формируем полный адрес страницы с учетом вложенности
    def get_full_page_dir(self, tmp_page):

        tmp_page_source = tmp_page

        full_page_dir = ''

        if hasattr(tmp_page.parent, 'alias'):
            while hasattr(tmp_page.parent, 'alias'):
                if tmp_page.parent.alias != '/':
                    full_page_dir = '/' + str(tmp_page.parent.alias) + full_page_dir
                    tmp_page = tmp_page.parent
                else:
                    break
        else:
            full_page_dir = '/'

        return full_page_dir

    def uniqwords(self, source_html):
        operand_group_list = []
        tmp_html = str(source_html)
        while tmp_html.find('{') > -1:
            start_index = tmp_html.find('{')
            end_index = tmp_html.find('}')
            operand = tmp_html[start_index+1:end_index]
            operand = operand.replace('\,','&#44;')
            tmp_html = tmp_html.replace('{'+operand+'}','')
            operand_group_list.append(operand)
        return operand_group_list

    def uniqtext(self, region_count, source_html):
        param_result = int(region_count)         # Сколько копий текстов нужно получить с максимальной уникальностью
        param_copys = param_result * 20
        uniq_texts_container = []
        uniq_hashes_container = []

        # Создаем список с уникальными текстами
        texts_container = list(range(param_copys))
        hash_container = list(range(param_copys))
        i = 0
        for i in range(param_copys):
            texts_container[i] = ''
            hash_container[i] = ''
            tmp_html = str(source_html)
            
            while tmp_html.find('{') > -1:
                start_index = tmp_html.find('{')
                end_index = tmp_html.find('}')
                operand = tmp_html[start_index+1:end_index]
                operand_list = operand.split('|')
                rand = random.randint(0,len(operand_list)-1)
                tmp_html = tmp_html.replace('{'+operand+'}',operand_list[rand])
                hash_container[i] = hash_container[i] + str(rand)
            texts_container[i] = texts_container[i] + tmp_html
        
        # Составляем матрицу уникальности
        uniq_matrix = [[0] * len(hash_container) for i in range(len(hash_container))]
        for index_current, hash_current in enumerate(hash_container):
            for index_compare, hash_compare in enumerate(hash_container):
                if index_current == index_compare:
                    continue
                nouniq_count = 0
                for index_hash_current_char, hash_current_char in enumerate(hash_current):
                    if hash_current_char == hash_compare[index_hash_current_char]:
                        nouniq_count = nouniq_count + 1
                nouniq_count = nouniq_count / len(hash_container)
                uniq_matrix[index_current][index_compare] = nouniq_count
        
        # Перебираем матрицу уникальности, отбираем нужное число наиболее уникальных текстов
        uniq_sum_list = [9999] * len(hash_container)
        
        for uniq_matrix_row_index, uniq_matrix_row in enumerate(uniq_matrix):
            row_item_sum = 0
            for uniq_matrix_row_item_index, uniq_matrix_row_item in enumerate(uniq_matrix_row):
                row_item_sum = row_item_sum + uniq_matrix_row_item
            uniq_sum_list[uniq_matrix_row_index] = row_item_sum
        
        for uniq_sum_current in sorted(uniq_sum_list)[:param_result]:
            for uniq_sum_list_compare_index, uniq_sum_list_compare in enumerate(uniq_sum_list):
                if uniq_sum_current == uniq_sum_list_compare:
                    uniq_texts_container.append(texts_container[uniq_sum_list_compare_index])
                    uniq_hashes_container.append(hash_container[uniq_sum_list_compare_index])
                
        return uniq_hashes_container

    def add_arguments(self, parser):
        parser.add_argument('site_titles', nargs='+')

    def handle(self, *args, **options):
           
        today = datetime.datetime.today()
        for site_title in options['site_titles']:
            
            # Получаем сайт
            try:
                site = Site.objects.get(title=site_title)
            except Site.DoesNotExist:
                raise CommandError('Site "%s" does not exist' % site_title)
            
            # Получаем регионы сайта
            try:
                regions = site.region_set.all()
            except:
                raise CommandError('Cant get regions for site "%s"' % site.title)

            # Создаем словарь с параметрами страницы
            page_data = dict()
            page_data['site_title'] = site.title
            page_data['domain'] = site.domain
            
            errors_count = 0

            # Перебираем регионы
            for region in regions:
                
                self.stdout.write('Сборка региона > ' + region.title)
                # Заносим в словарь параметров страницы падежи
                padeji = region.padeji.split(',')
                page_data['reg_i'] = padeji[0]
                page_data['reg_r'] = padeji[1]
                page_data['reg_d'] = padeji[2]
                page_data['reg_v'] = padeji[3]
                page_data['reg_t'] = padeji[4]
                page_data['reg_p'] = padeji[5]

                # Заносим в словарь параметров страницы контакты
                page_data['phone'] = region.phone
                page_data['email'] = region.email
                page_data['address'] = region.address

                for page in site.page_set.all():
                    
                    # Заносим в словарь параметров страницы мета-данные
                    page_data['metatitle'] = page.metatitle
                    page_data['metadescription'] = page.metadescription

                    # Заменяем в metatitle падежи регионов
                    page_data['metatitle'] = page_data['metatitle'].replace('[[*reg_i]]',page_data['reg_i'])
                    page_data['metatitle'] = page_data['metatitle'].replace('[[*reg_r]]',page_data['reg_r'])
                    page_data['metatitle'] = page_data['metatitle'].replace('[[*reg_d]]',page_data['reg_d'])
                    page_data['metatitle'] = page_data['metatitle'].replace('[[*reg_v]]',page_data['reg_v'])
                    page_data['metatitle'] = page_data['metatitle'].replace('[[*reg_t]]',page_data['reg_t'])
                    page_data['metatitle'] = page_data['metatitle'].replace('[[*reg_p]]',page_data['reg_p'])

                    # Заменяем в metadescription падежи регионов
                    page_data['metadescription'] = page_data['metadescription'].replace('[[*reg_i]]',page_data['reg_i'])
                    page_data['metadescription'] = page_data['metadescription'].replace('[[*reg_r]]',page_data['reg_r'])
                    page_data['metadescription'] = page_data['metadescription'].replace('[[*reg_d]]',page_data['reg_d'])
                    page_data['metadescription'] = page_data['metadescription'].replace('[[*reg_v]]',page_data['reg_v'])
                    page_data['metadescription'] = page_data['metadescription'].replace('[[*reg_t]]',page_data['reg_t'])
                    page_data['metadescription'] = page_data['metadescription'].replace('[[*reg_p]]',page_data['reg_p'])
                    
                    # Заменяем в metatitle название компании
                    page_data['metatitle'] = page_data['metatitle'].replace('[[*site_title]]',page_data['site_title'])

                    # Заменяем в metadescription название компании
                    page_data['metadescription'] = page_data['metadescription'].replace('[[*site_title]]',page_data['site_title'])
                    
                    # Получаем шаблон
                    template = page.template
                    template_html = template.html
                    
                    # Заменяем в html коде шаблона вызовы чанков на их код
                    while 1 > 0:
                        try:
                            chunk_search = re.search(r'\[\[\$.+\]\]', template_html)
                            chunk_name = chunk_search.group(0).replace('[[$','').replace(']]','')
                            chunk = Chunk.objects.get(title=chunk_name, site=site.id)
                            template_html = template_html.replace(chunk_search.group(0),chunk.html)
                        except:
                            break
                    
                    # Заменяем в html коде шаблона параметры страницы на значения этих параметров
                    while 1 > 0:
                        try:
                            param_search = re.search(r'\[\[\*.+\]\]', template_html)
                            param_name = param_search.group(0).replace('[[*','').replace(']]','')
                            template_html = template_html.replace(param_search.group(0),page_data[param_name])
                        except:
                            break

                    # Заменяем в html коде шаблона вызовы плейсхолдеров на их код
                    while 1 > 0:
                        try:
                            placeholder_search = re.search(r'\[\[\+.+\]\]', template_html)
                            placeholder_name = placeholder_search.group(0).replace('[[+','').replace(']]','')
                            try:
                                placeholder = page.placeholder_set.get(title=placeholder_name)
                            except:
                                errors_count += 1
                                self.stdout.write('Ошибка плейсхолдера! ' + page.title + ' / ' + placeholder_name)
                            

                            # Актуализация полей uniqcodes и uniqwords
                            if placeholder.uniqenable == True:
                                letsmakeuniqcodes = False
                                # Формируем uniqwords
                                result_uniqwords = self.uniqwords(str(placeholder.html))
                                
                                # Проверяем, если менее 1 группы для уникализации, выводим ошибку
                                if len(result_uniqwords) < 1:
                                    errors_count += 1
                                    self.stdout.write('Менее 1 группы для уникализации! ' + page.title + ' / ' + placeholder_name)
                                else:
                                    
                                    if str(result_uniqwords) != str(placeholder.uniqwords):
                                        
                                        if placeholder.uniqwords != '':
                                            if placeholder.uniqcodes == '':
                                                placeholder.uniqwords = str(result_uniqwords)
                                                placeholder.save(update_fields=['uniqwords'])
                                                letsmakeuniqcodes = True
                                            else:
                                                placeholder_uniqwords = placeholder.uniqwords[2:-2].split('\', \'')
                                                for result_uniqwords_item_index, result_uniqwords_item in enumerate(result_uniqwords):

                                                    # Проверяем если обрабатывается последний элемент, не добавлен ли он
                                                    # 1. добавление в конец
                                                    # если индекс текущего равен последнему И длина новой группы больше старой, добавляем в конец
                                                    if ((result_uniqwords_item_index + 1) == len(result_uniqwords)) and (len(result_uniqwords) > len(placeholder_uniqwords)):

                                                        # self.stdout.write(str(result_uniqwords_item_index + 1))
                                                        # self.stdout.write(str(len(result_uniqwords)))
                                                        # self.stdout.write(str(len(result_uniqwords)))
                                                        # self.stdout.write(str(len(placeholder_uniqwords)))

                                                        placeholder_uniqwords.append(result_uniqwords_item)
                                                        placeholder.uniqwords = str(placeholder_uniqwords)

                                                        placeholder_uniqcodes = json.loads(placeholder.uniqcodes.replace('\'','"'))
                                                        for region_item in placeholder.page.site.region_set.all():
                                                            placeholder_uniqcodes[region_item.alias] = placeholder_uniqcodes[region_item.alias] + str(random.randint(0,len(result_uniqwords_item.split('|'))-1))
                                                            placeholder.uniqcodes = json.dumps(placeholder_uniqcodes)
                                                        
                                                        placeholder.save(update_fields=['uniqcodes','uniqwords'])
                                                    
                                                    # Сравниваем новую группу со старой по индексу
                                                    elif str(result_uniqwords_item) != str(placeholder_uniqwords[result_uniqwords_item_index].replace('\'','')):
                                                    # Если они отличаются

                                                        # 2. добавление в середину или начало
                                                        # если следующий за текущим элемент в новой группе совпадает с текущим (по индексу) в старой, добавляем элемент
                                                        if (len(result_uniqwords) > len(placeholder_uniqwords)) and (str(result_uniqwords[result_uniqwords_item_index+1]) == str(placeholder_uniqwords[result_uniqwords_item_index].replace('\'',''))):
                                                                                                                    
                                                            placeholder_uniqwords.insert(result_uniqwords_item_index, result_uniqwords_item)
                                                            placeholder.uniqwords = str(placeholder_uniqwords)

                                                            placeholder_uniqcodes = json.loads(placeholder.uniqcodes.replace('\'','"'))
                                                            for region_item in placeholder.page.site.region_set.all():
                                                                placeholder_uniqcodes_full = placeholder_uniqcodes[region_item.alias]
                                                                placeholder_uniqcodes_leftpart = placeholder_uniqcodes_full[:result_uniqwords_item_index]
                                                                placeholder_uniqcodes_rightpart = placeholder_uniqcodes_full[result_uniqwords_item_index:]
                                                                placeholder_uniqcodes[region_item.alias] = placeholder_uniqcodes_leftpart + str(random.randint(0,len(result_uniqwords_item.split('|'))-1)) + placeholder_uniqcodes_rightpart
                                                                placeholder.uniqcodes = json.dumps(placeholder_uniqcodes)

                                                            placeholder.save(update_fields=['uniqcodes','uniqwords'])

                                                        # 3. удаление из середины или начала
                                                        # если текущий элемент новой группы совпадает со следующим (по индексу) в старой, удаляем элемент
                                                        elif (len(result_uniqwords) < len(placeholder_uniqwords)) and (str(result_uniqwords_item) == str(placeholder_uniqwords[result_uniqwords_item_index+1].replace('\'',''))):
                                                        
                                                            placeholder_uniqwords.pop(result_uniqwords_item_index)
                                                            placeholder.uniqwords = str(placeholder_uniqwords)

                                                            placeholder_uniqcodes = json.loads(placeholder.uniqcodes.replace('\'','"'))
                                                            for region_item in placeholder.page.site.region_set.all():
                                                                placeholder_uniqcodes_full = placeholder_uniqcodes[region_item.alias]
                                                                placeholder_uniqcodes_leftpart = placeholder_uniqcodes_full[:result_uniqwords_item_index]
                                                                placeholder_uniqcodes_rightpart = placeholder_uniqcodes_full[result_uniqwords_item_index+1:]
                                                                placeholder_uniqcodes[region_item.alias] = placeholder_uniqcodes_leftpart + placeholder_uniqcodes_rightpart
                                                                placeholder.uniqcodes = json.dumps(placeholder_uniqcodes)

                                                            placeholder.save(update_fields=['uniqcodes','uniqwords'])

                                                # 4. Удаление из конца
                                                # После проверки всех элементов в новой группе, проверяем, если размер новой < размера старой, значит нужно удалить посл. элемент из старой    
                                                if len(result_uniqwords) < len(placeholder_uniqwords):
                                                    placeholder_uniqwords.pop()
                                                    placeholder.uniqwords = str(placeholder_uniqwords)

                                                    placeholder_uniqcodes = json.loads(placeholder.uniqcodes.replace('\'','"'))
                                                    for region_item in placeholder.page.site.region_set.all():
                                                        placeholder_uniqcodes[region_item.alias] = placeholder_uniqcodes[region_item.alias][:-1]
                                                        placeholder.uniqcodes = json.dumps(placeholder_uniqcodes)

                                                    placeholder.save(update_fields=['uniqcodes','uniqwords'])


                                        else:
                                            placeholder.uniqwords = str(result_uniqwords)
                                            placeholder.save(update_fields=['uniqwords'])
                                            letsmakeuniqcodes = True
                                    else:
                                        if placeholder.uniqcodes == '':
                                            letsmakeuniqcodes = True
                                        
                                    if letsmakeuniqcodes == True:
                                        # Формируем uniqcodes
                                        result_uniqcodes_dict = {}
                                        result_uniqcodes = self.uniqtext(str(placeholder.page.site.region_set.count()), placeholder.html)
                                        # self.stdout.write(str(result_uniqcodes))
                                        region_count = 0
                                        for region_item in placeholder.page.site.region_set.all():
                                            result_uniqcodes_dict[region_item.alias] = result_uniqcodes[region_count]
                                            region_count += 1
                                        placeholder.uniqcodes = str(result_uniqcodes_dict)
                                        placeholder.save(update_fields=['uniqcodes'])

                                # Уникализация текста согласно полей уникализации
                                placeholder_uniqwords_list = placeholder.uniqwords[2:-2].split('\', \'')
                                placeholder_uniqcodes_dict = json.loads(placeholder.uniqcodes.replace('\'','"'))
                                placeholder_uniqcodes_current_region = placeholder_uniqcodes_dict[region.alias]
                                for placeholder_uniqcodes_current_region_item_index, placeholder_uniqcodes_current_region_item in enumerate(list(placeholder_uniqcodes_current_region)):
                                    placeholder_uniqwords_list_current = placeholder_uniqwords_list[placeholder_uniqcodes_current_region_item_index]
                                    placeholder_uniqwords_list_current_list = placeholder_uniqwords_list_current.split('|')
                                    placeholder.html = placeholder.html.replace('{' + placeholder_uniqwords_list_current + '}', str(placeholder_uniqwords_list_current_list[int(placeholder_uniqcodes_current_region_item)]))

                            else:
                                needtosave = False
                                if placeholder.uniqcodes != '':
                                    placeholder.uniqcodes = ''
                                    needtosave = True
                                if placeholder.uniqwords != '':
                                    placeholder.uniqwords = ''
                                    needtosave = True
                                if needtosave == True:
                                    placeholder.save(update_fields=['uniqcodes','uniqwords'])
                                

                            # Заменяем в html коде плейсхолдера падежи
                            placeholder.html = placeholder.html.replace('[[*reg_i]]',page_data['reg_i'])
                            placeholder.html = placeholder.html.replace('[[*reg_r]]',page_data['reg_r'])
                            placeholder.html = placeholder.html.replace('[[*reg_d]]',page_data['reg_d'])
                            placeholder.html = placeholder.html.replace('[[*reg_v]]',page_data['reg_v'])
                            placeholder.html = placeholder.html.replace('[[*reg_t]]',page_data['reg_t'])
                            placeholder.html = placeholder.html.replace('[[*reg_p]]',page_data['reg_p'])

                            # Заменяем в html коде плейсхолдера вызовы параметров страницы
                            placeholder.html = placeholder.html.replace('[[*domain]]',page_data['domain'])
                            placeholder.html = placeholder.html.replace('[[*phone]]',page_data['phone'])
                            placeholder.html = placeholder.html.replace('[[*phone_clean]]',page_data['phone'].replace(' ','').replace('(','').replace(')','').replace('-',''))
                            placeholder.html = placeholder.html.replace('[[*email]]',page_data['email'])
                            placeholder.html = placeholder.html.replace('[[*address]]',page_data['address'])

                            template_html = template_html.replace(placeholder_search.group(0),placeholder.html)
                        except:
                            break

                    # Заменяем региональные хуки на значения
                    while 1 > 0:
                        try:
                            regionhook_search = re.search(r'\[\[\!.+\]\]', template_html)
                            regionhook_condition = regionhook_search.group(0).replace('[[!','').replace(']]','')
                            regionhook_list = regionhook_condition.split('&')
                            regionhook_dict = dict()
                            for regionhook_item in regionhook_list:
                                regionhook_item = regionhook_item.split('=')
                                regionhook_item_regioncode = regionhook_item[0]
                                regionhook_item_content = regionhook_item[1].replace('"','')
                                regionhook_dict[regionhook_item_regioncode] = regionhook_item_content
                            if region.alias in regionhook_dict:
                                regionhook_output = regionhook_dict[region.alias]
                            else:
                                regionhook_output = regionhook_dict['else']
                            template_html = template_html.replace(regionhook_search.group(0),regionhook_output)
                            break
                        except:
                            break

                    # РЕЗУЛЬТАТ
                    # На данном этапе получен полностью скомпилированный код страницы
                    # self.stdout.write(site.title + '(' + region.title + '): ' + page.title + ' > код сформирован')

                    # Формируем полный адрес страницы с учетом вложенности
                    full_page_dir = self.get_full_page_dir(page)

                    # Создаем временную папку в соответствии с адресом страницы
                    path = os.getcwd()
                    path = path + '/build/'
                    if region.main_region:
                        new_dir = path + site.title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + full_page_dir
                    else:
                        if site.hosting == 'beget':
                            new_dir = path + site.title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + '/public_html' + full_page_dir
                        elif site.hosting == 'regru':
                            new_dir = path + site.title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + full_page_dir
                    
                    try:
                        os.makedirs(new_dir, exist_ok=True)
                    except OSError as exc:
                        errors_count += 11
                        self.stdout.write("Создать директорию %s не удалось!" % new_dir)

                    # Сохраняем файл
                    if str(page.alias) != '/':
                        full_page_path = new_dir + '/' + str(page.alias) + '.html'
                    else:
                        full_page_path = new_dir + '/index.html'
                    
                    try:
                        f = open(full_page_path, 'w')
                        f.write(template_html)
                        f.close()
                        # self.stdout.write(site.title + '(' + region.title + '): ' + page.title + ' > файл создан')
                    except:
                        errors_count += 1
                        self.stdout.write('Ошибка создания файла! ' + page.title)
                
                # Копируем ассеты в папку поддомена
                try:
                    path = os.getcwd()
                    assets_path = path + '/build_assets/' + site.title + '/'
                    if region.main_region:
                        subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/'
                    else:
                        if site.hosting == 'beget':
                            subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + '/public_html/'
                        elif site.hosting == 'regru':
                            subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + '/'
                    shutil.copytree(assets_path, subdomain_path+'assets/')
                except:
                    errors_count += 1
                    self.stdout.write('Ошибка копирования assets!')

                # Копирование фавикона в корень поддомена
                try:
                    path = os.getcwd()
                    if region.main_region:
                        subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/'
                    else:
                        if site.hosting == 'beget':
                            subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + '/public_html/'
                        elif site.hosting == 'regru':
                            subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + '/'
                    shutil.copyfile(subdomain_path + site.favicon, subdomain_path + 'favicon.ico')
                except:
                    errors_count += 1
                    self.stdout.write('Ошибка копирования favicon!')

                # Создаем robots.txt в папке поддомена
                # try:
                #     path = os.getcwd()
                #     subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/'
                #     if region.main_region:
                #         robots = open(subdomain_path + 'robots_main.txt', 'w')
                #     else:
                #         robots = open(subdomain_path + 'robots_' + region.alias + '.txt', 'w')
                        
                #     robots.write(site.robots)

                #     if site.ssl:
                #         protocol = 'https://'
                #     else:
                #         protocol = 'http://'

                #     if region.main_region:
                #         robots.write('\nSitemap: ' + protocol + site.domain + '/sitemap.xml')
                #     else:
                #         robots.write('\nSitemap: ' + protocol + region.alias + '.' + site.domain + '/sitemap.xml')

                #     robots.close()
                # except:
                #     errors_count += 1
                #     self.stdout.write('Ошибка создания Robots.txt')
                try:
                    path = os.getcwd()
                    if region.main_region:
                        subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/'
                    else:
                        if site.hosting == 'beget':
                            subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + '/public_html/'
                        elif site.hosting == 'regru':
                            subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + '/'
                    robots = open(subdomain_path + 'robots.txt', 'w')
                    robots.write(site.robots)

                    if site.ssl:
                        protocol = 'https://'
                    else:
                        protocol = 'http://'

                    if region.main_region:
                        robots.write('\nSitemap: ' + protocol + site.domain + '/sitemap.xml')
                    else:
                        robots.write('\nSitemap: ' + protocol + region.alias + '.' + site.domain + '/sitemap.xml')

                    robots.close()
                except:
                    errors_count += 1
                    self.stdout.write('Ошибка создания Robots.txt')
                
                # Создаем .htaccess в папке поддомена
                try:
                    path = os.getcwd()
                    if region.main_region:
                        subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/'
                    else:
                        subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + '/'
                    htaccess = open(subdomain_path + '.htaccess', 'w')
                    
                    if region.main_region:
                        htaccess.write('RewriteEngine On')
                        # Убираем .html
                        htaccess.write('\nRewriteBase /')
                        htaccess.write('\nRewriteCond %{THE_REQUEST} ^[A-Z]{3,9}\ /([^.]+)\.html\ HTTP')
                        htaccess.write('\nRewriteRule ^([^.]+)\.html$ https://' + site.domain + '/$1 [R=301,L]')
                        htaccess.write('\nRewriteCond %{REQUEST_URI} !(\.[^./]+)$')
                        htaccess.write('\nRewriteCond %{REQUEST_fileNAME} !-d')
                        htaccess.write('\nRewriteCond %{REQUEST_fileNAME} !-f')
                        htaccess.write('\nRewriteRule (.*) /$1.html [L]')
                        if site.hosting == 'beget':
                            # Универсальная переадресация поддоменов в директории
                            htaccess.write('\nRewriteRule ^(.*)$ $1.html')
                            htaccess.write('\nRewriteCond %{HTTP_HOST} ^(.*).' + site.domain + '$\nRewriteRule ^(.*)$ /%1/public_html/$1 [L]')
                        # Правила обработки поддоменов для каждого региона
                        # for region_item in regions:
                        #     if region_item.main_region:
                        #         continue
                        #     else:
                        #         htaccess.write('\nRewriteCond %{HTTP_HOST} ^' + region_item.alias + '\.' + site.domain + '$')
                        #         htaccess.write('\nRewriteCond %{REQUEST_URI} !/' + region_item.alias + '/public_html/')
                        #         htaccess.write('\nRewriteRule ^(.*)$ /' + region_item.alias + '/public_html/$1 [L]')
                    else:
                        htaccess.write('RewriteEngine On')
                        if site.hosting == 'regru':
                            # Убираем .html
                            htaccess.write('\nRewriteBase /')
                            htaccess.write('\nRewriteCond %{THE_REQUEST} ^[A-Z]{3,9}\ /([^.]+)\.html\ HTTP')
                            htaccess.write('\nRewriteRule ^([^.]+)\.html$ https://' + region.alias + '.' + site.domain + '/$1 [R=301,L]')
                            htaccess.write('\nRewriteCond %{REQUEST_URI} !(\.[^./]+)$')
                            htaccess.write('\nRewriteCond %{REQUEST_fileNAME} !-d')
                            htaccess.write('\nRewriteCond %{REQUEST_fileNAME} !-f')
                            htaccess.write('\nRewriteRule (.*) /$1.html [L]')
                            
                    htaccess.close()
                except:
                    errors_count += 1
                    self.stdout.write('Ошибка создания .htaccess')

                # Создаем sitemap.xml в папке поддомена
                try:
                    if site.ssl:
                        protocol = 'https://'
                    else:
                        protocol = 'http://'

                    path = os.getcwd()
                    if region.main_region:
                        subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/'
                        subdomain_domain = protocol + site.domain
                    else:
                        if site.hosting == 'beget':
                            subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + '/public_html/'
                            subdomain_domain = protocol + region.alias + '.' + site.domain
                        elif site.hosting == 'regru':
                            subdomain_path = path + '/build/' + site_title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/' + region.alias + '/'
                            subdomain_domain = protocol + region.alias

                    sitemap = open(subdomain_path + 'sitemap.xml', 'w')

                    sitemap.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
		
                    for page in site.page_set.all():
                        if str(page.alias) != '/':
                            full_page_path = subdomain_domain + self.get_full_page_dir(page) + '/' + str(page.alias)
                        else:
                            full_page_path = subdomain_domain + '/'

                        sitemap.write('\t<url>\n\t\t<loc>' + full_page_path + '</loc>\n\t\t<lastmod>' + str(today.strftime("%Y-%m-%dT%H:%M:%S")) + '+01:00</lastmod>\n\t\t<priority>' + str(page.sitemap_priority) + '</priority>\n\t</url>\n')
                    
                    sitemap.write('</urlset>')
                    sitemap.close()

                except:
                    errors_count += 1
                    self.stdout.write('Ошибка создания Sitemap.xml')
            
            self.stdout.write('-----------------------------------------------------------------------')
            # Архивируем папку сборки
            try:
                path = os.getcwd()
                path = path + '/build/' + site.title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/'
                build_zip=zipfile.ZipFile(path + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '.zip','w')
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_rel_path = str(os.path.join(root,file))
                        if (str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '.zip') in file_rel_path:
                            continue
                        file_rel_path = file_rel_path.replace(str(os.getcwd()) + '/build/' + site.title + '/' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + '/','')
                        build_zip.write(os.path.join(root,file),file_rel_path)
                build_zip.close()
                self.stdout.write('Архив ' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + ' создан.')
            except:
                self.stdout.write('Ошибка создания архива ' + str(today.strftime("%Y-%m-%d-%H-%M-%S")))

            self.stdout.write('-----------------------------------------------------------------------')
            if errors_count != 0:
                self.stdout.write(str(errors_count) + ' ошибок (сборка № ' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + ')')
            else:
                self.stdout.write('Сборка № ' + str(today.strftime("%Y-%m-%d-%H-%M-%S")) + ' выполнена успешно.')
            site.build = str(today.strftime("%Y-%m-%d-%H-%M-%S"))
            site.save(update_fields=['build'])

            #self.stdout.write(str(page))