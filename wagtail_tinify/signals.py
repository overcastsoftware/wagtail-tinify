from wagtail_tinify.models import TinyPngOptimizeThread
from wagtail.wagtailimages import get_image_model
from django.dispatch.dispatcher import receiver


rendition_model = get_image_model().get_rendition_model()

@receiver(post_save, sender=rendition_model)
def rendition_optimize(sender, instance, **kwargs):
    TinyPngOptimizeThread(instance).start()
