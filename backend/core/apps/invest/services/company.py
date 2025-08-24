from apps.invest.models import Instrument


class ShareService:
    @staticmethod
    def get_peers(share: Instrument, limit: int = 4) -> list[Instrument]:
        peers = Instrument.objects.filter(instrument_type='share', company__is_visible=True).exclude(pk=share.id)
        return sorted(peers, key=lambda x: ShareService._get_sort_score(x, share), reverse=True)[:limit]

    @staticmethod
    def _get_sort_score(share: Instrument, target_share: Instrument):
        country_score = 4 if share.company.country == target_share.company.country else 3
        sector_score = 4 if share.company.sector == target_share.company.sector else 2
        return country_score + sector_score