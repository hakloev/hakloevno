from django.db import models
from django.core.urlresolvers import reverse


class WeekPlan(models.Model):
    start_date = models.DateField()

    def __str__(self):
        # Display as week number
        return str(self.start_date.isocalendar()[1])


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    url = models.URLField(blank=False)
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('food:recipe', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['title']


class WeekPlanRecipes(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    WEEKDAYS = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday')
    )

    week = models.ForeignKey(WeekPlan)
    recipe = models.ForeignKey(Recipe)
    day = models.IntegerField(choices=WEEKDAYS)

    def __str__(self):
        return 'Week %s, %s => %s' % (self.week, self.WEEKDAYS[self.day][1], self.recipe)

    class Meta:
        ordering = ['week', 'day']
        unique_together = ('week', 'day')  # This will crash if week is not a date, need year as well
        verbose_name = 'Plan Element'
        verbose_name_plural = 'Plan Elements'
