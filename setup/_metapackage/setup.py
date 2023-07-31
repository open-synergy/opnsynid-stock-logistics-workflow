import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-opnsynid-stock-logistics-workflow",
    description="Meta package for open-synergy-opnsynid-stock-logistics-workflow Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-stock_move_backdating',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
