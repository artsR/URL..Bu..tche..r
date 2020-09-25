from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from django import forms

from .models import Url



class UrlForm(forms.Form):
    url = forms.URLField(
        initial='http://',
        widget=forms.URLInput(attrs={'placeholder': 'Shorten URL', 'class': ''})
    )
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Custom Slug', 'class': ''})
    )

    def __init__(self, *args, user=None, **kwargs):
        super(UrlForm, self).__init__(*args, **kwargs)
        if (user is not None) and (not user.is_authenticated):
            self.fields['captcha'] = ReCaptchaField(widget=ReCaptchaV2Checkbox)


    def clean_slug(self):
        """Checks if provided by user `slug` can be saved into database:
        1. there is no record with `slug` ID
        2. there is record with `slug` ID but it is expired.
        """
        new_slug = self.cleaned_data['slug']

        if not new_slug:
            return new_slug

        slug = Url.objects.filter(slug=new_slug).first()
        if slug is None or slug.expired():
            return new_slug
        else:
            raise forms.ValidationError('Slug already exists', code='already_used')
