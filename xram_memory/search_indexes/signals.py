from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry

__all__ = (
    'update_document',
    'delete_document',
)


@receiver(post_save)
def update_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'taxonomy' or app_label == 'artifact':
        if model_name == 'keyword':
            instances = instance.news.all()
            for _instance in instances:
                registry.update(_instance)

        if model_name == 'subject':
            instances = instance.news.all()
            for _instance in instances:
                registry.update(_instance)


@receiver(post_delete)
def delete_document(sender, **kwargs):
    app_label = sender._meta.app_label
    model_name = sender._meta.model_name
    instance = kwargs['instance']

    if app_label == 'taxonomy':
        if model_name == 'keyword':
            instances = instance.news.all()
            for _instance in instances:
                registry.update(_instance)

        if model_name == 'subject':
            instances = instance.news.all()
            for _instance in instances:
                registry.update(_instance)
