from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from random import randrange
from django.conf import settings
from django.core.mail import send_mail
from Eshop.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay
from .models import *

def home(Request):
    data=Product.objects.all().order_by('id').reverse()[:8]
    return render(Request,'home.html',{'data':data})

def shop(Request,mc,sc,br):
    if(mc=='All' and sc=='All' and br=='All'):
        data=Product.objects.all().order_by('id').reverse()
    elif(mc!='All' and sc=='All' and br=='All'): 
        data=Product.objects.filter(maincategory=Maincategory.objects.get(name=mc)).order_by('id').reverse()   
    elif(mc=='All' and sc!='All' and br=='All'):
        data=Product.objects.filter(subcategory=Subcategory.objects.get(name=sc)).order_by('id').reverse()    
    elif(mc=='All' and sc=='All' and br!='All'):
        data=Product.objects.filter(brand=Brand.objects.get(name=br)).order_by('id').reverse()
    elif(mc!='All' and sc!='All' and br=='All'): 
        data=Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc)).order_by('id').reverse()
    elif(mc!='All' and sc=='All' and br!='All'):
        data=Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),brand=Brand.objects.get(name=br)).order_by('id').reverse()
    elif(mc=='All' and sc!='All' and br!='All'):
        data=Product.objects.filter(subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br)).order_by('id').reverse()
    else:
        data=Product.objects.filter(maincategory=Maincategory.objects.get(name=mc),subcategory=Subcategory.objects.get(name=sc),brand=Brand.objects.get(name=br)).order_by('id').reverse()
    maincategory=Maincategory.objects.all()
    subcategory=Subcategory.objects.all()
    brand=Brand.objects.all()
    return render(Request,'shop.html',{'data':data,'maincategory':maincategory,'subcategory':subcategory,'brand':brand,'mc':mc,'sc':sc,'br':br})

def singleProduct(Request,id):
    try:
      data=Product.objects.get(id=id)
      return render(Request,'single.html',{'data':data})
    except:
        return redirect("/admin/")  
    


def signupPage(Request):
   if(Request.method=='POST'):
       p=Request.POST.get('password')
       cp=Request.POST.get('cpassword')
       if(p==cp):
            b=Buyer()
            b.name=Request.POST.get('name')
            b.username=Request.POST.get('username')
            b.phone=Request.POST.get('phone')
            b.email=Request.POST.get('email')
            user=User(username=b.username,email=b.email)
            try:
               if(user):
                user.set_password(p)
                user.save()
                b.save()
                subject = 'Your Buyer Account Is Created : Team Eshop'
                message ='Hello  ' +b.name+',' '\nThanks To Create A Buyer Account. \nNow You Can Buy Any Products :  Team Eshop'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [b.email]
                send_mail( subject, message, email_from, recipient_list )
                return redirect("/login/")
            except:

                 messages.error(Request,"User Name Already Taken !!!!!")    
       else:
            messages.error(Request,"Password And Confirm Password Does't Matched !!!!!")                       
   return render(Request,'signup.html')


def loginPage(Request):
    if(Request.method=="POST"):
        username=Request.POST.get('username')
        password=Request.POST.get('password')
        user=authenticate(username=username,password=password)

        try:
            if(user is not None):
                login(Request,user)
                if(user.is_superuser):
                   return redirect("/admin/")
                else:
                    return redirect("/profile/")  
            else:
                messages.error(Request,"Username Or Password is Invaid")
        except:
            pass
    return render(Request,'login.html')



def logoutPage(Request):
    logout(Request)
    return redirect("/login/")


@login_required(login_url="/login/")
def profilepage(Request):
    user=User.objects.get(username=Request.user)
    if(user.is_superuser):
        return redirect("/admin/")
    else:
        buyer=Buyer.objects.get(username=user.username)
        
    return render(Request,'profile.html',{'user':buyer})


@login_required(login_url="/login/")
def updateProfile(Request):
    user=User.objects.get(username=Request.user)
    if(user.is_superuser):
        return redirect('/admin/')
    else:
         buyer=Buyer.objects.get(username=user.username)
         if(Request.method=="POST"):
            buyer.name=Request.POST.get('name')
            buyer.email=Request.POST.get('email')
            buyer.phone=Request.POST.get('phone')
            buyer.addressline1=Request.POST.get('addressline1')
            buyer.addressline2=Request.POST.get('addressline2')
            buyer.addressline3=Request.POST.get('addressline3')
            buyer.pin=Request.POST.get('pin')
            buyer.city=Request.POST.get('city')
            buyer.state=Request.POST.get('state')
            if(Request.FILES.get('pic5')):
                buyer.pic5=Request.FILES.get('pic5')
            buyer.save()
            return redirect('/profile/')
    return render(Request,'update.html',{'user':buyer})

@login_required(login_url='/login/')
def cartpage(Request,id):
    cart=Request.session.get('cart',None)
    p=Product.objects.get(id=id)
    if(cart is None):
        cart={str(p.id):{'pid':p.id,'pic':p.pic1.url,'name':p.name,'color':p.color,'size':p.size,'discount':p.discount,'total':p.finalprice,'price':p.finalprice,'baseprice':p.baseprice,'qty':1,'maincategory':p.maincategory.name,'subcategory':p.subcategory.name,'brand':p.brand.name}}
    else:
        if(str(p.id) in cart):
            item=cart[str(p.id)]
            item['qty']=item['qty']+1
            item['total']=item['total']+item['price']
            cart[str(p.id)]=item
        else:
            cart.setdefault(str(p.id),{'pid':p.id,'pic':p.pic1.url,'name':p.name,'color':p.color,'size':p.size,'discount':p.discount,'price':p.finalprice,'total':p.finalprice,'baseprice':p.baseprice,'qty':1,'maincategory':p.maincategory.name,'subcategory':p.subcategory.name,'brand':p.brand.name})
            
    Request.session['cart']=cart
    Request.session.set_expiry(60*60*24*45) 
    return redirect("/cart/")


@login_required(login_url='/login/')
def cartfrontpage(Request):
    cart=Request.session.get('cart',None)
    c=[]
    total=0
    shipping=0
    if(cart is not None):
        for value in cart.values():
            total=total+value['total']
            c.append(value)
        if(total<1000 and total>0 ):
            shipping=150
    final=total+shipping
    return render(Request,'cart.html',{'cart':c,'final':final,'total':total,'shipping':shipping})


@login_required(login_url='/login/')
def deletecart(Request,pid):
    cart=Request.session.get('cart',None)
    if(str(pid) in cart):
        for  key in cart.keys():
            if(str(pid)==key):
             del cart[key]
             break    
    Request.session['cart']=cart
    return redirect('/cart/')


@login_required(login_url='/login/')
def UpadeCart(Request,pid,op):
    cart=Request.session.get('cart',None)
    if(str(pid) in cart):
        for  key,value in cart.items():
            if(str(pid)==key  and str(op)=='inc' ):
              value['qty']=value['qty']+1
              value['total']=value['total']+value['price']
            elif(str(pid)==key and str(op)=='dec' and value['qty']>1):
              value['qty']=value['qty']-1
              value['total']=value['total']-value['price']  
              break    
            
    Request.session['cart']=cart
    return redirect("/cart/")


@login_required(login_url='/login/')
def AddToWishlist(Request,pid):
    try:   
   
        user=Buyer.objects.get(username=Request.user.username)
        p=Product.objects.get(id=pid)
        try:
             w=Wishlist.objects.get(user=user,product=p)
        except:
            w=Wishlist()
            w.user=user
            w.product=p
            w.save() 
    except:        
          pass
    return redirect("/wishlist/")
        # return redirect('/admin/')
    # return render(Request,'wishlist.html',{'Wishlist':wishlist,'user':buyer})

@login_required(login_url='/login/')
def wish(Request):
    # wishlist=Request.session.get('wishlist',None)
   
    user=User.objects.get(username=Request.user)
    if(user.is_superuser):
        return redirect("/admin/")
    elif(user is  None):
        messages.error(Request,"Please Login")
    else:   
        buyer=Buyer.objects.get(username=user.username)
        wishlist=Wishlist.objects.filter(user=buyer)
    return render(Request,'wishlist.html',{'wishlist':wishlist})  
# ,'final':final,'total':total,'shipping':shipping


@login_required(login_url='/login/')
def deleteWishlist(Request,pid):
               try: 
                    user=Buyer.objects.get(username=Request.user.username)
                    p=Product.objects.get(id=pid)
                    try:
                        w=Wishlist.objects.get(user=user,product=p)
                        w.delete()
                    except:
                        pass    
               except:
                   pass
               return redirect('/wishlist/')            


@login_required(login_url='/login/')
def CheckoutPage(Request):
    cart=Request.session.get('cart',None)
    try:
        buyer=Buyer.objects.get(username=Request.user.username)
        c=[]
        shipping=0
        total=0
        if(cart is not None):
            for values in cart.values():
                total=total+values['total']
                c.append(values)
            if(total<1000 and total>0):
                   shipping=shipping+150
        final=total+shipping
           
    except:
        pass    
    return render(Request,'checkout.html',{'user':buyer,'cart':c,'total':total,'shipping':shipping,'final':final})



client=razorpay.Client(auth=(RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY))
@login_required(login_url='/login/')
def OrderPage(Request):
    if(Request.method=='POST'):
        mode=Request.POST.get('mode')
        user=Buyer.objects.get(username=Request.user.username)
        cart=Request.session.get('cart',None)  
        if(cart is None):
            return redirect("/cart/")
        else: 
            check=Checkout()
            check.user=user
            total=0
            shipping=0
            for value in cart.values():
                total=total+value['total']
            if(total<1000 and total>0):
                shipping=150 
            final=total+shipping
            check.total=total
            check.shipping=shipping
            check.final=final
            check.save()
            for value in cart.values():
                cp=CheckoutProduct()
                cp.checkout=check
                cp.p=Product.objects.get(id=value['pid'])
                cp.qty=value['qty'] 
                cp.total=value['total']  
                cp.save()  
            subject = 'Your Order Has Been Placed : Team Eshop'
            message ='Thanks To Shop With Us   \nNow You Can Track Your Order On Your Order Page :Team Eshop'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email,]
            send_mail( subject, message, email_from, recipient_list ) 
            if(mode=='COD'):
                   return redirect('/confirmation/')
            else:
                orderAmount = check.final*100
                orderCurrency = "INR"
                paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
                paymentId = paymentOrder['id']
                check.save()
                return render(Request,"pay.html",{
                    "amount":orderAmount,
                    "api_key":RAZORPAY_API_KEY,
                    "order_id":paymentId,
                    "User":user
                })            
       
    else:
        return redirect("/checkout/")
    
@login_required(login_url='/login/')
def  ConfirmationPage(Request):
    return render(Request,'confirmation.html')



@login_required(login_url='/login/')
def  history(Request):
    user=Buyer.objects.get(username=Request.user.username)
    buyer=Buyer.objects.get(username=user.username)
    orders=Checkout.objects.filter(user=buyer)
    return render(Request,'history.html',{'orders':orders})     

def contactPage(Request):
    if(Request.method=="POST"):
        contact=Contact()
        contact.name=Request.POST.get('name')
        contact.email=Request.POST.get('email')
        contact.phone=Request.POST.get('phone')
        contact.subject=Request.POST.get('subject')
        contact.message=Request.POST.get('message')
        contact.save()
        messages.success(Request,"Thanks to Share Your Query With US!! Our Team Will Contact You Soon!!!!")
    return render(Request,'contact.html')   


def SearchPage(Request):
    search=Request.POST.get("search")
    data=Product.objects.filter(Q(name__icontains=search)|Q(color__icontains=search)|Q(size__icontains=search)|Q(description__icontains=search))
    maincategory=Maincategory.objects.all()
    subcategory=Subcategory.objects.all()
    brand=Brand.objects.all()
    return render(Request,'shop.html',{'data':data,'maincategory':maincategory,'subcategory':subcategory,'brand':brand,'mc':'All','sc':'All','br':'All'})



def ForgetUsername(Request):
    if(Request.method=="POST"):
        try:
          username=Request.POST.get('username')
          user=User.objects.get(username=username)
          if(user.is_superuser):
              return redirect("/admin/")
              
          else:
              buyer=Buyer.objects.get(username=username)
              otp=randrange(100000,999999)
              buyer.otp=otp
              buyer.save()
              subject = 'OTP for Password Reset : Team Eshop'
              message =' OTP for Password Reset  is  ' +str(otp)+'\nTeam OnlineBazar'
              email_from = settings.EMAIL_HOST_USER
              recipient_list = [buyer.email,]
              send_mail( subject, message, email_from, recipient_list )
              Request.session["resetuser"]=username
              return redirect("/forget-otp/")
        except:
          messages.error(Request,"Invalid Username !!!!!")   
    return render(Request,"forget-username.html")


def forgetOTP(Request):
    if(Request.method=="POST"):
        try:
            username=Request.session.get('resetuser',None)
            otp=Request.POST.get('otp')
            if(username):
                buyer=Buyer.objects.get(username=username)
                if(int(otp)==buyer.otp):
                    return redirect("/password/")
                else:
                    messages.error(Request,"Invalid OTP !!!")
            else:
                messages.error(Request,"Unauthorized ! ! ! ! ! Try Again")
        except:
            messages.error(Request,'Invalid Value, Please Enter a valid OTP Number')        

    return render(Request,'forget-otp.html')



def CreateNewPassword(Request):
    if(Request.method=="POST"):
        password=Request.POST.get('password')
        cpassword=Request.POST.get('cpassword')
        username=Request.session.get('resetuser',None)
        if(username):
            if(password==cpassword):
                u=User.objects.get(username=username)
                u.set_password(password)
                u.save()
                return redirect("/login/")
            else:
              messages.error(Request,'''Password And Confirm Password Does't Match ''')        
        else:
            messages.error(Request,'Invalid User. Try Again')        
    return render(Request,'password.html')


@login_required(login_url='/login/')
def paymentSuccess(request,rppid,rpoid,rpsid):
    buyer = Buyer.objects.get(username=request.user)
    check = Checkout.objects.filter(user=buyer)
    check=check[::-1]
    check=check[0]
    check.rppid=rppid
    check.paymentmode=1
    # check.rpoid=rpoid
    # check.rpsid=rpsid
    check.paymentstatus=1
    check.save()
    return redirect('/confirmation/')
