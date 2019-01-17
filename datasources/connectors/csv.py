import csv
import json
import typing

from django.http import JsonResponse

import mongoengine
from mongoengine import context_managers

from .base import DataSetConnector


class CsvConnector(DataSetConnector):
    """
    Data connector for retrieving data from CSV files.
    """
    def get_metadata(self,
                     params: typing.Optional[typing.Mapping[str, str]] = None):
        """
        Return a JSON response from a CSV file.

        :param params: Query params - ignored
        :return: Metadata
        """
        with open(self.location, 'r') as csvfile:
            # Requires a header row
            reader = csv.DictReader(csvfile)
            return reader.fieldnames

    def get_response(self,
                     params: typing.Optional[typing.Mapping[str, str]] = None):
        """
        Return a JSON response from a CSV file.

        CSV file must have a header row with column titles.

        :param params: Optional query parameter filters
        :return: Requested data
        """
        try:
            with open(self.location, 'r') as csvfile:
                # Requires a header row
                reader = csv.DictReader(csvfile)

                if params is None:
                    params = {}

                rows = []
                for row in reader:
                    for key, value in params.items():
                        try:
                            if row[key].strip() != value.strip():
                                break

                        except KeyError:
                            # The filter field isn't in the data so no row can satisfy it
                            break

                    else:
                        # All filters match
                        rows.append(dict(row))

            return JsonResponse({
                'status': 'success',
                'data': rows,
            })

        except UnicodeDecodeError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid CSV file',
            }, status=500)


class CsvRow(mongoengine.DynamicDocument):
    """
    MongoDB dynamic document to store CSV data.
    """
    pass


class CsvToMongoConnector(DataSetConnector):
    @staticmethod
    def _type_convert(val):
        """
        Attempt to convert a value into a numeric type.

        :param val: Value to attempt to convert
        :return: Converted value or unmodified value if conversion was not possible
        """
        for t in (int, float):
            try:
                return t(val)

            except ValueError:
                pass

        return val

    @staticmethod
    def _flatten_params(params: typing.Optional[typing.Mapping[str, typing.List[str]]]):
        result = {}

        if params is None:
            return result

        for key, val_list in params.items():
            # TODO resolve duplicate param check
            if isinstance(val_list, list):
                raise ValueError('A query parameter was provided twice')

            result[key] = CsvToMongoConnector._type_convert(val_list[0])

        return result

    def clear(self):
        with context_managers.switch_collection(CsvRow, self.location) as CsvRowCollection:
            CsvRowCollection.objects.delete()

    def post_data(self, data: typing.Union[typing.MutableMapping[str, str],
                                           typing.List[typing.MutableMapping[str, str]]]):
        def add_row(row: typing.MutableMapping[str, str]):
            for k, v in row.items():
                row[k] = self._type_convert(v)

            if 'id' in row:
                row['x_id'] = row.pop('id')

            CsvRowCollection(**row).save()

        # Put data in collection belonging to this data source
        with context_managers.switch_collection(CsvRow, self.location) as CsvRowCollection:
            try:
                # Data is a dictionary - a single row
                # TODO make id column more general
                add_row(data)

            except AttributeError:
                # Data is a list of dictionaries - multiple rows
                for row in data:
                    add_row(row)

    def get_response(self,
                     params: typing.Optional[typing.Mapping[str, str]] = None):
        with context_managers.switch_collection(CsvRow, self.location) as CsvRowCollection:
            data = CsvRowCollection.objects

            # TODO accept parameters provided twice as an inclusive OR
            params = self._flatten_params(params)
            records = data(**params)
            data = json.loads(records.exclude('_id').to_json())

            # TODO make id column more general
            for item in data:
                if 'x_id' in item:
                    item['id'] = item.pop('x_id')

            return JsonResponse({
                'status': 'success',
                'data': data,
            })
