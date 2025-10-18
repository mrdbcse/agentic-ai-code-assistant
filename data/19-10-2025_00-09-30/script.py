# Python script for data ingestion using Peewee ORM (PostgreSQL)
# Assumes you have installed peewee and psycopg2-binary
# pip install peewee psycopg2-binary

import json
from peewee import *
from playhouse.postgres_ext import PostgresqlExtDatabase, JSONField
from datetime import datetime

# Database connection
pg_db = PostgresqlExtDatabase(
    "solar_db",  # Change to your DB name
    user="postgres",  # Change to your DB user
    password="password",  # Change to your DB password
    host="localhost",
    port=5432,
)


# Peewee Models (partial, only for relevant tables for this context)
class BaseModel(Model):
    class Meta:
        database = pg_db


class Organization(BaseModel):
    id = BigIntegerField(primary_key=True)
    name = TextField(null=True)
    url = TextField(null=True)


class Contact(BaseModel):
    id = BigIntegerField(primary_key=True)
    email = TextField(null=True)
    phone = TextField(null=True)
    url = TextField(null=True)
    first_name = TextField(null=True)
    family_name = TextField(null=True)
    display = TextField(null=True)
    passport_number = TextField(null=True)
    licence_number = TextField(null=True)
    custom_contact_info_1 = TextField(null=True)
    custom_contact_info_2 = TextField(null=True)
    middle_name = TextField(null=True)
    gender = IntegerField(null=True)
    date_of_birth = DateField(null=True)
    user_id = BigIntegerField(null=True)
    org_id = ForeignKeyField(Organization, backref="contacts", null=True)
    identifier = TextField(null=True)
    type = IntegerField(null=True)
    custom_data = JSONField(null=True)


class Project(BaseModel):
    id = BigIntegerField(primary_key=True)
    identifier = UUIDField(null=True)
    title = TextField(null=True)
    address = TextField(null=True)
    notes = TextField(null=True)
    is_residential = BooleanField(null=True)
    is_pricing_locked = BooleanField(null=True)
    installation_date = DateField(null=True)
    language = TextField(null=True)
    lat = FloatField(null=True)
    lon = FloatField(null=True)
    locality = TextField(null=True)
    state = TextField(null=True)
    zip = TextField(null=True)
    country_iso2 = TextField(null=True)
    country_name = TextField(null=True)
    org_id = ForeignKeyField(Organization, backref="projects", null=True)
    created_date = DateTimeField(null=True)
    modified_date = DateTimeField(null=True)
    contract_date = DateField(null=True)
    contract = TextField(null=True)
    design = TextField(null=True)
    number_of_phases = IntegerField(null=True)
    number_of_wires = IntegerField(null=True)
    number_of_storeys = IntegerField(null=True)
    payment_option_sold = TextField(null=True)
    payment_option_sold_title = TextField(null=True)
    priority = IntegerField(null=True)
    project_installed = IntegerField(null=True)
    project_sold = IntegerField(null=True)
    roof_type_name = TextField(null=True)
    roof_type = TextField(null=True)
    simulate_first_year_only = BooleanField(null=True)
    site_notes = TextField(null=True)
    sold_date = DateTimeField(null=True)
    stage = IntegerField(null=True)
    usage_annual_or_guess = FloatField(null=True)
    usage = FloatField(null=True)
    allow_email_notifications = BooleanField(null=True)
    is_lite = BooleanField(null=True)
    custom_data = JSONField(null=True)


class System(BaseModel):
    id = BigIntegerField(primary_key=True)
    url = TextField(null=True)
    name = TextField(null=True)
    uuid = UUIDField(null=True)
    order = IntegerField(null=True)
    system_lifetime = IntegerField(null=True)
    inverter_range = TextField(null=True)
    dc_optimizer_active = BooleanField(null=True)
    dc_optimizer_efficiency = FloatField(null=True)
    show_customer = BooleanField(null=True)
    is_current = BooleanField(null=True)
    auto_string = BooleanField(null=True)
    discount = FloatField(null=True)
    adders_per_system = FloatField(null=True)
    adders_per_panel = FloatField(null=True)
    adders_per_watt = FloatField(null=True)
    kw_stc = FloatField(null=True)
    battery_total_kwh = FloatField(null=True)
    price_including_tax = FloatField(null=True)
    price_excluding_tax = FloatField(null=True)
    net_profit = FloatField(null=True)
    module_quantity = IntegerField(null=True)
    co2_tons_lifetime = FloatField(null=True)
    project_id = ForeignKeyField(Project, backref="systems", null=True)
    org_id = ForeignKeyField(Organization, backref="systems", null=True)
    pricing_scheme = TextField(null=True)
    battery_scheme = TextField(null=True)
    output_annual_kwh = FloatField(null=True)
    consumption_offset_percentage = FloatField(null=True)
    integration_json = JSONField(null=True)
    commission = FloatField(null=True)
    commission_override_manually = FloatField(null=True)
    system_sold = BooleanField(null=True)


class SystemModule(BaseModel):
    id = AutoField()
    system_id = ForeignKeyField(System, backref="modules")
    module_activation_id = BigIntegerField(null=True)
    code = TextField(null=True)
    manufacturer_name = TextField(null=True)
    quantity = IntegerField(null=True)


class SystemInverter(BaseModel):
    id = AutoField()
    system_id = ForeignKeyField(System, backref="inverters")
    inverter_activation_id = BigIntegerField(null=True)
    code = TextField(null=True)
    manufacturer_name = TextField(null=True)
    quantity = IntegerField(null=True)


class SystemBattery(BaseModel):
    id = AutoField()
    system_id = ForeignKeyField(System, backref="batteries")
    battery_activation_id = BigIntegerField(null=True)
    code = TextField(null=True)
    manufacturer_name = TextField(null=True)
    quantity = IntegerField(null=True)


class Event(BaseModel):
    id = BigIntegerField(primary_key=True)
    org = TextField(null=True)
    project_id = ForeignKeyField(Project, backref="events", null=True)
    duration = IntegerField(null=True)
    event_type_id = IntegerField(null=True)
    action_id = BigIntegerField(null=True)
    start = DateTimeField(null=True)
    end = DateTimeField(null=True)
    created_date = DateTimeField(null=True)
    modified_date = DateTimeField(null=True)
    who_display = TextField(null=True)
    who_email = TextField(null=True)
    who_portrait_image_public_url = TextField(null=True)
    completion_date = DateTimeField(null=True)
    title = TextField(null=True)
    project_name = TextField(null=True)
    is_planned = BooleanField(null=True)
    task_status = IntegerField(null=True)
    is_complete = BooleanField(null=True)
    notes = TextField(null=True)
    is_archived = BooleanField(null=True)
    categories = ArrayField(IntegerField, null=True)
    form_config = IntegerField(null=True)
    event_icon = IntegerField(null=True)


# Add more models as needed for other tables


def parse_date(date_str):
    if not date_str:
        return None
    try:
        if "T" in date_str:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return datetime.strptime(date_str, "%Y-%m-%d")
    except Exception:
        return None


def main():
    # Connect to DB
    pg_db.connect()
    # Create tables if not exist (for demo, in prod use migrations)
    pg_db.create_tables(
        [
            Organization,
            Contact,
            Project,
            System,
            SystemModule,
            SystemInverter,
            SystemBattery,
            Event,
        ]
    )

    # Example: Ingesting a single project from the context (normally, parse from JSON or similar)
    # For demo, hardcoded values from the context
    org, _ = Organization.get_or_create(
        id=178878,
        defaults={
            "name": "AOPL Energy Private Limited",
            "url": "https://api.opensolar.com/api/orgs/178878/",
        },
    )

    # Contacts
    contact1, _ = Contact.get_or_create(
        id=1593482706,
        defaults={
            "email": "",
            "phone": "",
            "url": "https://api.opensolar.com/api/orgs/178878/contacts/1593482706/",
            "first_name": "Pritis",
            "family_name": "Nayak",
            "display": "Pritis Nayak",
            "gender": 2,
            "date_of_birth": parse_date("1990-01-01"),
            "org_id": org,
        },
    )
    contact2, _ = Contact.get_or_create(
        id=1593514961,
        defaults={
            "email": "7954997@os.code",
            "phone": "",
            "url": "https://api.opensolar.com/api/orgs/178878/contacts/1593514961/",
            "display": "7954997@os.code",
            "gender": 0,
            "user_id": 2980286,
            "org_id": org,
        },
    )

    # Project
    project, _ = Project.get_or_create(
        id=7954997,
        defaults={
            "identifier": "de25868b-aa8d-4daa-a2ec-11e02214463c",
            "title": "101 Oxford Towers\nOld HAL Airport Road\nBangalore, India - 560008",
            "address": None,
            "notes": "This solar project is created for the Customer Pritis Nayak",
            "is_residential": True,
            "is_pricing_locked": True,
            "installation_date": parse_date("2025-09-12"),
            "language": "en",
            "lat": 12.9554,
            "lon": 77.6534,
            "locality": "kolkata",
            "state": "WB",
            "zip": None,
            "country_iso2": "IN",
            "country_name": "India",
            "org_id": org,
            "created_date": parse_date("2025-09-08T09:07:12.923578Z"),
            "modified_date": parse_date("2025-09-12T08:14:45.165845Z"),
            "contract_date": parse_date("2025-09-12"),
            "contract": None,
            "design": "Design Exists",
            "number_of_phases": 3,
            "number_of_wires": None,
            "number_of_storeys": None,
            "payment_option_sold": "https://api.opensolar.com/api/orgs/178878/payment_options/907396/",
            "payment_option_sold_title": "Cash",
            "priority": 3,
            "roof_type_name": "Flat Concrete",
            "roof_type": "https://api.opensolar.com/api/roof_types/7/",
            "simulate_first_year_only": False,
            "site_notes": "",
            "sold_date": parse_date("2025-09-12T08:11:01.398107Z"),
            "stage": 0,
        },
    )

    # System
    system, _ = System.get_or_create(
        id=9354996,
        defaults={
            "url": "https://api.opensolar.com/api/orgs/178878/systems/9354996/",
            "name": "",
            "uuid": "4D8FDCE5-FD00-49A7-895F-44E74563A1E3",
            "order": 0,
            "system_lifetime": 0,
            "inverter_range": None,
            "dc_optimizer_active": False,
            "dc_optimizer_efficiency": 1.0,
            "show_customer": True,
            "is_current": False,
            "auto_string": True,
            "discount": 0.0,
            "adders_per_system": 0.0,
            "adders_per_panel": 0.0,
            "adders_per_watt": 0.0,
            "kw_stc": 1.29,
            "battery_total_kwh": 9.8,
            "price_including_tax": 5985.0,
            "price_excluding_tax": 5985.0,
            "net_profit": 107479.77,
            "module_quantity": 4,
            "co2_tons_lifetime": 17.16,
            "project_id": project,
            "org_id": org,
            "pricing_scheme": "https://api.opensolar.com/api/orgs/178878/pricing_schemes/340674/",
            "battery_scheme": None,
            "output_annual_kwh": 1271,
            "consumption_offset_percentage": 118,
            "integration_json": None,
            "commission": None,
            "commission_override_manually": 0.0,
            "system_sold": True,
        },
    )

    # System Modules
    SystemModule.get_or_create(
        system_id=system,
        module_activation_id=1094449,
        defaults={
            "code": "SPR-P3-335-BLK",
            "manufacturer_name": "SunPower",
            "quantity": 2,
        },
    )
    SystemModule.get_or_create(
        system_id=system,
        module_activation_id=1094448,
        defaults={
            "code": "JKM310M-72B",
            "manufacturer_name": "Jinko Solar Co., Ltd.",
            "quantity": 2,
        },
    )

    # System Inverter
    SystemInverter.get_or_create(
        system_id=system,
        inverter_activation_id=1159736,
        defaults={"code": "Primo 5.0-1", "manufacturer_name": "Fronius", "quantity": 1},
    )

    # System Battery
    SystemBattery.get_or_create(
        system_id=system,
        battery_activation_id=689751,
        defaults={
            "code": "LG Energy Solution RESU10 HV-Type R",
            "manufacturer_name": "LG Energy Solution",
            "quantity": 1,
        },
    )

    # Events (example for a few events)
    Event.get_or_create(
        id=40249274,
        defaults={
            "org": "https://api.opensolar.com/api/orgs/178878/",
            "project_id": project,
            "duration": 66,
            "event_type_id": 2,
            "action_id": None,
            "start": parse_date("2025-09-13 06:34:36.463571+00:00"),
            "end": parse_date("2025-09-13T06:35:42.700549Z"),
            "created_date": parse_date("2025-09-13T06:34:36.491343Z"),
            "modified_date": parse_date("2025-09-13T06:34:36.491354Z"),
            "who_display": "7954997@os.code",
            "who_email": "7954997@os.code",
            "who_portrait_image_public_url": None,
            "completion_date": None,
            "title": "7954997@os.code Viewed Online Proposal for 1 minute, 6 seconds",
            "project_name": "my test address line 1.0 my test address line 2.0",
            "is_planned": False,
            "task_status": 0,
            "is_complete": False,
            "notes": None,
            "is_archived": False,
            "categories": [1],
            "form_config": 2,
            "event_icon": 2,
        },
    )
    # Add more events as needed

    print("Data ingestion complete.")
    pg_db.close()


if __name__ == "__main__":
    main()
