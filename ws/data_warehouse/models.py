from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
    
    
class Regions(models.Model):
    """ 
        Model used to save regional specification. For each region
        URLs for downloading MaxTemp, MinTemp, MeanTemp, Sunshine
        Rainfall, RainDays and DaysOfAirFrost should be provided.
        These URLs are used as the bases for crawling raw data.
    """
    PRESENT_TYPES = (
        ('ORDERED', 'ORDERED'),
        ('RANKED', 'RANKED')
    )

    RESOURCE_TYPES = (
        ('MAX', 'Max temperature'),
        ('MIN', 'Min temperature'),
        ('MEN', 'Mean temperature'),
        ('SSN', 'Sunshine'),
        ('RNF', 'Rain fall'),
        ('RND', 'Rain days'),
        ('DAF', 'Days of air frost'),        
    )
    
    name = models.CharField(max_length=50,
                            blank=False,
                            validators=[])
    resource_url = models.URLField(blank=False)
    resource_type = models.CharField(max_length=3,
                                     choices=RESOURCE_TYPES,
                                     default='MAX')
    resource_present_type = models.CharField(max_length=10,
                                             choices=PRESENT_TYPES,
                                             default='ORDERED')

    
    def __str__(self):
        return self.name


class AnnualRecord(models.Model):
    """ Model used to save annual data """
    # Don't understand why such ForeignKey frequently give rise to exception
    # So will change to CharField and look at the issue later
    #region = models.ForeignKey("Regions", on_delete=models.CASCADE)
    region = models.CharField(max_length=50,
                              blank=False,
                              validators=[])
    year = models.IntegerField(null=False, blank=False)
    max_temp = models.FloatField(null=True)
    min_temp = models.FloatField(null=True)
    mean_temp = models.FloatField(null=True)
    sunshine = models.FloatField(null=True)
    rainfall = models.FloatField(null=True)
    raindays = models.FloatField(null=True)
    days_of_air_frist = models.FloatField(null=True) 
    month = models.CharField(max_length=3,
                             choices=(
                                 ('JAN', 'January'),
                                 ('FEB', 'February'),
                                 ('MAR', 'March'),
                                 ('APR', 'April'),
                                 ('MAY', 'May'),
                                 ('JUN', 'June'),
                                 ('JUL', 'July'),
                                 ('AUG', 'August'),
                                 ('SEP', 'September'),
                                 ('OCT', 'October'),
                                 ('NOV', 'November'),
                                 ('DEC', 'December'),
                                 ('ERR', 'Error'), ),
                             default='ERR')


class SeasonRecord(models.Model):
    """ Model used to save seasonal data """
    #region = models.ForeignKey("Regions", on_delete=models.CASCADE)
    region = models.CharField(max_length=50,
                              blank=False,
                              validators=[])
    year = models.IntegerField(null=False, blank=False)
    max_temp = models.FloatField(null=True)
    min_temp = models.FloatField(null=True)
    mean_temp = models.FloatField(null=True)
    sunshine = models.FloatField(null=True)
    rainfall = models.FloatField(null=True)
    raindays = models.FloatField(null=True)
    days_of_air_frist = models.FloatField(null=True) 
    season = models.CharField(max_length=6,
                              choices=(('WIN', 'Dec-Feb'),
                                       ('SPR', 'Mar-May'),
                                       ('SUM', 'Jun-Aug'),
                                       ('AUT', 'Sep-Nov'),
                                       ('ANN', 'Jan-Dec'),
                                       ('Err', 'Error')),
                              default='Err')
