=====
Wagtail-tinify
=====

Wagtail-tinify optimizes the renditions that wagtail creates. It supports both locally served files as well as files served from Amazon S3. It also supports cachebusting for Cloudflare, should you be using it as CDN in front of the S3 bucket.

Quick start
-----------

1. Add "wagtail-tinify" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'wagtain-tinify',
    ]

2. Add TINYPNG_API_KEY=XXXXXX to your .env (if you dont have an API key, go to https://tinypng.com/developers to request one.)

3. If you are using S3 for storing images, make sure that the .env includes AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, 
AWS_STORAGE_BUCKET_NAME, and AWS_REGION

4. If you are using Cloudflare as a CDN, you also need to include CF_API_KEY in your .env

Thats it! You now need to delete all renditions from the wagtailimages_rendition table and reload your site. You should see the counter on your account page at tinypng increase, and pagespeed should stop complaining about uncompressed images. Note that this plugin will compress all renditions, including those used in the Admin panel. You have 500 free images per month, but if you use lots of images you might need to bump up to a paid plan.