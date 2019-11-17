from typing import Dict, List, NamedTuple, Union


Labels = Dict[str, str]
Json = Union[dict, list, str]


class Alert(NamedTuple):
    annotations: Labels
    endsAt: str
    labels: Labels
    startsAt: str
    status: str
    fingerprint: str = ''
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

    def as_dict(self):
        _dict = self._asdict()
        _dict['alerts'] = list(map(lambda x: x._asdict(), self.alerts))
        return _dict
