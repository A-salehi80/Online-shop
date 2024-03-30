from django.shortcuts import render
from .models import Blog, Colors, ChildCategory
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from usermanager.models import Profile
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404
from .models import Item, Cart, CartItem, Category, Main_Page, Large_banner


def index(request):
    blog = Blog.objects.all()
    categories = Category.objects.all()[:6]
    category_menu = Category.objects.all()
    main_page = Main_Page.objects.all()[:1].get()
    large_banner = Large_banner.objects.all()
    item_list = Item.objects.all()
    item_list_latest = Item.objects.all().order_by('ID_NO')
    total_price = 0
    total_no = 0

    if request.user.is_authenticated:
        item_list_latest = Item.objects.all().order_by('ID_NO')
        item_list = Item.objects.all()
        category_menu = Category.objects.all()
        prof = request.user.profile
        cart = prof.cart.cartitem_set.all()
        cart_count = cart.count()
        main_page = Main_Page.objects.all()[:1].get()
        large_banner = Large_banner.objects.all()
        user_cart = request.user.profile.cart.cartitem_set.all()
        for item in cart:
            total_no += 1
            item_price = item.item.price * item.quantity
            total_price += item_price

        context = {
            'blog': blog,
            'cart_count': cart_count,
            'categories': categories,
            'main_page': main_page,
            'large_banner': large_banner,
            'cart': cart,
            'item_list': item_list,
            'item_list_latest': item_list_latest,
            'total_price': total_price,
            'total_no': total_no,
            'user_cart': user_cart,
            'category_menu':category_menu

        }
        return render(request, 'index.html', context)

    context = {
        'blog': blog,
        'categories': categories,
        'main_page': main_page,
        'large_banner': large_banner,
        'item_list': item_list,
        'item_list_latest': item_list_latest,
        'category_menu': category_menu,

    }

    return render(request, 'index.html', context)


def product_detail(request, product_id):
    product = Item.objects.get(id=product_id)
    tags = product.tags.get_queryset()
    product_related = Item.objects.filter(tags__in=tags).exclude(id=product_id).distinct()
    prof = request.user.profile
    cart = prof.cart.cartitem_set.all()
    total_price = 0
    total_no = 0
    cart_count = cart.count()
    user_cart = request.user.profile.cart.cartitem_set.all()

    for item in cart:
        total_no += 1
        item_price = item.item.price * item.quantity
        total_price += item_price

    context = {
        'product': product,
        'product_related': product_related,
        'total_price': total_price,
        'total_no': total_no,
        'cart_count': cart_count,
        'user_cart':user_cart
    }
    return render(request, 'product-detail.html', context)


def cart_view(request):
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
        'total_no': total_no
    }
    return render(request, 'Cart.html', context)


@csrf_exempt
def decrease_cart_item_quantity(request, cart_item_id, decrease_amount):
    # Retrieve the CartItem object based on cart_item_id
    try:
        cart_item = CartItem.objects.get(pk=cart_item_id)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'محصول یافت نشد'}, status=404)

    # Ensure that decrease_amount is a positive integer
    decrease_amount = int(decrease_amount)
    cart_item.quantity -= decrease_amount
    if cart_item.quantity < 0:
        cart_item.quantity = 0

        cart_item.save(update_fields=['quantity'])
    else:

        # Save the updated cart item
        cart_item.save(update_fields=['quantity'])
    if cart_item.quantity == 0:
        cart_item.delete()

    return JsonResponse({'success': 'با موفقیت انجام شد'})


@csrf_exempt
def increase_cart_item_quantity(request, cart_item_id, increase_amount):
    # Retrieve the CartItem object based on cart_item_id
    try:
        cart_item = CartItem.objects.get(pk=cart_item_id)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'محصول یافت نشد'}, status=404)

    # Ensure that decrease_amount is a positive integer
    increase_amount = int(increase_amount)
    cart_item.quantity += increase_amount
    if cart_item.quantity > 10:
        cart_item.quantity = 10

        cart_item.save(update_fields=['quantity'])
    else:

        # Save the updated cart item
        cart_item.save(update_fields=['quantity'])

    return JsonResponse({'success': 'با موفقیت انجام شد'})


@csrf_exempt
def delete_item(request, cart_item_id):

    try:
        cart_item = CartItem.objects.get(pk=cart_item_id)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'محصول یافت نشد'}, status=404)

    cart_item.delete()
    return JsonResponse({'success': 'با موفقیت انجام شد'})


@csrf_exempt
def delete_all(request, cart_item_id):

    try:
        cart_item = CartItem.objects.get(pk=cart_item_id)
    except CartItem.DoesNotExist:
        return JsonResponse({'error': 'محصول یافت نشد'}, status=404)

    cart_item.delete()
    return JsonResponse({'success': 'با موفقیت انجام شد'})


@csrf_exempt
def add_to_cart(request, product_id, selectedColor):
    # Retrieve the product and color objects
    product = get_object_or_404(Item, pk=product_id)
    color = get_object_or_404(Colors, id=selectedColor)

    # Get or create the user's cart
    cart, _ = Cart.objects.get_or_create(profile=request.user.profile)

    # Check if the product with the selected color already exists in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=product, color=color)

    # If the item already exists, increase its quantity
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return JsonResponse({'message': 'با موفقیت انجام شد'})


def childcategory_finder(request, child_id):
    childcategory = ChildCategory.objects.filter(id=child_id).get()
    items = Item.objects.filter(child_cat=childcategory)
    context = {
        'items': items
    }
    return render(request, 'shop.html', context)


def categoryfinder(request, category_id):
    category = Category.objects.filter(id=category_id).get()
    items = Item.objects.filter(category=category)
    context = {
        'items': items
    }

    return render(request, 'shop.html', context)
