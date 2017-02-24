# _*_ coding:utf-8 _*_

from django import forms
from models import UsageStatus, AssetCategory


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=20, min_length=4)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    remember_me = forms.CharField(widget=forms.CheckboxInput, required=False)


class AssetAddForm(forms.Form):
    usagestatus_select = [('',''),]
    assetcategory_select = [('',''),]
    categery_list = AssetCategory.objects.filter(id__gt=1).values()
    statu_list = UsageStatus.objects.filter(id__gt=1).values()
    for i in statu_list:
        d = i['StatusName']
        usagestatus_select.append((d,d))
    for i in categery_list:
        d = i['CategoryName']
        assetcategory_select.append((d, d))
    department = forms.CharField(widget=forms.TextInput(attrs={'class': 'one'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'one'}), required=False)
    assetbrand = forms.CharField(widget=forms.TextInput(attrs={'class': 'one'}))
    assettype = forms.CharField(widget=forms.TextInput(attrs={'class': 'one'}))
    serialnumber = forms.CharField(widget=forms.TextInput(attrs={'class': 'one'}))
    # serianumber = forms.ImageField(required=False)
    buytime = forms.DateField(widget=forms.DateInput(attrs={'class': 'one'}), input_formats=['%Y-%m-%d',], help_text="2017-01-01")
    buychannel = forms.CharField(widget=forms.TextInput(attrs={'class': 'one'}))
    buyprice = forms.CharField(widget=forms.TextInput(attrs={'class': 'one'}))
    buyer = forms.CharField(widget=forms.TextInput(attrs={'class': 'one'}))
    assetcategory = forms.ChoiceField(choices=assetcategory_select,
                                      widget=forms.Select(attrs={'class':'dropdown-toggle drop-down-custom', 'style': 'height:30px;width:100%;text-align:center'}))
    usagestatus = forms.ChoiceField(choices=usagestatus_select,
                                    widget=forms.Select(attrs={'class': 'dropdown-toggle', 'style': 'height:30px;width:100%;text-align:center'}))
    # place = forms.CharField(widget=forms.TextInput(attrs={'class': 'multiline'}))
    place = forms.CharField(widget=forms.TextInput(attrs={'class': 'one'}))
    remark = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'multiline'}))


class UploadFile(forms.Form):
    upload_file = forms.FileField()
