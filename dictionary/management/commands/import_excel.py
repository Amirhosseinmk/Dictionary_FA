from django.core.management.base import BaseCommand
import pandas as pd
from dictionary.models import Word, Definition

class Command(BaseCommand):
    help = 'Import vocabulary from Excel file'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='Path to the Excel file')
        parser.add_argument('--sheet', type=str, default='Sheet1', help='Worksheet name')
        parser.add_argument('--word-col', type=int, default=0, help='Column index for word (0-based)')
        parser.add_argument('--def-col', type=int, default=1, help='Column index for definition (0-based)')
        parser.add_argument('--no-header', action='store_true', help='Treat first row as data (no header row)')

    def handle(self, *args, **options):
        excel_file = options['excel_file']
        sheet = options['sheet']
        word_col = options['word_col']
        def_col = options['def_col']
        no_header = options['no_header']
        header = None if no_header else 0

        try:
            df = pd.read_excel(excel_file, sheet_name=sheet, header=header)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error reading Excel file: {e}'))
            return

        if word_col >= len(df.columns) or def_col >= len(df.columns):
            self.stdout.write(self.style.ERROR(f'Column indices {word_col} or {def_col} out of range. Available columns: {len(df.columns)}'))
            return

        words_to_create = []
        definitions_to_create = []
        word_texts = set()

        for index, row in df.iterrows():
            word_text = str(row.iloc[word_col]).strip()
            def_text = str(row.iloc[def_col]).strip()

            if not word_text or not def_text or word_text.lower() in ['nan', 'none']:
                continue  # skip empty rows

            word_texts.add(word_text)

        # Get existing words
        existing_words = set(Word.objects.filter(text__in=word_texts).values_list('text', flat=True))
        new_word_texts = word_texts - existing_words

        # Create new words
        words_to_create = [Word(text=text) for text in new_word_texts]
        Word.objects.bulk_create(words_to_create)

        # Now create definitions
        word_dict = {word.text: word for word in Word.objects.filter(text__in=word_texts)}

        for index, row in df.iterrows():
            word_text = str(row.iloc[word_col]).strip()
            def_text = str(row.iloc[def_col]).strip()

            if not word_text or not def_text or word_text.lower() in ['nan', 'none']:
                continue

            word = word_dict[word_text]
            definition = Definition(word=word, text=def_text, order=1)
            definitions_to_create.append(definition)

        Definition.objects.bulk_create(definitions_to_create)

        self.stdout.write(self.style.SUCCESS(f'Created {len(words_to_create)} new words.'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(definitions_to_create)} definitions.'))
        self.stdout.write(self.style.SUCCESS('Import completed.'))