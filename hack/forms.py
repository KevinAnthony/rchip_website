from django import forms
import datetime

class HackForm(forms.Form):
	word1 = forms.CharField()
	val1 = forms.IntegerField()
	word2 = forms.CharField(required=False)
	val2 = forms.IntegerField(required=False)
	word3 = forms.CharField(required=False)
	val3 = forms.IntegerField(required=False)
	word4 = forms.CharField(required=False)
 	val4 = forms.IntegerField(required=False)
	
	CurrentWord = forms.CharField()

