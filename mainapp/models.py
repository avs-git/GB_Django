from django.db import models
from django.utils.functional import cached_property


class Category(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    parent = models.ForeignKey('self', default=None, null=True, blank=True, related_name='nested_category',
                               on_delete=models.DO_NOTHING)
    nesting_level = models.IntegerField(default=0)
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    image_preview = models.ImageField(verbose_name='Картинка категории. Preview', upload_to='products_images/preview',
                                      blank=True)
    image = models.ImageField(verbose_name='Картинка категории', upload_to='products_images/preview', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True, db_index=True)

    def child_products(self):
        return Product.objects.filter(category=self).count()

    def get_childs(self):
        return Category.objects.filter(parent=self)

    @cached_property
    def get_cached_active_categories(self):
        return Category.objects.all().select_related()

    def __str__(self):
        return self.name


# class SubCategory(models.Model):
#     class Meta:
#         verbose_name = 'Подкатегория'
#         verbose_name_plural = 'Подкатегории'
#
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     name = models.CharField(verbose_name='имя подкатегории', max_length=128)
#     description = models.TextField(verbose_name='описание подкатегории', blank=True)
#     image_preview = models.ImageField(verbose_name='Preview/ подкатегории', upload_to='products_images/preview',
#                                       blank=True)
#     image = models.ImageField(verbose_name='Картинка подкатегории', upload_to='products_images/preview', blank=True)
#     is_active = models.BooleanField(verbose_name='активна', default=True)
#
#     def get_id(self):
#         return self.pk
#
#     def __str__(self):
#         return f"{self.name} ({self.category.name})"


class Product(models.Model):
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='имя продукта', max_length=128)
    image = models.ImageField(verbose_name='Изображение товара', upload_to='products_images', blank=True)
    image_preview = models.ImageField(verbose_name='Preview', upload_to='products_images/preview', blank=True)
    short_desc = models.CharField(verbose_name='краткое описание продукта', max_length=60, blank=True)
    description = models.TextField(verbose_name='описание продукта', blank=True)
    price = models.DecimalField(verbose_name='цена продукта', max_digits=8, decimal_places=2, default=0, db_index=True)
    SKU = models.CharField(verbose_name='Артикул', max_length=25, blank=True)
    quantity = models.PositiveIntegerField(verbose_name='количество на складе', default=0)
    is_active = models.BooleanField(verbose_name='активно', default=True, db_index=True)

    def get_id(self):
        return self.pk

    def __str__(self):
        return f"{self.name}({self.category.name}))"

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')


    @staticmethod
    def get_price(self):
        product = Product.objects.filter(pk=self.pk).select_related().first()
        return product.price
