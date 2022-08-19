from django.db import models


class TagManager(models.Manager):
    def create_tag(self, name):
        if name is None:
            raise TypeError('tag must have name')

        if self.filter(name=name).exists():
            return self.filter(name=name)

        tag = self.model(
            name = name,
        )
        tag.save()

        return tag


class Tag(models.Model):
   name = models.CharField(max_length=30, unique=True, primary_key=False)
   objects = TagManager()
