from dataclasses import dataclass, asdict


@dataclass
class EntityBase:
    id: int
    codigo: int
    descripcion: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return asdict(self)
