from django.contrib.gis.db import models as gis_models
from django.db import models
from apps.companies.models import Company
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class WasteCategory(models.Model):
    """Categoría principal: Plástico, Vidrio, Papel, Metal, Orgánico"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    code = models.CharField(max_length=10, unique=True, verbose_name="Código")
    description = models.TextField(blank=True, verbose_name="Descripción")
    color_hex = models.CharField(max_length=7, default="#00AA00", verbose_name="Color en mapa")


    class Meta:
        verbose_name = "Categoría de residuo"
        verbose_name_plural = "Categorías de residuo"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.code})"  

class WasteSubcategory(models.Model):
    category = models.ForeignKey(
        WasteCategory,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Categoría",
    )
    name = models.CharField(max_length=100, verbose_name="Nombre")
    code = models.CharField(max_length=20, unique=True, verbose_name="Código")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_rep = models.BooleanField(
        default=False,
        verbose_name="Categoría REP",
    )
    material_code = models.CharField(
    max_length=10,
    blank=True,
    verbose_name="Código de material",
    help_text="Ej: 1 (PET), 2 (HDPE), ALU (Aluminio), GL (Vidrio), PAP (Papel)",
)

    # Nombre del icono en Material Icons o FontAwesome
    # Ej: "delete_outline", "recycling", "battery_alert"
    icon_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Nombre de icono",
        help_text="Nombre del icono en Material Icons. Ej: 'recycling', 'water_drop'",
    )
    # Color del icono en hex — puede diferir del color de la categoría padre
    icon_color = models.CharField(
        max_length=7,
        default="#00AA00",
        verbose_name="Color del icono",
        help_text="Hexadecimal, ej: #1565C0",
    )

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

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

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



class Container(models.Model):
    """
    Receptáculo específico para un tipo de residuo en un Punto de Reciclaje.
    """

    class Status(models.TextChoices):
        ACTIVE = "active", "Activo"
        INACTIVE = "inactive", "Inactivo"
        MAINTENANCE = "maintenance", "En mantención"


    class ContainerType(models.TextChoices):
        STANDARD = "standard", "Contenedor Estándar (Tacho)"
        COMPOST = "compost", "Compostera / Vermicompostera"
        SPECIFIC = "specific", "Contenedor Específico (Ej: Neumáticos)"
        HAZARDOUS = "hazardous", "Contenedor Autorizado (Aceites/Peligrosos)"
   

    # Relaciones
    recycling_point = models.ForeignKey(
        'RecyclingPoint', 
        on_delete=models.CASCADE, 
        related_name="containers",
        verbose_name="Punto de reciclaje"
    )
    
    waste_subcategories = models.ManyToManyField(
    'WasteSubcategory',
    blank=True,
    verbose_name="Subcategorías de residuo",
    )

    # Atributos
    name = models.CharField(
    max_length=100,
    blank=True,
    verbose_name="Nombre",
    help_text="Ej: Contenedor PET 1",
)
    fill_level = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Nivel de llenado actual (0% a 100%)",
        verbose_name="Nivel de llenado"
    )

    last_fill_update = models.DateTimeField(
        auto_now=True,
        null=True,
        verbose_name="Última actualización de nivel"
    )
    container_type = models.CharField(
        max_length=20,
        choices=ContainerType.choices,
        default=ContainerType.STANDARD,
        verbose_name="Tipo de contenedor"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Estado del contenedor"
    )

    required_state = models.CharField(
        max_length=200, 
        help_text="Ej: Limpio, seco y en botellas cerradas",
        blank=True,
        verbose_name="Estado requerido del residuo"
    )

    capacity_liters = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        verbose_name="Capacidad (Litros)"
    )

    last_collection = models.DateTimeField(
        null=True, 
        blank=True, 
        verbose_name="Último retiro"
    )

    class Meta:
        verbose_name = "Contenedor"
        verbose_name_plural = "Contenedores"

    def __str__(self):
     return self.name or f"Contenedor {self.pk}"
