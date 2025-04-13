from django.contrib import admin
from django.contrib.auth.models import Group
 
from base.models import Item, Tag, Category, User, Profile, Order
from django.contrib.auth.admin import UserAdmin
from base.forms import UserCreationForm
 
from django import forms  # 追記
import json  # 追記
 
 
class TagInline(admin.TabularInline):
    model = Item.tags.through
 
 
class ItemAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    exclude = ['tags']
 
 
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
 
 
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        (None, {'fields': ('is_active', 'is_admin',)})
    )
 
    list_display = ('username', 'email', 'is_active',)
    list_filter = ()
    ordering = ()
    filter_horizontal = ()
 
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
    )
 
    add_form = UserCreationForm
    inlines = (ProfileInline,)
 
 
class CustomJsonField(forms.JSONField):  # 追記
    def prepare_value(self, value):  # 追記
        loaded = json.loads(value)  # 追記
        return json.dumps(loaded, indent=2, ensure_ascii=False)  # 追記
 
 
class OrderAdminForm(forms.ModelForm):  # 追記
    items = CustomJsonField()  # 追記
    shipping = CustomJsonField()  # 追記
 
 
class OrderAdmin(admin.ModelAdmin):  # 追記
    form = OrderAdminForm  # 追記
 
 
admin.site.register(Order, OrderAdmin)  # OrderAdminを追記
admin.site.register(Item, ItemAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)