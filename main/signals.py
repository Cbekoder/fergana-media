from pyexpat.errors import messages

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article, Video, BotMessageIDs
from .utils import sendArticle, sendVideo, delete_message


@receiver(post_save, sender=Article)
def send_article_photo(sender, instance, **kwargs):
    messages_list = BotMessageIDs.objects.filter(article = instance.id)
    if messages_list:
        message = messages_list[0]
    else:
        message = None
    if instance.region:
        region = instance.region.name
    else:
        region = None
    if instance.to_send_bot and instance.publish:
        if message:
            sendArticle(
                instance.id,
                message.message_id,
                instance.title,
                instance.intro,
                instance.image.path,
                instance.categories.values_list('title', flat=True),
                region,
                instance.news_of_the_day,
            )
        else:
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
                BotMessageIDs.objects.create(article = instance, message_id=response['result']['message_id'])
            else:
                print("error in bot")
    else:
        if message:
            delete_message(message.message_id)
            message.delete()



@receiver(post_save, sender=Video)
def send_video_photo(sender, instance, created, **kwargs):
    message_list = BotMessageIDs.objects.filter(video = instance.id)
    if message_list:
        message = message_list[0]
    else:
        message = None
    if instance.cover:
        cover = instance.cover.path
    else:
        cover = None
    if instance.to_send_bot and instance.publish:
        if message.message_id is None:
            response = sendVideo(
                None,
                instance.title,
                instance.intro,
                cover,
                instance.url,
                instance.categories.values_list('title', flat=True)
            )
            if response:
                BotMessageIDs.objects.create(video = instance, message_id=response['result']['message_id'])
            else:
                print("error in bot")
        else:
            sendVideo(
                message.message_id,
                instance.title,
                instance.intro,
                cover,
                instance.url,
                instance.categories.values_list('title', flat=True)
            )
    else:
        if message.message_id:
            delete_message(message.message_id)
            message.delete()
