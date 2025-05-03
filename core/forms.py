from django import forms
from .choices import SURAH_CHOICES
from unfold.widgets import UnfoldAdminCheckboxSelectMultiple
from .models import MemorizationRecord
from django.utils.translation import gettext_lazy as _


class MemorizationRecordForm(forms.ModelForm):
    surah = forms.MultipleChoiceField(
        choices=SURAH_CHOICES,
        # widget=UnfoldAdminCheckboxSelectMultiple(),
        required=False,
        label=_("Surah"),
        widget=UnfoldAdminCheckboxSelectMultiple,
    )

    class Meta:
        model = MemorizationRecord
        fields = "__all__"
