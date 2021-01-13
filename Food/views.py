import stripe

from sslcommerz_lib import SSLCOMMERZ
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import auth, User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse
from django.views.generic import ListView, DetailView
from accounts.models import UserAddress, UserDefaultAddress, UserStripe
from stuffs.models import Comment, Review, Voucher
from .models import foodItem, restaurantList, Profile, UserProfile, Wishlist, Rating, Cart, CartItem, Manager, Order
from .utils import random_id_generator, transaction_id_generator
from accounts.forms import UserAddressForm
from Food.forms import UserForm, ProfileForm, UserUpdateForm, ProfileUpdateForm
from stuffs.forms import RestaurantForm

try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret = settings.STRIPE_SECRET_KEY
except Exception as e:
    # stripe_pub = 'pk_test_51I1VjSGJV6kACCf44SV40CG7DbrPXnqrxhMs1Kx7RyGyMaZaYKshmKtwDHdHxid7DHqLyawFyBCqpN7nXMJ4Vgs400Ejp71Llj'
    raise NotImplementedError(str(e))

stripe.api_key = stripe_secret

# Create your views here.
def index(request):
    items = foodItem.objects.filter(onTrend=True, Availability='Available')  #is_valid foods
    rests = restaurantList.objects.filter(is_valid=True)
    
    context = {'items':items, 'rests':rests}
    return render(request, "enduser/index.html", context)


def registration_page(request):
    if request.method == "POST":
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'An account already exists with this username.')
            return redirect('registration')

        elif User.objects.filter(email=email).exists():
            messages.info(request, 'This email has been already used to create another account.')
            return redirect('registration')

        elif len(password1) < 8:
            messages.info(request, 'The password is too short. Use at least 8 characters.')
            return redirect('registration')

        elif password1 == password2:
            if u_form.is_valid() and p_form.is_valid():
                user = u_form.save()
                p_form = p_form.save(commit=False)
                p_form.user = user
                p_form.save()
                messages.success(request, f'Registration complete! You may login!')
                return redirect('../login')

            else:
                messages.info(request, 'Use a strong password of at least 8 characters.')
                return redirect('registration')

        else:
            messages.info(request, 'Password is not matching.')
            return redirect('registration')

    else:
        u_form = UserForm(request.POST)
        p_form = ProfileForm(request.POST)

    return render(request, "registration.html", {'u_form': u_form, 'p_form': p_form})


def staff_registration(request):
    if request.method == "POST":
        u_form = UserForm(request.POST)
        # p_form = ProfileForm(request.POST)
        r_form = RestaurantForm(request.POST, request.FILES)

        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if User.objects.filter(username=username).exists():
            messages.info(request, 'An account already exists with this username.')
            return redirect('staff_registration')

        elif User.objects.filter(email=email).exists():
            messages.info(request, 'This email has been already used to create another account.')
            return redirect('staff_registration')

        elif len(password1) < 8:
            messages.info(request, 'The password is too short. Use at least 8 characters.')
            return redirect('staff_registration')

        elif password1 == password2:
            if u_form.is_valid() and r_form.is_valid():
                # user = r_form.save()
                # r_form = r_form.save(commit=False)
                # r_form.user = user
                user = u_form.save()
                rest = r_form.save()
                
                manager = Manager.objects.create(user=user, Restaurant=rest)
                manager.save()

                messages.success(request, f'Registration complete! You may login!')
                return redirect('login')

            else:
                messages.info(request, 'Use a strong password of at least 8 characters.')
                return redirect('staff_registration')

        else:
            messages.info(request, 'Password is not matching.')
            return redirect('staff_registration')

    else:
        u_form = UserForm(request.POST)
        r_form = RestaurantForm(request.POST, request.FILES)

    return render(request, "insert_restaurant.html", {'u_form': u_form, 'r_form': r_form})
 

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        try:
            userobject = User.objects.filter(username=User.objects.get(email=username)).first()
        except:
            userobject = User.objects.filter(username=username).first()

        try:
            id = userobject.id
        except:
            messages.info(request, 'Invalid Username/email account.')
            return redirect('../login')

        if Manager.objects.filter(user_id=id).exists() and User.objects.filter(username=username):
            is_manager = True
        else:
            is_manager = False

        try:
            user = auth.authenticate(username=User.objects.get(email=username), password=password)
        except:
            user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            # Session expires after 1 Hour automatically
            # request.session.set_expiry(3600)

            if is_manager:
                return redirect('../staff/')
            elif user.is_staff == True:
                return redirect('../super-admin')
            else:
                return redirect('../user/')

        else:
            messages.info(request, 'Password incorrect.')
            return redirect('../login')
    
    else:
        context = {}
        return render(request, "login.html", context)


@login_required
def logout(request):
    auth.logout(request)
    return redirect('../login')


def item_details(request, id):
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

    context = {
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
    }

    return render(request, "enduser/food_item.html", context)


@login_required
def user_profile(request):
    user = User.objects.filter(username=request.user.username).first()
    cur_user = UserProfile.objects.filter(user=user).first()

    try:
        address = UserDefaultAddress.objects.get(user=request.user)
    except:
        None
    
    context = {'user':user, 'cur_user':cur_user,'address':address}
    return render(request, "enduser/user_profile.html", context)


@login_required
def update_profile(request):
    user = User.objects.filter(username=request.user.username).first()
    cur_user = UserProfile.objects.filter(user=user).first()

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            return redirect('user_profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.userprofile)

    context = {'user':user, 'cur_user':cur_user, 'u_form':u_form, 'p_form':p_form}
    return render(request, "enduser/update_profile.html", context)


@login_required
def wishlist(request):
    lists = Wishlist.objects.filter(user=request.user)
    aval = False

    if lists.exists():
        aval = True

    paginator = Paginator(lists, per_page=3)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'lists':page_obj.object_list,
        'aval':aval,
        'paginator':paginator,
        'page_number':int(page_number)
    }

    return render(request, 'enduser/user_wishlist.html', context)


@login_required
def add_to_wishlist(request, id):
    item = get_object_or_404(foodItem, pk=id)

    if Wishlist.objects.filter(wished_item=item, user=request.user).exists():
        messages.info(request,'The item is already in your wishlist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    else:
        Wishlist.objects.get_or_create(wished_item=item, user=request.user)

        messages.info(request,'The item was added to your wishlist')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_from_wishlist(request, id):
    Wishlist.objects.filter(pk=id).delete()
    messages.info(request, 'The item is removed from your wishlist.', extra_tags='removed')

    return redirect('../wishlist')


@login_required
def clear_wishlist(request):
    Wishlist.objects.filter(user=request.user).delete()
    messages.info(request, 'Your wishlish is cleared.')

    return render(request, "enduser/user_wishlist.html")


@login_required
def order_history(request):
    order = Order.objects.filter(user=request.user)

    context = {'orders':order}
    return render(request, 'enduser/order_history.html', context)


@login_required
def order_cart(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None

    if the_id:
        new_total = 0.00

        for item in cart.cartitem_set.all():
            item.line_total = float(item.product.Price) * item.quantity
            new_total += item.line_total
            item.save()
        
        request.session['items_total'] = cart.cartitem_set.count()
        cart.sub_total = new_total
        cart.final_total = new_total - float(cart.tax_total)
        cart.save()

        context = {'cart':cart}
    else:
        context = {'empty':True}
 
    return render(request, "enduser/order_cart.html", context)


@login_required
def remove_from_order_cart(request, id):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        return HttpResponseRedirect(reverse('order_cart'))

    cartitem = CartItem.objects.get(id=id)
    cartitem.cart = None
    cartitem.save()
    messages.info(request, 'The item was removed from your cart.')
    
    return HttpResponseRedirect(reverse('order_cart'))


@login_required
def add_to_order_cart(request, id):
    try:
        qty = request.GET.get('qty')
        comment = request.GET.get('comment')
        update_qty = True

    except:
        qty = None
        update_qty = False

    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)

    try:
        item = CartItem.objects.filter(cart=cart).first()
        cur_rest = item.product.Restaurant_name
    except:
        cur_rest = None

    try:
        product = foodItem.objects.get(pk=id)
    except foodItem.DoesNotExist:
        pass
    except:
        pass

    try:
        rest = product.Restaurant_name
    except:
        rest = None

    if cur_rest is not None:
        if rest == cur_rest:
            pass
        else:
            messages.info(request, "Sorry! you can't add item to cart from different restaurant unless you proceed or delete the previous cart.", extra_tags='violation')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        message = 'Your cart was updated.'
    except:
        cart_item = CartItem.objects.create(cart=cart, product=product)
        message = 'The item was added to your cart.'

    if update_qty and qty:
        if int(qty) == 0:
            cart_item.delete()
        else:
            cart_item.quantity = cart_item.quantity + int(qty)
            cart_item.comment = comment
            cart_item.save()
            messages.info(request, message, extra_tags='added')
    else:
        pass

    request.session['items_total'] = cart.cartitem_set.count()
    cart.restaurant = product.Restaurant_name
    cart.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_order_cart(request, id):
    try:
        qty = request.GET.get('qty')
        comment = request.GET.get('comment')
        update_qty = True

    except:
        qty = None
        update_qty = False

    try:
        the_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id

    cart = Cart.objects.get(id=the_id)

    try:
        product = foodItem.objects.get(pk=id)
    except foodItem.DoesNotExist:
        pass
    except:
        pass

    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        message = 'Your cart was updated.'
    except:
        cart_item = CartItem.objects.create(cart=cart, product=product)
        message = 'The item was added to your cart.'

    if update_qty and qty:
        if int(qty) == 0:
            cart_item.delete()
        else:
            cart_item.quantity = int(qty)
            cart_item.comment = comment
            cart_item.save()
            messages.info(request, message, extra_tags='added')
    else:
        pass

    request.session['items_total'] = cart.cartitem_set.count()
    cart.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_order_cart(request):
    del request.session['cart_id']
    del request.session['items_total']
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def apply_voucher(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None

    if request.method == 'POST':
        voucher_id = request.POST.get('voucher')
        
        try:
            voucher = Voucher.objects.get(card_id=voucher_id)
        except:
            voucher = None

        if voucher is not None:
            cart.tax_total = float(cart.sub_total) * float(voucher.discount/100)
            cart.save()
        else:
            messages.warning(request, 'Invalid Voucher Code')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def remove_voucher(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None

    if the_id is not None:
        cart.tax_total = 0
        cart.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def checkout(request):    
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse("order_cart"))

    try:
        new_order = Order.objects.get(cart=cart)
        
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.restaurant = cart.restaurant
        new_order.user = request.user
        new_order.order_id = random_id_generator()
        new_order.save()
    except:
        new_order = None
        messages.info(request, 'ERROR 404: The page you are looking for is not available')
        return HttpResponseRedirect(reverse("order_cart"))

    if new_order is not None:
        new_order.sub_total = cart.sub_total
        new_order.tax_total = cart.tax_total
        new_order.final_total = cart.final_total
        final_amount = cart.final_total
        new_order.save()

    try:
        address_added = request.GET.get("address_added")
    except:
        address_added = None

    if address_added is None:
        address_form = UserAddressForm()
    else:
        address_form = None

    current_addresses = UserAddress.objects.filter(user=request.user)

    if request.method == "POST":
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
        except:
            customer = None

        if customer is not None:
            card = stripe.Customer.create_source(customer.id, source="tok_amex")

            charge = stripe.Charge.create(
                amount = int(final_amount*100),
                currency = 'bdt',
                card = card,
                customer = customer,
            )

            if charge["captured"]:
                new_order.charged = True
                new_order.save()

    if new_order.charged and new_order.address is not None:
        # new_order.status == 'Finished' # Should be single equal sign
        new_order.transaction_id = transaction_id_generator()
        new_order.save()
        del request.session['cart_id']
        del request.session['items_total']

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return HttpResponseRedirect(reverse("order_confirm"))

    context = {
        'order':new_order,
        'address_form':address_form,
        'current_addresses':current_addresses,
        'stripe_pub':stripe_pub
    }

    return render(request, "enduser/order_checkout.html", context)


def add_user_address(request):
    try:
        next_page = request.GET.get("next")
    except:
        next_page = None

    if request.method == 'POST':
        address_form = UserAddressForm(request.POST)

        try:
            the_id = request.session['cart_id']
            cart = Cart.objects.get(id=the_id)
            order = Order.objects.get(cart=cart)
        except:
            the_id = None
            return HttpResponseRedirect(reverse("order_cart"))

        print('Order is ', order)
        if address_form.is_valid():
            new_address = address_form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            order.address = new_address
            order.save()

            is_default = address_form.cleaned_data['setDefault']

            if is_default:
                default_address, created = UserDefaultAddress.objects.get_or_create(user=request.user)

                if created:
                    default_address.shipping = new_address
                    default_address.save()

            if next_page is not None:
                messages.info(request, 'Thank You! Your orders will be delivered soon.')
                return HttpResponseRedirect(reverse(str(next_page))+"?address-added=True")
    else:
        raise Http404


@login_required
def order_confirm(request):
    context = {}
    return render(request, "enduser/order_confirm.html", context)


def res_menu(request, id):
    rests = restaurantList.objects.filter(pk=id)
    menu_item = foodItem.objects.filter(Restaurant_name=id, onTrend=False, Availability='Available')
    items = foodItem.objects.filter(Restaurant_name=id, onTrend=True, Availability='Available')
    trend = False
    avail = False

    rate = Review.objects.filter(rest=id)
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

    if items.exists():
        trend = True
    if menu_item.exists():
        avail = True

    context = {
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
        'rests':rests,
        'menu':menu_item,
        'trend':trend,
        'avail':avail
    }

    return render(request, "enduser/Restaurant_menu.html", context)


def search(request):
    query = request.GET['query']
    rav = False
    mav = False

    food_rslts = foodItem.objects.filter(Item_name__icontains=query, Availability='Available')
    rest_rslts = restaurantList.objects.filter(Restaurant_name__icontains=query)
    m_count = food_rslts.count()
    r_count = rest_rslts.count()

    if food_rslts.exists():
        mav = True
    if rest_rslts.exists():
        rav = True

    context = {'food_rslts':food_rslts, 'rest_rslts':rest_rslts, 'mav':mav, 'rav':rav, 'm_count':m_count, 'r_count':r_count}
    return render(request, "enduser/search.html", context)


def search_price_range(request):
    min_price = request.GET.get('min')
    max_price = request.GET.get('max')

    if min_price == '':
        min_price = 0
    if max_price == '':
        max_price = 99999999

    if int(max_price) < int(min_price):
        messages.info(request, 'Invalid price range')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    food_rslts = foodItem.objects.filter(Price__range=(min_price, max_price), Availability='Available')

    f_count = food_rslts.count()
    mav = food_rslts.exists()
    filter = True

    context = {'food_rslts':food_rslts, 'f_count':f_count, 'av':mav, 'filter':filter}
    return render(request, "enduser/search.html", context)


def contact_us(request):
    context = {}
    return render(request, "enduser/contact_us.html", context)


@login_required
def rate_item(request, id):
    if request.method == 'POST':
        star = request.POST.get('rating')
        item = foodItem.objects.get(id=id)

        try:
            rate = Rating.objects.get(item=item, user=request.user)
            rate.stars = star
            rate.save()
            message = 'Your Review was Updated.'

        except Rating.DoesNotExist:
            Rating.objects.create(item=item, stars=star, user=request.user)
            message = 'Thanks for your review.'

        except:
            message = 'Something Went Wrong.'

        messages.success(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def add_comment(request, id):
    if request.method == 'POST':
        cmnt = request.POST.get('comment')
        item = foodItem.objects.get(id=id)

        Comment.objects.create(user=request.user, text=cmnt, item=item)

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def edit_comment(request, id):
    if request.method == 'POST':
        text = request.POST.get('comment')

        comment = Comment.objects.get(id=id)
        comment.text = text
        comment.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_comment(request, id):
    Comment.objects.get(id=id).delete()
    messages.info(request, 'Your Comment was deleted')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def review(request, id):
    if request.method == 'POST':
        star = request.POST.get('star')
        text = request.POST.get('text')
        rest = restaurantList.objects.get(id=id)

        if star != '':
            try:
                review = Review.objects.get(user=request.user, rest=rest)
            except:
                review = Review.objects.create(user=request.user, rest=rest)

            review.text = text
            review.stars = star
            review.save()
            messages.info(request, 'Thanks for your review')
        else:
            messages.info(request, 'Please select a star to review')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete_review(request, id):
    Review.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def payment(request, id):
    if request.method == 'POST':
        settings = { 'store_id': 'linb15fed6d17c8b6e', 'store_pass': 'linb15fed6d17c8b6e@ssl', 'issandbox': True }
        sslcommez = SSLCOMMERZ(settings)
        post_body = {}
        post_body['total_amount'] = 100.26
        post_body['currency'] = "BDT" 
        post_body['tran_id'] = "12345"
        post_body['success_url'] = "your success url"
        post_body['fail_url'] = "your fail url"
        post_body['cancel_url'] = "your cancel url"
        post_body['emi_option'] = 0
        post_body['cus_name'] = "test"
        post_body['cus_email'] = "test@test.com"
        post_body['cus_phone'] = "01700000000"
        post_body['cus_add1'] = "customer address"
        post_body['cus_city'] = "Dhaka"
        post_body['cus_country'] = "Bangladesh"
        post_body['shipping_method'] = "NO"
        post_body['multi_card_name'] = ""
        post_body['num_of_item'] = 1
        post_body['product_name'] = "Test"
        post_body['product_category'] = "Test Category"
        post_body['product_profile'] = "general"

        response = sslcommez.createSession(post_body)
        payment_url = response['GatewayPageURL']
        
        return redirect(payment_url)


class res_list(ListView):
    model = restaurantList
    template_name = "enduser/Restaurant_list.html"
