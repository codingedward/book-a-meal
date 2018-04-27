import json
from apispec import APISpec
from app import create_app

spec = APISpec(
    title='Book A Meal',
    version='0.0.1',
    info=dict(
        description='Andela book a meal challenge'
    )
    plugins=[
        'apispec.ext.flask'
        'apispec.ext.marshmallow'
    ]
)

app = create_app()

with open('swagger.json', 'w') as f:
    json.dump(spec.to_dict(), f)

