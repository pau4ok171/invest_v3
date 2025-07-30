from apps.invest.models import Company

class CompanyService:
    @staticmethod
    def get_peers(company: Company, limit: int = 4):
        peers = Company.objects.filter(is_visible=True).exclude(pk=company.id)
        return sorted(peers, key=lambda x: CompanyService._get_sort_score(x, company), reverse=True)[:limit]

    @staticmethod
    def _get_sort_score(peer_company: Company, target_company: Company):
        country_score = 4 if peer_company.country == target_company.country else 3
        sector_score = 4 if peer_company.sector == target_company.sector else 2
        return country_score + sector_score