from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from .task import post_created
from .models import *


@receiver(m2m_changed, sender=PostCategory)
def post_created_signals(instance, **kwargs):
    if kwargs['action'] == 'post_add':
        post_created.delay(instance.id)

#         emails = User.objects.filter(
#             subscriptions__category__in=instance.categories_post.all()
#         ).values_list('email', flat=True)

#         emails = set(emails)

#         subject = f'Новый пост в категории {instance.categories_post.all()}'       
#         #   subject = f'Новый пост в категории {','.join([category.name for category in instance.categories_post.all()])}'
        
#         text_content = (
#             f'Название: {instance.name_post}\n'
#             #f'Содержание: {instance.text_post}\n\n'
#             f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
#         )
#         html_content = (
#             f'Название: {instance.name_post}<br>'
#             #f'Содержание: {instance.text_post}<br><br>'
#             f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#             f'Ссылка на пост</a>'
#         )
#         for email in emails:
#             msg = EmailMultiAlternatives(subject, text_content, None, [email])
#             msg.attach_alternative(html_content, "text/html")
#             msg.send()