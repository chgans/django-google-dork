import re, random, urllib
from itertools import chain

from django.db import models
from django.core.exceptions import ValidationError
from model_utils.models import TimeStampedModel

class SearchEngineManager(models.Manager):
    """
    Custom manager for SearchEngine
    """
    def random(self):
        """
        return a google search engine randomly selected among the enablked ones
        """
        return random.choice(self.filter(enabled=True))

class SearchEngine(models.Model):
    """
    Model to capture google search engines
    """
    hostname = models.CharField(max_length=32, unique=True)
    
    objects = SearchEngineManager()

class CampaignNameField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length']=32
        super(CampaignNameField, self).__init__(*args, **kwargs)
        self._re = re.compile(r"^\w{4,32}$")

    def clean(self, value, model_instance):
        _value = super(models.CharField, self).clean(value, model_instance).strip()
        matched = self._re.match(_value)
        if not matched:
            raise ValidationError("CampaignNameField must be a word made of 4 to 32 characters: '%s'" % value)
        setattr(model_instance, self.name, _value)
        return _value
    

class Campaign(TimeStampedModel):
    """
    A Campaign is a named dork container that allows you to group your dorks a logical way.
    
    Campaign have a unique ``name`` and can be enabled/disabled using the proerty ``enabled``
    """
    name = CampaignNameField(unique=True)
    enabled = models.BooleanField(default=True)

    # TODO: generic foreign key

    @property
    def run_set(self):
        """
        Return a query_set for all the dork runs of this campaign 
        """
        qs = Run.objects.none()
        for dork in self.dork_set.all():
            qs |= dork.run_set
        return qs

    @property
    def result_set(self):
        """
        Return a query_set for all the results of all the dork runs of this campaign 
        """
        qs = Result.objects.none()
        for run in self.run_set.all():
            qs |= run.result_set.filter()
        return qs

# TODO: move somewhere else, create a testsuite and remove redundant tests from ./tests.py
class DorkQueryField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length']=256
        super(DorkQueryField, self).__init__(*args, **kwargs)
        self._re = re.compile(r"^.{1,256}$")

    def clean(self, value, model_instance):
        _value = super(models.CharField, self).clean(value, model_instance).strip()
        matched = self._re.match(_value)
        if not matched:
            raise ValidationError("DorkQueryField must be a word made of 1 to 256 characters: '%s'" % value)
        setattr(model_instance, self.name, _value)
        return _value

class Dork(TimeStampedModel):
    """
    The ``query`` property is actually the dork itself, this is what you
    would type in the google search box.  Dorks can be enabled/disabled by
    setting the ``enabled`` property.
    
    Notes: ``query`` and ``campaign`` are unique together, that is a
    identical queries cannot be associated with the same campaign.
    """
    campaign = models.ForeignKey('Campaign')
    query = DorkQueryField()
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ("campaign", "query")

    @property
    def result_set(self):
        """
        This property holds a QuerySet for all the results found during all runs
        """
        qs = Dork.objects.none()
        for run in self.run_set.all():
            qs |= run.result_set
        return qs


class Run(models.Model):
    """
    A Run is an execution of a Dork using a SearchEngine, it holds the
    results return by a google search engine.
    """
    dork = models.ForeignKey('Dork')
    engine = models.ForeignKey('SearchEngine')
    result_set = models.ManyToManyField('Result')
    created = models.DateTimeField(auto_now_add=True)

    def get_url(self, num, start):
        p = {
            'q': urllib.parse.quote(self.dork.query),
            'num': str(num),
            'start': str(start),
            # Required parameter. If this parameter does not have a valid
            # value, other parameters in the query string do not work as
            # expected. Set to 'firefox-a' in mozilla firefox.
            # A string that indicates a valid front end and the policies
            # defined for it, including KeyMatches, related queries,
            # filters, remove URLs, and OneBox Modules.
            # Notice that the rendering of the front end is determined by
            # the proxystylesheet parameter. Example: client=myfrontend
            'client': 'firefox-a',
            # Include omitted results if set to 0
            'filter': 0,
            # Turns the adult content filter on or off
            'safe': 'off',
            # Sets the character encoding that is used to interpret the query string.
            'ie': 'UTF-8',
            # Sets the character encoding that is used to encode the results.
            'oe': 'UTF-8',
            # Specifies whether to search public content (p), secure content (s), or both (a).
            'access': 'a',
            }
        params = "&".join(["%s=%s" % (k, v) for k, v in p.items() if v is not None])
        return "https://%s/search?%s" % (self.engine.hostname, params)

class Result(models.Model):
    title = models.CharField(max_length=1024)
    summary = models.TextField()
    url = models.URLField(max_length=1024)

    class Meta:
        unique_together = ("title", "summary", "url")
