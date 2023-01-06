from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import Customer, Product, Cart, OrderPlaced, Coupon, Ratings
from .forms import CustomerRegistrationForm, CustomerProfileForm, RatingForm
from django.views import View
from django.http import JsonResponse, request
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
	def get(self, request):
		totalitem = 0
		dryfruits = Product.objects.filter(category='DF')
		rice_and_pulses = Product.objects.filter(category='RP')
		
		
		# mobiles = Product.objects.filter(category='M')
		# groceries = Product.objects.filter(category='GR')
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		return render(request, 'app/home.html', {'dryfruits':dryfruits, 'rice_and_pulses':rice_and_pulses,'totalitem':totalitem})

class ProductDetailView(View):
	def get(self, request, pk):
		form = RatingForm
		totalitem = 0
		product = Product.objects.get(pk=pk)
		ratings = Ratings.objects.filter(product = pk)
		print(ratings)
		print(product.id)
		item_already_in_cart=False
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
			item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
		return render(request, 'app/productdetail.html', {'product':product, 'item_already_in_cart':item_already_in_cart, 'form': form, 'totalitem':totalitem, 'ratings': ratings})

@method_decorator(login_required, name='dispatch')
class SubmitRating(View):
	def post(self, request, pk):			
		form = RatingForm(request.POST)
		if form.is_valid():
			usr = request.user
			product = Product.objects.get(pk=pk)
			rating = form.cleaned_data['rating']
			newrat = Ratings(user = usr, product = product, rating =rating)
			newrat.save()
			messages.success(request, "Review Submitted")
			return redirect(f'/product-detail/{pk}')

@login_required()
def add_to_cart(request):
	user = request.user
	item_already_in_cart1 = False
	product = request.GET.get('prod_id')
	item_already_in_cart1 = Cart.objects.filter(Q(product=product) & Q(user=request.user)).exists()
	if item_already_in_cart1 == False:
		product_title = Product.objects.get(id=product)
		Cart(user=user, product=product_title).save()
		messages.success(request, 'Product Added to Cart Successfully !!' )
		return redirect('/cart')
	else:
		return redirect('/cart')
  # Below Code is used to return to same page
  # return redirect(request.META['HTTP_REFERER'])

@login_required
def show_cart(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
		user = request.user
		cart = Cart.objects.filter(user=user)
		amount = 0.0
		shipping_amount = 50.0
		totalamount=0.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		print(cart_product)
		if cart_product:
			for p in cart_product:
				tempamount = (p.quantity * p.product.discounted_price)
				amount = tempamount + (p.quantity*shipping_amount)
			totalamount = (amount)
			print(totalamount)
			return render(request, 'app/addtocart.html', {'carts':cart, 'amount':amount, 'totalamount':totalamount, 'totalitem':totalitem,})
		else:
			return render(request, 'app/emptycart.html', {'totalitem':totalitem})
	else:
		return render(request, 'app/emptycart.html', {'totalitem':totalitem})

def plus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity+=1
		c.save()
		amount = 0.0
		shipping_amount= 50.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount = tempamount + (p.quantity*shipping_amount)
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

def minus_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.quantity-=1
		c.save()
		amount = 0.0
		shipping_amount= 50.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount = tempamount + (p.quantity*shipping_amount)
			# print("After", amount)
		# print("Total", amount)
		data = {
			'quantity':c.quantity,
			'amount':amount,
			'totalamount':amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@login_required
def checkout(request):
	coupondiscountt = 0
	inputcoupon =  "None"
	if request.method == "POST":
			inputcoupon = request.POST['coupon']
			matchcoupon = Coupon.objects.filter(title = inputcoupon).first()
			if matchcoupon:
				if inputcoupon == matchcoupon.title:
					coupondiscountt = matchcoupon.worth
					print(coupondiscountt)
					messages.success(request, "Coupon Applied Successfully")
				else:
					coupondiscountt = 0
					messages.error(request, "Invalid or Expired Coupon Code ")
			else:
				coupondiscountt = 0
				messages.error(request, "Invalid Coupon. Please check it again")	
	user = request.user
	add = Customer.objects.filter(user=user)
	cart_items = Cart.objects.filter(user=request.user)
	amount = 0.0
	shipping_amount = 50.0
	totalamount=0.0
	cart_product = [p for p in Cart.objects.all() if p.user == request.user]
	if cart_product:
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			amount  =  tempamount + (p.quantity*50)
		totalamount = amount-coupondiscountt
	return render(request, 'app/checkout.html', {'add':add, 'cart_items':cart_items, 'totalcost':totalamount, 'couponapplied': inputcoupon})

@login_required
def payment_done(request):
	inpcoupon = request.GET.get('couponapplied')
	payment_screenshot = request.GET.get('form-control')
	print("Coupon Applied", inpcoupon)
	custid = request.GET.get('custid')
	print("Customer ID", custid)
	user = request.user
	cartid = Cart.objects.filter(user = user)
	customer = Customer.objects.get(id=custid)
	print(customer)
	for cid in cartid:
		OrderPlaced(user=user, customer=customer, product=cid.product, quantity=cid.quantity, couponapplied=inpcoupon, payment_screenshot = payment_screenshot).save()
		print("Order Saved")
		cid.delete()
		print("Cart Item Deleted")
		messages.success(request, "Thank You! Your order has been placed successfully and is awaiting confirmation")
	return redirect("orders")

def remove_cart(request):
	if request.method == 'GET':
		prod_id = request.GET['prod_id']
		c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
		c.delete()
		amount = 0.0
		shipping_amount= 70.0
		cart_product = [p for p in Cart.objects.all() if p.user == request.user]
		for p in cart_product:
			tempamount = (p.quantity * p.product.discounted_price)
			# print("Quantity", p.quantity)
			# print("Selling Price", p.product.discounted_price)
			# print("Before", amount)
			amount += tempamount
			# print("After", amount)
		# print("Total", amount)
		data = {
			'amount':amount,
			'totalamount':amount+shipping_amount
		}
		return JsonResponse(data)
	else:
		return HttpResponse("")

@login_required
def address(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	add = Customer.objects.filter(user=request.user)
	return render(request, 'app/address.html', {'add':add, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def orders(request):
	op = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')
	return render(request, 'app/orders.html', {'order_placed':op})

# ELECTRONIC ITEMS START FROM HERE

# View for Mobiles
def mobile(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			mobiles = Product.objects.filter(category='M')
	elif data == 'Redmi' or data == 'Samsung':
			mobiles = Product.objects.filter(category='M').filter(brand=data)
	elif data == 'below':
			mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)
	elif data == 'above':
			mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)
	return render(request, 'app/mobile.html', {'mobiles':mobiles, 'totalitem':totalitem})

# View for Laptops
def laptops(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			laptops = Product.objects.filter(category='L')
	elif data == 'Apple' or data == 'Samsung' or data == 'HP' or data == "Lenovo" or data == "Asus" or data == "Compac":
			laptops = Product.objects.filter(category='L').filter(brand=data)
	elif data == 'below':
			laptops = Product.objects.filter(category='L').filter(discounted_price__lt=30000)
	elif data == 'above':
			laptops = Product.objects.filter(category='L').filter(discounted_price__gt=10000)
	return render(request, 'app/laptops.html', {'laptops':laptops, 'totalitem':totalitem})


# View for Hearing and Music
def hearingandmusic(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			hearingandmusic = Product.objects.filter(category='HE')
	elif data == 'earphones' or data == 'headphones' or data == 'wireless' or data == 'earpods' or data == "speakers":
			hearingandmusic = Product.objects.filter(category='HE').filter(brand=data)
	return render(request, 'app/hearingandmusic.html', {'hearingandmusic':hearingandmusic, 'totalitem':totalitem})

# View for Watches
def watches(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			watches = Product.objects.filter(category='WA')
	elif data == 'realme' or data == 'apple' or data == 'redmi' or data == 'samsung' or data == "other":
			watches = Product.objects.filter(category='HE').filter(brand=data)
	return render(request, 'app/watches.html', {'watches':watches, 'totalitem':totalitem})

# View for Other Electronics
def electronics(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			electronics = Product.objects.filter(category='EL')
	elif data == 'washingmachines' or data == 'refrigerators' or data == "computeraccessories" or data == "heatingappliances" or data == "geysers" or data == "fans" or data == "juicersandmixers" or data == "wiresandcables" :
			electronics = Product.objects.filter(category='EL').filter(brand=data)
	return render(request, 'app/electronics.html', {'electronics':electronics, 'totalitem':totalitem})


# View for Walnuts
def groceries(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			groceries = Product.objects.filter(category='GR')
	elif data == 'Spices' or data == 'Oils' or data == 'GrainsandCereals' or data == 'Diary':
			groceries = Product.objects.filter(category='GR').filter(brand=data)
	return render(request, 'app/groceries.html', {'groceries':groceries, 'totalitem':totalitem})

# View for Frozen and Chilled
def almonds(request, data=None):
	totalitem = 0

	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			frozenandchilled = Product.objects.filter(category='FR')
	elif data == 'icecreams' or data == 'beverages' or data == 'familypacks':
			frozenandchilled = Product.objects.filter(category='FR').filter(brand=data)
	return render(request, 'app/almonds.html', {'frozenandchilled':frozenandchilled, 'totalitem':totalitem})

# View for Bakeries
def bakeries(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			bakeries = Product.objects.filter(category='BK')
	elif data == 'cookies' or data == 'cakes' or data == 'pastries' or data == "dals":
			bakeries = Product.objects.filter(category='BK').filter(brand=data)
	return render(request, 'app/bakeries.html', {'bakeries':bakeries, 'totalitem':totalitem})

# View for restaurant food
def restaurantfood(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			restaurantfood = Product.objects.filter(category='RF')
	elif data == 'pizzas' or data == 'burgers' or data == 'momos' or data == "chicken" or data == "biryanis":
			restaurantfood = Product.objects.filter(category='RF').filter(brand=data)
	return render(request, 'app/restaurantfood.html', {'restaurantfood':restaurantfood, 'totalitem':totalitem})

# Views for Fashion Products from here

# View for topwear
def topwear(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			topwear = Product.objects.filter(category='TW')
	elif data == 'menswinter' or data == 'womenswinter' or data == 'menssummer' or data == "womenssummer" or data == "hoodies" or data == "zippers":
			topwear = Product.objects.filter(category='TW').filter(brand=data)
	return render(request, 'app/topwear.html', {'topwear':topwear, 'totalitem':totalitem})

# View for bottom wear
def bottomwear(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			bottomwear = Product.objects.filter(category='BW')
	elif data == 'menswinter' or data == 'womenswinter' or data == 'menssummer' or data == "womenssummer":
			bottomwear = Product.objects.filter(category='BW').filter(brand=data)
	return render(request, 'app/bottomwear.html', {'bottomwear':bottomwear, 'totalitem':totalitem})

# View for knitted wear
def knittedwear(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			knittedwear = Product.objects.filter(category='KC')
	elif data == 'sweaters' or data == 'kidsets' or data == 'gloves' or data == "caps":
			knittedwear = Product.objects.filter(category='KC').filter(brand=data)
	return render(request, 'app/knittedwear.html', {'knittedwear':knittedwear, 'totalitem':totalitem})

# View for knitted wear
def footwear(request, data=None):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
	if data==None :
			footwear = Product.objects.filter(category='FW')
	elif data == 'formalmens' or data == 'formalwomens' or data == 'casualmens' or data == "casualwomens" or data == "kidsfootwear" or data == "wintershoes":
			footwear = Product.objects.filter(category='FW').filter(brand=data)
	return render(request, 'app/footwear.html', {'footwear':footwear, 'totalitem':totalitem})

# View for Rice
def rice(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
		rice = Product.objects.filter(category='RC')
	return render(request, 'app/rice.html', {'rice':rice, 'totalitem':totalitem})

# View for Rajma
def rajma(request):
	totalitem = 0
	if request.user.is_authenticated:
		totalitem = len(Cart.objects.filter(user=request.user))
		rajma = Product.objects.filter(category='Rajma')
	return render(request, 'app/rajma.html', {'rajma':rajma, 'totalitem':totalitem})

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form':form})
  
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations!! Registered Successfully.')
            form.save()
            return render(request, 'app/customerregistration.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
	def get(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm()
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})
		
	def post(self, request):
		totalitem = 0
		if request.user.is_authenticated:
			totalitem = len(Cart.objects.filter(user=request.user))
		form = CustomerProfileForm(request.POST)
		if form.is_valid():
			usr = request.user
			name  = form.cleaned_data['name']
			locality = form.cleaned_data['locality']
			city = form.cleaned_data['city']
			state = form.cleaned_data['state']
			zipcode = form.cleaned_data['zipcode']
			reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
			reg.save()
			messages.success(request, 'Congratulations!! Profile Updated Successfully.')
		return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary', 'totalitem':totalitem})

@login_required
def cancelorder(request, id):
	custid = request.GET.get('custid')
	print(custid)
	user = request.user
	ordertobecancelled = OrderPlaced.objects.filter(user  = user, product = id)
	context = {'ordertobecancelled': ordertobecancelled}
	return render(request, 'app/cancelorder.html', context)

@login_required
def cancellationdone(request, id):
	user = request.user
	ordertobecancelled = OrderPlaced.objects.filter(user  = user, id = id)
	ordertobecancelled.delete()
	messages.success(request, "Your Order Has Been Cancelled")
	return render(request, "app/orders.html")

def about(request):
	return render(request, 'app/about.html')
def bulk(request):
	return render(request, 'app/bulk.html')

def privacypolicy(request):
	return render(request, 'app/privacypolicy.html')

def search(request):
    query=request.GET['query']
    if len(query)>78:
        allProducts=Product.objects.none()
    else:
        allProductsTitle= Product.objects.filter(title__icontains=query)
        allProductsAuthor= Product.objects.filter(brand__icontains=query)
        allProductsContent =Product.objects.filter(category__icontains=query)
        allProducts=  allProductsTitle.union(allProductsContent, allProductsAuthor)
    if allProducts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    params={'allProducts': allProducts, 'query': query}
    return render(request, 'app/search.html', params)
