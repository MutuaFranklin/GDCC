from typing_extensions import Required
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.functions import Length
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.html import escape
from urllib.parse import urlparse



class Comment(models.Model):
    comment = models.TextField()
    content_type =   models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object=GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
       return self.comment

    class Meta:
        ordering = ['date_created']
    
    def clean(self, comment):
        return escape(comment)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

class ProteinSequence(models.Model):
    protein_sequence = models.CharField(max_length=10000)
    dna_sequence = models.CharField(max_length=10000)
    comments = GenericRelation(Comment)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

 
    def __str__(self):
       return self.protein_sequence

    class Meta:
        ordering = ['date_created']

    def clean(self):
        # required fields.
       
        if self.protein_sequence is  None:
            raise ValidationError({'protein_sequence':_('This field is required.')})

        if self.dna_sequence is  None:
            raise ValidationError({'dna_sequence':_('This field is required.')})

        if Length(self.dna_sequence)!=Length(self.dna_sequence)*3:
            raise ValidationError({'dna_sequence':_('This field characters should be three times as many as the number of characters of the protein amino acids field.')})


    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
        

class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)


    def __str__(self):
       return self.content

    class Meta:
        ordering = ['date_created']

    def clean(self, content):
        return escape(content)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)



class Notification(models.Model):
    notification_type_choice = ("Link", "Link"),("Static","Static"),("System","System")

    notification_type = models.TextField(choices=notification_type_choice)
    text_message = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

   
    def __str__(self):
       return self.text_message

    class Meta:
        ordering = ['date_created']

    
    def clean(self, text_message):
        if self.notification_type == 'Link':
            try:
                urlparse(text_message)
            except ValueError:
                raise ValidationError('Link notifications should contain a link')
                
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)




       
    