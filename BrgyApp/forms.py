from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import CertTribal, Brgy, Purok, Resident, Household, Deceased, Ofw, Blotter, Business, BrgyClearance, BusinessClearance, CertSoloParent, CertGoodMoral, CertIndigency, CertNonOperation, CertResidency, Brgy_Officials, JobSeekers
from django.core.exceptions import ValidationError

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',  # Add your CSS classes here
                'placeholder': 'Enter ' + field.replace('_', ' ').capitalize(),
            })

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ('username', 'first_name', 'last_name')
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Last Name'})
    )

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2')
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'})
    )
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your First Name'})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Last Name'})
    )
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'})
    )
    password2 = forms.CharField(
        label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat your Password'})
    )

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Password'})
    )

class BrgyForm(forms.ModelForm):
    class Meta:
        model = Brgy
        fields = ('brgy_name', 'municipality', 'description', 'image')
        widgets = {
            'brgy_name': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'municipality': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
            'class': 'form-control'
            }),
        }
    image = forms.ImageField(
        label="Photo",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
    )

class PurokForm(forms.ModelForm):
    class Meta:
        model = Purok
        fields = ('brgy', 'purok_name',)
        widgets = {
            'brgy': forms.Select(attrs={
            'class': 'form-select'
            }),
            'purok_name': forms.TextInput(attrs={
            'class': 'form-control'
            }),
        }

class ResidentForm(forms.ModelForm): 
    CIVIL_STATUS_CHOICES = (
        ('-----', '-----'),
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
        )
    Educaional_attainment_choices = (
        ('-----', '-----'),
        ("Elementary", "Elementary"),
        ("Secondary", "Secondary"),
        ("College / University Degree", "College / University Degree"),
        ("Vocational", "Vocational"),
        ("Masters degree", "Masters Degree"),
        ("Doctorate degree", "Doctorate Degree"),
        ("none","None")
    )
    Gender_choices = (
        ("Male", "Male"),
        ("Female", "Female"),
    )
    class Meta:
        
        model = Resident   
        fields = ('f_name', 'm_name', 'l_name',
                  'gender','house_no',
                  'phone_number', 'birth_date', 'birth_place',
                  'civil_status', 'religion', 'citizenship',
                  'profession', 'education', 'voter', 'solo_parent','pwd','indigent', 'image',
                  )
    
        widgets = {
                'house_no': forms.Select(attrs={
                'class': 'form-select'
                }),
            }

    f_name = forms.CharField(
        label="First Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'})
    )
    m_name = forms.CharField(
        label="Middle Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Middle Name'})
    )
    l_name = forms.CharField(
        label="Last Name",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'})
    )
    gender = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices=Gender_choices,
    )
    phone_number = forms.CharField(
        label="Contact Number",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'})
    )
    birth_date = forms.DateField(
        label="Date of Birth",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    birth_place = forms.CharField(
        label="Place of Birth",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Birth Place'})
    )
    civil_status = forms.ChoiceField(
        label="Civil Status",
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices=CIVIL_STATUS_CHOICES,
    )
    religion = forms.CharField(
        label="Religion",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Religion'})
    )
    citizenship = forms.CharField(
        label="Citizenship",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Citizenship'})
    )
    profession = forms.CharField(
        label="Profession",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Profession'})
    )
    education = forms.ChoiceField(
        label="Education",
        widget=forms.Select(attrs={'class': 'form-select', 'placeholder': 'Enter Education'}),
        choices=Educaional_attainment_choices,
    )
    voter = forms.BooleanField(
        label="Registered Voter",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    solo_parent = forms.BooleanField(
        label="Solo Parent",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    pwd = forms.BooleanField(
        label="Person with Disability",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    indigent = forms.BooleanField(
        label="Indigent",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    image = forms.ImageField(
        label="Photo",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set default image if the instance doesn't have an image
        if not self.instance.image:
            self.fields['image'].initial = 'item_images/default.jpg'

class HouseholdForm(forms.ModelForm):
    class Meta:
        model = Household
        fields = ('house_no', 'address', 'purok',)
    
        widgets = {
            'house_no': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'purok': forms.Select(attrs={
            'class': 'form-select'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        house_no = cleaned_data.get('house_no')

        # Check for duplicate house no
        if Household.objects.filter(house_no=house_no).exists():
            raise ValidationError('House no. already exists!')

        return cleaned_data

class DeceasedForm(forms.ModelForm):
    class Meta:
        model = Deceased
        fields = ('resident', 'date_of_death', 'cause_of_death',)
        widgets = {
            'resident': forms.Select(attrs={
            'class': 'form-select'
            }),
            'date_of_death': forms.DateInput(attrs={
            'class': 'form-control', 
            'type': 'date'
            }),
            'cause_of_death': forms.TextInput(attrs={
            'class': 'form-control'
            }),
        }

class OfwForm(forms.ModelForm):
    class Meta:
        model = Ofw
        fields = ('resident', 'passport_no', 'country',)
        widgets = {
            'resident': forms.Select(attrs={
            'class': 'form-select'
            }),
            'passport_no': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'country': forms.TextInput(attrs={
            'class': 'form-control'
            }),
        }

class brgyOfficialForm(forms.ModelForm):
    class Meta:
        model = Brgy_Officials
        fields = ('brgy_Captain', 'kagawad1', 'kagawad2', 'kagawad3', 'kagawad4', 'kagawad5', 'kagawad6', 'kagawad7', 'sk', 'secretary', 'treasurer')

        widgets = {
            'brgy_Captain': forms.Select(attrs={
            'class': 'form-select'
            }),
            'kagawad1': forms.Select(attrs={
            'class': 'form-select'
            }),
            'kagawad2': forms.Select(attrs={
            'class': 'form-select'
            }),
            'kagawad3': forms.Select(attrs={
            'class': 'form-select'
            }),
            'kagawad4': forms.Select(attrs={
            'class': 'form-select'
            }),
            'kagawad5': forms.Select(attrs={
            'class': 'form-select'
            }),
            'kagawad6': forms.Select(attrs={
            'class': 'form-select'
            }),
            'kagawad7': forms.Select(attrs={
            'class': 'form-select'           
            }),
            'sk': forms.Select(attrs={
            'class': 'form-select'
            }),
            'secretary': forms.Select(attrs={
            'class': 'form-select'
            }),
            'treasurer': forms.Select(attrs={
            'class': 'form-select'           
            }),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     complainants = self.cleaned_data.get('complainants')
    #     respondents = self.cleaned_data.get('respondents')
        
    #     if complainants == respondents:
    #         raise ValidationError("Complainant and respondent cannot be the same!")
        
    #     return cleaned_data

class BlotterForm(forms.ModelForm):
    status_choices = (
        ('-----', '-----'),
        ('Pending', 'Pending'),
        ('Solved', 'Solved'),
        )
    class Meta:
        model = Blotter
        fields = ('complainants', 'respondents', 'statement', 'location', 'status',)

        widgets = {
            'complainants': forms.Select(attrs={
            'class': 'form-select'
            }),
            'respondents': forms.Select(attrs={
            'class': 'form-select'
            }),
            'statement': forms.Textarea(attrs={
            'class': 'form-control'
            }),
            'location': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'status': forms.Select(attrs={
            'class': 'form-select'
            }),
        }
    status = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=status_choices,
    )

    def clean(self):
        cleaned_data = super().clean()
        complainants = self.cleaned_data.get('complainants')
        respondents = self.cleaned_data.get('respondents')
        
        if complainants == respondents:
            raise ValidationError("Complainant and respondent cannot be the same!")
        
        return cleaned_data

class BusinessForm(forms.ModelForm):
    status_choices = (
        ('-----', '-----'),
        ('ACTIVE', 'ACTIVE'),
        ('INACTIVE', 'INACTIVE'),
        )
    class Meta:
        model = Business
        fields = ('business_name', 'business_type', 'purok', 'proprietor', 'address', 'citizenship','status',)
        widgets = {
            'business_name': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'business_type': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'purok': forms.Select(attrs={
            'class': 'form-select'
            }),
            'proprietor': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'citizenship': forms.TextInput(attrs={
            'class': 'form-control'
            }),
        }
    status = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=status_choices,
    )

class JobSeekersForm(forms.ModelForm):
    class Meta:
        model = JobSeekers
        fields = ('resident',)
        widgets = {
            'resident': forms.Select(attrs={
            'class': 'form-select'
            }),
        }

class BrgyClearanceForm(forms.ModelForm):
    class Meta:
        model = BrgyClearance
        fields = ('resident', 'purpose', 'or_no', 'or_amount', 'or_date', 'ctc', 'ctc_amount', 'ctc_date',)
        widgets = {
            'resident': forms.Select(attrs={
            'class': 'form-select'
            }),
            'purpose': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_no': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'or_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
            'ctc': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'ctc_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'ctc_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        respondent = cleaned_data.get('resident')

        # Check for duplicate house no
        if Blotter.objects.filter(respondents=respondent).exists():
            raise ValidationError('This person has a pending blotter report!')

        return cleaned_data

class BusinessClearanceForm(forms.ModelForm):
    type_choices = (
        ('-----', '-----'),
        ('MANAGEMENT BUSINESS', 'MANAGEMENT BUSINESS'),
        ('CORPORATE BUSINESS', 'CORPORATE BUSINESS'),
        )
    class Meta:
        model = BusinessClearance
        fields = ('business', 'clearance_type', 'or_no', 'or_amount', 'or_date', 'ctc', 'ctc_amount', 'ctc_date',)
        widgets = {
            'business': forms.Select(attrs={
            'class': 'form-select'
            }),
            'or_no': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'or_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
            'ctc': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'ctc_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'ctc_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
        }
    clearance_type = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices=type_choices,
    )

class CertResidencyForm(forms.ModelForm):
    class Meta:
        model = CertResidency
        fields = ('resident', 'purpose', 'or_no', 'or_amount', 'or_date', 'ctc', 'ctc_amount', 'ctc_date',)
        widgets = {
            'resident': forms.Select(attrs={
            'class': 'form-select'
            }),
            'purpose': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_no': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'or_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
            'ctc': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'ctc_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'ctc_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
        }

class CertIndigencyForm(forms.ModelForm):
    class Meta:
        model = CertIndigency
        fields = ('resident', 'purpose', 'or_no', 'or_amount', 'or_date', 'ctc', 'ctc_amount', 'ctc_date',)
        widgets = {
            'resident': forms.Select(attrs={
            'class': 'form-select'
            }),
            'purpose': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_no': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'or_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
            'ctc': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'ctc_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'ctc_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
        }

class CertSoloParentForm(forms.ModelForm):
    class Meta:
        model = CertSoloParent
        fields = ('resident', 'purpose', 'or_no', 'or_amount', 'or_date', 'ctc', 'ctc_amount', 'ctc_date',)
        widgets = {
            'resident': forms.Select(attrs={
            'class': 'form-select'
            }),
            'purpose': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_no': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'or_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
            'ctc': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'ctc_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'ctc_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
        }

class CertGoodMoralForm(forms.ModelForm):
    class Meta:
        model = CertGoodMoral
        fields = ('resident', 'purpose', 'or_no', 'or_amount', 'or_date', 'ctc', 'ctc_amount', 'ctc_date',)
        widgets = {
            'resident': forms.Select(attrs={
            'class': 'form-select'
            }),
            'purpose': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_no': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'or_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
            'ctc': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'ctc_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'ctc_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        respondent = cleaned_data.get('resident')

        # Check for duplicate house no
        if Blotter.objects.filter(respondents=respondent).exists():
            raise ValidationError('This person has a pending blotter report!')

        return cleaned_data

class CertTribalForm(forms.ModelForm):
    class Meta:
        model = CertTribal
        fields = ('resident', 'mother', 'tribe', 'purpose', 'or_no', 'or_amount', 'or_date', 'ctc', 'ctc_amount', 'ctc_date',)
        widgets = {
            'resident': forms.Select(attrs={
            'class': 'form-select'
            }),
            'mother': forms.Select(attrs={
            'class': 'form-select'
            }),
            'tribe': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'purpose': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_no': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'or_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
            'ctc': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'ctc_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'ctc_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        resident = self.cleaned_data.get('resident')
        mother = self.cleaned_data.get('mother')
        
        if resident == mother:
            raise ValidationError("Resident and Mother cannot be the same!")
        
        return cleaned_data

class CertNonOperationForm(forms.ModelForm):
    class Meta:
        model = CertNonOperation
        fields = ('business', 'ceased_date', 'purpose', 'or_no', 'or_amount', 'or_date', 'ctc', 'ctc_amount', 'ctc_date',)
        widgets = {
            'business': forms.Select(attrs={
            'class': 'form-select'
            }),
            'ceased_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
            'purpose': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_no': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'or_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'or_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
            'ctc': forms.TextInput(attrs={
            'class': 'form-control'
            }),
            'ctc_amount': forms.NumberInput(attrs={
            'class': 'form-control'
            }),
            'ctc_date': forms.DateInput(attrs={
            'class': 'form-control', 'type': 'date',
            }),
        }