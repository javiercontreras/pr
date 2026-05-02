from django.db import models

# Create your models here.
class Container(models.Model):

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
    waste_categories = models.ManyToManyField(
        WasteCategory,
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
        return f"{self.name} — {self.recycling_point.name}"