from django import forms


class KeywordForm(forms.Form):
    name = forms.CharField(max_length=200, label='name')
   

class KeywordSearchForm(forms.Form):
    name = forms.CharField(max_length=200, label='name')
    country = forms.CharField(max_length=200, label='country')


class KeywordGenerationForm(forms.Form):
    topic = forms.CharField(max_length=200, label='topic')
    intent = forms.CharField(max_length=200, label='intent')
    additional_instructions = forms.CharField(max_length=500, label='additional_instructions', required=False)

class AddKeywordToClusterForm(forms.Form):
    keyword_name = forms.CharField(max_length=200, label='keyword_name')
    cluster_id = forms.IntegerField(label='cluster_id')


class KeywordClusterForm(forms.Form):
    keyword_cluster_name = forms.CharField(max_length=200, label='keyword_cluster_name')