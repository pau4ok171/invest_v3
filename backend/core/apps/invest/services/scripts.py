import asyncio
from pathlib import Path
import os
import glob

from asgiref.sync import sync_to_async
from django.conf import settings
from django.core.files import File
from googletrans import Translator

from apps.invest.models import Company


def upload_images_to_companies():
    path_to_folder = Path('C:\\Users\\pau4o\\Downloads\\Finargo\\company_logos')
    companies = Company.objects.all()
    for company in companies:
        if not company.logo.name == 'companies/logos/default.png':
            continue

        image_path_pattern = f'{path_to_folder}/{company.slug}_*'
        matching_files = glob.glob(image_path_pattern)

        if not len(matching_files):
            continue

        file_path = matching_files[0]
        file_name = os.path.basename(file_path)
        with open(file_path, 'rb') as f:
            company.logo.save(f'{company.ticker}_{file_name}', File(f))


def get_company_description(company: Company, lang_code: str) -> str:
    company.set_current_language(lang_code)
    return company.description


def save_company_translation(
    company: Company,
    lang_code: str,
    translated_text: str
) -> None:
    company.set_current_language(lang_code)
    company.description = translated_text
    company.save()


async def translate_company_description(
    company: Company,
    lang_code: str,
    desc_ru: str,
    translator: Translator
):
    try:
        translated = await translator.translate(desc_ru, dest=lang_code, src='ru')
        await sync_to_async(save_company_translation)(company, lang_code, translated.text)

    except Exception as e:
        print(f'Error on translation for {company.ticker} ({lang_code}): {e}')


async def process_company(company: Company, translator: Translator):
    desc_ru = await sync_to_async(get_company_description)(company, 'ru')

    if not desc_ru:
        return

    for lang_code, _ in settings.LANGUAGES:
        if lang_code == 'ru':
            continue

        desc_target = await sync_to_async(get_company_description)(company, lang_code)
        if desc_target:
            continue

        await translate_company_description(company, lang_code, desc_ru, translator)


async def translate_description_field():
    async with Translator() as translator:
        companies = (company async for company in Company.objects.all())
        await asyncio.gather(*(process_company(c, translator) for c in companies))


def set_translated_fields_from_en():
    companies = Company.objects.all()
    for company in companies:
        company.set_current_language('en')
        title = company.title
        desc = company.description
        short_title = company.short_title

        if not company.short_title_genitive:
            company.short_title_genitive = short_title
            company.save()
        short_title_genitive = company.short_title_genitive

        for lang_code, _ in settings.LANGUAGES:
            if lang_code == 'en':
                continue

            company.set_current_language(lang_code)
            if not company.title:
                company.title = title
            if not company.description:
                company.description = desc
            if not company.short_title:
                company.short_title = short_title
            if not company.short_title_genitive:
                if lang_code == 'ru':
                    company.short_title_genitive = company.short_title
                else:
                    company.short_title_genitive = short_title_genitive
            company.save()


if __name__ == '__main__':
    # upload_images_to_companies()
    # asyncio.run(translate_description_field())
    # set_translated_fields_from_en()
    pass
