from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView
from .models import foodItem, restaurantList, Comment, Review
from accounts.models import UserAddress
from Food.models import Manager, UserProfile, Order, Cart, CartItem, Rating
from stuffs.forms import ItemForm, RestaurantForm, RestaurantUpdateForm
from Food.forms import UserUpdateForm, ProfileUpdateForm

from datetime import datetime
from datetime import date


# Create your views here.
def index(request):
    try:
        user = Manager.objects.get(user=request.user)
    except TypeError:
        raise   Http404

    rest = user.Restaurant

    review_count = Review.objects.filter(rest=rest).count()
    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'rest':rest
    }

    return render(request, "restaurantStuffs/index.html", context)


@login_required
def user_profile(request):

    try:
        user = Manager.objects.get(user=request.user)
    except TypeError:
        raise   Http404

    rest = user.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()
    user = User.objects.filter(username=request.user.username).first()
    cur_user = UserProfile.objects.filter(user=user).first()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'rest':rest,
        'user':user,
        'cur_user':cur_user
    }
    
    return render(request, "restaurantStuffs/user_profile.html", context)


@login_required
def update_profile(request):
    try:
        user = Manager.objects.get(user=request.user)
    except TypeError:
        raise   Http404

    rest = user.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()
    user = User.objects.filter(username=request.user.username).first()
    cur_user = UserProfile.objects.filter(user=user).first()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            return redirect('user_staff_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'rest':rest,
        'user':user,
        'cur_user':cur_user,
        'u_form':u_form,
        'p_form':p_form
    }

    return render(request, "restaurantStuffs/update_profile.html", context)


def item_details(request, id):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant

    item = foodItem.objects.filter(pk=id).first()
    rate = Rating.objects.filter(item=item)
    count = rate.count()

    sum = 0
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0

    for r in rate:
        val = int(r.stars)

        if val == 1:
            one = one + 1
        if val == 2:
            two = two + 1
        if val == 3:
            three = three + 1
        if val == 4:
            four = four + 1
        if val == 5:
            five = five + 1

        sum = sum + val

    try:
        p_one = 100*one/count
    except ZeroDivisionError:
        p_one = 0

    try:
        p_two = 100*two/count
    except ZeroDivisionError:
        p_two = 0

    try:
        p_three = 100*three/count
    except ZeroDivisionError:
        p_three = 0

    try:
        p_four = 100*four/count
    except ZeroDivisionError:
        p_four = 0

    try:
        p_five = 100*five/count
    except ZeroDivisionError:
        p_five = 0

    try:
        avg = format(sum/count, '.1f')
    except:
        avg = 0

    items = foodItem.objects.filter(Restaurant_name=rest)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()

    context = {
        'rest':rest,
        'item':item,
        'avg':avg,
        'count':count,
        'one':one,
        'two':two,
        'three':three,
        'four':four,
        'five':five,
        'per_one':p_one,
        'per_two':p_two,
        'per_three':p_three,
        'per_four':p_four,
        'per_five':p_five,
        'item_count':item_count,
        'order_count':order_count
    }

    return render(request, "restaurantStuffs/food_item.html", context)


@login_required
def allItems(request):
    try:
        manager = Manager.objects.get(user=request.user)
    except TypeError:
        raise   Http404

    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()

    sidenav = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'rest':rest
    }

    flag = rest.is_valid
    items = foodItem.objects.filter(Restaurant_name=rest)
    count = items.count()
    av = items.exists()

    paginator = Paginator(items, per_page=4)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'items':page_obj.object_list,
        'count':count,
        'av':av,
        'flag':flag,
        'paginator':paginator,
        'page_number':int(page_number)
    }

    context.update(sidenav)
    return render(request, "restaurantStuffs/item.html", context)


@login_required
def add_item(request):
    try:
        manager = Manager.objects.get(user=request.user)
    except TypeError:
        raise   Http404

    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()
    form = ItemForm(request.POST, request.FILES)

    if request.method == 'POST':
        if form.is_valid():
            item = form.save()
            item.Restaurant_name = rest
            item.save()

            return redirect('../myitems')

    else:
        form = ItemForm()
    
    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'rest':rest,
        'form':form
    }
    return render(request, 'restaurantStuffs/addItem.html', context)


@login_required
def edit_item(request, id):
    try:
        user = Manager.objects.get(user=request.user)
    except TypeError:
        raise   Http404

    rest = user.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()
    item = get_object_or_404(foodItem, pk=id)

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            return redirect('../myitems')
    
    else:
        form = ItemForm(instance=item)
        
        context = {
            'item_count':item_count,
            'order_count':order_count,
            'review_count':review_count,
            'rest':rest,
            'form':form
        }
        
        return render(request, "restaurantStuffs/editItem.html", context)


@login_required
def delete_item(request, id):
    foodItem.objects.filter(pk=id).delete()
    return redirect('../myitems')


@login_required
def cus_orders(request):
    manager = Manager.objects.get(user=request.user)
    current_year = date.today().year
    monthList = ['none', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    if request.method == 'POST':
        year = request.POST.get('year')
        month = request.POST.get('month')

        if year == '' and month == '':
            pass
        elif year == '':
            year = date.today().year

        monthValue = monthList.index(month)

        if monthValue == 0:
            orders = Order.objects.filter(timestamp__year=year)
            timeline = year
        else:
            orders = Order.objects.filter(timestamp__year=year, timestamp__month=monthValue)
            timeline = month + " " + str(year)

    else:
        orders = Order.objects.filter(restaurant=manager.Restaurant, timestamp__date=date.today())
        timeline = 'Today : ' + str(date.today())

    income = 0.0
    for order in orders:
        income += float(order.final_total)

    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=manager.Restaurant).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'count':orders.count(),
        'rest':rest,
        'orders':orders,
        'timeline':timeline,
        'income':income,
        'c_year':current_year
    }

    return render(request, "restaurantStuffs/customer_orders.html", context)


# Order Filters
@login_required
def all_orders(request):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)
    current_year = date.today().year
    
    orders = Order.objects.filter(restaurant=manager.Restaurant)
    timeline = 'All'

    income = 0.0
    for order in orders:
        income += float(order.final_total)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=manager.Restaurant).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'count':orders.count(),
        'rest':rest,
        'orders':orders,
        'timeline':timeline,
        'income':income,
        'c_year':current_year
    }

    return render(request, "restaurantStuffs/customer_orders.html", context)


@login_required
def today_orders(request):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)
    current_year = date.today().year
    
    orders = Order.objects.filter(restaurant=manager.Restaurant, timestamp__date=date.today())
    timeline = 'Today : ' + str(date.today())

    income = 0.0
    for order in orders:
        income += float(order.final_total)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=manager.Restaurant).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'count':orders.count(),
        'rest':rest,
        'orders':orders,
        'timeline':timeline,
        'income':income,
        'c_year':current_year
    }

    return render(request, "restaurantStuffs/customer_orders.html", context)


@login_required
def this_month_orders(request):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)
    current_year = date.today().year
    
    monthList = ['none', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    orders = Order.objects.filter(restaurant=manager.Restaurant, timestamp__month=date.today().month)
    timeline = 'This month : ' + monthList[date.today().month] + ' ' + str(current_year)

    income = 0.0
    for order in orders:
        income += float(order.final_total)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=manager.Restaurant).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'count':orders.count(),
        'rest':rest,
        'orders':orders,
        'timeline':timeline,
        'income':income,
        'c_year':current_year
    }

    return render(request, "restaurantStuffs/customer_orders.html", context)


@login_required
def this_year_orders(request):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)
    current_year = date.today().year
    
    orders = Order.objects.filter(restaurant=manager.Restaurant)
    timeline = 'This year : ' + str(current_year)

    income = 0.0
    for order in orders:
        income += float(order.final_total)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=manager.Restaurant).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'count':orders.count(),
        'rest':rest,
        'orders':orders,
        'timeline':timeline,
        'income':income,
        'c_year':current_year
    }

    return render(request, "restaurantStuffs/customer_orders.html", context)


@login_required
def new_orders(request):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)
    current_year = date.today().year
    
    orders = Order.objects.filter(restaurant=manager.Restaurant, viewed=False)
    timeline = 'New'

    income = 0.0
    for order in orders:
        income += float(order.final_total)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=manager.Restaurant).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'count':orders.count(),
        'rest':rest,
        'orders':orders,
        'timeline':timeline,
        'income':income,
        'c_year':current_year
    }

    return render(request, "restaurantStuffs/customer_orders.html", context)


@login_required
def started_orders(request):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)
    current_year = date.today().year
    
    orders = Order.objects.filter(restaurant=manager.Restaurant, status='Started')
    timeline = 'Started'

    income = 0.0
    for order in orders:
        income += float(order.final_total)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=manager.Restaurant).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'count':orders.count(),
        'rest':rest,
        'orders':orders,
        'timeline':timeline,
        'income':income,
        'c_year':current_year
    }

    return render(request, "restaurantStuffs/customer_orders.html", context)


@login_required
def abandoned_orders(request):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)
    current_year = date.today().year
    
    orders = Order.objects.filter(restaurant=manager.Restaurant, status='Abandoned')
    timeline = 'All time'

    income = 0.0
    for order in orders:
        income += float(order.final_total)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=manager.Restaurant).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'count':orders.count(),
        'rest':rest,
        'orders':orders,
        'timeline':timeline,
        'income':income,
        'c_year':current_year
    }

    return render(request, "restaurantStuffs/customer_orders.html", context)


@login_required
def finished_orders(request):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)
    current_year = date.today().year
    
    orders = Order.objects.filter(restaurant=manager.Restaurant, status='Finished')
    timeline = 'All time'

    income = 0.0
    for order in orders:
        income += float(order.final_total)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=manager.Restaurant).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'count':orders.count(),
        'rest':rest,
        'orders':orders,
        'timeline':timeline,
        'income':income,
        'c_year':current_year
    }

    return render(request, "restaurantStuffs/customer_orders.html", context)


@login_required
def view_orders(request, id):
    order = Order.objects.get(id=id)
    
    if not order.viewed:
        order.viewed = True

    order.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def accept_orders(request, id):
    order = Order.objects.get(id=id)
    order.status = 'Started'
    order.save()

    messages.info(request, 'The order was accepted.', extra_tags='accept')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def reject_orders(request, id):
    order = Order.objects.get(id=id)
    order.status = 'Abandoned'
    order.save()

    messages.info(request, 'The order was rejected.', extra_tags='reject')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def finish_orders(request, id):
    order = Order.objects.get(id=id)
    order.status = 'Finished'
    order.save()

    messages.info(request, 'The order was finished.', extra_tags='accepts')
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_orders(request, id):
    Order.objects.get(id=id).delete()
    messages.info(request, 'The order was deleted.', extra_tags='delete')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def res_profile(request):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant
    
    menu_item = foodItem.objects.filter(Restaurant_name=rest, onTrend=False, Availability='Available')
    items = foodItem.objects.filter(Restaurant_name=rest, onTrend=True, Availability='Available')
    trend = False
    avail = False

    if items.exists():
        trend = True
    if menu_item.exists():
        avail = True

    rate = Review.objects.filter(rest=rest)
    count = rate.count()

    sum = 0
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0

    for r in rate:
        val = int(r.stars)

        if val == 1:
            one = one + 1
        if val == 2:
            two = two + 1
        if val == 3:
            three = three + 1
        if val == 4:
            four = four + 1
        if val == 5:
            five = five + 1

        sum = sum + val

    try:
        p_one = 100*one/count
    except ZeroDivisionError:
        p_one = 0

    try:
        p_two = 100*two/count
    except ZeroDivisionError:
        p_two = 0

    try:
        p_three = 100*three/count
    except ZeroDivisionError:
        p_three = 0

    try:
        p_four = 100*four/count
    except ZeroDivisionError:
        p_four = 0

    try:
        p_five = 100*five/count
    except ZeroDivisionError:
        p_five = 0

    try:
        avg = format(sum/count, '.1f')
    except:
        avg = 0

    review_count = 0
    for it in foodItem.objects.filter(Restaurant_name=rest):
        review_count += Comment.objects.filter(item=it).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()

    sidenav = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'rest':rest
    }

    rateContext = {
        'avg':avg,
        'count':count,
        'one':one,
        'two':two,
        'three':three,
        'four':four,
        'five':five,
        'per_one':p_one,
        'per_two':p_two,
        'per_three':p_three,
        'per_four':p_four,
        'per_five':p_five,
        'items':items,
        'rest':rest,
        'menu':menu_item,
        'trend':trend,
        'avail':avail
    }

    if restaurantList.objects.filter(Restaurant_name=manager.Restaurant.Restaurant_name, is_valid=True).exists():
        context = {'flag':True}
    else:
        context = {'flag':False}

    context.update(sidenav)
    context.update(rateContext)

    print(context)
    return render(request, "restaurantStuffs/restaurant_profile.html", context)


@login_required
def update_res_profile(request):
    manager = Manager.objects.get(user=request.user)
    rest = manager.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()

    if request.method == 'POST':
        form = RestaurantUpdateForm(request.POST, request.FILES, instance=rest)

        if form.is_valid():
            form.save()

            return redirect('res_profile')

    else:
        form = RestaurantUpdateForm(instance=rest)

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'rest':rest,
        'form':form
    }

    return render(request, "restaurantStuffs/update_res_profile.html", context)


def reviews(request):
    rest = Manager.objects.get(user=request.user).Restaurant
    reviews = Review.objects.filter(rest=rest)
    count = reviews.count()

    sum = 0
    one = 0
    two = 0
    three = 0
    four = 0
    five = 0

    for r in reviews:
        val = int(r.stars)

        if val == 1:
            one = one + 1
        if val == 2:
            two = two + 1
        if val == 3:
            three = three + 1
        if val == 4:
            four = four + 1
        if val == 5:
            five = five + 1

        sum = sum + val

    try:
        p_one = 100*one/count
    except ZeroDivisionError:
        p_one = 0

    try:
        p_two = 100*two/count
    except ZeroDivisionError:
        p_two = 0

    try:
        p_three = 100*three/count
    except ZeroDivisionError:
        p_three = 0

    try:
        p_four = 100*four/count
    except ZeroDivisionError:
        p_four = 0

    try:
        p_five = 100*five/count
    except ZeroDivisionError:
        p_five = 0

    try:
        avg = format(sum/count, '.1f')
    except:
        avg = 0

    items = foodItem.objects.filter(Restaurant_name=rest)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()

    context = {
        'rest':rest,
        'item':item,
        'avg':avg,
        'count':count,
        'one':one,
        'two':two,
        'three':three,
        'four':four,
        'five':five,
        'per_one':p_one,
        'per_two':p_two,
        'per_three':p_three,
        'per_four':p_four,
        'per_five':p_five,
        'item_count':item_count,
        'order_count':order_count
    }

    return render(request, 'restaurantStuffs/reviews.html', context)


def contact_us(request):
    try:
        user = Manager.objects.get(user=request.user)
    except TypeError:
        raise   Http404

    rest = user.Restaurant
    items = foodItem.objects.filter(Restaurant_name=rest)

    review_count = 0
    for item in items:
        review_count += Comment.objects.filter(item=item).count()

    item_count = foodItem.objects.filter(Restaurant_name=rest).count()
    order_count = Order.objects.filter(restaurant=rest).count()

    context = {
        'item_count':item_count,
        'order_count':order_count,
        'review_count':review_count,
        'rest':rest
    }
    
    return render(request, "restaurantStuffs/contact_us.html", context)
