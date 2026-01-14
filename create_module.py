import sys
import os

if len(sys.argv) < 2:
    print("Error: Debe pasar el nombre del modulo. Ejemplo: python3 create_module.py mi_modulo")
    sys.exit(1)

module_name = sys.argv[1]
model_name = module_name.replace('_', '.')

base_path = r"C:\Program Files\Odoo 18.0.20251218\server\addons"

folders = [
    module_name,
    f"{module_name}/models",
    f"{module_name}/views",
    f"{module_name}/security",
    f"{module_name}/static",
]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)


manifest_content = f"""{{
    'name': '{module_name.capitalize()}',
    'version': '18.0.1.0.0',
    'category': 'Uncategorized',
    'summary': 'Módulo creado para Odoo 18',
    'description': 'Descripción de {module_name}',
    'author': 'Bryan Balcazar',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/{module_name}_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}}"""

with open(f"{module_name}/__manifest__.py", "w") as f:
    f.write(manifest_content)


with open(f"{module_name}/__init__.py", "w") as f:
    f.write("from . import models")


with open(f"{module_name}/models/__init__.py", "w") as f:
    f.write(f"from . import {module_name}")


model_content = f"""from odoo import models, fields

class {module_name.replace('_', '').capitalize()}(models.Model):
    _name = '{model_name}'
    _description = '{module_name.replace('_', ' ')}'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(string='Activo', default=True)
"""
with open(f"{module_name}/models/{module_name}.py", "w") as f:
    f.write(model_content)


view_content = f"""<odoo>
    <record id="view_{module_name}_list" model="ir.ui.view">
        <field name="name">{model_name}.list</field>
        <field name="model">{model_name}</field>
        <field name="arch" type="xml">
            <list>
                <field name="name"/>
            </list>
        </field>
    </record>

    <record id="view_{module_name}_form" model="ir.ui.view">
        <field name="name">{model_name}.form</field>
        <field name="model">{model_name}</field>
        <field name="arch" type="xml">
            <form>
                <sheet>
                    <group>
                        <field name="name"/>
                    </group>
                </sheet>
            </form>
        </field>
    </record>

    <record id="action_{module_name}" model="ir.actions.act_window">
        <field name="name">{module_name.capitalize()}</field>
        <field name="res_model">{model_name}</field>
        <field name="view_mode">list,form</field>
    </record>

    <menuitem id="menu_{module_name}_root" name="{module_name.capitalize()}" sequence="10"/>
    <menuitem id="menu_{module_name}_main" name="Registros" parent="menu_{module_name}_root" action="action_{module_name}" sequence="10"/>
</odoo>
"""
with open(f"{module_name}/views/{module_name}_views.xml", "w") as f:
    f.write(view_content)

csv_model_id = f"model_{model_name.replace('.', '_')}"
security_content = f"id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink\n"
security_content += f"access_{module_name},{module_name},{csv_model_id},base.group_user,1,1,1,1"

with open(f"{module_name}/security/ir.model.access.csv", "w") as f:
    f.write(security_content)

print(f"¡Módulo '{module_name}' creado con éxito para Odoo 18!")