import dataclasses


@dataclasses.dataclass
class User:
    id: int
    username: str
    password: str

    @classmethod
    def from_dict(self, d):
        return self(**d)

    def to_dict(self):
        return dataclasses.asdict(self)
