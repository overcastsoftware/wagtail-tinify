from __future__ import unicode_literals

import os, threading, tinify
from urlparse import urlparse
from django.db.models.signals import post_save
from django.templatetags.static import StaticNode
from django.conf import settings

aws_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_bucket = os.getenv('AWS_STORAGE_BUCKET_NAME')
aws_region = os.getenv('AWS_REGION')
cf_api_key = os.getenv('CF_API_KEY')
cf_api_email = os.getenv('CF_API_EMAIL')
cf_zone_id = os.getenv('CF_ZONE_ID')
tinify.key = os.getenv('TINYPNG_API_KEY')

# If cloudflare key is not set, then we don't need to import Cloudflare
if cf_api_key and cf_api_email and cf_api_key:
    import CloudFlare

class TinyPngOptimizeThread(threading.Thread):
    def __init__(self, instance, **kwargs):
        self.instance = instance
        super(TinyPngOptimizeThread, self).__init__(**kwargs)

    def run(self):
        if tinify.key != None:
            # If aws keys are available, use them to fetch the image and write back
            if aws_key_id and aws_secret and aws_bucket and aws_region:
                source_url_http = urlparse(StaticNode.handle_simple(self.instance.file.name), scheme='http').geturl()
                source_url_https = urlparse(StaticNode.handle_simple(self.instance.file.name), scheme='https').geturl()
                source = tinify.from_url(source_url_https)
                path = "%s/%s" % (aws_bucket, self.instance.file.name)
                source.store(service='s3',aws_access_key_id=aws_key_id,aws_secret_access_key=aws_secret,region=aws_region,path=path)
                if cf_zone_id and cf_api_key and cf_api_email:
                    cf = CloudFlare.CloudFlare()
                    cf.zones.purge_cache.delete(cf_zone_id, data={'files':[source_url_http, source_url_https]})
            # Else we grab the local image, optimize it and override the local file
            else:
                path = os.getcwd()+self.instance.url
                source = tinify.from_file(path)
                source.to_file(path)
        else:
            print "No tinify key"

