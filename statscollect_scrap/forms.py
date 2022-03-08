from django import forms
from statscollect_scrap import models


class ProcessedGameForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProcessedGameForm, self).__init__(*args, **kwargs)
        self.fields["gamesheet_ds"].queryset = models.ScrapedDataSheet.objects.filter(
            source__in=["WHOSC", "LFP"]
        ).order_by("-match_date")
