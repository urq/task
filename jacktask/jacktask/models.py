from django.db import models

class Task(models.Model):
    description = models.TextField()
    tags = models.ManyToManyField('Tag', null=True)
    status = models.CharField(
                default='P',
                max_length=1,
                choices=(('P','Pending'), ('C', 'Completed'))
             )
    priority = models.CharField(
                  default='L',
                  max_length=1,
                  choices=(('H','High'),('M','Medium'),('L','Low'))
               )
    dependencies = models.ManyToManyField('self', symmetrical=False, null=True)
    artifacts = models.ForeignKey('Artifact', null=True)

    # dates and times
    estimated_time = models.PositiveIntegerField(null=True)
    actual_time = models.PositiveIntegerField(null=True)
    due = models.DateTimeField(null=True)
    notification = models.ForeignKey('Notification', null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    last_modified_datetime = models.DateTimeField(auto_now=True)
    done_datetime = models.DateTimeField(null=True)

    # recurrance stuff
    start_datetime = models.DateTimeField(null=True)
    until_datetime = models.DateTimeField(null=True)
    occurrences = models.IntegerField(null=True)
    repeats = models.CharField(
                    null=True,
                    max_length=1,
                    choices=(('H','Hourly'),
                             ('D','Daily'),
                             ('M','Monthly'),
                             ('Y','Yearly'))
              )
    # repeat_on =

class Tag(models.Model):
    name = models.CharField(max_length=256)
    tasks = models.ManyToManyField('Task', null=True)

class Artifact(models.Model):
    pass

class Notification(models.Model):
    # notify = models.IntegerField(description="The number of seconds before or after an event to send a notification. Positive values occur after the event. Negative values occur before the event.")
    pass

class Day(models.Model):
    pass
