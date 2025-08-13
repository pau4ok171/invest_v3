import asyncio
import json
from typing import Optional, TypeGuard

import decouple

from dataclasses import asdict

from tinkoff.invest import AsyncClient, Page
from tinkoff.invest.async_services import AsyncServices
from tinkoff.invest.schemas import PageResponse

TOKEN = decouple.config('TINKOFF_KEY')


class TinkoffService:
    def __init__(self):
        self.services: Optional[AsyncServices] = None
        self._client: Optional[AsyncClient] = None

    async def __aenter__(self):
        self._client = AsyncClient(TOKEN)
        self.services = await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.__aexit__(exc_type, exc_val, exc_tb)
        self.services = None
        self._client = None


    def _check_services_initialization(self) -> TypeGuard[AsyncServices]:
        if self.services is None:
            raise RuntimeError('Services not initialized. Use async context manager')
        return True

    async def get_brands(self):
        if not self._check_services_initialization():
            return

        brands = []
        for i in range(0, 67): # 6592/100=67
            brands_response = await self.services.instruments.get_brands(
                paging=Page(limit=100, page_number=i)
            )
            brands.extend(brands_response.brands)

        brands_dicts = [asdict(brand) for brand in brands]

        with open('brands.json', 'w', encoding='utf-8') as f:
            json.dump(brands_dicts, f, ensure_ascii=False, indent=2)

        print(f'Успешно сохранено {len(brands)} брендов в brands.json')

    async def get_brands_pagination(self) -> Optional[PageResponse]:
        if not self._check_services_initialization():
            return

        result = await self.services.instruments.get_brands()
        paging = result.paging

        return paging

    async def get_asset_info(self):
        if not self._check_services_initialization():
            return

        result = await self.services.instruments.get_brands_by(id='83904d0e-7864-46bd-9495-a462fcc680a7')
        return result


    async def main(self):
        pass


async def main():
    async with TinkoffService() as service:
        result = await service.get_asset_info()
        print(result)

if __name__ == '__main__':
    asyncio.run(main())