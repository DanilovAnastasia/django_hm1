from django.core.exceptions import ValidationError
from django.forms import ModelForm, BooleanField

from catalog.models import Product, Version


# Данный класс создаем для стилизации форм, Это Mixin, класс ни от чего не наследуется
class StyleFormMixin:
    """Класс для стилизации форм"""

    # Переопределяем метод __init__
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Так как мы получаем словарь, для выведения обоих значение (value| key) применяем значение items()
        for field_name, field in self.fields.items():
            # Задаем условия - если у поля Булевое значение
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, ModelForm):
    """Класс для создание форм для модели Продукт"""
    banned_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

    class Meta:
        model = Product
        fields = ('name', 'description', 'photo', 'category', 'price')
        # fields = '__all__'  # Использование всех полей модели
        # fields = ('first_name',)  # Использование только перечисленных полей
        # exclude = ('last_name',)  # Использование всех полей, кроме перечисленных
        # Описан может быть только один из вариантов

    def clean_name(self):
        """Метод для проверки валидации имени Продукта при создании нового объекта"""
        cleaned_data = self.cleaned_data['name']
        if cleaned_data.lower() in self.banned_words:
            raise ValidationError(f'Слова, запрещенные к использованию в названии продукта: '
                                  f'{str(self.banned_words)[1:-2]}')
        return cleaned_data

    def clean_description(self):
        """Метод для проверки валидации описания Продукта при создании нового объекта"""
        cleaned_data = self.cleaned_data['description']
        if cleaned_data.lower() in self.banned_words:
            raise ValidationError(f'Слова, запрещенные к использованию в описании продукта: '
                                  f'{str(self.banned_words)[1:-2]}')
        return cleaned_data


class VersionForm(StyleFormMixin, ModelForm):
    """Класс для создание форм для модели Версия"""

    class Meta:
        model = Version
        fields = ('id', 'product', 'name', 'number', 'is_current')