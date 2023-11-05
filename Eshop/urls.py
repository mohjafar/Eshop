from django.contrib import admin
from django.urls import path
from Mainapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home),
    path('shop/<str:mc>/<str:sc>/<str:br>/',views.shop),
    path('single/<int:id>/',views.singleProduct),
    path('login/',views.loginPage),
    path('signup/',views.signupPage),
    path('profile/',views.profilepage),
    path('logout/',views.logoutPage),
    path('update/',views.updateProfile),
    path('add-to-cart/<int:id>/',views.cartpage),
    path('cart/',views.cartfrontpage),
    path('delete-cart/<int:pid>/',views.deletecart),
    path('update-cart/<int:pid>/<str:op>/',views.UpadeCart),
    path('wishlist/',views.wish),
    path('wishlist1/<int:pid>/',views.AddToWishlist),
    path('delete-Wishlist/<int:pid>/',views.deleteWishlist),
    path('checkout/',views.CheckoutPage),
    path('order/',views.OrderPage),
    path('history/',views.history),
    path('confirmation/',views.ConfirmationPage),
    path('contact/',views.contactPage),
    path('search/',views.SearchPage),
    path('forget-username/',views.ForgetUsername),
    path('forget-otp/',views.forgetOTP),
    path('password/',views.CreateNewPassword),
    path('paymentSuccess/<str:rppid>/<str:rpoid>/<str:rpsid>/',views.paymentSuccess),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
