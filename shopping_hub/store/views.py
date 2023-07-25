from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import  check_password
from django.shortcuts import render , redirect , HttpResponseRedirect

from django.views import View

from .models.products import Products
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order

# Create your views here.
class Index(View):
    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
            

        prod = Products.objects.all()[:90]
        cat = Category.objects.all()

        cat_id = request.GET.get('category')
        if cat_id:
            prod = Products.objects.filter(category=cat_id)[:90]
        else:
            prod = Products.objects.all()[:90]
        print('you are : ',request.session.get('email'))
        return render(request, 'index.html',{"products":prod, "categories": cat})

    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1 :
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+ 1
                
            else:
                cart[product] = 1

        else:
            cart = {}
            cart[product] = 1
        
        request.session['cart'] = cart

        print(request.session['cart'])
        return redirect('index')







def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = validateCustomer(customer, email)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.save()
            # return render(request, 'signup.html')
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)


# signup validation
def validateCustomer(customer, email):
        error_message = None
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif Customer.objects.filter(email = email):
            error_message = 'Email Address Already Registered..'

        return error_message





    

def logout(request):
    request.session.clear()
    return redirect('login')




class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Products.objects.filter(id__in = ids)
        # print(products)
        return render(request , 'cart.html' , {'products' : products} )









class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'login.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('index')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'login.html', {'error': error_message})










class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        ids = list(cart.keys())
        products = Products.objects.filter(id__in = ids)

        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
            # emptying the cart
        request.session['cart'] = {}

        return redirect('cart')
    




def recommend(request):
    
    return render(request, 'recommend.html')