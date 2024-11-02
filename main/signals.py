from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article
from .utils import sendArticle


@receiver(post_save, sender=Article)
def send_article_photo(sender, instance, created, **kwargs):
    if created and instance.message_id is None:
        response = sendArticle(
            instance.id,
            None,
            instance.title,
            instance.intro,
            instance.image.path,
            instance.categories.values_list('title', flat=True),
            instance.region.name,
            instance.news_of_the_day,
        )
        instance.message_id = response['result']['message_id']
        instance.save()
    else:
        sendArticle(
            instance.id,
            instance.message_id,
            instance.title,
            instance.intro,
            instance.image.path,
            instance.categories.values_list('title', flat=True),
            instance.region.name,
            instance.news_of_the_day,
        )
