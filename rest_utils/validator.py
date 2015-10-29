import sqlalchemy.sql.sqltypes
import trafaret as t
from trafaret.contrib.rfc_3339 import DateTime


class ValidationError(t.DataError):
    pass


class ColumnScissors:
    def _enum_col(self, column, **kwargs):
        return t.Enum(*column.type.enums)

    def _str_col(self, column, **kwargs):
        return t.String(max_length=column.type.length, **kwargs)

    def _int_col(self, column, **kwargs):
        return t.Int(**kwargs)

    def _datetime_col(self, column, **kwargs):
        return DateTime(**kwargs)  # RFC3339

    def _bool_col(self, column, **kwargs):
        return t.StrBool()

    def cut(self, column, **kwargs):
        cut_method = 'cut_{}'.format(column.name)
        if hasattr(self, cut_method):
            trafaret = getattr(self, cut_method)(column, **kwargs)
        else:
            trafaret = self.default_cut(column, **kwargs)
        return trafaret

    def default_cut(self, column, **kwargs):
        if isinstance(column.type, sqlalchemy.sql.sqltypes.Enum):
            trafaret = self._enum_col(column, **kwargs)
        elif isinstance(column.type, sqlalchemy.sql.sqltypes.String):
            trafaret = self._str_col(column, **kwargs)
        elif isinstance(column.type, sqlalchemy.sql.sqltypes.Integer):
            trafaret = self._int_col(column, **kwargs)
        elif isinstance(column.type, sqlalchemy.sql.sqltypes.DateTime):
            trafaret = self._datetime_col(column, **kwargs)
        elif isinstance(column.type, sqlalchemy.sql.sqltypes.Boolean):
            trafaret = self._bool_col(column, **kwargs)
        else:
            raise NotImplementedError('{} has no implementation in validator'.format(str(column.type)))
        return trafaret


class ModelValidator(ColumnScissors):
    def __init__(self, model):
        self._model = model

    @property
    def _validator(self):
        if self._model is None:
            raise ValidationError('ModelValidator is not associated with model')
        fields = {}
        for column in self._model.__table__.columns.values():
            if column.primary_key and column.autoincrement:
                continue
            key_opts = {}
            key_opts['optional'] = column.nullable
            key = t.Key(column.name, **key_opts)

            val_opts = {}
            val_opts['allow_blank'] = column.nullable
            trafaret = self.cut(column, **val_opts)
            if not trafaret:
                continue
            if column.nullable:
                trafaret |= t.Null()
                trafaret |= (t.String(max_length=0, allow_blank=True) >> (lambda x: None))
            fields[key] = trafaret
        return t.Dict(fields)

    def check(self, instance):
        return self._validator.check(instance)


class ModelSerializer(ColumnScissors):
    def __init__(self, model):
        self._model = model

    @property
    def _validator(self):
        if self._model is None:
            raise ValidationError('ModelSerializer is not associated with model')
        fields = {}
        for column in self._model.__table__.columns.values():
            key = t.Key(column.name)
            trafaret = self.cut(column)
            if column.nullable:
                trafaret |= t.Null()
                trafaret |= (t.String(max_length=0, allow_blank=True) >> (lambda x: None))
            fields[key] = trafaret
        return t.Dict(fields)

    def serialize(self, instance):
        return self._validator.check(instance)

    def _datetime_col(self, column, **kwargs):
        return DateTime(**kwargs) >> (lambda dt: dt.isoformat())
