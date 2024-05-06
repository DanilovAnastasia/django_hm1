from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView


from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


# Create your views here.
# def home(request):
#     context = {
#         'title': 'Главная',
#         'object_list': Product.objects.all(),
#     }
#     return render(request, 'catalog/home.html', context)

# class ProductListView(ListView):
#     model = Product
#     template_name = 'catalog/home.html'
#     extra_context = {
#         'title': 'Главная'
#     }


class ProductListView(ListView):
    """Класс для вывода страницы со всеми продуктами"""
    model = Product

    def get_context_data(self, *args, **kwargs):
        """Метод для получения версий Продукта и вывода только активной версии"""
        context = super().get_context_data(*args, **kwargs)
        products = self.get_queryset()
        for product in products:
            product.version = product.versions.filter(is_current=True).first()

        # Данная строчка нужна, чтобы в contex добавились новые данные о Продуктах
        context["object_list"] = products

        return context


# class ProductDetailView(DetailView):
#     model = Product
#     template_name = 'catalog/product.html'
#     extra_context = {
#         'title': 'Описание продукта'
#     }


# class ProductDetailView(DetailView):
#     """Класс для вывода страницы с одним продуктом по pk"""
#     model = Product
#
#     def get_object(self, queryset=None):
#         """Метод для настройки работы счетчика просмотра продукта"""
#         self.object = super().get_object(queryset)
#         self.object.view_count += 1
#         self.object.save()
#         return self.object

class ProductDetailView(DetailView):
    """Класс для вывода страницы с одним продуктом по pk"""
    model = Product

    def get_object(self, queryset=None):
        """Метод для настройки работы счетчика просмотра продукта"""
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        print(self.object.views_count)
        self.object.save()
        return self.object




class ProductCreateView(CreateView):
    model = Product
    # Добавляем формы. Заменяем fields на form_class
    # fields = ('name', 'description', 'preview', 'category', 'price')
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products_list')

    def get_context_data(self, **kwargs):
        """Метод для создания Формсета и настройки его работы"""
        context_data = super().get_context_data(**kwargs)

        # Создаем ФОРМСЕТ
        # В агрументах прописывается только форма для модели Версия,
        # так как в этом классе form_class = ProductForm уже был указан выше
        # Количество экземпляров, выводимое на страницу
        # instance говорит о том, откуда мы получаем информацию, нужен только для редактирования объекта,
        # для создания не обязателен,
        # extra=1 - означает, что будет выводиться только новая форма для заполнения
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST)

        else:
            context_data['formset'] = VersionFormset()

        return context_data

    def form_valid(self, form):
        """Метод для проверки валидации формы и формсета"""
        context_data = self.get_context_data()
        formset = context_data['formset']
        # Задаем условие, при котором д.б. валидными и форма и формсет
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            # save() данная функция сохраняет внесенные изменения
            formset.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


# def contacts(request):
#     context = {
#         'title': 'Контакты'
#     }
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')
#         print(f'{name} ({email}): {message}')
#     return render(request, 'catalog/contacts.html', context)

class ContactsPageView(TemplateView):
    template_name = 'catalog/contacts.html'
    extra_context = {
        'title': 'Контакты'
    }

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            message = request.POST.get('message')
            print(f'{name} ({phone}): {message}')

        return render(request, 'catalog/contacts.html', context=self.extra_context)


# def product(request, pk):
#     context = {
#         'object': Product.objects.get(pk=pk),
#         'title': 'Описание продукта'
#     }
#     return render(request, 'catalog/product.html', context)


class ProductUpdateView(UpdateView):
    model = Product
    # Добавляем формы. Заменяем fields на form_class
    # fields = ('name', 'description', 'preview', 'category', 'price')
    form_class = ProductForm

    def get_success_url(self):
        """ Метод для определения пути, куда будет совершен переход после редактирования продкута"""
        return reverse('catalog:product_detail', args=[self.get_object().pk])
        # ранее было args=[self.kwargs.get('pk')]

    def get_context_data(self, **kwargs):
        """Метод для создания Формсета и настройки его работы"""
        context_data = super().get_context_data(**kwargs)
        # В агрументах прописывается только форма для модели Версия,
        # так как в этом классе form_class = ProductForm уже был указан выше
        # Количество экземпляров, выводимое на страницу
        # instance говорит о том, откуда мы получаем информацию, нужен только для редактирования объекта,
        # для создания не обязателен,
        # extra=1 - означает, что будет выводиться только новая форма для заполнения
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)

        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)

        else:
            context_data['formset'] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        """Метод для проверки валидации формы и формсета"""
        context_data = self.get_context_data()
        formset = context_data['formset']
        # Задаем условие, при котором д.б. валидными и форма и формсет
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            # save() данная функция сохраняет внесенные изменения
            formset.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products_list')