from organizations.dtos import SiteCreateDTO, SiteUpdateDTO
from organizations.models import Site
from organizations.repositories import SiteRepository


class SiteService:
    def __init__(self):
        self.repository = SiteRepository()

    def create_site(self, dto: SiteCreateDTO) -> Site:
        if self.repository.exists(country_id=dto.country_id, name=dto.name):
            raise ValueError("A site with this name already exists.")
        return self.repository.create(
            country_id=dto.country_id,
            name=dto.name,
            site_type=dto.site_type,
            email=dto.email,
            phone=dto.phone,
            address=dto.address,
            city=dto.city,
            postal_code=dto.postal_code,
            latitude=dto.latitude,
            longitude=dto.longitude,
        )

    def update_site(self, site: Site, dto: SiteUpdateDTO) -> Site:
        if Site.objects.exclude(pk=site.pk).filter(
            country_id=dto.country_id, name=dto.name
        ).exists():
            raise ValueError("A site with this name already exists.")
        return self.repository.update(
            site,
            country_id=dto.country_id,
            name=dto.name,
            site_type=dto.site_type,
            email=dto.email,
            phone=dto.phone,
            address=dto.address,
            city=dto.city,
            postal_code=dto.postal_code,
            latitude=dto.latitude,
            longitude=dto.longitude,
            is_active=dto.is_active,
        )

    def delete(self, site: Site):
        self.repository.delete(site)

    def get(self, pk):
        return self.repository.get(pk)
