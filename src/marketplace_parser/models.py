from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import json

@dataclass
class Parameter:
    """Модель параметра товара"""
    param_id: int
    name: str
    description: str
    required: bool
    values: List[Any]
    category_id: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            'param_id': self.param_id,
            'name': self.name,
            'description': self.description,
            'required': self.required,
            'values': json.dumps(self.values),
            'category_id': self.category_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Parameter':
        return cls(
            param_id=data['id'],
            name=data.get('name', ''),
            description=data.get('description', ''),
            required=data.get('required', False),
            values=data.get('values', []),
            category_id=data.get('category_id', 0)
        )
