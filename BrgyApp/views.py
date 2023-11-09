from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .models import CertTribal, Brgy, Purok, Resident, Brgy_Officials, Household, Deceased, Ofw, Blotter, Business, BrgyClearance, BusinessClearance, CertResidency, CertGoodMoral, CertIndigency, CertNonOperation, CertSoloParent, JobSeekers
from .forms import CustomUserChangeForm, SignupForm, CertTribalForm, BrgyForm, PurokForm, ResidentForm, brgyOfficialForm, DeceasedForm, OfwForm, BlotterForm, BusinessForm, BrgyClearanceForm, BusinessClearanceForm, CertGoodMoralForm, CertIndigencyForm, CertNonOperationForm, CertResidencyForm, CertSoloParentForm, HouseholdForm, JobSeekersForm
from django.http import JsonResponse, Http404, HttpResponse
from .excel_import import import_residents_from_excel
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from .utils import render_to_pdf
from django.views.generic import View
from datetime import datetime, date, timedelta
from reportlab.lib import colors
import os
from django.db.models import Sum, Count, Q, ExpressionWrapper, F, IntegerField, Value, When, Case
from dateutil.relativedelta import relativedelta
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
# Create your views here.
#@login_required
month_names = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}
def logout_view(request):
    logout(request)
    return redirect('login')

def Signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
    

def Users(request):
    users=User.objects.all()
    return render (request,'Users.html',{'users' : users })

def AdEdUsers(request, pk):
    try:
        user = get_object_or_404(User, pk=pk)
        if request.method == 'POST':
            form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect('Users')
        else:
            form = CustomUserChangeForm(instance=user)
        return render(request, 'AdEdUsers.html', {'form': form})
    except Http404:  
        if request.method == 'POST':
            form = SignupForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('Users')
        else:
            form = SignupForm()
        return render(request, 'AdEdUsers.html', {'form': form})

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session with the new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password_change_done')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })

@login_required
def index(request):     
    months = ["January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
    ]
    today = datetime.now()
    day_Before = today-timedelta(days=1)
    thisMonth = datetime.now().month
    month_Before = datetime.now().date().replace(day=1) - timedelta(days=1)
    thisYear = datetime.now().year 

    resident = Resident.objects.all()
    household = Household.objects.all().count()
    # household = Resident.objects.exclude(house_no__isnull=True).values('house_no').annotate(total_count=Count('id')).count()
    business = Business.objects.all()
    brgyclearance = BrgyClearance.objects.all()
    businessclearance = BusinessClearance.objects.all()
    residency = CertResidency.objects.all()
    indigency = CertIndigency.objects.all()
    soloparent = CertSoloParent.objects.all()
    goodmoral = CertGoodMoral.objects.all()
    nonoperation = CertNonOperation.objects.all()
    tribal = CertTribal.objects.all()
    jobseekers = JobSeekers.objects.all()

    # date_filter = request.GET.get('elementValue')  # Assuming you're using GET requests
    # final_date = 'Today'
    # if date_filter == 'Today':
    #     final_date = today
    # elif date_filter == 'This Month':
    #     final_date = thisMonth
    # elif date_filter == 'This Year':
    #     final_date = thisYear

    blotter = Blotter.objects.filter(status='Pending').order_by("date_created")
    brgyClearance_total = brgyclearance.filter(date_created__year=thisYear).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    businessClearance_total = businessclearance.filter(date_created__year=thisYear).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    residency_total = residency.filter(date_created__year=thisYear).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    indigency_total = indigency.filter(date_created__year=thisYear).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    soloparent_total = soloparent.filter(date_created__year=thisYear).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    goodmoral_total = goodmoral.filter(date_created__year=thisYear).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    nonoperation_total = nonoperation.filter(date_created__year=thisYear).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    tribal_total = tribal.filter(date_created__year=thisYear).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    jobseekers_total = jobseekers.filter(date_created__year=thisYear).aggregate(total_count=Count('id'))
    


    # brgyClearance_monthly = brgyclearance.filter(or_date__year=thisYear).annotate(date_month=TruncMonth('or_date')).values('date_month').annotate(total_amount=Sum('or_amount'), total_count=Count('id')).distinct()
    # businessClearance_monthly = businessclearance.filter(or_date__year=thisYear).annotate(date_month=TruncMonth('or_date')).values('date_month').annotate(total_amount=Sum('or_amount')).distinct()
    
    series1 = []
    series2 = []
    series3 = []
    series4 = []
    series5 = []
    series6 = []
    series7 = []
    series8 = []

    for m in range(1, 13):
        values1 = brgyclearance.filter(or_date__month=m).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
        series1.append(values1['total_amount'] or 0)
        values2 = businessclearance.filter(or_date__month=m).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
        series2.append(values2['total_amount'] or 0)
        values3 = residency.filter(or_date__month=m).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
        series3.append(values3['total_amount'] or 0)
        values4 = indigency.filter(or_date__month=m).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
        series4.append(values4['total_amount'] or 0)
        values5 = soloparent.filter(or_date__month=m).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
        series5.append(values5['total_amount'] or 0)
        values6 = goodmoral.filter(or_date__month=m).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
        series6.append(values6['total_amount'] or 0)
        values7 = nonoperation.filter(or_date__month=m).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
        series7.append(values7['total_amount'] or 0)
        values8 = tribal.filter(or_date__month=m).aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))      
        series8.append(values8['total_amount'] or 0)

        

    # resident_graph_data = resident.values('purok__purok_name').annotate(total_count=Count('purok')).distinct()
    resident_graph_data = Resident.objects.values('house_no__purok__purok_name').annotate(total_count=Count('id'))
    resident_count = resident.count()
    business_active_count = business.filter(status='ACTIVE').count()
    business_inactive_count = business.filter(status='INACTIVE').count()

    context = {
        'resident': resident,'household': household,'resident_count': resident_count,
        'blotter': blotter,'business_active_count': business_active_count,
        'business_inactive_count': business_inactive_count,'brgyClearance_total': brgyClearance_total,
        'businessClearance_total': businessClearance_total,'residency_total': residency_total,
        'indigency_total': indigency_total,'soloparent_total': soloparent_total,
        'goodmoral_total': goodmoral_total,'nonoperation_total': nonoperation_total,
        'tribal_total': tribal_total,'jobseekers_total': jobseekers_total,'months': months,
        'thisYear': thisYear,'series1': series1,
        'series2': series2,'series3': series3,'series4': series4,
        'series5': series5,'series6': series6,
        'series7': series7,'series8': series8,
        'resident_graph_data': resident_graph_data,
    }
    return render(request, 'index.html', context)

def calculate_age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

def get_filtered_clearance_data(request):
    today = datetime.now()
    thisMonth = datetime.now().month
    thisYear = datetime.now().year 
    date_filter = request.GET.get('elementValue')  # Assuming you're using GET requests
    
    # if date_filter == 'Today':
    #     print(date_filter)
    #     brgyclearance = BrgyClearance.objects.all().filter(date_created=today)
    #     businessclearance = BusinessClearance.objects.all().filter(date_created=today)
    #     residency = CertResidency.objects.all().filter(date_created=today)
    #     indigency = CertIndigency.objects.all().filter(date_created=today)
    #     soloparent = CertSoloParent.objects.all().filter(date_created=today)
    #     goodmoral = CertGoodMoral.filter(date_created=today)
    #     nonoperation = CertNonOperation.objects.all().filter(date_created=today)
    #     tribal = CertTribal.objects.all().filter(date_created=today)
    # elif date_filter == 'This Month':
    #     print(date_filter)
    #     brgyclearance = BrgyClearance.objects.all().filter(date_created=thisMonth)
    #     businessclearance = BusinessClearance.objects.all().filter(date_created=thisMonth)
    #     residency = CertResidency.objects.all().filter(date_created=thisMonth)
    #     indigency = CertIndigency.objects.all().filter(date_created=thisMonth)
    #     soloparent = CertSoloParent.objects.all().filter(date_created=thisMonth)
    #     goodmoral = CertGoodMoral.filter(date_created=thisMonth)
    #     nonoperation = CertNonOperation.objects.all().filter(date_created=thisMonth)
    #     tribal = CertTribal.objects.all().filter(date_created=thisMonth)
    # elif date_filter == 'This Year':
    print(date_filter)
    brgyclearance = BrgyClearance.objects.all().filter(date_created=thisYear)
    businessclearance = BusinessClearance.objects.all().filter(date_created=thisYear)
    residency = CertResidency.objects.all().filter(date_created=thisYear)
    indigency = CertIndigency.objects.all().filter(date_created=thisYear)
    soloparent = CertSoloParent.objects.all().filter(date_created=thisYear)
    goodmoral = CertGoodMoral.filter(date_created=thisYear)
    nonoperation = CertNonOperation.objects.all().filter(date_created=thisYear)
    tribal = CertTribal.objects.all().filter(date_created=thisYear)
    # else:
    #     pass
        # Handle other cases or default to a specific date filter
    
    brgyClearance_total = brgyclearance.aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    businessClearance_total = businessclearance.aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    residency_total = residency.aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    indigency_total = indigency.aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    soloparent_total = soloparent.aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    goodmoral_total = goodmoral.aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    nonoperation_total = nonoperation.aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    tribal_total = tribal.aggregate(total_amount=Sum('or_amount'), total_count=Count('id'))
    response_data = {
        'brgyClearance_total': brgyClearance_total,
        'businessClearance_total': businessClearance_total,
        'residency_total': residency_total,
        'indigency_total': indigency_total,
        'soloparent_total': soloparent_total,
        'goodmoral_total': goodmoral_total,
        'nonoperation_total': nonoperation_total,
        'tribal_total': tribal_total
    }

    return JsonResponse(response_data)

@login_required
class GeneratePDF(View):
    def get(self, request, *args, **kwargs):
        # template = get_template('resident/ResidentList.html')
        resident = Resident.objects.all()
        pdf = render_to_pdf('List.html', {'resident': resident})
        return HttpResponse(pdf, content_type='application/pdf')

def report_header(p, y_position):
    brgy = Brgy.objects.first()  
    # def draw_title(y_position, line_height):
    title_header1 = 'Republic of the Philippines'
    title_header2 = 'Province of Cagayan'
    title_header3 = f'Municipality of {brgy.municipality}'
    title_header4 = f'BARANGAY {brgy.brgy_name.upper()}'
    #title = "RESIDENTS LIST"
    p.setFont("Helvetica", 11)  
    p.drawCentredString(290, 800, title_header1)
    p.drawCentredString(290, 788, title_header2)
    p.setFont("Helvetica", 13) 
    p.drawCentredString(290, 768, title_header3)
    p.drawCentredString(290, 748, title_header4)
    # image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media\item_images\brgy_logo.png')
    app_directory = os.path.dirname(os.path.abspath(__file__))
    project_directory = os.path.dirname(app_directory)
    image_path = os.path.join(project_directory, 'media', 'item_images', os.path.basename(brgy.image.name))
    # Embed the image in the PDF
    p.drawImage(image_path, 125, 743, width=70, height=70)

    return p

def report_header_landscape(p, y_position):
    brgy = Brgy.objects.first()
    # def draw_title(y_position, line_height):
    title_header1 = 'Republic of the Philippines'
    title_header2 = 'Province of Cagayan'
    title_header3 = f'Municipality of {brgy.municipality}'
    title_header4 = f'BARANGAY {brgy.brgy_name.upper()}'
    #title = "RESIDENTS LIST"
    p.setFont("Helvetica", 11)  
    p.drawCentredString(440, 800 - 240, title_header1)
    p.drawCentredString(440, 788 - 240, title_header2)
    p.setFont("Helvetica", 13) 
    p.drawCentredString(440, 768 - 240, title_header3)
    p.drawCentredString(440, 748 - 240, title_header4)
    # image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media\item_images\brgy_logo.png')
    app_directory = os.path.dirname(os.path.abspath(__file__))
    project_directory = os.path.dirname(app_directory)
    image_path = os.path.join(project_directory, 'media', 'item_images', os.path.basename(brgy.image.name))
    # Embed the image in the PDF
    p.drawImage(image_path, 275, 743 - 240, width=70, height=70)

    return p

def report_body(p, y_position, line_height, purok_id, residenden):
    titulo = ""
    if purok_id != '0':
        if residenden == "Sr":
            residents = Resident.objects.filter(Q(house_no__purok=purok_id) & Q(birth_date__lt=date.today() - relativedelta(years=+60)))
            titulo = "All Senior Citizens in " + Purok.objects.filter(pk=purok_id).first().purok_name
        elif residenden == "Solo":
            residents = Resident.objects.filter(Q(house_no__purok=purok_id) & Q(solo_parent=True))
            titulo = "All Solo Parents in " + Purok.objects.filter(pk=purok_id).first().purok_name
        elif residenden == "pwd":
             residents = Resident.objects.filter(Q(house_no__purok=purok_id) & Q(pwd=True))
             titulo = "All Persons with disability in " + Purok.objects.filter(pk=purok_id).first().purok_name
        elif residenden == "voter":
            residents = Resident.objects.filter(Q(house_no__purok=purok_id) & Q(voter=True))
            titulo = "All Registered Voters in " + Purok.objects.filter(pk=purok_id).first().purok_name
        else:
            residents = Resident.objects.filter(house_no__purok=purok_id)
            titulo = Purok.objects.filter(pk=purok_id).first().purok_name
        # residents = Resident.objects.filter(house_no__purok=purok_id)
    else:
        if residenden == "Sr":
            residents = Resident.objects.filter(birth_date__lt=date.today() - relativedelta(years=+60)) 
            titulo = "All Senior Citizens"
        elif residenden == "Solo":
            residents = Resident.objects.filter(solo_parent=True)
            titulo = "All Solo Parents"
        elif residenden == "pwd":
             residents = Resident.objects.filter(pwd=True)
             titulo = "All Persons with disability"
        elif residenden == "voter":
            residents = Resident.objects.filter(voter=True)
            titulo = "All Registered Voters"
        else:
            residents = Resident.objects.all()
            titulo =""
  
    
    # residents = Resident.objects.all()
    total = residents.count()
    current_date = datetime.now().date()
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "RESIDENTS LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(450, y_position + 20, f"As of: {current_date}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "NAME")
        p.drawString(230, y_position, "AGE")
        p.drawString(270, y_position, "GENDER")
        p.drawString(340, y_position, "ADDRESS")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, resident in enumerate(residents, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {resident.f_name} {resident.l_name}")
        p.drawString(230, y_position, f"{calculate_age(resident.birth_date)}")
        p.drawString(270, y_position, f"{resident.gender}")
        p.drawString(340, y_position, f"{resident.house_no.address}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_brgyClearance_list(p, y_position, line_height, dateFrom, dateTo):
    titulo = ""
    if dateFrom != dateTo:
        titulo = "(" + str(dateFrom) + ")" + " to " + "(" + str(dateTo) + ")"
    else:
        titulo = "(" + str(dateFrom) + ")"
    
    brgyClearance = BrgyClearance.objects.filter(date_created__range=[dateFrom, dateTo])
    total_amount = brgyClearance.aggregate(total_amount=Sum('or_amount'))
    total_amount_value = total_amount.get('total_amount', 0)
    total = brgyClearance.count()
    # current_date = datetime.now().date()
    
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "BRGY CLEARANCE LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(420, y_position + 20, f"Total Amount: {total_amount_value}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "NAME")
        p.drawString(230, y_position, "PURPOSE")
        p.drawString(320, y_position, "DATE CREATED")
        p.drawString(450, y_position, "AMOUNT")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, clearance in enumerate(brgyClearance, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {clearance.resident}")
        p.drawString(230, y_position, f"{clearance.purpose}")
        p.drawString(320, y_position, f"{clearance.date_created.strftime('%Y-%m-%d')}")
        p.drawString(450, y_position, f"{clearance.or_amount}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_Indigency_list(p, y_position, line_height, dateFrom, dateTo):
    titulo = ""
    if dateFrom != dateTo:
        titulo = "(" + str(dateFrom) + ")" + " to " + "(" + str(dateTo) + ")"
    else:
        titulo = "(" + str(dateFrom) + ")"
    
    certIndigency = CertIndigency.objects.filter(date_created__range=[dateFrom, dateTo])
    total_amount = certIndigency.aggregate(total_amount=Sum('or_amount'))
    total_amount_value = total_amount.get('total_amount', 0)
    total = certIndigency.count()
    # current_date = datetime.now().date()
    
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "CERTIFICATE OF INDIGENCY LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(420, y_position + 20, f"Total Amount: {total_amount_value}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "NAME")
        p.drawString(230, y_position, "PURPOSE")
        p.drawString(320, y_position, "DATE CREATED")
        p.drawString(450, y_position, "AMOUNT")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, clearance in enumerate(certIndigency, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {clearance.resident}")
        p.drawString(230, y_position, f"{clearance.purpose}")
        p.drawString(320, y_position, f"{clearance.date_created.strftime('%Y-%m-%d')}")
        p.drawString(450, y_position, f"{clearance.or_amount}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_SoloParent_list(p, y_position, line_height, dateFrom, dateTo):
    titulo = ""
    if dateFrom != dateTo:
        titulo = "(" + str(dateFrom) + ")" + " to " + "(" + str(dateTo) + ")"
    else:
        titulo = "(" + str(dateFrom) + ")"
    
    certSoloParent = CertSoloParent.objects.filter(date_created__range=[dateFrom, dateTo])
    total_amount = certSoloParent.aggregate(total_amount=Sum('or_amount'))
    total_amount_value = total_amount.get('total_amount', 0)
    total = certSoloParent.count()
    # current_date = datetime.now().date()
    
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "CERTIFICATE OF SOLO PARENT LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(420, y_position + 20, f"Total Amount: {total_amount_value}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "NAME")
        p.drawString(230, y_position, "PURPOSE")
        p.drawString(320, y_position, "DATE CREATED")
        p.drawString(450, y_position, "AMOUNT")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, clearance in enumerate(certSoloParent, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {clearance.resident}")
        p.drawString(230, y_position, f"{clearance.purpose}")
        p.drawString(320, y_position, f"{clearance.date_created.strftime('%Y-%m-%d')}")
        p.drawString(450, y_position, f"{clearance.or_amount}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_JobSeekers_list(p, y_position, line_height, dateFrom, dateTo):
    titulo = ""
    if dateFrom != dateTo:
        titulo = "(" + str(dateFrom) + ")" + " to " + "(" + str(dateTo) + ")"
    else:
        titulo = "(" + str(dateFrom) + ")"
    
    jobseekers = JobSeekers.objects.filter(date_created__range=[dateFrom, dateTo])
    # total_amount = certGoodMoral.aggregate(total_amount=Sum('or_amount'))
    # total_amount_value = total_amount.get('total_amount', 0)
    total = jobseekers.count()
    # current_date = datetime.now().date()
    
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "FIRST TIME JOB SEEKERS LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        # p.drawString(420, y_position + 20, f"Total Amount: {total_amount_value}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "DATE")
        p.drawString(120, y_position, "NAME")
        p.drawString(230, y_position, "AGE")
        p.drawString(280, y_position, "GENDER")
        p.drawString(350, y_position, "ADDRESS")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, seekers in enumerate(jobseekers, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {seekers.date_created.strftime('%Y-%m-%d')}")
        p.drawString(120, y_position, f"{seekers.resident}")
        p.drawString(230, y_position, f"{calculate_age(seekers.resident.birth_date)}")
        # p.drawString(320, y_position, f"{seekers.date_created.strftime('%Y-%m-%d')}")
        p.drawString(280, y_position, f"{seekers.resident.gender}")
        p.drawString(350, y_position, f"{seekers.resident.house_no.address}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_GoodMoral_list(p, y_position, line_height, dateFrom, dateTo):
    titulo = ""
    if dateFrom != dateTo:
        titulo = "(" + str(dateFrom) + ")" + " to " + "(" + str(dateTo) + ")"
    else:
        titulo = "(" + str(dateFrom) + ")"
    
    certGoodMoral = CertGoodMoral.objects.filter(date_created__range=[dateFrom, dateTo])
    total_amount = certGoodMoral.aggregate(total_amount=Sum('or_amount'))
    total_amount_value = total_amount.get('total_amount', 0)
    total = certGoodMoral.count()
    # current_date = datetime.now().date()
    
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "CERTIFICATE OF GOOD MORAL LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(420, y_position + 20, f"Total Amount: {total_amount_value}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "NAME")
        p.drawString(230, y_position, "PURPOSE")
        p.drawString(320, y_position, "DATE CREATED")
        p.drawString(450, y_position, "AMOUNT")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, clearance in enumerate(certGoodMoral, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {clearance.resident}")
        p.drawString(230, y_position, f"{clearance.purpose}")
        p.drawString(320, y_position, f"{clearance.date_created.strftime('%Y-%m-%d')}")
        p.drawString(450, y_position, f"{clearance.or_amount}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_Tribal_list(p, y_position, line_height, dateFrom, dateTo):
    titulo = ""
    if dateFrom != dateTo:
        titulo = "(" + str(dateFrom) + ")" + " to " + "(" + str(dateTo) + ")"
    else:
        titulo = "(" + str(dateFrom) + ")"
    
    certTribal = CertTribal.objects.filter(date_created__range=[dateFrom, dateTo])
    total_amount = certTribal.aggregate(total_amount=Sum('or_amount'))
    total_amount_value = total_amount.get('total_amount', 0)
    total = certTribal.count()
    # current_date = datetime.now().date()
    
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "CERTIFICATE OF TRIBAL MEMBERSHIP LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(420, y_position + 20, f"Total Amount: {total_amount_value}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "NAME")
        p.drawString(230, y_position, "PURPOSE")
        p.drawString(320, y_position, "DATE CREATED")
        p.drawString(450, y_position, "AMOUNT")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, clearance in enumerate(certTribal, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {clearance.resident}")
        p.drawString(230, y_position, f"{clearance.purpose}")
        p.drawString(320, y_position, f"{clearance.date_created.strftime('%Y-%m-%d')}")
        p.drawString(450, y_position, f"{clearance.or_amount}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_NonOperation_list(p, y_position, line_height, dateFrom, dateTo):
    titulo = ""
    if dateFrom != dateTo:
        titulo = "(" + str(dateFrom) + ")" + " to " + "(" + str(dateTo) + ")"
    else:
        titulo = "(" + str(dateFrom) + ")"
    
    certNonOperation = CertNonOperation.objects.filter(date_created__range=[dateFrom, dateTo])
    total_amount = certNonOperation.aggregate(total_amount=Sum('or_amount'))
    total_amount_value = total_amount.get('total_amount', 0)
    total = certNonOperation.count()
    # current_date = datetime.now().date()
    
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "CERTIFICATE OF NON-OPERATION OF BUSINESS LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(420, y_position + 20, f"Total Amount: {total_amount_value}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "BUSINESS NAME")
        p.drawString(200, y_position, "CEASED DATE")
        p.drawString(300, y_position, "PURPOSE")
        p.drawString(380, y_position, "DATE CREATED")
        p.drawString(495, y_position, "AMOUNT")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, clearance in enumerate(certNonOperation, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {clearance.business}")
        p.drawString(200, y_position, f"{clearance.ceased_date.strftime('%Y-%m-%d')}")
        p.drawString(300, y_position, f"{clearance.purpose}")
        p.drawString(380, y_position, f"{clearance.date_created.strftime('%Y-%m-%d')}")
        p.drawString(495, y_position, f"{clearance.or_amount}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_Residency_list(p, y_position, line_height, dateFrom, dateTo):
    titulo = ""
    if dateFrom != dateTo:
        titulo = "(" + str(dateFrom) + ")" + " to " + "(" + str(dateTo) + ")"
    else:
        titulo = "(" + str(dateFrom) + ")"
    
    certResidency = CertResidency.objects.filter(date_created__range=[dateFrom, dateTo])
    total_amount = certResidency.aggregate(total_amount=Sum('or_amount'))
    total_amount_value = total_amount.get('total_amount', 0)
    total = certResidency.count()
    # current_date = datetime.now().date()
    
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "CERTIFICATE OF RESIDENCY LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(420, y_position + 20, f"Total Amount: {total_amount_value}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "NAME")
        p.drawString(230, y_position, "PURPOSE")
        p.drawString(320, y_position, "DATE CREATED")
        p.drawString(450, y_position, "AMOUNT")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, clearance in enumerate(certResidency, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {clearance.resident}")
        p.drawString(230, y_position, f"{clearance.purpose}")
        p.drawString(320, y_position, f"{clearance.date_created.strftime('%Y-%m-%d')}")
        p.drawString(450, y_position, f"{clearance.or_amount}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_businessClearance_list(p, y_position, line_height, dateFrom, dateTo):
    titulo = ""
    if dateFrom != dateTo:
        titulo = "(" + str(dateFrom) + ")" + " to " + "(" + str(dateTo) + ")"
    else:
        titulo = "(" + str(dateFrom) + ")"
    
    businessClearance = BusinessClearance.objects.filter(date_created__range=[dateFrom, dateTo])
    total_amount = businessClearance.aggregate(total_amount=Sum('or_amount'))
    total_amount_value = total_amount.get('total_amount', 0)
    total = businessClearance.count()
    # current_date = datetime.now().date()
    
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "BUSINESS CLEARANCE LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(420, y_position + 20, f"Total Amount: {total_amount_value}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "BUSINESS NAME")
        p.drawString(230, y_position, "BUSINESS TYPE")
        p.drawString(350, y_position, "DATE CREATED")
        p.drawString(470, y_position, "AMOUNT")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, clearance in enumerate(businessClearance, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {clearance.business}")
        p.drawString(230, y_position, f"{clearance.business.business_type}")
        p.drawString(350, y_position, f"{clearance.date_created.strftime('%Y-%m-%d')}")
        p.drawString(470, y_position, f"{clearance.or_amount}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_household(p, y_position, line_height, purok_id):
    titulo = ""
    if purok_id != '0':
        households = Household.objects.filter(purok=purok_id).order_by("house_no")
        # residents = Resident.objects.filter(house_no=purok_id).order_by("house_no")
        titulo = Purok.objects.filter(pk=purok_id).first().purok_name
        # residents = Resident.objects.filter(house_no__purok=purok_id)
    else:
        households = Household.objects.all().order_by("house_no")
        # residents = Resident.objects.filter(house_no=purok_id).order_by("house_no")
        # titulo = Purok.objects.filter(pk=purok_id).first().purok_name
        # residents = Resident.objects.all().order_by("house_no")
        titulo = ""
    
    # residents = Resident.objects.all()
    total = households.count()
    current_date = datetime.now().date()
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "HOUSEHOLD LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(450, y_position + 20, f"As of: {current_date}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "HOUSE NO.")
        p.drawString(160, y_position, "NAME")
        p.drawString(300, y_position, "AGE")
        p.drawString(360, y_position, "GENDER")
        p.drawString(440, y_position, "PUROK/ZONE")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
    no = 0    
    # previous_house_no = None  # Initialize previous_house_no
    for i, household in enumerate(households, start=1):
        house_no = household.house_no
        residents = Resident.objects.filter(house_no=household)
        for resident in residents:
            no += 1
            if y_position <= 50:
                p.showPage()  # Start a new page
                y_position = 650  # Reset Y position for the new page
                draw_header()  # Draw row header for the new page
                report_header(p, y_position)
                y_position -= line_height
            p.setFont("Helvetica", 10)
            p.drawString(50, y_position, f"{no}. {house_no}")
            p.drawString(160, y_position, f"{resident.f_name} {resident.l_name}")
            p.drawString(300, y_position, f"{calculate_age(resident.birth_date)}")
            p.drawString(360, y_position, f"{resident.gender}")
            p.drawString(440, y_position, f"{household.purok}")

            # if previous_house_no != f"{resident.house_no}":
            
                # previous_house_no = f"{resident.house_no}"
            # p.line(50, y_position - 5, 550, y_position - 5)
            y_position -= line_height
        p.line(50, y_position + 15, 550, y_position + 15)
    return p

def report_body_blotter(p, y_position, line_height, status):
    titulo = ""
    if status != 'all':
        if status == "Pending":
            blotter = Blotter.objects.filter(status=status)
            titulo = "Pending"
        else:
            blotter = Blotter.objects.filter(status=status)
            titulo = "Solved"
        # residents = Resident.objects.filter(house_no__purok=purok_id)
    else:
            blotter = Blotter.objects.all()
            titulo =""
  
    # residents = Resident.objects.all()
    total = blotter.count()
    current_date = datetime.now().date()
    def draw_header():
        p.drawCentredString(440, y_position + 37, titulo)
        p.setFont("Helvetica-Bold", 16)    
        p.drawCentredString(440, y_position + 55, "BLOTTER LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(700, y_position + 20, f"As of: {current_date}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 800, y_position + 15)
        p.drawString(50, y_position, "Compainant")
        p.drawString(200, y_position, "Respondent")
        p.drawString(360, y_position, "Statement")
        p.drawString(560, y_position, "Location")
        p.drawString(720, y_position, "Date")
        p.line(50, y_position - 5, 800, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, blotter in enumerate(blotter, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {blotter.complainants}")
        p.drawString(200, y_position, f"{blotter.respondents}")
        p.drawString(360, y_position, f"{blotter.statement}")
        p.drawString(560, y_position, f"{blotter.location}")
        p.drawString(720, y_position, f"{blotter.date_created.strftime('%Y-%m-%d')}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_ofw(p, y_position, line_height, purok_id):
    titulo = ""
    if purok_id != '0':
        ofw = Ofw.objects.filter(resident__purok=purok_id)
        titulo = "All OFW in " + Purok.objects.filter(pk=purok_id).first().purok_name
    else:
        ofw = Ofw.objects.all()
        titulo = ""
  
    # residents = Resident.objects.all()
    total = ofw.count()
    current_date = datetime.now().date()
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "OFW LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(450, y_position + 20, f"As of: {current_date}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "NAME")
        p.drawString(240, y_position, "PASSPORT NUMBER")
        p.drawString(430, y_position, "COUNTRY")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, resident in enumerate(ofw, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {resident.resident}")
        p.drawString(240, y_position, f"{resident.passport_no}")
        p.drawString(430, y_position, f"{resident.country}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_deceased(p, y_position, line_height, purok_id):
    titulo = ""
    if purok_id != '0':
        deceased = Deceased.objects.filter(resident__purok=purok_id)
        titulo = "All Deceased in " + Purok.objects.filter(pk=purok_id).first().purok_name
    else:
        deceased = Deceased.objects.all()
        titulo = ""
  
    # residents = Resident.objects.all()
    total = deceased.count()
    current_date = datetime.now().date()
    def draw_header():
        p.setFont("Helvetica-Bold", 16) 
        p.drawCentredString(290, y_position + 37, titulo)
        p.drawCentredString(290, y_position + 55, "DECEASED LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(450, y_position + 20, f"As of: {current_date}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "NAME")
        p.drawString(260, y_position, "DATE OF DEATH")
        p.drawString(400, y_position, "CAUSE OF DEATH")
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, resident in enumerate(deceased, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {resident.resident}")
        p.drawString(260, y_position, f"{resident.date_of_death}")
        p.drawString(400, y_position, f"{resident.cause_of_death}")
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_body_business(p, y_position, line_height, purok_id, status):
    titulo = ""
    if purok_id != '0':
        if status == "ACTIVE":
            business = Business.objects.filter(Q(house_no__purok=purok_id) & Q(status='ACTIVE'))
            titulo = "All Active Business in " + Purok.objects.filter(pk=purok_id).first().purok_name
        elif status == "INACTIVE":
            business = Business.objects.filter(Q(house_no__purok=purok_id) & Q(status='INACTIVE'))
            titulo = Purok.objects.filter(pk=purok_id).first().purok_name
        else:
            business = Business.objects.filter(purok=purok_id)
            titulo = Purok.objects.filter(pk=purok_id).first().purok_name
        # residents = Resident.objects.filter(house_no__purok=purok_id)
    else:
        if status == "ACTIVE":
            business = Business.objects.filter(status='ACTIVE')
            titulo = "All Active Business"
        elif status == "INACTIVE":
            business = Business.objects.filter(status='INACTIVE')
            titulo = "All Inactive Business"
        else:
            business = Business.objects.all()
            titulo = ""
  
    # residents = Resident.objects.all()
    total = business.count()
    current_date = datetime.now().date()
    def draw_header():
        p.drawCentredString(290, y_position + 37, titulo)
        p.setFont("Helvetica-Bold", 16)      
        p.drawCentredString(290, y_position + 55, "BUSINESS LIST")          
        p.setFont("Helvetica", 12)
        p.drawString(50, y_position + 20, f"Total Count: {total}")
        p.drawString(450, y_position + 20, f"As of: {current_date}")
        p.setFont("Helvetica-Bold", 12)
        p.line(50, y_position + 15, 550, y_position + 15)
        p.drawString(50, y_position, "BUSINESS NAME")
        # p.drawString(180, y_position, "BUSINESS TYPE")
        p.drawString(190, y_position, "ADDRESS")
        p.drawString(400, y_position, "PROPRIETOR'S NAME")
        
        p.line(50, y_position - 5, 550, y_position - 5)    
          
    draw_header()
    y_position -= line_height
        
    
    for i, business in enumerate(business, start=1):
        if y_position <= 50:
            p.showPage()  # Start a new page
            y_position = 650  # Reset Y position for the new page
            draw_header()  # Draw row header for the new page
            report_header(p, y_position)
            y_position -= line_height

        p.setFont("Helvetica", 10)
        p.drawString(50, y_position, f"{i}. {business.business_name}")
        # p.drawString(180, y_position, f"{business.business_type}")
        p.drawString(190, y_position, f"{business.address}")
        p.drawString(400, y_position, f"{business.proprietor}")
        
        # p.line(50, y_position - 5, 550, y_position - 5)
        y_position -= line_height
    return p

def report_brgyOfficials(p, y_position, footer_text):
    officials = Brgy_Officials.objects.first()  
    twelve_space = 12
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position, f"{officials.brgy_Captain}")
    p.setFont("Helvetica", 10)
    p.drawString(75, y_position - twelve_space, "Punong Barangay")
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position - (twelve_space * 3), f"{officials.kagawad1}")
    p.setFont("Helvetica", 10)
    p.drawString(70, y_position - (twelve_space * 4), "Barangay Kagawad")
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position - (twelve_space * 6), f"{officials.kagawad2}")
    p.setFont("Helvetica", 10)
    p.drawString(70, y_position - (twelve_space * 7), "Barangay Kagawad")
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position - (twelve_space * 9), f"{officials.kagawad3}")
    p.setFont("Helvetica", 10)
    p.drawString(70, y_position - (twelve_space * 10), "Barangay Kagawad")
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position - (twelve_space * 12), f"{officials.kagawad4}")
    p.setFont("Helvetica", 10)
    p.drawString(70, y_position - (twelve_space * 13), "Barangay Kagawad")
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position - (twelve_space * 15), f"{officials.kagawad5}")
    p.setFont("Helvetica", 10)
    p.drawString(70, y_position - (twelve_space * 16), "Barangay Kagawad")
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position - (twelve_space * 18), f"{officials.kagawad6}")
    p.setFont("Helvetica", 10)
    p.drawString(70, y_position - (twelve_space * 19), "Barangay Kagawad")
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position - (twelve_space * 21), f"{officials.kagawad7}")
    p.setFont("Helvetica", 10)
    p.drawString(70, y_position - (twelve_space * 22), "Barangay Kagawad")
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position - (twelve_space * 24), f"{officials.sk}")
    p.setFont("Helvetica", 10)
    p.drawString(70, y_position - (twelve_space * 25), "SK Chairman")
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position - (twelve_space * 27), f"{officials.secretary}")
    p.setFont("Helvetica", 10)
    p.drawString(70, y_position - (twelve_space * 28), "Barangay Secretary")
    p.setFont("Helvetica-Bold", 11)
    p.drawCentredString(115, y_position - (twelve_space * 30), f"{officials.treasurer}")
    p.setFont("Helvetica", 10)
    p.drawString(70, y_position - (twelve_space * 31), "Barangay Treasurer")
    p.setFont("Helvetica-Bold", 10)
    p.drawCentredString(115, footer_text, "Not valid without dry seal")
    p.setFont("Helvetica", 10)
    p.drawCentredString(115, footer_text - 20, "Valid for 6 months from this date.")

def report_body_Oath(p, y_position, line_height, pk):
    
    def get_day_with_suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{day}{suffix}"
    jobseekers = JobSeekers.objects.get(pk=pk)
    brgy = Brgy.objects.first()
    brgy_officials = Brgy_Officials.objects.first()
    current_date = datetime.now().date()
    formatted_day = get_day_with_suffix(current_date.day)
    p.setStrokeColor(colors.black)  # Set the frame color
    p.rect(30, 40, 530, 655)
    def draw_header():
        p.setFont("Helvetica-Bold", 13) 
        p.drawCentredString(290, y_position + 50, "OFFICE OF THE PUNONG BARANGAY")       
        p.setFont("Helvetica-Bold", 12)
        p.line(30, y_position + 80, 560, y_position + 80)
        p.line(40, y_position + 77, 550, y_position + 77)     
        p.setFont("Times-Bold", 25)
        p.drawCentredString(290, y_position, "OATH OF UNDERTAKING")
        # p.line(200, y_position + 20, 560, y_position + 20) 
        # p.line(200, 695, 200, 40)
         # Set the width and height for the paragraph
        x, y = 50, y_position  # Starting position
        
        # p.setFont("Helvetica", 11.25)
        # p.drawString(205, y_position, "TO WHOM IT MAY CONCERN:")
        y -= line_height
        y -= line_height
        
        content_lines = [
            f"This is to certify that, Mr/Mrs. {jobseekers.resident}, a resident of {jobseekers.resident.house_no.address}, {brgy.brgy_name}, {brgy.municipality} for (years/months) availing the benefits of Republic Act 11261.",    
            f"Otherwise known as the first Time jobseekers Act of 2019 do hereby declare, agree and undertake to abide and be bound by the following:",     
            f"1. That this is the first time that I will actively look for a job, and  therefore requesting that a Barangay Certificate be issued in my favor to avail the benefit of the law;",
            f"2. That I am aware that the benefit anmd priviledge/s under said law shall be valid only for one (1) year from the date that the barangay issued.",
            f"3. That I can avail the benefits of the law only once;",
            f"4. That I understand that my personal information shall be included in the Roster/List of first Time Jobseekers and will not be used for any unlawful purpose;",
            f"5. That I will inform and/or report to the Barangay personally, through text or the other means, or through my family/relatives once I get employed; and",
            f"6. That iam not beneficiary of the jobstart program under R.A. No. 10889 and other laws give me similar exemptions for the documents or transactions exempted under R.A. 11261",
            f"7. That if issued the request Certification, I will not use the same in any fraud, neither falsity nor help and/or assist in the fabrication of the said certification.",
            f"8. That this undertaking is made solely for the purpose of obtaining a Barangay Certificate consistent with the objective of R.A. 11261 and not for any other purpose.",
            f"9. That this consent to the use of my personal information pursuant of the Data Privacy Act and other applicable laws, rules, and regulations.",
            f"Issued this {formatted_day} day of {month_names.get(current_date.month)}, {current_date.year}. at Barangay {brgy.brgy_name} {brgy.municipality}, Cagayan.",
        ]
        indentation = "              "     
        text = p.beginText(x, y)
        text.setFont("Helvetica", 11.25)
        max_width = 500

        # for i, line in enumerate(content_lines):
        #     if i in (0, 1, len(content_lines) - 1):
        #         indented_line = indentation + line
        #     else:
        #         indented_line = line

        #     words = indented_line.split()
        #     current_line = indentation
        #     for word in words:
        #         test_line = current_line + " " + word
        #         width = p.stringWidth(test_line, "Helvetica", 11.25)
        #         if width <= max_width:
        #             current_line = test_line
        #         else:
        #             p.setFont("Helvetica", 11.25)
        #             p.drawString(x, y, current_line)
        #             y -= 30
        #             current_line = indentation + word
        #     p.drawString(x, y, current_line)
        #     y -= 30


        # Write wrapped text to the canvas
        for i, line in enumerate(content_lines):
        # for line in content_lines:
            

            words = line.split()
            if not words:
                continue
            if i in (0, 1, len(content_lines) - 1):
                current_line = indentation
            else:
                current_line = ""
                
            # words = line.split()
            #  
            # current_line = indentation
            
            for word in words:
                test_line = current_line + " " + word
                width = p.stringWidth(test_line, "Helvetica", 11.25)
                if width <= max_width:
                    current_line = test_line  # Add word if within width
                else:
                    p.setFont("Helvetica", 11.25)
                    p.drawString(x, y, current_line)  # Draw the line
                    y -= 15  # Move to the next line
                    current_line = word # Start a new line with the current word
            p.drawString(x, y, current_line)
            y -= 20


        # Add the content lines to the TextObject
        # for line in content_lines:
        #     text.textLine(line)
        
        # Draw the TextObject on the canvas
        p.drawText(text)

        p.setFont("Helvetica-Bold", 12)
        captain_name = str(brgy_officials.brgy_Captain).upper()
        # Calculate the width of the text
        text_width = p.stringWidth(f"HON. {captain_name}", "Helvetica", 12)

        # Calculate the starting position to center the text
        x_position = 215 + ((180 - text_width) / 2)

        # Draw the centered text
        # p.drawCentredString(290, 305, f"HON. {captain_name}")  
        # p.drawString(x_position, 305, f"HON. {captain_name}")
        p.setFont("Helvetica-Bold", 10)
        p.drawCentredString(115, 160, "First Time Job Seeker")
        # p.drawString(250, 290, "PUNONG BARANGAY")
        p.line(50, 170, 180, 170)

        p.setFont("Helvetica-Oblique", 8.25)
        p.drawString(50, 125, "Witnessed by:")
        p.setFont("Helvetica-Bold", 10)
        p.drawCentredString(115, 90, "Barangay Officials")  
        # p.drawString(265, 200, "Barangay Officials")
        p.line(50, 100, 180, 100)
        
    draw_header()
    y_position -= line_height

    return p

def report_body_JobSeekers(p, y_position, line_height, pk):
    
    def get_day_with_suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{day}{suffix}"
    jobseekers = JobSeekers.objects.get(pk=pk)
    brgy = Brgy.objects.first()
    brgy_officials = Brgy_Officials.objects.first()
    current_date = datetime.now().date()
    formatted_day = get_day_with_suffix(current_date.day)
    p.setStrokeColor(colors.black)  # Set the frame color
    p.rect(30, 40, 530, 655)
    def draw_header():
        p.setFont("Helvetica-Bold", 13) 
        p.drawCentredString(290, y_position + 50, "OFFICE OF THE PUNONG BARANGAY")       
        p.setFont("Helvetica-Bold", 12)
        p.line(30, y_position + 80, 560, y_position + 80)
        p.line(40, y_position + 77, 550, y_position + 77)     
        p.setFont("Times-Bold", 25)
        p.drawCentredString(290, y_position, "C E R T I F I C A T I O N")
        # p.line(200, y_position + 20, 560, y_position + 20) 
        # p.line(200, 695, 200, 40)
         # Set the width and height for the paragraph
        x, y = 50, y_position  # Starting position
        
        # p.setFont("Helvetica", 11.25)
        # p.drawString(205, y_position, "TO WHOM IT MAY CONCERN:")
        y -= line_height
        y -= line_height
        y -= line_height
        
        content_lines = [
            f"This is to certify that, Mr/Mrs. {jobseekers.resident}, a resident of {jobseekers.resident.house_no.address}, {brgy.brgy_name}, {brgy.municipality}, Cagayan, and is qualified to avail of R.A. 11261 or the First Time Job Seekers Assistance Act of 2019.",
            
            f"This is to certify further that the holder/bearer was informed of his/her rights, including the duties and responsibilities accorded bt R.A. 11261 through the oath of undertaking he/she has signed and executed in the presence of Barangay Officials.",
            
            f"Issued this {formatted_day} day of {month_names.get(current_date.month)}, {current_date.year}. at Barangay Camasi, Peñablanca, Cagayan.",
        ]
        indentation = "              "     
        text = p.beginText(x, y)
        text.setFont("Helvetica", 11.25)
        max_width = 500
        # Write wrapped text to the canvas
        for line in content_lines:
            words = line.split()  # Split the line into words
            if not words:
                continue  # Skip empty lines
            current_line = indentation  # Start with the first word
            for word in words[0:]:
                test_line = current_line + " " + word
                width = p.stringWidth(test_line, "Helvetica", 11.25)
                if width <= max_width:
                    current_line = test_line  # Add word if within width
                else:
                    p.setFont("Helvetica", 11.25)
                    p.drawString(x, y, current_line)  # Draw the line
                    y -= line_height  # Move to the next line
                    current_line = word  # Start a new line with the current word
            p.drawString(x, y, current_line)
            y -= 50
        # Add the content lines to the TextObject
        # for line in content_lines:
        #     text.textLine(line)
        
        # Draw the TextObject on the canvas
        p.drawText(text)

        p.setFont("Helvetica-Bold", 12)
        captain_name = str(brgy_officials.brgy_Captain).upper()
        # Calculate the width of the text
        text_width = p.stringWidth(f"HON. {captain_name}", "Helvetica", 12)

        # Calculate the starting position to center the text
        x_position = 215 + ((180 - text_width) / 2)

        # Draw the centered text
        p.drawCentredString(290, 305, f"HON. {captain_name}")  
        # p.drawString(x_position, 305, f"HON. {captain_name}")
        p.setFont("Helvetica", 10)
        p.drawCentredString(290, 290, "PUNONG BARANGAY")
        # p.drawString(250, 290, "PUNONG BARANGAY")
        p.line(190, 300, 390, 300)

        p.setFont("Helvetica", 8.25)
        # p.drawString(200, 180, "APPROVED:")
        p.setFont("Helvetica", 10)
        p.drawCentredString(290, 200, "Barangay Officials")  
        # p.drawString(265, 200, "Barangay Officials")
        p.line(190, 210, 390, 210)
        
    draw_header()
    y_position -= line_height

    return p

def report_body_brgyClearance(p, y_position, line_height, pk):
    brgyclearance = BrgyClearance.objects.get(pk=pk)
    resident = brgyclearance.resident
    current_date = datetime.now().date()
    p.setStrokeColor(colors.black)  # Set the frame color
    p.rect(30, 40, 530, 655)
    def draw_header():
        p.setFont("Helvetica-Bold", 13) 
        p.drawCentredString(290, y_position + 50, "OFFICE OF THE SANGGUNIANG BARANGAY")       
        p.setFont("Helvetica-Bold", 12)
        p.line(30, y_position + 80, 560, y_position + 80)
        p.line(40, y_position + 77, 550, y_position + 77)     
        p.setFont("Times-Bold", 20)
        p.drawString(250, y_position + 25, "BARANGAY CLEARANCE")
        p.line(200, y_position + 20, 560, y_position + 20) 
        p.line(200, 695, 200, 40)
         # Set the width and height for the paragraph
        x, y = 205, y_position  # Starting position
        
        content_lines = [
            "TO WHOM IT MAY CONCERN:",
            " ",
            " ",
            "       THIS IS TO CERTIFY that the person whose signature and ",
            " ",
            "right thumb mark appears herein is a bonafide resident of this ",
            " ",
            "community and it has no pending case nor derogatory/criminal ",
            " ",
            f"record filed in this office as of {current_date}",
            " ",
            f"FULL NAME: {brgyclearance.resident}",
            " ",
            f"ADDRESS: {resident.house_no.address}",
            " ",
            f"CIVIL STATUS: {resident.civil_status}",
            " ",
            f"NATIONALITY: {resident.citizenship}",
            " ",
            f"PURPOSE: {brgyclearance.purpose}",
            " ",
        ]
        
        text = p.beginText(x, y)
        text.setFont("Helvetica", 11.25)
        
        # Add the content lines to the TextObject
        for line in content_lines:
            text.textLine(line)
        
        # Draw the TextObject on the canvas
        p.drawText(text)

        p.setStrokeColor(colors.black)
        p.rect(400, 300, 100, 80)
        p.drawString(405, 290, "Right Thumbmark")
        p.line(370, 270, 530, 270)

        p.setFont("Helvetica", 8.25)
        p.drawString(290, 250, "Recommending Approval:")
        p.setFont("Helvetica", 10)
        p.drawString(370, 210, "Barangay Secretary")
        p.line(330, 220, 500, 220)

        p.setFont("Helvetica", 8.25)
        p.drawString(290, 180, "APPROVED:")
        p.setFont("Helvetica", 10)
        p.drawString(375, 150, "Punong Barangay")
        p.line(330, 160, 500, 160)

        footer_text = 110
        p.drawString(205, footer_text, f"Paid under O.R. No.:{brgyclearance.or_no}")
        p.drawString(205, footer_text - 12, f"Amount Paid:{brgyclearance.or_amount}")
        p.drawString(205, footer_text - 24, f"Date:{brgyclearance.or_date}")
        p.drawString(205, footer_text - 36, f"CTC No.:{brgyclearance.ctc}")
        p.drawString(205, footer_text - 48, f"Amount Paid:{brgyclearance.ctc_amount}")
        p.drawString(205, footer_text - 60, f"Date:{brgyclearance.ctc_date}")

        
        
    draw_header()
    y_position -= line_height

    return p

def report_body_tribal(p, y_position, line_height, pk):
    def get_day_with_suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{day}{suffix}"
    tribal = CertTribal.objects.get(pk=pk)
    resident = tribal.resident
    current_date = datetime.now().date()
    formatted_day = get_day_with_suffix(current_date.day)
    p.setStrokeColor(colors.black)  # Set the frame color
    p.rect(30, 40, 530, 655)
    def draw_header():
        p.setFont("Helvetica-Bold", 13) 
        p.drawCentredString(290, y_position + 50, "OFFICE OF THE SANGGUNIANG BARANGAY")       
        p.setFont("Helvetica-Bold", 12)
        p.line(30, y_position + 80, 560, y_position + 80)
        p.line(40, y_position + 77, 550, y_position + 77)     
        p.setFont("Times-Bold", 17)
        p.drawString(210, y_position + 25, "CERTIFICATE OF TRIBAL MEMBERSHIP")
        p.line(200, y_position + 20, 560, y_position + 20) 
        p.line(200, 695, 200, 40)
         # Set the width and height for the paragraph
        x, y = 205, y_position  # Starting position
        
        p.setFont("Helvetica", 11.25)
        p.drawString(205, y_position, "TO WHOM IT MAY CONCERN:")
        y -= line_height
        y -= line_height
        
        content_lines = [
            f"This is to certify that, Mr/Mrs. {tribal.resident}, 23 years old, {resident.citizenship}, of legal age, {resident.civil_status} and a resident of Camasi, Peñablanca, Cagayan, {resident.house_no.purok} Belongs to {tribal.tribe} of INDIGENOUS CULTURAL COMMUNITTIES / INDIGENOUS PEOPLE.",
            f"This is to certify further that {tribal.mother} mother of {tribal.resident} as well as their ancestors are all recognized members of {tribal.tribe} known to be natives of Camasi Peñablanca, Cagayan.",
            f"Issued this {formatted_day} day of {month_names.get(current_date.month)}, {current_date.year}. at Barangay Camasi, Peñablanca, Cagayan.",
        ]
        indentation = "              "     
        text = p.beginText(170, y)
        text.setFont("Helvetica", 11.25)
        max_width = 355
        # Write wrapped text to the canvas
        for line in content_lines:
            words = line.split()  # Split the line into words
            if not words:
                continue  # Skip empty lines
            current_line = indentation  # Start with the first word
            for word in words[0:]:
                test_line = current_line + " " + word
                width = p.stringWidth(test_line, "Helvetica", 11.25)
                if width <= max_width:
                    current_line = test_line  # Add word if within width
                else:
                    p.setFont("Helvetica", 11.25)
                    p.drawString(x, y, current_line)  # Draw the line
                    y -= line_height  # Move to the next line
                    current_line = word  # Start a new line with the current word
            p.drawString(x, y, current_line)
            y -= 30
        # Add the content lines to the TextObject
        # for line in content_lines:
        #     text.textLine(line)
        
        # Draw the TextObject on the canvas
        p.drawText(text)

        p.setStrokeColor(colors.black)
        p.rect(400, 300, 100, 80)
        p.drawString(405, 290, "Right Thumbmark")
        p.line(370, 270, 530, 270)

        p.setFont("Helvetica", 8.25)
        p.drawString(290, 250, "Recommending Approval:")
        p.setFont("Helvetica", 10)
        p.drawString(370, 210, "Barangay Secretary")
        p.line(330, 220, 500, 220)

        p.setFont("Helvetica", 8.25)
        p.drawString(290, 180, "APPROVED:")
        p.setFont("Helvetica", 10)
        p.drawString(375, 150, "Punong Barangay")
        p.line(330, 160, 500, 160)

        footer_text = 110
        p.drawString(205, footer_text, f"Paid under O.R. No.:{tribal.or_no}")
        p.drawString(205, footer_text - 12, f"Amount Paid:{tribal.or_amount}")
        p.drawString(205, footer_text - 24, f"Date:{tribal.or_date}")
        p.drawString(205, footer_text - 36, f"CTC No.:{tribal.ctc}")
        p.drawString(205, footer_text - 48, f"Amount Paid:{tribal.ctc_amount}")
        p.drawString(205, footer_text - 60, f"Date:{tribal.ctc_date}")

        
        
    draw_header()
    y_position -= line_height

    return p

def report_body_goodmoral(p, y_position, line_height, pk):
    def get_day_with_suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{day}{suffix}"
    goodmoral = CertGoodMoral.objects.get(pk=pk)
    resident = goodmoral.resident
    current_date = datetime.now()
    formatted_day = get_day_with_suffix(current_date.day)
    p.setStrokeColor(colors.black)  # Set the frame color
    p.rect(30, 40, 530, 655)
    def draw_header():
        p.setFont("Helvetica-Bold", 13) 
        p.drawCentredString(290, y_position + 50, "OFFICE OF THE SANGGUNIANG BARANGAY")       
        p.setFont("Helvetica-Bold", 12)
        p.line(30, y_position + 80, 560, y_position + 80)
        p.line(40, y_position + 77, 550, y_position + 77) 
        p.setFont("Times-Bold", 15)
        p.drawString(210, y_position + 25, "CERTIFICATE OF GOOD MORAL CHARACTER")
        p.line(200, y_position + 20, 560, y_position + 20) 
        p.line(200, 695, 200, 40)    

         # Set the width and height for the paragraph
        x, y = 205, y_position  # Starting position
        p.setFont("Helvetica", 11.25)
        p.drawString(205, y_position, "TO WHOM IT MAY CONCERN:")
        y -= line_height
        y -= line_height
        content_lines = [
            f"This is to certify that, {goodmoral.resident}, 23 years old, {resident.citizenship}, of legal age, {resident.civil_status} is a resident of Camasi, Peñablanca, Cagayan.",

            "The above-named person is known to me to be a law abiding citizen and of good moral character and reputation.",

            f"This certification is issued upon request of the above-named person for {goodmoral.purpose} purposes.",

            f"Issued this {formatted_day} day of {month_names.get(current_date.month)}, {current_date.year}. at Barangay Camasi, Peñablanca, Cagayan.",

        ]
        
        indentation = "              "     
        text = p.beginText(170, y)
        text.setFont("Helvetica", 11.25)
        max_width = 355
        # Write wrapped text to the canvas
        for line in content_lines:
            words = line.split()  # Split the line into words
            if not words:
                continue  # Skip empty lines
            current_line = indentation  # Start with the first word
            for word in words[0:]:
                test_line = current_line + " " + word
                width = p.stringWidth(test_line, "Helvetica", 11.25)
                if width <= max_width:
                    current_line = test_line  # Add word if within width
                else:
                    p.setFont("Helvetica", 11.25)
                    p.drawString(x, y, current_line)  # Draw the line
                    y -= 15  # Move to the next line
                    current_line = word  # Start a new line with the current word
            p.drawString(x, y, current_line)
            y -= 30


        # p.setStrokeColor(colors.black)
        # p.rect(400, 300, 100, 80)
        # p.drawString(405, 290, "Right Thumbmark")
        # p.line(370, 270, 530, 270)

        p.setFont("Helvetica", 9.25)
        p.drawString(290, 350, "Recommending Approval:")
        p.setFont("Helvetica", 11)
        p.drawString(370, 310, "Barangay Secretary")
        p.line(330, 320, 500, 320)

        p.setFont("Helvetica", 9.25)
        p.drawString(290, 280, "APPROVED:")
        p.setFont("Helvetica", 11)
        p.drawString(375, 250, "Punong Barangay")
        p.line(330, 260, 500, 260)

        footer_text = 110
        p.drawString(205, footer_text, f"Paid under O.R. No.:{goodmoral.or_no}")
        p.drawString(205, footer_text - 12, f"Amount Paid:{goodmoral.or_amount}")
        p.drawString(205, footer_text - 24, f"Date:{goodmoral.or_date}")
        p.drawString(205, footer_text - 36, f"CTC No.:{goodmoral.ctc}")
        p.drawString(205, footer_text - 48, f"Amount Paid:{goodmoral.ctc_amount}")
        p.drawString(205, footer_text - 60, f"Date:{goodmoral.ctc_date}")
        
    draw_header()
    y_position -= line_height

    return p

def report_body_residency(p, y_position, line_height, pk):
    def get_day_with_suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{day}{suffix}"
    residency = CertResidency.objects.get(pk=pk)
    resident = residency.resident
    current_date = datetime.now()
    formatted_day = get_day_with_suffix(current_date.day)
    p.setStrokeColor(colors.black)  # Set the frame color
    p.rect(30, 40, 530, 655)
    def draw_header():
        p.setFont("Helvetica-Bold", 13) 
        p.drawCentredString(290, y_position + 50, "OFFICE OF THE SANGGUNIANG BARANGAY")       
        p.setFont("Helvetica-Bold", 12)
        p.line(30, y_position + 80, 560, y_position + 80)
        p.line(40, y_position + 77, 550, y_position + 77) 
        p.setFont("Times-Bold", 20)
        p.drawString(230, y_position + 25, "CERTIFICATE OF RESIDENCY")
        p.line(200, y_position + 20, 560, y_position + 20) 
        p.line(200, 695, 200, 40)    

         # Set the width and height for the paragraph
        x, y = 205, y_position  # Starting position
        p.setFont("Helvetica", 11.25)
        p.drawString(205, y_position, "TO WHOM IT MAY CONCERN:")
        y -= line_height
        y -= line_height
        content_lines = [

            f"This is to certify that, {residency.resident}, of legal age ,{resident.civil_status}, {resident.citizenship}, whose specimen signature appears below is a PERMANENT RESIDENT of this Barangay.",

            f"Based on records of this office, he/she has been residing at {resident.house_no.purok} Camasi Peñablanca, Cagayan.",

            f"This certification is issued upon request of the above-named person for {residency.purpose} purposes.",

            f"Issued this {formatted_day} day of {month_names.get(current_date.month)}, {current_date.year}. at Barangay Camasi, Peñablanca, Cagayan.",

        ]
        
        indentation = "              "     
        text = p.beginText(170, y)
        text.setFont("Helvetica", 11.25)
        max_width = 355
        # Write wrapped text to the canvas
        for line in content_lines:
            words = line.split()  # Split the line into words
            if not words:
                continue  # Skip empty lines
            current_line = indentation  # Start with the first word
            for word in words[0:]:
                test_line = current_line + " " + word
                width = p.stringWidth(test_line, "Helvetica", 11.25)
                if width <= max_width:
                    current_line = test_line  # Add word if within width
                else:
                    p.setFont("Helvetica", 11.25)
                    p.drawString(x, y, current_line)  # Draw the line
                    y -= 15  # Move to the next line
                    current_line = word  # Start a new line with the current word
            p.drawString(x, y, current_line)
            y -= 30
        
        # Draw the TextObject on the canvas
        p.drawText(text)

        # p.setStrokeColor(colors.black)
        # p.rect(400, 300, 100, 80)
        p.drawString(210, 390, "Specimen Signature:")
        p.line(210, 370, 350, 370)

        p.setFont("Helvetica", 9.25)
        p.drawString(290, 300, "Recommending Approval:")
        p.setFont("Helvetica", 11)
        p.drawString(370, 260, "Barangay Secretary")
        p.line(330, 270, 500, 270)

        p.setFont("Helvetica", 9.25)
        p.drawString(290, 230, "APPROVED:")
        p.setFont("Helvetica", 11)
        p.drawString(375, 200, "Punong Barangay")
        p.line(330, 210, 500, 210)

        footer_text = 110
        p.drawString(205, footer_text, f"Paid under O.R. No.:{residency.or_no}")
        p.drawString(205, footer_text - 12, f"Amount Paid:{residency.or_amount}")
        p.drawString(205, footer_text - 24, f"Date:{residency.or_date}")
        p.drawString(205, footer_text - 36, f"CTC No.:{residency.ctc}")
        p.drawString(205, footer_text - 48, f"Amount Paid:{residency.ctc_amount}")
        p.drawString(205, footer_text - 60, f"Date:{residency.ctc_date}")
        
    draw_header()
    y_position -= line_height

    return p

def report_body_soloparent(p, y_position, line_height, pk):
    def get_day_with_suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{day}{suffix}"
    soloparent = CertSoloParent.objects.get(pk=pk)
    resident = soloparent.resident
    current_date = datetime.now()
    formatted_day = get_day_with_suffix(current_date.day)
    p.setStrokeColor(colors.black)  # Set the frame color
    p.rect(30, 40, 530, 655)
    def draw_header():
        p.setFont("Helvetica-Bold", 13) 
        p.drawCentredString(290, y_position + 50, "OFFICE OF THE SANGGUNIANG BARANGAY")       
        p.setFont("Helvetica-Bold", 12)
        p.line(30, y_position + 80, 560, y_position + 80)
        p.line(40, y_position + 77, 550, y_position + 77) 
        p.setFont("Times-Bold", 20)
        p.drawString(220, y_position + 25, "CERTIFICATE OF SOLO PARENT")
        p.line(200, y_position + 20, 560, y_position + 20) 
        p.line(200, 695, 200, 40)    

         # Set the width and height for the paragraph
        x, y = 205, y_position  # Starting position
        p.setFont("Helvetica", 11.25)
        p.drawString(205, y_position, "TO WHOM IT MAY CONCERN:")
        y -= line_height
        y -= line_height
        content_lines = [

            f"This is to certify that, {soloparent.resident}, 23 years old, {resident.citizenship}, of legal age, {resident.gender}, {resident.civil_status}, and a resident of {resident.house_no.purok} Camasi Peñablanca, whose specimen signature appears below is a SOLO PARENT who soley provides parental/maternal care and support to her/his child/children.",

            f"              This certification is issued upon request of the above-named person for {soloparent.purpose} purposes.",

            f"              Issued this {formatted_day} day of {month_names.get(current_date.month)}, {current_date.year}. at Barangay Camasi, Peñablanca, Cagayan.",

        ]
        
        indentation = "              "     
        text = p.beginText(170, y)
        text.setFont("Helvetica", 11.25)
        max_width = 355
        # Write wrapped text to the canvas
        for line in content_lines:
            words = line.split()  # Split the line into words
            if not words:
                continue  # Skip empty lines
            current_line = indentation  # Start with the first word
            for word in words[0:]:
                test_line = current_line + " " + word
                width = p.stringWidth(test_line, "Helvetica", 11.25)
                if width <= max_width:
                    current_line = test_line  # Add word if within width
                else:
                    p.setFont("Helvetica", 11.25)
                    p.drawString(x, y, current_line)  # Draw the line
                    y -= 15  # Move to the next line
                    current_line = word  # Start a new line with the current word
            p.drawString(x, y, current_line)
            y -= 30
        
        # Draw the TextObject on the canvas
        p.drawText(text)

        # p.setStrokeColor(colors.black)
        # p.rect(400, 300, 100, 80)
        p.drawString(210, 390, "Specimen Signature:")
        p.line(210, 370, 350, 370)

        p.setFont("Helvetica", 9.25)
        p.drawString(290, 300, "Recommending Approval:")
        p.setFont("Helvetica", 11)
        p.drawString(370, 260, "Barangay Secretary")
        p.line(330, 270, 500, 270)

        p.setFont("Helvetica", 9.25)
        p.drawString(290, 230, "APPROVED:")
        p.setFont("Helvetica", 11)
        p.drawString(375, 200, "Punong Barangay")
        p.line(330, 210, 500, 210)

        footer_text = 110
        p.drawString(205, footer_text, f"Paid under O.R. No.:{soloparent.or_no}")
        p.drawString(205, footer_text - 12, f"Amount Paid:{soloparent.or_amount}")
        p.drawString(205, footer_text - 24, f"Date:{soloparent.or_date}")
        p.drawString(205, footer_text - 36, f"CTC No.:{soloparent.ctc}")
        p.drawString(205, footer_text - 48, f"Amount Paid:{soloparent.ctc_amount}")
        p.drawString(205, footer_text - 60, f"Date:{soloparent.ctc_date}")
        
    draw_header()
    y_position -= line_height

    return p

def report_body_indigency(p, y_position, line_height, pk):
    def get_day_with_suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{day}{suffix}"
    indigency = CertIndigency.objects.get(pk=pk)
    resident = indigency.resident
    current_date = datetime.now().date()
    formatted_day = get_day_with_suffix(current_date.day)
    p.setStrokeColor(colors.black)  # Set the frame color
    p.rect(30, 40, 530, 655)
    def draw_header():
        p.setFont("Helvetica-Bold", 13) 
        p.drawCentredString(290, y_position + 50, "OFFICE OF THE SANGGUNIANG BARANGAY")       
        p.setFont("Helvetica-Bold", 12)
        p.line(30, y_position + 80, 560, y_position + 80)
        p.line(40, y_position + 77, 550, y_position + 77) 
        p.setFont("Times-Bold", 20)
        p.drawString(237, y_position + 25, "CERTIFICATE OF INDIGENCY")
        p.line(200, y_position + 20, 560, y_position + 20) 
        p.line(200, 695, 200, 40)    

         # Set the width and height for the paragraph
        x, y = 205, y_position  # Starting position
        p.setFont("Helvetica", 11.25)
        p.drawString(205, y_position, "TO WHOM IT MAY CONCERN:")
        y -= line_height
        y -= line_height
        content_lines = [
            f"This is to certify that, Mr/Mrs. {indigency.resident}, 23 years old, {resident.citizenship}, of legal age, {resident.civil_status} is a resident of Camasi, Peñablanca, Cagayan.",

            "              IT is certified further that the above - mentioned person belongs to the indigent sector of this community.",

            f"              This certification is issued upon request of the above-named person for {indigency.purpose} purposes.",

            f"              Issued this {formatted_day} day of {month_names.get(current_date.month)}, {current_date.year}. at Barangay Camasi, Peñablanca, Cagayan.",
        ]
        
        indentation = "              "     
        text = p.beginText(170, y)
        text.setFont("Helvetica", 11.25)
        max_width = 355
        # Write wrapped text to the canvas
        for line in content_lines:
            words = line.split()  # Split the line into words
            if not words:
                continue  # Skip empty lines
            current_line = indentation  # Start with the first word
            for word in words[0:]:
                test_line = current_line + " " + word
                width = p.stringWidth(test_line, "Helvetica", 11.25)
                if width <= max_width:
                    current_line = test_line  # Add word if within width
                else:
                    p.setFont("Helvetica", 11.25)
                    p.drawString(x, y, current_line)  # Draw the line
                    y -= 15  # Move to the next line
                    current_line = word  # Start a new line with the current word
            p.drawString(x, y, current_line)
            y -= 30
        
        # Draw the TextObject on the canvas
        p.drawText(text)

        p.setStrokeColor(colors.black)
        p.rect(400, 300, 100, 80)
        p.drawString(405, 290, "Right Thumbmark")
        p.line(370, 270, 530, 270)

        p.setFont("Helvetica", 8.25)
        p.drawString(290, 250, "Recommending Approval:")
        p.setFont("Helvetica", 10)
        p.drawString(370, 210, "Barangay Secretary")
        p.line(330, 220, 500, 220)

        p.setFont("Helvetica", 8.25)
        p.drawString(290, 180, "APPROVED:")
        p.setFont("Helvetica", 10)
        p.drawString(375, 150, "Punong Barangay")
        p.line(330, 160, 500, 160)

        footer_text = 110
        p.drawString(205, footer_text, f"Paid under O.R. No.:{indigency.or_no}")
        p.drawString(205, footer_text - 12, f"Amount Paid:{indigency.or_amount}")
        p.drawString(205, footer_text - 24, f"Date:{indigency.or_date}")
        p.drawString(205, footer_text - 36, f"CTC No.:{indigency.ctc}")
        p.drawString(205, footer_text - 48, f"Amount Paid:{indigency.ctc_amount}")
        p.drawString(205, footer_text - 60, f"Date:{indigency.ctc_date}")
        
    draw_header()
    y_position -= line_height

    return p

def report_body_businessClearance(p, y_position, line_height, pk):
    def get_day_with_suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{day}{suffix}"
    business_clearance = BusinessClearance.objects.get(pk=pk)
    business = business_clearance.business
    current_date = datetime.now().date()
    formatted_day = get_day_with_suffix(current_date.day)
    p.setStrokeColor(colors.black)  # Set the frame color
    p.rect(30, 40, 530, 655)
    def draw_header():
        p.setFont("Helvetica-Bold", 13) 
        p.drawCentredString(290, y_position + 50, "OFFICE OF THE BARANGAY CHAIRMAN")       
        p.setFont("Helvetica-Bold", 12)
        p.line(30, y_position + 80, 560, y_position + 80)
        p.line(40, y_position + 77, 550, y_position + 77) 
        p.setFont("Times-Bold", 14)
        p.drawString(203, y_position + 25, "MANAGEMENT BUSINESS BARANGAY CLEARANCE")
        p.line(200, y_position + 20, 560, y_position + 20) 
        p.line(200, 695, 200, 40)    

         # Set the width and height for the paragraph
        x, y = 205, y_position  # Starting position
        p.drawString(205, y_position, "TO WHOM IT MAY CONCERN:")
        y -= line_height
        y -= line_height
        content_lines = [

            f"This is to certify that, Mr. / Ms. / Mrs. {business.proprietor}, {business.citizenship}, of legal age, is a resident of {business.address}, has manifested his/her intent to engage business in this barangay in his/her capacity as the owner of said business with business name {business.business_name} a {business.business_type}.",
            "THIS FURTHER CERTIFIES that the nature of the business does not destroy the moral values of its residents escpecially the youth and the children, nor does it cause the breach of peace and order and harmony in the barangay, nor endangers the safety and health of its constituents, nor unnecessarily destroys the environment to the detriment of the residents thereof.",
 
            "THIS FURTHER CERTIFIES that the applicant has paid the amount of in consideration thereof by virtue of Barangay Ordinance No. 07, S-2023 entitled barangay revenue code 2019, and that all pertinentordinances of this barangay are hereby complied with and shall henceforth be observed with due respect and obidience to the local authorities.",

            "THIS FURTHER CERTIFIES that the issuance of this Business Barangay Clearance is pursuant to Section 152 'c' of RA 7160 wherein the city/municipality shall never issue any permit or license for any business or activity is located or conducted",

            f"Issued this {formatted_day} day of {month_names.get(current_date.month)}, {current_date.year}. at Barangay Camasi, Peñablanca, Cagayan.",

        ]
        
        indentation = "              "     
        max_width = 355
        # Write wrapped text to the canvas
        for line in content_lines:
            words = line.split()  # Split the line into words
            if not words:
                continue  # Skip empty lines
            current_line = indentation  # Start with the first word
            for word in words[0:]:
                test_line = current_line + " " + word
                width = p.stringWidth(test_line, "Helvetica", 11.25)
                if width <= max_width:
                    current_line = test_line  # Add word if within width
                else:
                    p.setFont("Helvetica", 11.25)
                    p.drawString(x, y, current_line)  # Draw the line
                    y -= 15  # Move to the next line
                    current_line = word  # Start a new line with the current word
            p.drawString(x, y, current_line)
            y -= 20
        # Draw the TextObject on the canvas
        # p.drawText(text)

        p.setStrokeColor(colors.black)
        p.rect(400, 165, 100, 80)
        p.drawString(406, 155, "Right Thumbmark")
        p.line(365, 145, 525, 145)

        p.setFont("Helvetica", 8.25)
        p.drawString(290, 110, "APPROVED:")
        p.setFont("Helvetica", 10)
        p.drawString(375, 80, "Punong Barangay")
        p.line(330, 90, 500, 90)

        footer_text = 235
        p.drawString(205, footer_text, f"Paid under O.R. No.:{business_clearance.or_no}")
        p.drawString(205, footer_text - 12, f"Amount Paid:{business_clearance.or_amount}")
        p.drawString(205, footer_text - 24, f"Date:{business_clearance.or_date}")
        p.drawString(205, footer_text - 36, f"CTC No.:{business_clearance.ctc}")
        p.drawString(205, footer_text - 48, f"Amount Paid:{business_clearance.ctc_amount}")
        p.drawString(205, footer_text - 60, f"Date:{business_clearance.ctc_date}")
        
    draw_header()
    y_position -= line_height

    return p

def report_body_nonOperation(p, y_position, line_height, pk):
    def get_day_with_suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{day}{suffix}"
    nonoperation = CertNonOperation.objects.get(pk=pk)
    business = nonoperation.business
    current_date = datetime.now().date()
    formatted_day = get_day_with_suffix(current_date.day)
    p.setStrokeColor(colors.black)  # Set the frame color
    p.rect(30, 40, 530, 655)
    def draw_header():
        p.setFont("Helvetica-Bold", 13) 
        p.drawCentredString(290, y_position + 50, "OFFICE OF THE BARANGAY CHAIRMAN")       
        p.setFont("Helvetica-Bold", 12)
        p.line(30, y_position + 80, 560, y_position + 80)
        p.line(40, y_position + 77, 550, y_position + 77)     
        p.setFont("Times-Bold", 20)
        p.drawString(205, y_position + 25, "CERTIFICATE OF NON-OPERATION")
        p.line(200, y_position + 20, 560, y_position + 20) 
        p.line(200, 695, 200, 40)
         # Set the width and height for the paragraph
        x, y = 205, y_position  # Starting position
        p.setFont("Helvetica", 11.25)
        p.drawString(205, y_position, "TO WHOM IT MAY CONCERN:")
        y -= line_height
        y -= line_height
        content_lines = [

            f"THIS IS TO CERTIFY THAT {nonoperation.business} a business enterprise with principal address {business.purok}, barangay Camasi, Peñablanca, represented by {business.proprietor} of legal age, {business.citizenship} citizen, with residence at {business.address} whose specimen signature appears, below, has not transacted any business and ceased operation since {nonoperation.ceased_date} up to present.",

            f"This certification is issued upon request of the above-named person for {nonoperation.purpose} purposes.",

            f"Issued this {formatted_day} day of {month_names.get(current_date.month)}, {current_date.year}. at Barangay Camasi, Peñablanca, Cagayan.",

        ]
        
        indentation = "              "     
        text = p.beginText(170, y)
        text.setFont("Helvetica", 11.25)
        max_width = 355
        # Write wrapped text to the canvas
        for line in content_lines:
            words = line.split()  # Split the line into words
            if not words:
                continue  # Skip empty lines
            current_line = indentation  # Start with the first word
            for word in words[0:]:
                test_line = current_line + " " + word
                width = p.stringWidth(test_line, "Helvetica", 11.25)
                if width <= max_width:
                    current_line = test_line  # Add word if within width
                else:
                    p.setFont("Helvetica", 11.25)
                    p.drawString(x, y, current_line)  # Draw the line
                    y -= 15  # Move to the next line
                    current_line = word  # Start a new line with the current word
            p.drawString(x, y, current_line)
            y -= 30


        p.drawString(210, 390, "Specimen Signature:")
        p.line(210, 370, 350, 370)

        p.setStrokeColor(colors.black)
        p.rect(400, 300, 100, 80)
        p.drawString(405, 290, "Right Thumbmark")
        p.line(370, 270, 530, 270)

        p.setFont("Helvetica", 8.25)
        p.drawString(290, 250, "Recommending Approval:")
        p.setFont("Helvetica", 10)
        p.drawString(370, 210, "Barangay Secretary")
        p.line(330, 220, 500, 220)

        p.setFont("Helvetica", 8.25)
        p.drawString(290, 180, "APPROVED:")
        p.setFont("Helvetica", 10)
        p.drawString(375, 150, "Punong Barangay")
        p.line(330, 160, 500, 160)

        footer_text = 110
        p.drawString(205, footer_text, f"Paid under O.R. No.:{nonoperation.or_no}")
        p.drawString(205, footer_text - 12, f"Amount Paid:{nonoperation.or_amount}")
        p.drawString(205, footer_text - 24, f"Date:{nonoperation.or_date}")
        p.drawString(205, footer_text - 36, f"CTC No.:{nonoperation.ctc}")
        p.drawString(205, footer_text - 48, f"Amount Paid:{nonoperation.ctc_amount}")
        p.drawString(205, footer_text - 60, f"Date:{nonoperation.ctc_date}")

        
        
    draw_header()
    y_position -= line_height

    return p

def pdf_report_view(pdf_buffer):
    # pdf_buffer = generate_pdf_report()
    # pdf_report_view(pdf_buffer)
    response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="resident_report.pdf"'
    
    return response

def pdf_ofw_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    purok = request.GET.get('purok')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_ofw(p, y_position, line_height, purok)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_JobSeekers(request, pk):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_JobSeekers(p, y_position, line_height, pk)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_Oath(request, pk):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_Oath(p, y_position, line_height, pk)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_deceased_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    purok = request.GET.get('purok')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_deceased(p, y_position, line_height, purok)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_business_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    purok = request.GET.get('purok')
    status = request.GET.get('status')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_business(p, y_position, line_height, purok, status)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_resident_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    purok = request.GET.get('purok')
    residenden = request.GET.get('residenden')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body(p, y_position, line_height, purok, residenden)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_brgyClearance_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_brgyClearance_list(p, y_position, line_height, fromDate, toDate)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_JobSeekers_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_JobSeekers_list(p, y_position, line_height, fromDate, toDate)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_certResidency_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_Residency_list(p, y_position, line_height, fromDate, toDate)
     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_certIndigency_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_Indigency_list(p, y_position, line_height, fromDate, toDate)
     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_certSoloParent_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_SoloParent_list(p, y_position, line_height, fromDate, toDate)
     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_certGoodMoral_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_GoodMoral_list(p, y_position, line_height, fromDate, toDate)
     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_certTribal_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_Tribal_list(p, y_position, line_height, fromDate, toDate)
     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_certNonOperation_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_NonOperation_list(p, y_position, line_height, fromDate, toDate)
     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_businessClearance_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    fromDate = request.GET.get('fromDate')
    toDate = request.GET.get('toDate')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_businessClearance_list(p, y_position, line_height, fromDate, toDate)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_household_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)
    purok = request.GET.get('purok')
    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   

    report_body_household(p, y_position, line_height, purok)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_blotter_list(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=landscape(A4))
    p.setFont("Helvetica", 12)
    status = request.GET.get('status')
    y_position = 400  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header_landscape(p, y_position)   

    report_body_blotter(p, y_position, line_height, status)

     
    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_brgyClearance(request, pk):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)   

    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   
    report_body_brgyClearance(p, y_position, line_height, pk)
    report_brgyOfficials(p, y_position, 110)

    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_goodmoral(request, pk):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)   

    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   
    report_body_goodmoral(p, y_position, line_height, pk)
    report_brgyOfficials(p, y_position, 110)

    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_residency(request, pk):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)   

    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   
    report_body_residency(p, y_position, line_height, pk)
    report_brgyOfficials(p, y_position, 110)

    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_indigency(request, pk):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)   

    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   
    report_body_indigency(p, y_position, line_height, pk)
    report_brgyOfficials(p, y_position, 110)

    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_soloparent(request, pk):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)   

    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   
    report_body_soloparent(p, y_position, line_height, pk)
    report_brgyOfficials(p, y_position, 110)

    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_tribal(request, pk):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)   

    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   
    report_body_tribal(p, y_position, line_height, pk)
    report_brgyOfficials(p, y_position, 110)

    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_businessClearance(request, pk):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)   

    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   
    report_body_businessClearance(p, y_position, line_height, pk)
    report_brgyOfficials(p, y_position, 110)

    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

def pdf_nonOperation(request, pk):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)   

    y_position = 650  # Starting Y position for the first line
    line_height = 20  # Height of each line  

    report_header(p, y_position)   
    report_body_nonOperation(p, y_position, line_height, pk)
    report_brgyOfficials(p, y_position, 110)

    p.save()
    buffer.seek(0)
    return pdf_report_view(buffer)

@login_required
def brgy_list(request):      
    brgy = Brgy.objects.all()
    return render(request, 'brgy/brgyList.html', {'brgy': brgy})

@login_required
def BlotterList(request):      
    blotter = Blotter.objects.all().order_by("-date_created")
    return render(request, 'blotter/BlotterList.html', {'blotter': blotter})

@login_required
def JobSeekersList(request):      
    jobseekers = JobSeekers.objects.annotate(
        age=ExpressionWrapper(
            date.today().year - F('resident__birth_date__year') - 
            Case(
                When(
                    resident__birth_date__month__gt=date.today().month,
                    then=Value(1)
                ),
                When(
                    resident__birth_date__month=date.today().month,
                    resident__birth_date__day__gt=date.today().day,
                    then=Value(1)
                ),
                default=Value(0),
                output_field=IntegerField()
            ),
            output_field=IntegerField()
        )
    ).order_by('-date_created')
    return render(request, 'jobseekers/JobSeekersList.html', {'jobseekers': jobseekers})

@login_required
def BrgyClearanceList(request):      
    brgyclearance = BrgyClearance.objects.all().order_by('-date_created')
    return render(request, 'brgyclearance/BrgyClearanceList.html', {'brgyclearance': brgyclearance})

@login_required
def CertIndigencyList(request):      
    certindigency = CertIndigency.objects.all().order_by('-date_created')
    return render(request, 'certindigency/CertIndigencyList.html', {'certindigency': certindigency})

@login_required
def CertResidencyList(request):      
    certresidency = CertResidency.objects.all().order_by('-date_created')
    return render(request, 'certresidency/CertResidencyList.html', {'certresidency': certresidency})

@login_required
def CertSoloParentList(request):      
    certsoloparent = CertSoloParent.objects.all().order_by('-date_created')
    return render(request, 'certsoloparent/CertSoloparentList.html', {'certsoloparent': certsoloparent})

@login_required
def CertNonOperationList(request):      
    certnonoperation = CertNonOperation.objects.all().order_by('-date_created')
    return render(request, 'certnonoperation/CertNonoperationList.html', {'certnonoperation': certnonoperation})

@login_required
def CertGoodMoralList(request):      
    certgoodmoral = CertGoodMoral.objects.all().order_by('-date_created')
    return render(request, 'certgoodmoral/CertGoodmoralList.html', {'certgoodmoral': certgoodmoral})

@login_required
def CertTribalList(request):      
    tribal = CertTribal.objects.all().order_by('-date_created')
    return render(request, 'certtribal/CertTribalList.html', {'tribal': tribal})

@login_required
def BusinessClearanceList(request):      
    businessclearance = BusinessClearance.objects.all().order_by('-date_created')
    return render(request, 'businessclearance/BusinessClearanceList.html', {'businessclearance': businessclearance})

@login_required
def BusinessList(request):      
    business = Business.objects.all()
    purok_list= Purok.objects.all().order_by("purok_name") 
    return render(request, 'business/BusinessList.html', {'business': business, 'purok_list': purok_list})

@login_required
def PurokList(request):      
    purok = Purok.objects.all()
    return render(request, 'purok/PurokList.html', {'purok': purok})

@login_required
def ResidentList(request):
    purok_list= Purok.objects.all().order_by("purok_name") 
    resident = Resident.objects.annotate(
        age=ExpressionWrapper(
            date.today().year - F('birth_date__year') - 
            Case(
                When(
                    birth_date__month__gt=date.today().month,
                    then=Value(1)
                ),
                When(
                    birth_date__month=date.today().month,
                    birth_date__day__gt=date.today().day,
                    then=Value(1)
                ),
                default=Value(0),
                output_field=IntegerField()
            ),
            output_field=IntegerField()
        )
    ).order_by("house_no")
           
    return render(request, 'resident/ResidentList.html', {'resident': resident,'purok_list': purok_list})

@login_required
def HouseholdList(request):      
    # resident = Resident.objects.exclude(house_no__isnull=True)
    purok_list= Purok.objects.all().order_by("purok_name") 
    # members = resident.values('house_no').annotate(total_count=Count('id')).order_by('house_no')
    household = Household.objects.all().order_by("house_no")
    member_count = household.annotate(resident_count=Count('resident'))
    return render(request, 'household/HouseholdList.html', {'member_count': member_count, 'purok_list': purok_list, 'household': household})

@login_required
def filter_resident(request):
    purok = request.GET.get('purok')
    
    if purok != '':
        resident = Resident.objects.filter(purok=purok)  
    else:
        resident = Resident.objects.all()
       
    try:   
        # Prepare the order items data as a list of dictionaries
        order_items_data = []
        for r in resident:
            order_items_data.append({
                'pk': r.pk,
                'name': r.f_name + ' ' + r.m_name + ' ' + r.l_name,
                'gender': r.gender,
                'kontak': r.phone_number,
                'address': r.address,
            })
        # print(order_items_data)
        return JsonResponse({'residents': order_items_data,} )
    
    except Resident.DoesNotExist:
        return JsonResponse({'residents': []})

@login_required
def get_members(request):
    sale_id = request.GET.get('sale_id')
    
    try:
        resident = Resident.objects.filter(house_no=sale_id)
        
        # Prepare the order items data as a list of dictionaries
        order_items_data = []
        for r in resident:
            order_items_data.append({
                'name': r.f_name + ' ' + r.m_name + ' ' + r.l_name,
                'gender': r.gender,
                'age': f"{calculate_age(r.birth_date)}",
            })
        return JsonResponse({'order_items': order_items_data,} )
    
    except Resident.DoesNotExist:
        return JsonResponse({'order_items': []})

@login_required
def DeceasedList(request):      
    deceased = Deceased.objects.all()
    purok_list= Purok.objects.all().order_by("purok_name") 
    return render(request, 'deceased/DeceasedList.html', {'deceased': deceased, 'purok_list': purok_list})

@login_required
def OfwList(request):      
    ofw = Ofw.objects.all()
    purok_list= Purok.objects.all().order_by("purok_name") 
    return render(request, 'ofw/OfwList.html', {'ofw': ofw, 'purok_list': purok_list})

@login_required
def Edit_brgy(request):
    brgy_count  = Brgy.objects.all().count()

    if brgy_count > 0:
        brgy = Brgy.objects.first()       
        if request.method == 'POST':
            form = BrgyForm(request.POST, request.FILES, instance=brgy)
            if form.is_valid():
                form.save()
                return redirect('Edit_brgy')
        else:
            form = BrgyForm(instance=brgy)

    else:
        if request.method == 'POST':
            form = BrgyForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('Edit_brgy')
        else:
            form = BrgyForm()
    return render(request, 'brgy/Edit_brgy.html', {'form': form})

@login_required
def brgy_list(request, pk):
    try:
        brgy = get_object_or_404(Brgy, pk=pk)
        if request.method == 'POST':
            form = BrgyForm(request.POST, request.FILES, instance=brgy)
            if form.is_valid():
                form.save()
                return redirect('brgy_list')
        else:
            form = BrgyForm(instance=brgy)
        return render(request, 'brgy/Edit_brgy.html', {'form': form, 'brgy': brgy})
    except Http404:  
        if request.method == 'POST':
            form = BrgyForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('brgy_list')
        else:
            form = BrgyForm()
        return render(request, 'brgy/Edit_brgy.html', {'form': form})
    
@login_required
def AdEdPurok(request, pk):
    try:
        purok = get_object_or_404(Purok, pk=pk)
        if request.method == 'POST':
            form = PurokForm(request.POST, request.FILES, instance=purok)
            if form.is_valid():
                form.save()
                return redirect('PurokList')
        else:
            form = PurokForm(instance=purok)
        return render(request, 'purok/AdEdPurok.html', {'form': form, 'purok': purok})
    except Http404:  
        if request.method == 'POST':
            form = PurokForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('PurokList')
        else:
            form = PurokForm()
        return render(request, 'purok/AdEdPurok.html', {'form': form})
    
@login_required    
def AdEdHousehold(request, pk):
    try:
        household = get_object_or_404(Household, pk=pk)
        if request.method == 'POST':
            form = HouseholdForm(request.POST, request.FILES, instance=household)
            if form.is_valid():
                form.save()
                return redirect('HouseholdList')
        else:
            form = HouseholdForm(instance=household)
        return render(request, 'household/AdEdHousehold.html', {'form': form, 'household': household})
    except Http404:  
        if request.method == 'POST':
            form = HouseholdForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('HouseholdList')
        else:
            form = HouseholdForm()
        return render(request, 'household/AdEdHousehold.html', {'form': form})
    
@login_required    
def AdEdJobSeekers(request, pk):
    try:
        jobseekers = get_object_or_404(JobSeekers, pk=pk)
        
        if request.method == 'POST':
            form = JobSeekersForm(request.POST, request.FILES, instance=jobseekers)
            if form.is_valid():
                form.save()
                # pdf_buffer = generate_pdf_report()
                # return pdf_report_view(pdf_buffer)
                return redirect('JobSeekersList')
        else:
            form = JobSeekersForm(instance=jobseekers)
        return render(request, 'jobseekers/AdEdJobSeekers.html', {'form': form, 'jobseekers': jobseekers})
    except Http404:  
        resident = Resident.objects.all()
        if request.method == 'POST':
            form = JobSeekersForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()                
                return redirect('JobSeekersList')               
        else:
            form = JobSeekersForm()
        return render(request, 'jobseekers/AdEdJobSeekers.html', {'form': form, 'resident': resident})

@login_required    
def AdEdBrgyClearance(request, pk):
    try:
        brgyclearance = get_object_or_404(BrgyClearance, pk=pk)
        
        if request.method == 'POST':
            form = BrgyClearanceForm(request.POST, request.FILES, instance=brgyclearance)
            if form.is_valid():
                form.save()
                # pdf_buffer = generate_pdf_report()
                # return pdf_report_view(pdf_buffer)
                return redirect('BrgyClearanceList')
        else:
            form = BrgyClearanceForm(instance=brgyclearance)
        return render(request, 'brgyclearance/AdEdBrgyClearance.html', {'form': form, 'brgyclearance': brgyclearance})
    except Http404:  
        resident = Resident.objects.all()
        if request.method == 'POST':
            form = BrgyClearanceForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()                
                return redirect('BrgyClearanceList')               
        else:
            form = BrgyClearanceForm()
        return render(request, 'brgyclearance/AdEdBrgyClearance.html', {'form': form, 'resident': resident})

@login_required    
def AdEdTribal(request, pk):
    try:
        tribal = get_object_or_404(CertTribal, pk=pk)
        if request.method == 'POST':
            form = CertTribalForm(request.POST, request.FILES, instance=tribal)
            if form.is_valid():
                form.save()
                # pdf_buffer = generate_pdf_report()
                # return pdf_report_view(pdf_buffer)
                return redirect('CertTribalList')
        else:
            form = CertTribalForm(instance=tribal)
        return render(request, 'certtribal/AdEdCertTribal.html', {'form': form, 'tribal': tribal})
    except Http404:  
        if request.method == 'POST':
            form = CertTribalForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                
                return redirect('CertTribalList')
                
        else:
            form = CertTribalForm()
        return render(request, 'certtribal/AdEdCertTribal.html', {'form': form})

@login_required
def AdEdCertGoodMoral(request, pk):
    try:
        certgoodmoral = get_object_or_404(CertGoodMoral, pk=pk)
        if request.method == 'POST':
            form = CertGoodMoralForm(request.POST, request.FILES, instance=certgoodmoral)
            if form.is_valid():
                form.save()
                return redirect('CertGoodMoralList')
        else:
            form = CertGoodMoralForm(instance=certgoodmoral)
        return render(request, 'certgoodmoral/AdEdCertGoodmoral.html', {'form': form, 'certgoodmoral': certgoodmoral})
    except Http404:  
        if request.method == 'POST':
            form = CertGoodMoralForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('CertGoodMoralList')
        else:
            form = CertGoodMoralForm()
        return render(request, 'certgoodmoral/AdEdCertGoodmoral.html', {'form': form})

@login_required
def AdEdCertResidency(request, pk):
    try:
        certresidency = get_object_or_404(CertResidency, pk=pk)
        if request.method == 'POST':
            form = CertResidencyForm(request.POST, request.FILES, instance=certresidency)
            if form.is_valid():
                form.save()
                return redirect('CertResidencyList')
        else:
            form = CertResidencyForm(instance=certresidency)
        return render(request, 'certresidency/AdEdCertResidency.html', {'form': form, 'certresidency': certresidency})
    except Http404:  
        if request.method == 'POST':
            form = CertResidencyForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('CertResidencyList')
        else:
            form = CertResidencyForm()
        return render(request, 'certresidency/AdEdCertResidency.html', {'form': form})

@login_required
def AdEdCertIndigency(request, pk):
    try:
        certindigency = get_object_or_404(CertIndigency, pk=pk)
        if request.method == 'POST':
            form = CertIndigencyForm(request.POST, request.FILES, instance=certindigency)
            if form.is_valid():
                form.save()
                return redirect('CertIndigencyList')
        else:
            form = CertIndigencyForm(instance=certindigency)
        return render(request, 'certindigency/AdEdCertIndigency.html', {'form': form, 'certindigency': certindigency})
    except Http404:  
        if request.method == 'POST':
            form = CertIndigencyForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('CertIndigencyList')
        else:
            form = CertIndigencyForm()
        return render(request, 'certindigency/AdEdCertIndigency.html', {'form': form})

@login_required
def AdEdCertSoloParent(request, pk):
    try:
        certsoloparent = get_object_or_404(CertSoloParent, pk=pk)
        if request.method == 'POST':
            form = CertSoloParentForm(request.POST, request.FILES, instance=certsoloparent)
            if form.is_valid():
                form.save()
                return redirect('CertSoloParentList')
        else:
            form = CertSoloParentForm(instance=certsoloparent)
        return render(request, 'certsoloparent/AdEdCertSoloparent.html', {'form': form, 'certsoloparent': certsoloparent})
    except Http404:  
        if request.method == 'POST':
            form = CertSoloParentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('CertSoloParentList')
        else:
            form = CertSoloParentForm()
        return render(request, 'certsoloparent/AdEdCertSoloparent.html', {'form': form})

@login_required
def AdEdCertNonOperation(request, pk):
    try:
        certnonoperation = get_object_or_404(CertNonOperation, pk=pk)
        if request.method == 'POST':
            form = CertNonOperationForm(request.POST, request.FILES, instance=certnonoperation)
            if form.is_valid():
                form.save()
                return redirect('CertNonOperationList')
        else:
            form = CertNonOperationForm(instance=certnonoperation)
        return render(request, 'certnonoperation/AdEdCertNonoperation.html', {'form': form, 'certnonoperation': certnonoperation})
    except Http404:  
        if request.method == 'POST':
            form = CertNonOperationForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('CertNonOperationList')
        else:
            form = CertNonOperationForm()
        return render(request, 'certnonoperation/AdEdCertNonoperation.html', {'form': form})

@login_required
def AdEdBusinessClearance(request, pk):
    try:
        businessclearance = get_object_or_404(BusinessClearance, pk=pk)
        if request.method == 'POST':
            form = BusinessClearanceForm(request.POST, request.FILES, instance=businessclearance)
            if form.is_valid():
                form.save()
                return redirect('BusinessClearanceList')
        else:
            form = BusinessClearanceForm(instance=businessclearance)
        return render(request, 'businessclearance/AdEdBusinessClearance.html', {'form': form, 'businessclearance': businessclearance})
    except Http404:  
        if request.method == 'POST':
            form = BusinessClearanceForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('BusinessClearanceList')
        else:
            form = BusinessClearanceForm()
        return render(request, 'businessclearance/AdEdBusinessClearance.html', {'form': form})

@login_required
def AdEdBlotter(request, pk):
    try:
        blotter = get_object_or_404(Blotter, pk=pk)
        if request.method == 'POST':
            form = BlotterForm(request.POST, request.FILES, instance=blotter)
            if form.is_valid():
                form.save()
                return redirect('BlotterList')
        else:
            form = BlotterForm(instance=blotter)
        return render(request, 'blotter/AdEdBlotter.html', {'form': form, 'blotter': blotter})
    except Http404:  
        if request.method == 'POST':
            form = BlotterForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()

                return redirect('BlotterList')
        else:
            form = BlotterForm()
        return render(request, 'blotter/AdEdBlotter.html', {'form': form})

@login_required
def AdEdBusiness(request, pk):
    try:
        business = get_object_or_404(Business, pk=pk)
        if request.method == 'POST':
            form = BusinessForm(request.POST, request.FILES, instance=business)
            if form.is_valid():
                form.save()
                return redirect('BusinessList')
        else:
            form = BusinessForm(instance=business)
        return render(request, 'business/AdEdBusiness.html', {'form': form, 'business': business})
    except Http404:  
        if request.method == 'POST':
            form = BusinessForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()

                return redirect('BusinessList')
        else:
            form = BusinessForm()
        return render(request, 'business/AdEdBusiness.html', {'form': form})

@login_required
def AdEdResident(request, pk):
    purok_list= Purok.objects.all().order_by("purok_name") 
    try:
        resident = get_object_or_404(Resident, pk=pk)        
        if request.method == 'POST':
            form = ResidentForm(request.POST, request.FILES, instance=resident)
            if form.is_valid():
                form.save()
                return redirect('ResidentList')
        else:
            form = ResidentForm(instance=resident)
        return render(request, 'resident/AdEdResident.html', {'form': form, 'resident': resident, 'purok_list': purok_list})
    except Http404:  
        if request.method == 'POST':
            form = ResidentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('ResidentList')
        else:
            form = ResidentForm()
        return render(request, 'resident/AdEdResident.html', {'form': form, 'purok_list': purok_list})

@login_required
def AdEdBrgyOfficials(request):
    officials_count  = Brgy_Officials.objects.all().count()

    if officials_count > 0:
        officials = Brgy_Officials.objects.first()       
        if request.method == 'POST':
            form = brgyOfficialForm(request.POST, request.FILES, instance=officials)
            if form.is_valid():
                form.save()
                return redirect('AdEdBrgyOfficials')
        else:
            form = brgyOfficialForm(instance=officials)

    else:
        if request.method == 'POST':
            form = brgyOfficialForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('AdEdBrgyOfficials')
        else:
            form = brgyOfficialForm()
    return render(request, 'officials.html', {'form': form})

@login_required
def AdEdDeceased(request, pk):
    try:
        deceased = get_object_or_404(Deceased, pk=pk)
        if request.method == 'POST':
            form = DeceasedForm(request.POST, request.FILES, instance=deceased)
            if form.is_valid():
                form.save()
                return redirect('DeceasedList')
        else:
            form = DeceasedForm(instance=deceased)
        return render(request, 'deceased/AdEdDeceased.html', {'form': form, 'deceased': deceased})
    except Http404:  
        if request.method == 'POST':
            form = DeceasedForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('DeceasedList')
        else:
            form = DeceasedForm()
        return render(request, 'deceased/AdEdDeceased.html', {'form': form})

@login_required
def AdEdOfw(request, pk):
    try:
        ofw = get_object_or_404(Ofw, pk=pk)
        if request.method == 'POST':
            form = OfwForm(request.POST, request.FILES, instance=ofw)
            if form.is_valid():
                form.save()
                return redirect('OfwList')
        else:
            form = OfwForm(instance=ofw)
        return render(request, 'ofw/AdEdOfw.html', {'form': form, 'ofw': ofw})
    except Http404:  
        if request.method == 'POST':
            form = OfwForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('OfwList')
        else:
            form = OfwForm()
        return render(request, 'ofw/AdEdOfw.html', {'form': form})

@login_required
def Delete_brgy(request, pk):
    if request.method == 'POST':
        brgy = get_object_or_404(Brgy, pk=pk)
        brgy.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_purok(request, pk):
    if request.method == 'POST':
        purok = get_object_or_404(Purok, pk=pk)
        purok.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_resident(request, pk):
    if request.method == 'POST':
        resident = get_object_or_404(Resident, pk=pk)
        # resident = Resident.objects.all()
        resident.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_household(request, pk):
    if request.method == 'POST':
        household = get_object_or_404(Household, pk=pk)
        household.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_deceased(request, pk):
    if request.method == 'POST':
        deceased = get_object_or_404(Deceased, pk=pk)
        deceased.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_ofw(request, pk):
    if request.method == 'POST':
        ofw = get_object_or_404(Ofw, pk=pk)
        ofw.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_blotter(request, pk):
    if request.method == 'POST':
        blotter = get_object_or_404(Blotter, pk=pk)
        blotter.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_business(request, pk):
    if request.method == 'POST':
        business = get_object_or_404(Business, pk=pk)
        business.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_brgyclearance(request, pk):
    if request.method == 'POST':
        brgyclearance = get_object_or_404(BrgyClearance, pk=pk)
        brgyclearance.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_tribal(request, pk):
    if request.method == 'POST':
        tribal = get_object_or_404(CertTribal, pk=pk)
        tribal.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_businessclearance(request, pk):
    if request.method == 'POST':
        businessclearance = get_object_or_404(BusinessClearance, pk=pk)
        businessclearance.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_certgoodmoral(request, pk):
    if request.method == 'POST':
        certgoodmoral = get_object_or_404(CertGoodMoral, pk=pk)
        certgoodmoral.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_certindigency(request, pk):
    if request.method == 'POST':
        certindigency = get_object_or_404(CertIndigency, pk=pk)
        certindigency.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_certresidency(request, pk):
    if request.method == 'POST':
        certresidency = get_object_or_404(CertResidency, pk=pk)
        certresidency.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_certnonoperation(request, pk):
    if request.method == 'POST':
        certnonoperation = get_object_or_404(CertNonOperation, pk=pk)
        certnonoperation.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

@login_required
def Delete_certsoloparent(request, pk):
    if request.method == 'POST':
        certsoloparent = get_object_or_404(CertSoloParent, pk=pk)
        certsoloparent.delete()
        return JsonResponse({'message': 'Item deleted successfully.'})
    return JsonResponse({'message': 'Invalid request method.'}, status=400)

def import_residents(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        result = import_residents_from_excel(file)
        if result is True:
            message = 'Import successful'
        else:
            message = f'Import failed: {result}'
    else:
        message = 'Upload an Excel file'

    return render(request, 'import_residents.html', {'message': message})
