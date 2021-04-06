from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem, Order, Customer, OrderItem_Gifts, OrderItem_bulk, Review, OrderItem_stitching
from cart.cart import Cart
from .tasks import order_created, order_created_admin, free_service, free_service_11
from shop.models import ProductSize, Product
from gifting.models import ProductGifting, Variants
from django.http import HttpResponse



def review_form(request, star=None):

    if request.method == 'POST':

         review = Review()
         review.name = request.POST.get('name')
         review.review = request.POST.get('review')
         review.stars = star
         review.save()
         return redirect('homepage')


    else:
        stars = range(1,5)
        return render(request,'review-form.html', {'stars':stars})




def bulk_orders(request, id, slug):

    return render(request,'orders/order/bulk_orders.html', {'id':id, 'slug':slug})


def order_create(request):
    cart = Cart(request)


    if request.method == 'POST':
        referral_code = None
        message = None
        message1= None
        service = 'shop'
        cust_obj = None


        order = Order()


        customer = Customer()
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cust = Customer.objects.filter(phone=phone, email=email)
        if cust:
            cust_obj = get_object_or_404(Customer, phone=phone, email=email)
            customer = None

        if not cust:

            customer.first_name = request.POST.get('fname')
            customer.last_name = request.POST.get('lname')
            customer.email = request.POST.get('email')
            customer.phone = request.POST.get('phone')
            order.customer = customer

        else:
            order.customer = cust_obj
        order.address = request.POST.get('address')
        order.postal_code = request.POST.get('postal')
        order.city = request.POST.get('city')
        order.preferred_contact = request.POST.get('contact-radio')


        referral_code = request.POST.get('referral-code')



        if referral_code == "":

            pass
        elif not customer:
            if cust_obj.reffered_by_id and referral_code:
                return HttpResponse(
                    "Warning: You have already used a referral code to become our customer. Please omit this field!!!")

        if referral_code == "":
            pass
        elif customer or cust_obj:

            referrer = Customer.objects.filter(referral_code=referral_code)
            if not referrer and referral_code:
                return HttpResponse("Warning: Wrong referral code provided!!!")
            else:
                phone = referrer.values()[0]['phone']

            if customer is None:
                if cust_obj.phone == phone:
                    return HttpResponse("Warning: Please do not use your own referral code!!!")

            elif not referrer:
                return HttpResponse("Warning: Invalid referral code!!! Please fill in a valid code or omit the option. ")
            else:
                if customer:
                    referrer = Customer.objects.get(referral_code=referral_code)
                    referrer_obj = get_object_or_404(Customer, phone=referrer.phone, email=referrer.email)
                    customer.reffered_by = referrer_obj
                elif cust_obj:
                    referrer = Customer.objects.get(referral_code=referral_code)
                    referrer_obj = get_object_or_404(Customer, phone=referrer.phone, email=referrer.email)
                    cust_obj.reffered_by = referrer_obj
                order.referral_code = referral_code
                count = referrer.refer_count
                count += 1
                referrer_obj.refer_count = count
                referrer_obj.save()

        if cust:
            if cust_obj.refer_count > 5:
                no_free_service = cust_obj.refer_count % 5
                free_service.delay(order.id, cust_obj.id)
                message = "Congratulations! You have won {} free service on this order for referring 5 friends." \
                          " Keep referring more to win more. Happy shopping!".format(no_free_service)

            count = cust_obj.first_ten_count

            if count == 11:
                message = ""

            elif count == 10:
                message1 = "Congrats! " \
                          "You've maybe won a free service for this transaction! Our executive will let you know more. " \
                          "The excitement doesn't end here, refer more friends to gain free services. Happy shopping!"
                free_service_11.delay(order.id)
                count += 1
                cust_obj.first_ten_count = count

            elif count == 9:
                message1 = "Congrats! " \
                          "You maybe eligible for a free service on the next transaction if you've transacted more than ₹15,000 for the first 10 transactions with us!" \
                          " Welcome to your family! The excitement doesn't end here,  refer more friends to gain free services. Happy shopping!"
                count += 1
                cust_obj.first_ten_count = count
                cust_obj.save()
            elif count < 11:
                count += 1
                cust_obj.first_ten_count = count
            cust_obj.save()
            referral_code = cust_obj.referral_code


        else:

            customer.first_ten_count = 1
            customer.save()
            referral_code = customer.referral_code

        order.save()


        for item in cart:
            product = item['product']
            if item['sizeS']:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         priceS=item['priceS'],
                                         quantityS=item['quantityS'],
                                         priceM=item['priceM'],
                                         quantityM=item['quantityM'],
                                         priceL=item['priceL'],
                                         quantityL=item['quantityL'],
                                         priceXL=item['priceXL'],
                                         quantityXL=item['quantityXL'],
                                         priceXXL=item['priceXXL'],
                                         quantityXXL=item['quantityXXL'] )

                quantityS = item['quantityS']
                product_size = ProductSize.objects.filter(product=product)
                size_difference = product_size.values()[0]['stock'] - quantityS
                for product_i in product_size:
                    if product_i.size == 'S':
                        product_i.stock = size_difference
                    if product_i.stock == 0:
                        product_i.available = False
                    product_i.save()




            elif item['sizeM']:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         priceS=item['priceS'],
                                         quantityS=item['quantityS'],
                                         priceM=item['priceM'],
                                         quantityM=item['quantityM'],
                                         priceL=item['priceL'],
                                         quantityL=item['quantityL'],
                                         priceXL=item['priceXL'],
                                         quantityXL=item['quantityXL'],
                                         priceXXL=item['priceXXL'],
                                         quantityXXL=item['quantityXXL'])

                quantityM = item['quantityM']

                product_size = ProductSize.objects.filter(product=product)
                size_difference = product_size.values()[1]['stock'] - quantityM
                for product_i in product_size:
                    if product_i.size == 'M':
                        product_i.stock = size_difference
                    if product_i.stock == 0:
                        product_i.available = False
                    product_i.save()


            elif item['sizeL']:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         priceS=item['priceS'],
                                         quantityS=item['quantityS'],
                                         priceM=item['priceM'],
                                         quantityM=item['quantityM'],
                                         priceL=item['priceL'],
                                         quantityL=item['quantityL'],
                                         priceXL=item['priceXL'],
                                         quantityXL=item['quantityXL'],
                                         priceXXL=item['priceXXL'],
                                         quantityXXL=item['quantityXXL'])

                quantityL = item['quantityL']

                product_size = ProductSize.objects.filter(product=product)
                size_difference = product_size.values()[2]['stock'] - quantityL
                for product_i in product_size:
                    if product_i.size == 'L':
                        product_i.stock = size_difference
                    if product_i.stock == 0:
                        product_i.available = False
                    product_i.save()


            elif item['sizeXL']:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         priceS=item['priceS'],
                                         quantityS=item['quantityS'],
                                         priceM=item['priceM'],
                                         quantityM=item['quantityM'],
                                         priceL=item['priceL'],
                                         quantityL=item['quantityL'],
                                         priceXL=item['priceXL'],
                                         quantityXL=item['quantityXL'],
                                         priceXXL=item['priceXXL'],
                                         quantityXXL=item['quantityXXL'])

                quantityXL = item['quantityXL']

                product_size = ProductSize.objects.filter(product=product)
                size_difference = product_size.values()[3]['stock'] - quantityXL
                for product_i in product_size:
                    if product_i.size == 'XL':
                        product_i.stock = size_difference
                    if product_i.stock == 0:
                        product_i.available = False
                    product_i.save()


            elif item['sizeXXL']:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         priceS=item['priceS'],
                                         quantityS=item['quantityS'],
                                         priceM=item['priceM'],
                                         quantityM=item['quantityM'],
                                         priceL=item['priceL'],
                                         quantityL=item['quantityL'],
                                         priceXL=item['priceXL'],
                                         quantityXL=item['quantityXL'],
                                         priceXXL=item['priceXXL'],
                                         quantityXXL=item['quantityXXL'])

                quantityXXL = item['quantityXXL']

                product_size = ProductSize.objects.filter(product=product)
                size_difference = product_size.values()[4]['stock'] - quantityXXL
                for product_i in product_size:
                    if product_i.size == 'XXL':
                        product_i.stock = size_difference
                    if product_i.stock == 0:
                        product_i.available = False
                    product_i.save()

            # clear the cart
        cart.clear()



        # launch asynchronous task
        order_created.delay(order.id)


        # launch asynchronous task



        return render(request, 'orders/order/created.html',
                      {'order': order, 'message': message, 'message1':message1, 'referral_code': referral_code, 'service':service})

    else:
        return render(request, 'orders/order/create.html', {'cart': cart})





def order_create_gifting(request, id=None, slug=None, variant=None):



    if request.method == 'POST':
        referral_code = None
        message = None
        message1 = None;
        service = 'gifting'
        cust_obj = None



        order = Order()
        if variant and id:
            product = OrderItem_Gifts()
            global variant_product
            variant_product = get_object_or_404(Variants, id=id, slug=slug)

            product.product = variant_product.product
            product.variant = variant_product


        elif not variant and id:
            product = OrderItem_Gifts()
            gift_product = get_object_or_404(ProductGifting, id=id, slug=slug)
            product.product = gift_product
            product.variant = None


        customer = Customer()
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cust = Customer.objects.filter(phone=phone, email=email)
        if cust:
            cust_obj = get_object_or_404(Customer, phone=phone, email=email)
            customer = None

        if not cust:

            customer.first_name = request.POST.get('fname')
            customer.last_name = request.POST.get('lname')
            customer.email = request.POST.get('email')
            customer.phone = request.POST.get('phone')

            order.customer = customer

        else:
            order.customer = cust_obj
        order.address = request.POST.get('address')
        order.postal_code = request.POST.get('postal')
        order.city = request.POST.get('city')
        order.preferred_contact = request.POST.get('contact-radio')



        product.order = order
        product.description = request.POST.get('custom-order')
        if 'image' in request.FILES:
           product.image = request.FILES['image']
        product.expected_by = request.POST.get('expected-by')

        referral_code = request.POST.get('referral-code')




        if referral_code == "":

            pass

        elif not customer:

            if cust_obj.reffered_by_id and referral_code:

               return HttpResponse("Warning: You have already used a referral code to become our customer. Please omit this field!!!")

        if referral_code == "":
            pass
        elif customer or cust_obj:

            referrer = Customer.objects.filter(referral_code=referral_code)

            if not referrer and referral_code:
                return HttpResponse("Warning: Wrong referral code provided!!!")
            else:
                phone = referrer.values()[0]['phone']

            if customer is None:


                if cust_obj.phone == phone:

                    return HttpResponse("Warning: Please do not use your own referral code!!!")

            elif not referrer:
                return HttpResponse(
                    "Warning: Invalid referral code!!! Please fill in a valid code or omit the option. ")
            else:
                if customer:
                    referrer = Customer.objects.get(referral_code=referral_code)
                    referrer_obj = get_object_or_404(Customer, phone=referrer.phone, email=referrer.email)
                    customer.reffered_by = referrer_obj
                elif cust_obj:
                    referrer = Customer.objects.get(referral_code=referral_code)
                    referrer_obj = get_object_or_404(Customer, phone=referrer.phone, email=referrer.email)
                    cust_obj.reffered_by = referrer_obj
                order.referral_code = referral_code

                count = referrer.refer_count
                count += 1
                referrer_obj.refer_count = count
                referrer_obj.save()


        if cust:
            if cust_obj.refer_count > 5:
                no_free_service = cust_obj.refer_count % 5

                free_service.delay(order.id, cust_obj.id)
                message = "Congratulations! You have won {} free service on this order for referring 5 friends." \
                          " Keep referring more to win more. Happy shopping!".format(no_free_service)



            count = cust_obj.first_ten_count

            if count == 11:
                message = ""

            elif count == 10:
                message1 = "Congrats! " \
                          "You've maybe won a free service for this transaction! Our executive will let you know more. " \
                          "The excitement doesn't end here, refer more friends to gain free services. Happy shopping!"
                free_service_11.delay(order.id)
                count += 1
                cust_obj.first_ten_count = count

            elif count == 9:
                message1 = "Congrats! " \
                          "You maybe eligible for a free service on the next transaction if you've transacted more than ₹15,000 for the first 10 transactions with us!" \
                          " Welcome to your family! The excitement doesn't end here,  refer more friends to gain free services. Happy shopping!"
                count += 1
                cust_obj.first_ten_count = count
                cust_obj.save()
            elif count < 11:
                count += 1
                cust_obj.first_ten_count = count

            cust_obj.save()
            referral_code = cust_obj.referral_code
        else:

            customer.first_ten_count = 1
            customer.save()
            referral_code = customer.referral_code

        order.save()
        product.save()


        # launch asynchronous task
        order_created.delay(order.id)

        # launch asynchronous task
        order_created_admin.delay(order.id)

        return render(request, 'orders/order/created.html',
                      {'order': order, 'message': message, 'message1':message1, 'referral_code': referral_code, 'service':service})

    else:
         return render(request, 'orders/order/create_gifting.html')




def order_create_bulk(request, id, slug):



    if request.method == 'POST':
        referral_code = None
        message = None
        message1 = None
        service = 'shop'
        cust_obj = None

        order = Order()
        customer = Customer()
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cust = Customer.objects.filter(phone=phone, email=email)
        if cust:
            cust_obj = get_object_or_404(Customer, phone=phone, email=email)
            customer = None

        if not cust:

            customer.first_name = request.POST.get('fname')
            customer.last_name = request.POST.get('lname')
            customer.email = request.POST.get('email')
            customer.phone = request.POST.get('phone')
            order.customer = customer

        else:
            order.customer = cust_obj

        order.address = request.POST.get('address')
        order.postal_code = request.POST.get('postal')
        order.city = request.POST.get('city')
        order.preferred_contact = request.POST.get('contact-radio')



        product = OrderItem_bulk()
        com = get_object_or_404(Product, id=id, slug=slug)
        product.product = com
        product.order = order
        product.description = request.POST.get('custom-order')
        product.expected_by = request.POST.get('expected-by')
        product.quantity = request.POST.get('quantity')

        referral_code = request.POST.get('referral-code')

        if referral_code == "":

            pass

        elif not customer:

            if cust_obj.reffered_by_id and referral_code:

               return HttpResponse("Warning: You have already used a referral code to become our customer. Please omit this field!!!")

        if referral_code == "":
            pass
        elif customer or cust_obj:

            referrer = Customer.objects.filter(referral_code=referral_code)

            if not referrer and referral_code:
                return HttpResponse("Warning: Wrong referral code provided!!!")
            else:
                phone = referrer.values()[0]['phone']

            if customer is None:


                if cust_obj.phone == phone:

                    return HttpResponse("Warning: Please do not use your own referral code!!!")

            elif not referrer:
                return HttpResponse(
                    "Warning: Invalid referral code!!! Please fill in a valid code or omit the option. ")
            else:
                if customer:
                    referrer = Customer.objects.get(referral_code=referral_code)
                    referrer_obj = get_object_or_404(Customer, phone=referrer.phone, email=referrer.email)
                    customer.reffered_by = referrer_obj
                elif cust_obj:
                    referrer = Customer.objects.get(referral_code=referral_code)
                    referrer_obj = get_object_or_404(Customer, phone=referrer.phone, email=referrer.email)
                    cust_obj.reffered_by = referrer_obj
                order.referral_code = referral_code

                count = referrer.refer_count
                count += 1
                referrer_obj.refer_count = count
                referrer_obj.save()


        if cust:
            if cust_obj.refer_count > 5:
                no_free_service = cust_obj.refer_count % 5

                free_service.delay(order.id, cust_obj.id)
                message = "Congratulations! You have won {} free service on this order for referring 5 friends." \
                          " Keep referring more to win more. Happy shopping!".format(no_free_service)



            count = cust_obj.first_ten_count

            if count == 11:
                message = ""

            elif count == 10:
                message1 = "Congrats! " \
                          "You've maybe won a free service for this transaction! Our executive will let you know more. " \
                          "The excitement doesn't end here, refer more friends to gain free services. Happy shopping!"
                free_service_11.delay(order.id)
                count += 1
                cust_obj.first_ten_count = count

            elif count == 9:
                message1 = "Congrats! " \
                          "You maybe eligible for a free service on the next transaction if you've transacted more than ₹15,000 for the first 10 transactions with us!" \
                          " Welcome to your family! The excitement doesn't end here,  refer more friends to gain free services. Happy shopping!"
                count += 1
                cust_obj.first_ten_count = count
                cust_obj.save()
            elif count < 11:
                count += 1
                cust_obj.first_ten_count = count

            cust_obj.save()
            referral_code = cust_obj.referral_code
        else:

            customer.first_ten_count = 1
            customer.save()
            referral_code = customer.referral_code

        order.save()
        product.save()
        # launch asynchronous task
        order_created.delay(order.id)

        # launch asynchronous task
        order_created_admin.delay(order.id)

        return render(request, 'orders/order/created.html',
                      {'order': order, 'message': message, 'message1':message1, 'referral_code': referral_code, 'service': service})

    else:
        return render(request, 'orders/order/create_gifting.html')




def order_create_stitching(request):


    if request.method == 'POST':
        referral_code = None
        message = None
        message1=None
        service = 'stitching'
        cust_obj = None

        order = Order()
        customer = Customer()
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        cust = Customer.objects.filter(phone=phone, email=email)
        if cust:
            cust_obj = get_object_or_404(Customer, phone=phone, email=email)
            customer = None

        if not cust:

            customer.first_name = request.POST.get('fname')
            customer.last_name = request.POST.get('lname')
            customer.email = request.POST.get('email')
            customer.phone = request.POST.get('phone')
            order.customer = customer


        else:
            order.customer = cust_obj

        order.address = request.POST.get('address')
        order.postal_code = request.POST.get('postal')
        order.city = request.POST.get('city')
        order.preferred_contact = request.POST.get('contact-radio')



        product = OrderItem_stitching()


        product.order = order
        product.description = request.POST.get('custom-order')
        product.expected_by = request.POST.get('expected-by')
        product.service = request.POST.get('service')

        referral_code = request.POST.get('referral-code')



        if referral_code == "":


            pass

        elif not customer:

            if cust_obj.reffered_by_id and referral_code:

               return HttpResponse("Warning: You have already used a referral code to become our customer. Please omit this field!!!")

        if referral_code == "":

            pass

        elif customer or cust_obj:

            referrer = Customer.objects.filter(referral_code=referral_code)

            if not referrer and referral_code:
                return HttpResponse("Warning: Wrong referral code provided!!!")
            else:
                phone = referrer.values()[0]['phone']

            if customer is None:


                if cust_obj.phone == phone:

                    return HttpResponse("Warning: Please do not use your own referral code!!!")

            elif not referrer:
                return HttpResponse(
                    "Warning: Invalid referral code!!! Please fill in a valid code or omit the option. ")
            else:
                if customer:
                    referrer = Customer.objects.get(referral_code=referral_code)
                    referrer_obj = get_object_or_404(Customer, phone=referrer.phone, email=referrer.email)
                    customer.reffered_by = referrer_obj
                elif cust_obj:
                    referrer = Customer.objects.get(referral_code=referral_code)
                    referrer_obj = get_object_or_404(Customer, phone=referrer.phone, email=referrer.email)
                    cust_obj.reffered_by = referrer_obj
                order.referral_code = referral_code

                count = referrer.refer_count
                count += 1
                referrer_obj.refer_count = count
                referrer_obj.save()


        if cust:
            if cust_obj.refer_count > 5:
                no_free_service = cust_obj.refer_count % 5

                free_service.delay(order.id, cust_obj.id)
                message = "Congratulations! You have won {} free service on this order for referring 5 friends." \
                          " Keep referring more to win more. Happy shopping!".format(no_free_service)



            count = cust_obj.first_ten_count

            if count == 11:
                message = ""

            elif count == 10:
                message1 = "Congrats! " \
                          "You've maybe won a free service for this transaction! Our executive will let you know more. " \
                          "The excitement doesn't end here, refer more friends to gain free services. Happy shopping!"
                free_service_11.delay(order.id)
                count += 1
                cust_obj.first_ten_count = count

            elif count == 9:
                message1 = "Congrats! " \
                          "You maybe eligible for a free service on the next transaction if you've transacted more than ₹15,000 for the first 10 transactions with us!" \
                          " Welcome to your family! The excitement doesn't end here,  refer more friends to gain free services. Happy shopping!"
                count += 1
                cust_obj.first_ten_count = count
                cust_obj.save()
            elif count < 11:
                count += 1
                cust_obj.first_ten_count = count

            cust_obj.save()
            referral_code = cust_obj.referral_code
        else:

            customer.first_ten_count = 1
            customer.save()
            referral_code = customer.referral_code

        order.save()
        product.save()

        # launch asynchronous task
        order_created.delay(order.id)

        # launch asynchronous task
        order_created_admin.delay(order.id)

        return render(request, 'orders/order/created.html',
                      {'order': order, 'message': message, 'message1':message1, 'referral_code': referral_code, 'service': service})


























