from django.db import models
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from datetime import datetime
from . import utils


class Recipe(models.Model):
    NOT_RATED = 0
    AWFUL = 1
    BAD = 2
    AVERAGE = 3
    GOOD = 4
    GREAT = 5
    SUPERB = 6
    RATING = (
        (NOT_RATED, 'Not rated'),
        (AWFUL, 'Awful'),
        (BAD, 'Bad'),
        (AVERAGE, 'Average'),
        (GOOD, 'Good'),
        (GREAT, 'Great'),
        (SUPERB, 'Superb')
    )

    title = models.CharField(max_length=100, blank=False, null=False)
    url = models.URLField(blank=False)
    slug = models.SlugField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveSmallIntegerField(choices=RATING, default=NOT_RATED)

    def __str__(self):
        return '%s (%d/6)' % (self.title, self.rating)

    def get_absolute_url(self):
        return reverse('food:recipe', kwargs={'slug': self.slug})

    def to_json(self):
        return {
            'pk': self.pk,
            'title': self.title,
            'rating': self.rating,
        }

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Recipe, self).save()

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'
        ordering = ['title']


class DinnerPlanQuerySet(models.QuerySet):
    def current_plan(self):
        """
        Adds current_plan to objects.
        Find the most recent plan, but if it does not exist
        a NoneType will be returned
        :return: The newest DinnerPlan object or NoneType
        """
        today = datetime.today()
        start, end = utils.calculate_week_ends_for_date(today)
        try:
            plan = self.get(start_date=start)
            return plan
        except DinnerPlan.DoesNotExist as e:
            return None


class DinnerPlan(models.Model):
    start_date = models.DateField(verbose_name='Start Date', unique=True)
    end_date = models.DateField(blank=True)
    cost = models.FloatField(blank=True, default=.0)

    objects = DinnerPlanQuerySet.as_manager()

    @property
    def week(self):
        """
        Returns the week number for models instance
        :return: String representation of the week number
        """
        return str(utils.get_week_from_date(self.start_date))

    @property
    def year(self):
        return str(self.start_date.year)

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
        ordering = ['-end_date']


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

    plan = models.ForeignKey(
        DinnerPlan,
        related_name='items',
        related_query_name='item',
        on_delete=models.CASCADE
    )

    recipe = models.ForeignKey(
        Recipe,
        related_name='items',
        related_query_name='item',
        on_delete=models.CASCADE
    )

    day = models.IntegerField(choices=WEEKDAYS, blank=False, null=False)
    eaten = models.BooleanField(default=False)

    def __str__(self):
        return '%s, week %s: %s' % (self.WEEKDAYS[self.day][1],
                                    DinnerPlan.objects.get(item=self).week,
                                    Recipe.objects.get(item=self).title
                                    )

    class Meta:
        ordering = ['plan', 'day']
        unique_together = ('plan', 'day')  # This will crash if week is not a date, need year as well
        verbose_name = 'Dinner Plan Item'
        verbose_name_plural = 'Dinner Plan Items'
