from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return '{}'.format(self.title)


class Currency(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    show_title = models.CharField(max_length=255, verbose_name='Отображаемое название')

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"

    def __str__(self):
        return '{} {}'.format(self.title, self.show_title)


class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание товара')
    img = models.ImageField(upload_to='img')
    price = models.DecimalField(max_digits=11, decimal_places=2)
    currency = models.ForeignKey(Currency, related_name='currency_products', blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, related_name='category_products', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return '{} {} {} {} {}'.format(self.title, self.description, self.img, self.price, self.currency)


class Order(models.Model):
    telegram_id = models.CharField(max_length=255, verbose_name='ID телеграм пользователя')
    product = models.ForeignKey(Product, related_name='product_orders', blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return '{} {}'.format(self.telegram_id, self.product)


