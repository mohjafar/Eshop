from django import template
from Mainapp.models import Checkout,CheckoutProduct,Product
register=template.Library()

@register.filter(name="checkoutProducts")
def checkoutProduct(checkoutid):
    checkout=Checkout.objects.get(id=checkoutid)
  
    cp=CheckoutProduct.objects.filter(checkout=checkout)
    c=[]
    for item in cp:
        x={'name':item.p.name,'maincategory':item.p.maincategory,'subcategory':item.p.subcategory,'brand':item.p.brand,'color':item.p.color,'size':item.p.size,'price':item.p.finalprice,'qty':item.qty,'total':item.total,'pic':item.p.pic1.url}
        c.append(x)
    return c

@register.filter(name="PaymenyStatus")
def payment(op):
    if(op==0):   
        return "Pending"
    else:
        return "Done"
    
@register.filter(name="PaymentMode")    
def PaymentMode(op):
    if(op==0):  
        return "COD" 
    else:
        return "Net Banking"
    
@register.filter(name="OrderStatus")
def OrderStatu(op):
    if(op==0):
        return "Order Place"
    elif(op==1):
        return "Not Packed"
    elif(op==2):
        return "Packed"
    elif(op==3):
        return "Ready To Shipped"
    elif(op==4):
        return "Shipped"
    elif(op==5):
        return "Out For Delivery"
    elif(op==6):
        return "Delivered"
    else:
        return "Cancelled"




