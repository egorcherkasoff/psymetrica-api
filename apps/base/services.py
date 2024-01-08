from django.core.exceptions import ValidationError
from PIL import Image


def validate_image(image):
    """проверка на изображения на валидность"""
    try:
        img = Image.open(image)
        img.verify()
    except:
        raise ValidationError("Неверный формат изображения.")


# TODO: FIX SORT
def sort_by_number(model, queryset):
    """сортировка сущностей по number и массовое обновление"""
    sorted = []

    for idx, obj in enumerate(queryset):
        print(idx)
        obj.number = idx + 1
        sorted.append(obj)
    model.objects.bulk_update(sorted, ["number"])
