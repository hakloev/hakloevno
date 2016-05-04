from django.db import models
from django.core.urlresolvers import reverse
from datetime import datetime
from . import utils


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


class DinnerPlanQuerySet(models.QuerySet):
    def current_plan(self):
        today = datetime.today()
        start, end = utils.calculate_week_ends_for_date(today)
        return self.filter(start_date=start).first()


class DinnerPlan(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(blank=True)
    cost = models.FloatField(verbose_name='Total cost', blank=True, null=True)
    meals = models.ManyToManyField(Recipe, through='DinnerPlanItem')

    objects = DinnerPlanQuerySet.as_manager()

    @property
    def week(self):
        """
        Returns the week number for models instance
        :return: String representation of the week number
        """
        return str(utils.get_week_from_date(self.start_date))

    def __str__(self):
        # Display as week number
        return 'Dinner Plan for week %s' % self.week

    def save(self, *args, **kwargs):
        self.start_date, self.end_date = utils.calculate_week_ends_for_date(self.start_date)
        super(DinnerPlan, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('food:plan_details', kwargs={'year': str(self.start_date.year),
                                                    'week': str(self.week)})

    class Meta:
        verbose_name = 'Dinner Plan'
        verbose_name_plural = 'Dinner Plans'
        get_latest_by = 'end_date'


class DinnerPlanItem(models.Model):
    # Define possible days
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

    period = models.ForeignKey(DinnerPlan, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    day = models.IntegerField(choices=WEEKDAYS)
    eaten = models.BooleanField(default=False)

    def __str__(self):
        return '%s, week %s: %s' % (self.WEEKDAYS[self.day][1], str(self.period.week), self.recipe)

    class Meta:
        ordering = ['period', 'day']
        unique_together = ('period', 'day')  # This will crash if week is not a date, need year as well
        verbose_name = 'Dinner Plan Element'
        verbose_name_plural = 'Dinner Plan Elements'