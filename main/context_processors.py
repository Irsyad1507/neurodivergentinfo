from datetime import datetime

def year_copyright(request):
    return {
        'current_year': datetime.now().year
    }