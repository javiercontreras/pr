from django.db import models

# Create your models here.
class Company(models.Model):

    class CompanyType(models.TextChoices):
        MUNICIPALITY = "municipality", "Municipio"
        PRIVATE = "private", "Empresa privada"
        NGO = "ngo", "ONG"

    name = models.CharField(max_length=200, verbose_name="Nombre")
    rut = models.CharField(max_length=20, unique=True, verbose_name="RUT")
    company_type = models.CharField(
        max_length=20,
        choices=CompanyType.choices,
        default=CompanyType.PRIVATE,
        verbose_name="Tipo de empresa",
    )
    address = models.CharField(max_length=300, blank=True, verbose_name="Dirección")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Email de contacto")
    billing_email = models.EmailField(blank=True, verbose_name="Email de facturación")
    billing_address = models.CharField(max_length=300, blank=True, verbose_name="Dirección de facturación")
    logo = models.ImageField(upload_to="companies/logos/", null=True, blank=True, verbose_name="Logo")
    is_active = models.BooleanField(default=True, verbose_name="Activa")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"
        ordering = ["name"]

    def __str__(self):
        return self.name