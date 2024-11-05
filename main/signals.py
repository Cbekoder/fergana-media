from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article, Video
from .utils import sendArticle, sendVideo


@receiver(post_save, sender=Article)
def send_article_photo(sender, instance, created, **kwargs):
    if instance.region:
        region = instance.region.name
    else:
        region = None
    if instance.to_send_bot:
        if instance.message_id is None:
            response = sendArticle(
                instance.id,
                None,
                instance.title,
                instance.intro,
                instance.image.path,
                instance.categories.values_list('title', flat=True),
                region,
                instance.news_of_the_day,
            )
            if response:
                instance.message_id = response['result']['message_id']
                instance.save()
            else:
                print("error in bot")
        else:
            sendArticle(
                instance.id,
                instance.message_id,
                instance.title,
                instance.intro,
                instance.image.path,
                instance.categories.values_list('title', flat=True),
                region,
                instance.news_of_the_day,
            )

@receiver(post_save, sender=Video)
def send_video_photo(sender, instance, created, **kwargs):
    if instance.cover:
        cover = instance.cover.path
    else:
        cover = None
    if instance.to_send_bot:
        if instance.message_id is None:
            response = sendVideo(
                None,
                instance.title,
                instance.intro,
                cover,
                instance.url,
                instance.categories.values_list('title', flat=True)
            )
            if response:
                instance.message_id = response['result']['message_id']
                instance.save()
            else:
                print("error in bot")
        else:
            sendVideo(
                instance.message_id,
                instance.title,
                instance.intro,
                cover,
                instance.url,
                instance.categories.values_list('title', flat=True)
            )
