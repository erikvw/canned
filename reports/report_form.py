from django import forms
from edc_form_validators import FormValidatorMixin
from edc_sites.forms import SiteModelFormMixin
from reports.models import Reports


class ReportsForm(SiteModelFormMixin, FormValidatorMixin, forms.ModelForm):

    form_validator_cls = None

    class Meta:
        model = Reports
        fields = "__all__"
