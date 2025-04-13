from django.shortcuts import redirect
from django.conf import settings
from django.views.generic import View, ListView
from base.models import Item
from collections import OrderedDict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class CartListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'pages/cart.html'

    def get_queryset(self):
        cart = self.request.session.get('cart', None)
        if not cart or not cart.get('items'):
            return Item.objects.none()  # 安全に空リスト返す

        queryset = []
        total = 0
        for item_pk, quantity in cart['items'].items():
            try:
                obj = Item.objects.get(pk=item_pk)
            except Item.DoesNotExist:
                continue  # 存在しない item は無視する
            obj.quantity = quantity
            obj.subtotal = int(obj.price * quantity)
            queryset.append(obj)
            total += obj.subtotal

        tax_included_total = int(total * (settings.TAX_RATE + 1))

        # カート情報をセッションに更新
        cart['total'] = total
        cart['tax_included_total'] = tax_included_total
        self.request.session['cart'] = cart

        # 取得した queryset を返す
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # カートの合計情報をコンテキストに追加
        cart = self.request.session.get('cart', {})
        context["total"] = cart.get('total', 0)
        context["tax_included_total"] = cart.get('tax_included_total', 0)
        
        return context


class AddCartView(LoginRequiredMixin, View):

    # # getメソッドではトップへリダイレクトする場合はこのようにかけます。
    # def get(self, request):
    #     return redirect('/')
    
    def post(self, request):
        item_pk = request.POST.get('item_pk')
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', None)
        if cart is None or len(cart) == 0:
            items = OrderedDict()
            cart = {'items': items}
        if item_pk in cart['items']:
            cart['items'][item_pk] += quantity
        else:
            cart['items'][item_pk] = quantity
        request.session['cart'] = cart
        return redirect('/cart/')


@login_required
def remove_from_cart(request, pk):
    cart = request.session.get('cart', None)
    if cart is not None:
        del cart['items'][pk]
        request.session['cart'] = cart
    return redirect('/cart/')