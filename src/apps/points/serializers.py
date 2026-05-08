from rest_framework import serializers
from .models import Container, WasteSubcategory, WasteCategory, RecyclingPoint


class WasteCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WasteCategory
        fields = ["id", "name", "code", "color_hex"]


class WasteSubcategorySerializer(serializers.ModelSerializer):
    category = WasteCategorySerializer(read_only=True)

    class Meta:
        model = WasteSubcategory
        fields = ["id", "name", "code", "material_code", "icon_name", "icon_color", "is_rep", "category"]


class ContainerSerializer(serializers.ModelSerializer):
    waste_subcategories = WasteSubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Container
        fields = [
            "id",
            "name",
            "container_type",
            "status",
            "fill_level",
            "last_fill_update",
            "last_collection",
            "capacity_liters",
            "required_state",
            "waste_subcategories",
            "recycling_point",
        ]