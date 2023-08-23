import pandas as pd
from .models import Resident, Purok

def import_residents_from_excel(file_path):
    try:
        df = pd.read_excel(file_path)  # Read Excel file using pandas

        for index, row in df.iterrows():
            purok_name = row['purok']  # Get the purok name from the Excel file
            purok_instance, created = Purok.objects.get_or_create(purok_name=purok_name)
            
            Resident.objects.create(
                f_name=row['f_name'],
                l_name=row['l_name'],
                m_name=row['m_name'],
                gender=row['gender'],
                house_no =row['house_no'],
                address =row['address'],
                purok=purok_instance,
                phone_number = row['phone_number'],
                birth_date = row['birth_date'],
                birth_place = row['birth_place'],
                civil_status = row['civil_status'],
                religion = row['religion'],
                citizenship = row['citizenship'],
                profession = row['profession'],   
                education = row['education'],
            )
        
        return True  # Import successful
    except Exception as e:
        return str(e)  # Return error message
