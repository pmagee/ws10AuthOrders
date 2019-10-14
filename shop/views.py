from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.db.models import Count
from django.contrib.auth.models import Group, User
from .forms import SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

def product_list(request, category_id=None):
    category = None
    products = Product.objects.all()
    ccat = Category.objects.annotate(num_products=Count('products'))
    if(category_id):
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)

    return render(request, 'products.html',
                    {'products': products,
                    'countcat':ccat})

def signupView(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			signup_user = User.objects.get(username=username)
			customer_group = Group.objects.get(name='Customer')
			customer_group.user_set.add(signup_user)
	else:
		form = SignUpForm()
	return render(request, 'accounts/signup.html', {'form':form})

def signinView(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				return redirect('products')
			else:
				return redirect('signup')
	else:
		form = AuthenticationForm()
	return render(request,'accounts/signin.html', {'form':form })

def signoutView(request):
	logout(request)
	return redirect('signin')