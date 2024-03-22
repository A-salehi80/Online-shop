from django.shortcuts import render
from .models import Blog
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from usermanager.models import Profile
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404
from .models import Item, Cart, CartItem, Category, Main_Page, Large_banner


def index(request):
    blog = Blog.objects.all()
    categories = Category.objects.all()[:5]
    main_page = Main_Page.objects.all()[:1].get()
    large_banner = Large_banner.objects.all()
    if request.user.is_authenticated:
        prof = request.user.profile
        cart = prof.cart.cartitem_set.all()
        cart_count = cart.count()
        main_page = Main_Page.objects.all()[:1].get()
        large_banner = Large_banner.objects.all()

        context = {
           'blog': blog,
           'cart_count': cart_count,
           'categories': categories,
            'main_page':main_page,
            'large_banner':large_banner,
            'cart':cart

        }
        return render(request, 'index.html', context)

    context = {
        'blog': blog,
        'categories': categories,
        'main_page': main_page,
        'large_banner':large_banner,

    }

    return render(request, 'index.html', context)


def add_to_cart(request, product_id):
    product = get_object_or_404(Item, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')


def product_detail(request, product_id):
    product = Item.objects.get(id=product_id)
    context={
        'product': product}
    return render(request, 'product-detail.html', context)


def cart_total_price(request):
    cart = request.user.profile.cart
    total_price = 0
    for item in cart.cartitem_set.all():
        item_price = item.item.price * item.quantity
        total_price += item_price
    return total_price


def Cart_view(request):
    cart = request.user.profile.cart
    cart_price = cart.cartitem_set.aggregate(total_price=Sum('item__price'))['total_price']
    user_cart = request.user.profile.cart.cartitem_set.all()
    cart_count = cart.cartitem_set.all().count()
    total_price = 0
    total_no = 0
    for item in cart.cartitem_set.all():
        total_no += 1
        item_price = item.item.price * item.quantity
        total_price += item_price

    context = {
        'user_cart': user_cart,
        'cart_count': cart_count,
        'cart_price': cart_price,
        'total_price': total_price,
        'total_no':total_no
    }
    return render(request, 'Cart.html', context)

@csrf_exempt
def decrease_cart_item_quantity(request, cart_item_id, decrease_amount):
    # Retrieve the CartItem object based on cart_item_id
    try:
        cart_item = CartItem.objects.get(pk=cart_item_id)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'CartItem not found'}, status=404)

    # Ensure that decrease_amount is a positive integer
    decrease_amount = int(decrease_amount)
    cart_item.quantity -= decrease_amount
    if cart_item.quantity < 0:
        cart_item.quantity = 0
        cart_item.save(update_fields=['quantity'])

    # Save the updated cart item
    cart_item.save(update_fields=['quantity'])

    return JsonResponse({'success': 'Quantity decreased successfully'})
