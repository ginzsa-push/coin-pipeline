"""create initial table creation

Revision ID: fac39439494b
Revises: 
Create Date: 2025-08-19 13:01:30.446386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fac39439494b'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


coin_fiat_schema = {
            'id': 'int64',
            'name': 'object',
            'symbol': 'object',
            'slug': 'object',
            'num_market_pairs': 'int64',
            'date_added': 'object',
            'price': 'float64',
            'fiat': 'object',
            'market_cap': 'float64',
            'volume_24h': 'float64',
            'volume_change_24h': 'float64',
            'percent_change_1h': 'float64',
            'percent_change_24h': 'float64',
            'percent_change_7d': 'float64',
            "percent_change_30d": 'float64',
            "percent_change_60d": 'float64',
            "percent_change_90d": 'float64',
            "market_cap": 'float64',
            "market_cap_dominance": 'float64',
            "fully_diluted_market_cap": 'float64',
            "tvl": 'float64',
            'tags': 'int64',
            "max_supply": 'float64',
            "circulating_supply": 'int64',
            "total_supply": 'int64',
            "is_active": 'bool',
            "infinite_supply": 'bool',
            "platform": 'object',
            "cmc_rank": 'int64',
            "is_fiat": 'bool',
            "self_reported_circulating_supply": 'object',
            "self_reported_market_cap": 'object',
            "tvl_ratio": 'float64',
            "last_updated": 'object',
        }

type_mapping = {
    'int64': sa.BigInteger,
    'object': sa.String,
    'float64': sa.Float,
    'bool': sa.Boolean,
    'datetime64[ns]': sa.DateTime,
    'int32': sa.Integer,
    'int16': sa.SmallInteger,
    'int8': sa.SmallInteger,
    'int': sa.Integer, 
    'float': sa.Float,
    'str': sa.String,
    'unicode': sa.Unicode,
    'text': sa.Text,
    'fiat_timestamp': sa.DateTime
}


def upgrade() -> None:
    """Upgrade schema."""
    columns = [
        sa.Column('id', type_mapping[coin_fiat_schema['id']], primary_key=True),
        sa.Column('name', type_mapping[coin_fiat_schema['name']], nullable=False),
        sa.Column('symbol', type_mapping[coin_fiat_schema['symbol']], nullable=False),
        sa.Column('slug', type_mapping[coin_fiat_schema['slug']], nullable=False),
        sa.Column('num_market_pairs', type_mapping[coin_fiat_schema['num_market_pairs']], nullable=False),
        sa.Column('date_added', type_mapping[coin_fiat_schema['date_added']], nullable=False),
        sa.Column('price', type_mapping[coin_fiat_schema['price']], nullable=False),
        sa.Column('fiat', type_mapping[coin_fiat_schema['fiat']], nullable=False),
        sa.Column('market_cap', type_mapping[coin_fiat_schema['market_cap']], nullable=False),
        sa.Column('volume_24h', type_mapping[coin_fiat_schema['volume_24h']], nullable=False),
        sa.Column('volume_change_24h', type_mapping[coin_fiat_schema['volume_change_24h']], nullable=False),
        sa.Column('percent_change_1h', type_mapping[coin_fiat_schema['percent_change_1h']], nullable=False),
        sa.Column('percent_change_24h', type_mapping[coin_fiat_schema['percent_change_24h']], nullable=False),
        sa.Column('percent_change_7d', type_mapping[coin_fiat_schema['percent_change_7d']], nullable=False),
        sa.Column('percent_change_30d', type_mapping[coin_fiat_schema['percent_change_30d']], nullable=False),
        sa.Column('percent_change_60d', type_mapping[coin_fiat_schema['percent_change_60d']], nullable=False),
        sa.Column('percent_change_90d', type_mapping[coin_fiat_schema['percent_change_90d']], nullable=False),
        sa.Column('market_cap_dominance', type_mapping[coin_fiat_schema['market_cap_dominance']], nullable=False),
        sa.Column('fully_diluted_market_cap', type_mapping[coin_fiat_schema['fully_diluted_market_cap']], nullable=False),
        sa.Column('tvl', type_mapping[coin_fiat_schema['tvl']], nullable=False),
        sa.Column('tags', type_mapping[coin_fiat_schema['tags']], nullable=False),
        sa.Column('max_supply', type_mapping[coin_fiat_schema['max_supply']], nullable=False),
        sa.Column('circulating_supply', type_mapping[coin_fiat_schema['circulating_supply']], nullable=False),
        sa.Column('total_supply', type_mapping[coin_fiat_schema['total_supply']], nullable=False),
        sa.Column('is_active', type_mapping[coin_fiat_schema['is_active']], nullable=False),
        sa.Column('infinite_supply', type_mapping[coin_fiat_schema['infinite_supply']], nullable=False),
        sa.Column('platform', type_mapping[coin_fiat_schema['platform']], nullable=True),
        sa.Column('cmc_rank', type_mapping[coin_fiat_schema['cmc_rank']], nullable=False),
        sa.Column('is_fiat', type_mapping[coin_fiat_schema['is_fiat']], nullable=False),
        sa.Column('self_reported_circulating_supply', type_mapping[coin_fiat_schema['self_reported_circulating_supply']], nullable=True),
        sa.Column('self_reported_market_cap', type_mapping[coin_fiat_schema['self_reported_market_cap']], nullable=True),
        sa.Column('tvl_ratio', type_mapping[coin_fiat_schema['tvl_ratio']], nullable=False),
        sa.Column('last_updated', type_mapping[coin_fiat_schema['last_updated']], nullable=False),
        sa.Column('fiat_timestamp',type_mapping['fiat_timestamp'], nullable=True),
        sa.Column('GBP', type_mapping['float64'], nullable=True),
        sa.Column('CAD', type_mapping['float64'], nullable=True),
        sa.Column('JPY', type_mapping['float64'], nullable=True),
        sa.Column('MXN', type_mapping['float64'], nullable=True),
    ]

    op.create_table('coin_fiat_table', *columns)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('coin_fiat_table')
