from typing import Dict, List, NamedTuple


Labels = Dict[str, str]


class Alert(NamedTuple):
    annotations: Labels
    endsAt: str
    fingerprint: str
    labels: Labels
    startsAt: str
    status: str
    generatorURL: str = ''


class Alerts(NamedTuple):
    alerts: List[Alert]
    externalURL: str
    receiver: str
    status: str
    version: str
    commonAnnotations: Labels = {}
    commonLabels: Labels = {}
    groupKey: str = ''
    groupLabels: Labels = {}

    @classmethod
    def from_dict(cls, _dict: Dict):
        alerts = list(map(lambda x: Alert(**x), _dict['alerts']))
        _dict.pop('alerts')
        return cls(
            alerts=alerts,
            **_dict
        )
