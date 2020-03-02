# (C) Datadog, Inc. 2020-present
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)
"""
Declarations used for type checking our code, including our manipulation of JSON documents returned by RethinkDB.
"""
import datetime as dt
from typing import Any, List, Literal, Mapping, Tuple, TypedDict, Union

# Lightweight shim to decouple collection functions from the check class.
Metric = TypedDict(
    'Metric',
    {'type': Literal['gauge', 'monotonic_count', 'service_check'], 'name': str, 'value': float, 'tags': List[str]},
)

Instance = TypedDict(
    'Instance', {'host': str, 'port': int, 'user': str, 'password': str, 'tls_ca_cert': str}, total=False
)


# Configuration documents.
# See: https://rethinkdb.com/docs/system-tables/#configuration-tables

Server = TypedDict('Server', {'id': str, 'name': str, 'cache_size_mb': str, 'tags': List[str]})

Table = TypedDict('Table', {'id': str, 'name': str, 'db': str})  # TODO: more fields


# System statistics documents.
# See: https://rethinkdb.com/docs/system-stats/

ClusterQueryEngine = TypedDict(
    'ClusterQueryEngine', {'queries_per_sec': int, 'read_docs_per_sec': int, 'written_docs_per_sec': int},
)

ClusterStats = TypedDict('ClusterStats', {'id': Tuple[Literal['cluster']], 'query_engine': ClusterQueryEngine})

ConfigTotals = TypedDict(
    'ConfigTotals',
    {
        'servers': int,
        'databases': int,
        'tables_per_database': Mapping[str, int],
        'secondary_indexes_per_table': Mapping[str, int],
    },
)

ServerQueryEngine = TypedDict(
    'ServerQueryEngine',
    {
        'client_connections': int,
        'clients_active': int,
        'queries_per_sec': int,
        'queries_total': int,
        'read_docs_per_sec': int,
        'read_docs_total': int,
        'written_docs_per_sec': int,
        'written_docs_total': int,
    },
)

ServerStats = TypedDict(
    'ServerStats', {'id': Tuple[Literal['server'], str], 'server': str, 'query_engine': ServerQueryEngine},
)

TableQueryEngine = TypedDict('TableQueryEngine', {'read_docs_per_sec': int, 'written_docs_per_sec': int})

TableStats = TypedDict(
    'TableStats', {'id': Tuple[Literal['table'], str], 'table': str, 'db': str, 'query_engine': TableQueryEngine},
)

ReplicaQueryEngine = TypedDict(
    'ReplicaQueryEngine',
    {'read_docs_per_sec': int, 'read_docs_total': int, 'written_docs_per_sec': int, 'written_docs_total': int},
)

ReplicaCache = TypedDict('ReplicaCache', {'in_use_bytes': int})

ReplicaDiskSpaceUsage = TypedDict(
    'ReplicaDiskSpaceUsage', {'metadata_bytes': int, 'data_bytes': int, 'garbage_bytes': int, 'preallocated_bytes': int}
)

ReplicaDisk = TypedDict(
    'ReplicaDisk',
    {
        'read_bytes_per_sec': int,
        'read_bytes_total': int,
        'written_bytes_per_sec': int,
        'written_bytes_total': int,
        'space_usage': ReplicaDiskSpaceUsage,
    },
)

ReplicaStorageEngine = TypedDict('ReplicaStorageEngine', {'cache': ReplicaCache, 'disk': ReplicaDisk})

ReplicaStats = TypedDict(
    'ReplicaStats',
    {
        'id': Tuple[Literal['table_server'], str, str],
        'server': str,
        'table': str,
        'db': str,
        'query_engine': ReplicaQueryEngine,
        'storage_engine': ReplicaStorageEngine,
    },
)


# Status documents.
# See: https://rethinkdb.com/docs/system-tables/#status-tables

ShardReplica = TypedDict('ShardReplica', {'server': str, 'state': str})
Shard = TypedDict('Shard', {'primary_replicas': List[str], 'replicas': List[ShardReplica]})
TableStatusFlags = TypedDict(
    'TableStatusFlags',
    {'ready_for_outdated_reads': bool, 'ready_for_reads': bool, 'ready_for_writes': bool, 'all_replicas_ready': bool},
)
TableStatus = TypedDict(
    'TableStatus', {'id': str, 'name': str, 'db': str, 'status': TableStatusFlags, 'shards': List[Shard]}
)

ServerNetwork = TypedDict(
    'ServerNetwork',
    {
        # NOTE: only fields of interest are listed here.
        'time_connected': dt.datetime,
        'connected_to': Mapping[str, bool],
    },
)
ServerProcess = TypedDict(
    'ServerProcess', {'argv': List[str], 'cache_size_mb': int, 'pid': int, 'time_started': dt.datetime, 'version': str}
)
ServerStatus = TypedDict('ServerStatus', {'id': str, 'name': str, 'network': ServerNetwork, 'process': ServerProcess})


# System jobs documents.
# See: https://rethinkdb.com/docs/system-jobs/

IndexConstructionInfo = TypedDict('IndexConstructionInfo', {'db': str, 'table': str, 'index': str, 'progress': int})
IndexConstructionJob = TypedDict(
    'IndexConstructionJob',
    {
        'type': Literal['index_construction'],
        'id': Tuple[Literal['index_construction'], str],
        'duration_sec': float,
        'info': IndexConstructionInfo,
        'servers': List[str],
    },
)

BackfillInfo = TypedDict(
    'BackfillInfo', {'db': str, 'destination_server': str, 'source_server': str, 'table': str, 'progress': int}
)
BackfillJob = TypedDict(
    'BackfillJob',
    {
        'type': Literal['backfill'],
        'id': Tuple[Literal['backfill'], str],
        'duration_sec': float,
        'info': BackfillInfo,
        'servers': List[str],
    },
)

# NOTE: this is a union type tagged by the 'type' key.
# See: https://mypy.readthedocs.io/en/latest/literal_types.html#intelligent-indexing
Job = Union[IndexConstructionJob, BackfillJob]

# ReQL command results.
# See: https://rethinkdb.com/api/python/

# NOTE: Ideally 'left' and 'right' would be generics here, but this isn't supported by 'TypedDict' yet.
# See: https://github.com/python/mypy/issues/3863
JoinRow = TypedDict('JoinRow', {'left': Any, 'right': Any})
