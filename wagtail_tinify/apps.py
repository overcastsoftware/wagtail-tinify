from __future__ import unicode_literals

from django.apps import AppConfig


class WagtailTinifyConfig(AppConfig):
    name = 'wagtail_tinify'

    def ready(self):
        from wagtail_tinify import signals