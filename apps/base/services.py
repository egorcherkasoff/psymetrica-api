from django.core.exceptions import ValidationError
from PIL import Image


def validate_image(image):
    """проверка на изображения на валидность"""
    print("cheching img")
    try:
        img = Image.open(image)
        img.verify()
    except:
        raise ValidationError("Неверный формат изображения.")


def sort_by_number(model, queryset, start_number):
    """сортировка сущностей по number и массовое обновление"""
    sorted = []

    for idx, obj in enumerate(queryset, start=start_number):
        obj.number = idx
        sorted.append(obj)
    model.objects.bulk_update(sorted, ["number"])
