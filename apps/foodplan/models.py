from django.db import models
from django.core.urlresolvers import reverse
from datetime import timedelta


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


class DinnerPlan(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(blank=True)
    cost = models.FloatField(verbose_name='Total cost', blank=True, null=True)
    meals = models.ManyToManyField(Recipe, through='DinnerPlanItem')

    def __str__(self):
        # Display as week number
        return 'Dinner Plan for week %s' % self._week()

    def save(self, *args, **kwargs):
        self.start_date, self.end_date = self.calculate_week_ends()
        super(DinnerPlan, self).save(*args, **kwargs)

    def _week(self):
        return self.start_date.isocalendar()[1]

    def get_week_number(self):
        """
        Returns the week number for models instance
        :return:
        """
        return str(self._week())

    def calculate_week_ends(self):
        """
        Calculates start and end date for week
        :return: beginning and end of week
        """
        day_of_week = self.start_date.weekday()
        to_beginning_of_week = timedelta(days=day_of_week)
        beginning_of_week = self.start_date - to_beginning_of_week
        to_ending_of_week = timedelta(days=6 - day_of_week)
        end_of_week = self.start_date + to_ending_of_week
        return beginning_of_week, end_of_week

    def get_absolute_url(self):
        return reverse('food:plan_details', kwargs={'year': str(self.start_date.year),
                                                    'week': self.get_week_number()})

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

    def __str__(self):
        return '%s, week %s: %s' % (self.WEEKDAYS[self.day][1], str(self.period.get_week_number()), self.recipe)

    class Meta:
        ordering = ['day', 'period']
        unique_together = ('period', 'day')  # This will crash if week is not a date, need year as well
        verbose_name = 'Dinner Plan Element'
        verbose_name_plural = 'Dinner Plan Elements'
