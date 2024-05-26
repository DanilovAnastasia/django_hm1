from django.forms import inlineformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView


from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version


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


# Добавляем миксин LoginRequiredMixin, чтобы неавторизованные Пользователи не смогли зайти
# на данный инпоинт (точка входа)
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("catalog:products_list")

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
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )

        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(self.request.POST)

        else:
            context_data["formset"] = VersionFormset()

        return context_data

    def form_valid(self, form):
        """Метод для проверки валидации формы и формсета"""
        context_data = self.get_context_data()
        formset = context_data["formset"]
        # Задаем условие, при котором д.б. валидными и форма и формсет
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            # save() данная функция сохраняет внесенные изменения
            formset.save()
            # Добавлено для автоматического привязывания Пользователя к продукту
            # (ранее было вынесено в отдельный form_valid)
            self.object = form.save()
            self.object.author = self.request.user
            self.object.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


# Добавляем миксин LoginRequiredMixin, чтобы неавторизованные Пользователи не смогли зайти
# на данный инпоинт (точка входа)
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_form_class(self):
        """Метод возвращающий форму для отображения в контроллере в зависимости от группы Пользователя"""
        # Получаем пользователя
        user = self.request.user
        # 1-й вариант: может быть использовано, когда есть только ожна группа Модератор, без подгрупп
        # if user.groups.filter(name='moderator').exists:
        #     return ProductModeratorForm
        # 2-й вариант:
        perms = ("catalog.set_published", "catalog.change_description", "catalog.change_category")
        if user == self.object.author:
            return ProductForm

        if user.has_perms(perms):
            return ProductModeratorForm

        raise HttpResponseForbidden

    def get_success_url(self):
        """Метод для определения пути, куда будет совершен переход после редактирования продкута"""
        return reverse("catalog:product_detail", args=[self.get_object().pk])
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
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )

        if self.request.method == "POST":
            context_data["formset"] = VersionFormset(
                self.request.POST, instance=self.object
            )

        else:
            context_data["formset"] = VersionFormset(instance=self.object)

        return context_data

    def form_valid(self, form):
        """Метод для проверки валидации формы и формсета"""
        context_data = self.get_context_data()
        formset = context_data["formset"]
        # Задаем условие, при котором д.б. валидными и форма и формсет
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            # save() данная функция сохраняет внесенные изменения
            formset.save()
            return super().form_valid(form)

        else:
            return self.render_to_response(
                self.get_context_data(form=form, formset=formset)
            )


# Добавляем миксин LoginRequiredMixin, чтобы неавторизованные Пользователи не смогли зайти
# на данный инпоинт (точка входа)
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy("catalog:products_list")