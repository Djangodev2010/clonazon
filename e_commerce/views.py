from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import FormView, ListView, DetailView, CreateView, TemplateView
from django.contrib import messages
from .models import Product, Category, Review, Profile, CartItem
from django.db.models import F
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, RatingForm, UserLoginForm, CartForm
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import get_object_or_404, redirect

# Create your views here.

@method_decorator(login_required(login_url=reverse_lazy('e_commerce:register')), name='dispatch')
class HomeView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'e-com/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('name')
        context['profile'] = Profile.objects.filter(user=self.request.user)
        return context

@method_decorator(login_required(login_url=reverse_lazy('e_commerce:register')), name='dispatch')
class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'e-com/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.filter(slug=self.kwargs.get('slug')).first()
        if product:
            product.count = F('count') + 1
            product.save()
        
        category = product.category
        context['related_products'] = Product.objects.filter(category=category).order_by('-count')[:8]
        context['categories'] = Category.objects.all().order_by('name')
        context['reviews'] = Review.objects.filter(product__name=product)
        context['profile'] = Profile.objects.filter(user=self.request.user)
        context['profiles'] = Profile.objects.all()
        context['cate'] = Category.objects.filter(name=product.category)
        return context

@method_decorator(login_required(login_url=reverse_lazy('e_commerce:register')), name='dispatch')
class SearchView(ListView):
    model = Product
    template_name = 'e-com/search_product.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all().order_by('id')
        return context

    def get_queryset(self):
        q = self.request.GET.get('q')
        product = Product.objects.filter(name__icontains=q)
        return product

@method_decorator(login_required(login_url=reverse_lazy('e_commerce:register')), name='dispatch')
class CategoryProductView(ListView):
    model = Product
    template_name = 'e-com/category_product.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.filter(name=self.kwargs.get('cate_name'))
        context['categories'] = Category.objects.all().order_by('name')[:8]
        context['profile'] = Profile.objects.filter(user=self.request.user)
        return context

    def get_queryset(self):
        category = self.kwargs.get('cate_name')
        return Product.objects.filter(category__name=category)

@method_decorator(login_required(login_url=reverse_lazy('e_commerce:register')), name='dispatch')
class ReviewWriteView(CreateView):
    model = Review
    template_name = 'e-com/review_write.html'
    form_class = RatingForm
    success_url = reverse_lazy('e_commerce:index')

    def form_valid(self, form):
        # Check if the user has already reviewed this specific product
        if Review.objects.filter(user=self.request.user, product__slug=self.kwargs['slug']).exists():
            messages.info(self.request, 'Cannot Review Multiple Times On The Same Product!')
            # Construct the URL separately
            product_detail_url = reverse('e_commerce:product_detail', kwargs={'slug': self.kwargs['slug']})
            return HttpResponseRedirect(product_detail_url)
        else:
            form.instance.user = self.request.user
            form.instance.product = Product.objects.get(slug=self.kwargs['slug'])
            return super().form_valid(form)

@method_decorator(login_required(login_url=reverse_lazy('e_commerce:register')), name='dispatch')
class AllReviewView(ListView):
    model = Review
    template_name = 'e-com/all_review.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = Review.objects.filter(product=self.kwargs.get('id'))
        context['categories'] = Category.objects.all()
        context['profile'] = Profile.objects.filter(user=self.request.user)
        context['profiles'] = Profile.objects.all()
        return context
    
@method_decorator(login_required(login_url=reverse_lazy('e_commerce:register')), name='dispatch')
class ProfileView(TemplateView):
    model = Profile
    template_name = 'e-com/user_profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = Profile.objects.filter(user=self.request.user.id)
        return context
    
class RegisterView(CreateView):
    model = User
    template_name = 'authorization/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('e_commerce:login')

    def form_valid(self, form):
        # Save the user first
        user = form.save()
        # Create the profile
        Profile.objects.create(user=user, avatar=form.cleaned_data.get('avatar'))
        return super().form_valid(form)

class LoginView(FormView):
    template_name = 'authorization/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('e_commerce:index')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    
class AddToCartView(CreateView):
    model = CartItem
    template_name = 'e-com/add_to_cart.html'
    form_class = CartForm
    success_url = reverse_lazy('e_commerce:index')

    def post(self, request, *args, **kwargs):
        product = get_object_or_404(Product, name=self.kwargs['name'])
        user = request.user
        quantity = request.POST.get('quantity')

        if not quantity:
            messages.error(request, 'Quantity is required.')
            return redirect('e_commerce:index')

        try:
            cart_item = CartItem(user=user, name=product, quantity=quantity)
            cart_item.save()
            messages.success(request, 'Product added to cart successfully.')
        except Exception as e:
            messages.error(request, f'An error occurred!')
            return redirect('e_commerce:index')

        return super().post(request, *args, **kwargs)