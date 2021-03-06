from django.db import models


class RequestLogV1(models.Model):
    EXCLUDED_ATTRIBUTES = (
        'classification[annotations][0][results]',
        'classification[subject_ids][]',
        'password', )

    project = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def add_attributes(self, attribute_dict):
        for k, v in attribute_dict.items():
            if k not in RequestLogV1.EXCLUDED_ATTRIBUTES:
                RequestLogV1AttributeValue(name=k, value=v, parent=self).save()


class RequestLogV1AttributeValue(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    parent = models.ForeignKey(RequestLogV1)