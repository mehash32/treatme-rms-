from django.shortcuts import render
from django.http import request, HttpResponseRedirect
from stuffs.models import restaurantList, foodItem

# Create your views here.
def index(request):
    rest_valid = restaurantList.objects.filter(is_valid=True).order_by('id')
    rest_invalid = restaurantList.objects.filter(is_valid=False).order_by('id')

    context = {
        'rest_valid':rest_valid,
        'rest_invalid':rest_invalid
    }
    return render(request, 'admin/home.html', context)


def action(request, id):
    rest = restaurantList.objects.get(id=id)

    if rest.is_valid:
        rest.is_valid = False
        rest.save()
        items = foodItem.objects.filter(Restaurant_name=rest)

        for item in items:
            item.Availability = 'Out of Stock'
            item.save()

    else:
        rest.is_valid = True
        rest.save()
        items = foodItem.objects.filter(Restaurant_name=rest)

        for item in items:
            item.Availability = 'Available'
            item.save()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
