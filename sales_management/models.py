from django.db import models
from admin_panel.models import User

class Order(models.Model):
    user_created = models.ForeignKey(User, related_name='user', on_delete=models.DO_NOTHING)
    title = models.CharField('Назва замовлення', max_length=64)
    description = models.TextField('Опис', max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

class OrderFiles(models.Model):
    order_model = models.ForeignKey(Order, related_name='order_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')

order_status = (
    (1, 'Перегяд'),
    (2, 'Надіслана калькуляція'),
    (3, 'В процесі'),
    (4, 'Готово'),
    (5, 'Відхилено'),
    (6, 'Скасовано користувачем')
)

class TakenOrder(models.Model):
    order = models.ForeignKey(Order, related_name='order', on_delete=models.CASCADE)
    manager = models.ForeignKey(User, related_name='manager', on_delete=models.DO_NOTHING, default=1)
    status = models.SmallIntegerField(default=1, verbose_name='Статус:', choices=order_status)
    taken_at = models.DateTimeField(auto_now_add=True)
    response = models.TextField(verbose_name='Відповідь:', max_length=200, default='Немає відповіді')