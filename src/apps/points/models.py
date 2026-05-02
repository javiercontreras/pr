from django.contrib.gis.db import models as gis_models
from django.db import models
from apps.companies.models import Company


class WasteCategory(models.Model):
    """Categoría principal: Plástico, Vidrio, Papel, Metal, Orgánico"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    code = models.CharField(max_length=10, unique=True, verbose_name="Código")
    description = models.TextField(blank=True, verbose_name="Descripción")
    color_hex = models.CharField(max_length=7, default="#00AA00", verbose_name="Color en mapa")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Categoría de residuo"
        verbose_name_plural = "Categorías de residuo"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"  


class WasteSubcategory(models.Model):
    """
    Subcategoría de residuo.
    Ejemplo:
      Categoría: Plástico (PLA)
        Subcategoría: PET transparente (PET-T)
        Subcategoría: PET color (PET-C)
      Categoría: Vidrio (VID)
        Subcategoría: Vidrio transparente (VID-T)
        Subcategoría: Vidrio color (VID-C)
    """
    category = models.ForeignKey(
        WasteCategory,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Categoría",
    )
    name = models.CharField(max_length=100, verbose_name="Nombre")
    code = models.CharField(max_length=20, unique=True, verbose_name="Código")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Subcategoría de residuo"
        verbose_name_plural = "Subcategorías de residuo"
        ordering = ["category", "name"]

    def __str__(self):
        return f"{self.name} ({self.code})" 


class RecyclingPoint(gis_models.Model):
    """Lugar físico donde se ubican uno o más contenedores de reciclaje."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        INACTIVE = "inactive", "Inactivo"
        MAINTENANCE = "maintenance", "En mantención"

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="recycling_points",
        verbose_name="Empresa",
    )
    name = models.CharField(max_length=200, verbose_name="Nombre")
    address = models.CharField(max_length=300, verbose_name="Dirección")
    location = gis_models.PointField(
        geography=True,
        srid=4326,
        verbose_name="Ubicación GPS",
    )
    schedule = models.CharField(max_length=300, blank=True, verbose_name="Horario")
    image = models.ImageField(
        upload_to="recycling_points/",
        null=True,
        blank=True,
        verbose_name="Imagen",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Estado",
    )
    notes = models.TextField(blank=True, verbose_name="Notas internas")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Punto de reciclaje"
        verbose_name_plural = "Puntos de reciclaje"
        ordering = ["company", "name"]

    def __str__(self):
        return self.name  

    @property
    def latitude(self):
        return self.location.y if self.location else None

    @property
    def longitude(self):
        return self.location.x if self.location else None

    @property
    def total_containers(self):
        return self.containers.count()


class Container(models.Model):
    """
    Contenedor físico dentro de un punto de reciclaje.
    Puede aceptar uno o más subcategorías de residuo.
    """
    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        INACTIVE = "inactive", "Inactivo"
        MAINTENANCE = "maintenance", "En mantención"

    recycling_point = models.ForeignKey(
        RecyclingPoint,
        on_delete=models.CASCADE,
        related_name="containers",
        verbose_name="Punto de reciclaje",
    )
    waste_subcategories = models.ManyToManyField(
        WasteSubcategory,
        related_name="containers",
        blank=True,
        verbose_name="Tipos de residuo",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre",
        help_text="Ej: Contenedor multireciclaje 1",
    )
    capacity_liters = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Capacidad (litros)",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Estado",
    )
    image = models.ImageField(
        upload_to="containers/",
        null=True,
        blank=True,
        verbose_name="Imagen",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contenedor"
        verbose_name_plural = "Contenedores"
        ordering = ["recycling_point", "name"]

    def __str__(self):
        return self.name  # 
