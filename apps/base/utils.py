from datetime import datetime

def validate_files(request,field, update=False):
    """
    params
    request: request.data
    field: key of file
    """
    #Por defecto request.data es un QueryDict, es inmutable
    request = request.copy()

    if update:
        if type(request[field]) == str: request.__delitem__(field)
    else:
        if type(request[field]) == str: request.__setitem__(field, None)
 
    return request


# Esta función se creó pq en el front el campo date se escribe como dd/mm/YY 
# y el backend lo espera como YY/mm/dd
def format_date(date):
    date = datetime.strptime(date, '%d/%m/%Y')
    date = f'{date.year}-{date.month}-{date.day}'
    return date