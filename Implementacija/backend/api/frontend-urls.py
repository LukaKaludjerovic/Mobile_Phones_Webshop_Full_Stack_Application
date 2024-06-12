"""
author: Luka Mladenovic 0108-2021
author: Andrija Gajic 0033-2021
author: Luka Kaludjerovic 0041-2021
"""

from django.urls import path
from .views import index, render_about, render_login, new_customer, shop, payment, order, new_reseller, contact, dashboard_customer, dashboard_reseller, dashboard_admin, product, cart, delivery
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("", index, name="render_home"),
    path("about", render_about, name="render_about"),
    path("home", index, name="render_home"),
    path("login", render_login, name="render_login"),
    path("new-customer", new_customer, name="render_new_customer"),
    path("new-reseller", new_reseller, name="render_new_reseller"),
    path("order", order, name="render_order"),
    path("payment", payment, name="render_payment"),
    path("shop", shop, name="render_shop"),
    path("contact", contact, name="render_contact"),
    path("cart", cart, name="render_cart"),
    path("delivery", delivery, name="render_delivery"),
    path("product", product, name="render_product"), 
    path("dashboard-customer", dashboard_customer, name="render_dashboard_customer"),
    path("dashboard-reseller", dashboard_reseller, name="render_dashboard_reseller"),
    path("dashboard-admin", dashboard_admin, name="render_dashboard_admin")

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
