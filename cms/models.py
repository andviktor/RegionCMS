from django.db import models
from django.contrib import admin
from django.urls import reverse

class Site(models.Model):
    title = models.CharField(max_length=50, default="Новый сайт", verbose_name="Наименование")
    domain = models.CharField(max_length=50, default="mysite.ru", verbose_name="Домен")
    ssl = models.BooleanField(default=False, help_text="Сайт доступен по протоколу HTTPS", verbose_name="SSL сертификат")
    ftp_host = models.CharField(max_length=20, default="", verbose_name="FTP хост")
    ftp_user = models.CharField(max_length=30, default="", verbose_name="FTP пользователь")
    ftp_password = models.CharField(max_length=30, default="", verbose_name="FTP пароль")
    robots = models.TextField(default="", help_text="Директивы HOST и SITEMAP не указываются, они проставляются автоматически.", verbose_name="Robots.txt")
    favicon = models.CharField(max_length=50, default="assets/images/icons/favicon/favicon.ico", verbose_name="Фавикон")
    log = models.TextField(default="")
    build = models.CharField(max_length=30, default="", blank=True)
    upload_date = models.CharField(max_length=30, default="", blank=True)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('site-detail', kwargs={'pk': self.pk})
    class Meta:
        verbose_name_plural = "Сайты"

class Region(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name="Сайт")
    title = models.CharField(max_length=50, default="Новый регион", verbose_name="Наименование")
    main_region = models.BooleanField(default=False, help_text="Размещается на основном домене.", verbose_name="Основной регион")
    padeji = models.CharField(max_length=200, default="", help_text="Например: \"Москва,Москвы,Москве,Москву,Москвой,Москве\"", verbose_name="Наименование во всех падежах, через запятую")
    alias = models.CharField(max_length=50, default="", help_text="Например: \"msk\"", verbose_name="Псевдоним")
    phone = models.CharField(max_length=50, default="", verbose_name="Телефон")
    email = models.CharField(max_length=50, default="", verbose_name="E-mail")
    address = models.CharField(max_length=100, default="", verbose_name="Адрес")
    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Регионы"

class Template(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name="Сайт")
    title = models.CharField(max_length=50, default="Новый шаблон", verbose_name="Наименование")
    html = models.TextField(default="", verbose_name="HTML код")
   
    def __str__(self):
        return self.site.title + " / " + self.title
    class Meta:
        verbose_name_plural = "Шаблоны"

class Chunk(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name="Сайт")
    title = models.CharField(max_length=50, default="Новый чанк", verbose_name="Наименование")
    html = models.TextField(default="", verbose_name="HTML код")
   
    def __str__(self):
        return self.site.title + " / " + self.title
    class Meta:
        verbose_name_plural = "Чанки"

class Page(models.Model):
    site = models.ForeignKey(Site, on_delete=models.CASCADE, verbose_name="Сайт")
    title = models.CharField(max_length=100, default="Новая страница", verbose_name="Наименование")
    alias = models.CharField(max_length=100, default="", help_text="Для главной \"/\", для остальных без слэшей", verbose_name="Псевдоним")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, help_text="Макс. 3 уровня, пример: /first/second/third, родитель не указывается только у главной страницы, для остальных страниц 1 уровня родитель - Главная", verbose_name="Родительская страница")
    template = models.ForeignKey(Template, on_delete=models.CASCADE, verbose_name="Шаблон")
    metatitle = models.CharField(max_length=80, default="", verbose_name="META-title")
    metadescription = models.TextField(max_length=170, default="", verbose_name="META-description")
    sitemap_priority = models.CharField(max_length=5, default="1.0", verbose_name="Приоритет для Sitemap.xml")
   
    def __str__(self):
        return self.site.title + " / " + self.title
    class Meta:
        verbose_name_plural = "Страницы"

class Placeholder(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name="Страница")
    title = models.CharField(max_length=50, default="Новый плейсхолдер", verbose_name="Наименование")
    html = models.TextField(default="", verbose_name="HTML код")
    uniqenable = models.BooleanField(default=False, help_text="Включить уникализацию", verbose_name="Уникализация")
    uniqcodes = models.TextField(default="", blank=True)
    uniqwords = models.TextField(default="", blank=True)
   
    def __str__(self):
        return self.page.site.title + " / " + self.page.title + " / " + self.title
    class Meta:
        verbose_name_plural = "Плейсхолдеры"