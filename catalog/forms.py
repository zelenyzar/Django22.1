from django import forms
from .models import Product

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]

def _check_forbidden_words(text: str, field_name: str) -> None:
    if not text:
        return
    text_str = str(text)
    text_lower = text_str.lower()
    for word in FORBIDDEN_WORDS:
        if word in text_lower:
            raise forms.ValidationError(
                f"В поле '{field_name}' запрещено использовать слово '{word}'."
            )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "price"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_classes = "form-control shadow-sm"
        textarea_classes = f"{base_classes} rows=4"
        number_classes = f"{base_classes} text-start"

        self.fields["name"].widget.attrs.update({
            "class": base_classes,
            "placeholder": "Введите наименование продукта",
            "autocomplete": "off",
        })
        self.fields["description"].widget.attrs.update({
            "class": textarea_classes,
            "placeholder": "Описание продукта (без запрещённых слов)",
        })
        self.fields["image"].widget.attrs.update({
            "class": "form-control",
            "accept": "image/*",
        })
        self.fields["category"].widget.attrs.update({
            "class": "form-select",
        })
        self.fields["price"].widget.attrs.update({
            "class": number_classes,
            "step": "1",
            "min": "0",
            "placeholder": "0",
        })

    def clean_name(self):
        name = self.cleaned_data.get("name")
        _check_forbidden_words(name, "наименование")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if description is None:
            description = ""
        _check_forbidden_words(description, "описание")
        return description

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price
