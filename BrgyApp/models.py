from django.db import models
from django.core.exceptions import ValidationError

class Brgy(models.Model):
    brgy_name = models.CharField(max_length=150)
    municipality = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    
    def __str__(self):
        return self.brgy_name
    
class Purok(models.Model):
    brgy = models.ForeignKey(Brgy, on_delete=models.CASCADE)
    purok_name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.purok_name

class Household(models.Model):
    house_no = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    purok = models.ForeignKey(Purok, on_delete=models.CASCADE)

    def __str__(self):
        return self.house_no

class Resident(models.Model):  
    f_name = models.CharField(max_length=100)
    l_name = models.CharField(max_length=100)
    m_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=15)
    house_no = models.ForeignKey(Household, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    birth_date = models.DateField()
    birth_place = models.CharField(max_length=100)
    civil_status = models.CharField(max_length=50)
    religion = models.CharField(max_length=50)
    citizenship = models.CharField(max_length=50)
    profession = models.CharField(max_length=100)
    education = models.CharField(max_length=100)
    voter = models.BooleanField(default=False)
    solo_parent = models.BooleanField(default=False)
    pwd = models.BooleanField(default=False)
    indigent = models.BooleanField(default=False)
    image = models.ImageField(upload_to='item_images', blank=True, null=True)

    def __str__(self):
        full_name = f"{self.f_name} {self.m_name[0]}. {self.l_name}"
        return full_name
    
class JobSeekers(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.resident
    
class Brgy_Officials(models.Model):
    brgy_Captain = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='brgy_Captain')
    kagawad1 = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='kagawad1')
    kagawad2 = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='kagawad2')
    kagawad3 = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='kagawad3')
    kagawad4 = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='kagawad4')
    kagawad5 = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='kagawad5')
    kagawad6 = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='kagawad6')
    kagawad7 = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='kagawad7')
    sk = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='sk')
    secretary = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='secretary')
    treasurer = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='treasurer')
    def __str__(self):
        return self.purok_name
    
class Business(models.Model):
    business_name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100)
    purok = models.ForeignKey(Purok, on_delete=models.CASCADE)
    proprietor = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    citizenship = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.business_name
    
class BrgyClearance(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=100)
    clearance_type = models.CharField(max_length=100)
    or_no = models.CharField(max_length=50)
    or_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    or_date = models.DateField()
    ctc = models.CharField(max_length=50)
    ctc_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    ctc_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.purpose
    
class CertResidency(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=100)
    clearance_type = models.CharField(max_length=100)
    or_no = models.CharField(max_length=50)
    or_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    or_date = models.DateField()
    ctc = models.CharField(max_length=50)
    ctc_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    ctc_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.purpose
    
class CertIndigency(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=100)
    clearance_type = models.CharField(max_length=100)
    or_no = models.CharField(max_length=50)
    or_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    or_date = models.DateField()
    ctc = models.CharField(max_length=50)
    ctc_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    ctc_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.purpose
    
class CertSoloParent(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=100)
    clearance_type = models.CharField(max_length=100)
    or_no = models.CharField(max_length=50)
    or_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    or_date = models.DateField()
    ctc = models.CharField(max_length=50)
    ctc_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    ctc_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.purpose
    
class CertGoodMoral(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=100)
    clearance_type = models.CharField(max_length=100)
    or_no = models.CharField(max_length=50)
    or_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    or_date = models.DateField()
    ctc = models.CharField(max_length=50)
    ctc_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    ctc_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.purpose
    
class CertTribal(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='resident')
    mother = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='mother')
    tribe = models.CharField(max_length=100)
    purpose = models.CharField(max_length=100)
    clearance_type = models.CharField(max_length=100)
    or_no = models.CharField(max_length=50)
    or_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    or_date = models.DateField()
    ctc = models.CharField(max_length=50)
    ctc_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    ctc_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.purpose
    
class CertNonOperation(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    ceased_date = models.DateField()
    purpose = models.CharField(max_length=100)
    clearance_type = models.CharField(max_length=100)
    or_no = models.CharField(max_length=50)
    or_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    or_date = models.DateField()
    ctc = models.CharField(max_length=50)
    ctc_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    ctc_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.purpose
    
class BusinessClearance(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    clearance_type = models.CharField(max_length=100)
    or_no = models.CharField(max_length=50)
    or_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    or_date = models.DateField()
    ctc = models.CharField(max_length=50)
    ctc_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    ctc_date = models.DateField()
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.purpose
    
class Deceased(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    date_of_death = models.DateField()
    cause_of_death = models.CharField(max_length=100)
    
    def __str__(self):
        return self.date_of_death
    
class Ofw(models.Model):
    resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
    passport_no = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    
    def __str__(self):
        return self.passport_no
    
class Blotter(models.Model):
    complainants = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='complaints')
    respondents = models.ForeignKey(Resident, on_delete=models.CASCADE, related_name='responses')
    statement = models.TextField()
    location = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"Blotter {self.id}"

    # def save(self, *args, **kwargs):
    #     # Additional custom logic before saving, e.g., validation
    #     self.validate_complainants_and_respondents()
    #     super().save(*args, **kwargs)

    # def validate_complainants_and_respondents(self):
    #     if self.complainants == self.respondents:
    #         raise ValidationError("Complainant and respondent cannot be the same.")



