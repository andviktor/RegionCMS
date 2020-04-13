from django.core.management.base import BaseCommand, CommandError
from cms.models import Site
import re, os, sys, datetime, zipfile, paramiko, ftplib

class Command(BaseCommand):
    help = 'Print current site title'

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

            #try:
            # Разархивируем архив на сервере
            host = site.ftp_host
            user = site.ftp_user
            secret = site.ftp_password
            port = 22
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Подключение
            client.connect(hostname=host, username=user, password=secret, port=port)
            # Выполнение команд

            # Удаляем все файлы и директории
            for region in site.region_set.all():
                try:
                    if region.main_region:
                        domain_dir = site.domain
                        if site.hosting == 'beget':
                            stdin, stdout, stderr = client.exec_command('rm -rd ' + site.domain + '/public_html')
                        elif site.hosting == 'regru':
                            stdin, stdout, stderr = client.exec_command('cd www/' + site.domain + '/; rm -rd ./*')
                            stdin, stdout, stderr = client.exec_command('cd www/' + site.domain + '/; rm .htaccess')
                    else:
                        if site.hosting == 'beget':
                            domain_dir = region.alias + '.' + site.domain
                            stdin, stdout, stderr = client.exec_command('rm -rd ' + domain_dir + '/public_html')
                        elif site.hosting == 'regru':
                            domain_dir = region.alias
                            stdin, stdout, stderr = client.exec_command('cd www/' + site.domain + '/; rm -rd ./' + domain_dir)
                    self.stdout.write('Директория ' + domain_dir + ' очищена.')
                except:
                    self.stdout.write('Ошибка очистки директории ' + site.domain)

            # Читаем результат
            data = stdout.read() + stderr.read()
            # Выводим лог
            client_output = data.decode('ascii').splitlines(True)
            for client_output_line in client_output:
                self.stdout.write(client_output_line)

            self.stdout.write('-----------------------------------------------------------------------')

            if site.hosting == 'regru':
                try:
                    stdin, stdout, stderr = client.exec_command('cd www/' + site.domain + '/; ln -s . s113')
                except:
                    self.stdout.write('Ошибка создания символической ссылки на главный домен!')

                self.stdout.write('-----------------------------------------------------------------------')

            # Загружаем архив по FTP на сервер
            try:
                ftp = ftplib.FTP(site.ftp_host)
                ftp.login(site.ftp_user, site.ftp_password)
                self.stdout.write('Подключение по FTP к серверу прошло успешно.')
            except:
                self.stdout.write('Ошибка подключения к серверу по FTP!.')

            try:
                path = os.getcwd()
                path = path + '/build/' + site.title + '/' + site.build + '/' + site.build + '.zip'
                ftp.storbinary('STOR ' + site.build + '.zip', open(path, 'rb'))
                ftp.quit()
                self.stdout.write('Архив успешно загружен на сервер.')
            except:
                self.stdout.write('Ошибка загрузки архива сборки на сервер!')

            self.stdout.write('-----------------------------------------------------------------------')

            try:
                if site.hosting == 'beget':
                    stdin, stdout, stderr = client.exec_command('unzip -o ' + site.build + '.zip')
                elif site.hosting == 'regru':
                    stdin, stdout, stderr = client.exec_command('cd www/' + site.domain + '/; unzip ' + site.build + '.zip')
            except:
                self.stdout.write('Ошибка распаковки архива сборки на сервере!')

            # Читаем результат
            data = stdout.read() + stderr.read()
            # Выводим лог
            client_output = data.decode('ascii').splitlines(True)

            for client_output_line in client_output:
                self.stdout.write(client_output_line)

            self.stdout.write('-----------------------------------------------------------------------')

            try:
                if site.hosting == 'beget':
                    stdin, stdout, stderr = client.exec_command('rm ' + site.build + '.zip')
                elif site.hosting == 'regru':
                    stdin, stdout, stderr = client.exec_command('cd www/' + site.domain + '/; rm ' + site.build + '.zip')
                self.stdout.write('Файл архива сборки успешно удален.')
            except:
                self.stdout.write('Ошибка удаления архива сборки!')

            # Читаем результат
            data = stdout.read() + stderr.read()
            # Выводим лог
            client_output = data.decode('ascii').splitlines(True)
            for client_output_line in client_output:
                self.stdout.write(client_output_line)


            client.close()
                
            # except:
            #     self.stdout.write('Ошибка подключения по SSH!')

            self.stdout.write('-----------------------------------------------------------------------')
            self.stdout.write('Дата и время загрузки ' + str(today.strftime("%Y-%m-%d-%H-%M-%S")))
            site.upload_date = str(today.strftime("%Y-%m-%d-%H-%M-%S"))
            site.save(update_fields=['upload_date'])

            #self.stdout.write(str(page))