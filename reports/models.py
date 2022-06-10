from django.db import models
from edc_model.models import BaseUuidModel, HistoricalRecords
from edc_sites.models import CurrentSiteManager, SiteModelMixin
from edc_utils import get_utcnow


class Reports(SiteModelMixin, BaseUuidModel):

    report_datetime = models.DateTimeField(default=get_utcnow)

    report_name = models.CharField(max_length=30)

    report_description = models.TextField(null=True)

    sql_view_name = models.CharField(max_length=50, null=True)

    objects = models.Manager()

    history = HistoricalRecords()

    sites = CurrentSiteManager()

    def __str__(self):
        return self.report_name

    class Meta(BaseUuidModel.Meta):
        verbose_name = "Reports"
        verbose_name_plural = "Reports"
