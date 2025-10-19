# Python script for data ingestion using Peewee ORM (PostgreSQL)
# Assumes you have installed peewee and psycopg2-binary
# pip install peewee psycopg2-binary

import peewee as pw
import json
from datetime import datetime
from uuid import UUID

# Database connection
pg_db = pw.PostgresqlDatabase(
    "solar_db",  # Change to your DB name
    user="postgres",  # Change to your DB user
    password="password",  # Change to your DB password
    host="localhost",
    port=5432,
)

# Peewee Models (only for tables present in the provided DB Schema)


class BaseModel(pw.Model):
    class Meta:
        database = pg_db


class Organization(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    name = pw.CharField(max_length=255, null=True)
    url = pw.TextField(null=True)


class Project(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    identifier = pw.UUIDField(null=True)
    title = pw.TextField(null=True)
    address = pw.TextField(null=True)
    notes = pw.TextField(null=True)
    org_id = pw.BigIntegerField(null=True)
    org_name = pw.CharField(max_length=255, null=True)
    url = pw.TextField(null=True)
    is_residential = pw.BooleanField(null=True)
    is_pricing_locked = pw.BooleanField(null=True)
    installation_date = pw.DateField(null=True)
    language = pw.CharField(max_length=10, null=True)
    created_date = pw.DateTimeField(null=True)
    modified_date = pw.DateTimeField(null=True)
    lat = pw.DoubleField(null=True)
    lon = pw.DoubleField(null=True)
    locality = pw.CharField(max_length=255, null=True)
    state = pw.CharField(max_length=50, null=True)
    zip = pw.CharField(max_length=20, null=True)
    country_iso2 = pw.CharField(max_length=10, null=True)
    country_name = pw.CharField(max_length=100, null=True)
    contract_date = pw.DateField(null=True)
    contract = pw.TextField(null=True)
    contract_terms = pw.TextField(null=True)
    contract_template_mode = pw.CharField(max_length=50, null=True)
    payment_option_sold_title = pw.CharField(max_length=100, null=True)
    payment_option_sold = pw.TextField(null=True)
    number_of_phases = pw.IntegerField(null=True)
    number_of_wires = pw.IntegerField(null=True)
    number_of_storeys = pw.IntegerField(null=True)
    roof_type_name = pw.CharField(max_length=100, null=True)
    roof_type = pw.TextField(null=True)
    design = pw.TextField(null=True)
    proposal_message = pw.TextField(null=True)
    proposal_content = pw.TextField(null=True)
    proposal_template = pw.TextField(null=True)
    proposal_template_settings = pw.JSONField(null=True)
    simulate_first_year_only = pw.BooleanField(null=True)
    sold_date = pw.DateTimeField(null=True)
    valid_until_date = pw.DateField(null=True)
    wind_region = pw.CharField(max_length=50, null=True)
    has_cellular_coverage = pw.BooleanField(null=True)
    years_to_simulate = pw.IntegerField(null=True)
    docusign_contract_envelope_id = pw.CharField(max_length=100, null=True)
    allow_email_notifications = pw.BooleanField(null=True)
    is_lite = pw.BooleanField(null=True)
    custom_data = pw.JSONField(null=True)
    shared_with = pw.JSONField(null=True)
    auto_apply_max_simulate_years = pw.BooleanField(null=True)
    brighte_role_connection_status = pw.CharField(max_length=50, null=True)
    stage = pw.SmallIntegerField(null=True)
    stage_warning = pw.TextField(null=True)
    project_installed = pw.SmallIntegerField(null=True)
    project_sold = pw.SmallIntegerField(null=True)
    system_sold = pw.TextField(null=True)
    system_installed = pw.TextField(null=True)
    temperature_min_max = pw.ArrayField(pw.DoubleField, null=True)
    usage_annual_or_guess = pw.DoubleField(null=True)
    usage = pw.DoubleField(null=True)
    meter_identifier = pw.CharField(max_length=100, null=True)
    parcel_identifier = pw.CharField(max_length=100, null=True)
    serial_numbers_panels = pw.TextField(null=True)
    serial_numbers_inverters = pw.TextField(null=True)
    serial_numbers_batteries = pw.TextField(null=True)
    share_link = pw.TextField(null=True)
    stars = pw.JSONField(null=True)
    tags = pw.JSONField(null=True)
    tags_data = pw.JSONField(null=True)
    testimonials = pw.JSONField(null=True)
    testimonials_data = pw.JSONField(null=True)
    timezone_offset = pw.DoubleField(null=True)
    custom_project_info_1 = pw.TextField(null=True)
    custom_project_info_2 = pw.TextField(null=True)
    custom_project_info_3 = pw.TextField(null=True)
    custom_project_info_4 = pw.TextField(null=True)
    custom_project_info_5 = pw.TextField(null=True)
    private_files = pw.JSONField(null=True)
    private_files_data = pw.JSONField(null=True)
    premium_imagery_activations = pw.JSONField(null=True)
    activated_premium_imagery_wallet_product_ids = pw.ArrayField(
        pw.IntegerField, null=True
    )
    workflows = pw.JSONField(null=True)
    workflow = pw.JSONField(null=True)
    change_orders = pw.JSONField(null=True)
    design_modifiers = pw.JSONField(null=True)


class System(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    url = pw.TextField(null=True)
    name = pw.CharField(max_length=255, null=True)
    uuid = pw.UUIDField(null=True)
    order = pw.IntegerField(null=True)
    system_lifetime = pw.IntegerField(null=True)
    inverter_range = pw.TextField(null=True)
    dc_optimizer_active = pw.BooleanField(null=True)
    dc_optimizer_efficiency = pw.DoubleField(null=True)
    show_customer = pw.BooleanField(null=True)
    is_current = pw.BooleanField(null=True)
    auto_string = pw.BooleanField(null=True)
    discount = pw.DoubleField(null=True)
    adders_per_system = pw.DoubleField(null=True)
    adders_per_panel = pw.DoubleField(null=True)
    adders_per_watt = pw.DoubleField(null=True)
    kw_stc = pw.DoubleField(null=True)
    battery_total_kwh = pw.DoubleField(null=True)
    price_including_tax = pw.DoubleField(null=True)
    price_excluding_tax = pw.DoubleField(null=True)
    net_profit = pw.DoubleField(null=True)
    module_quantity = pw.IntegerField(null=True)
    co2_tons_lifetime = pw.DoubleField(null=True)
    project_id = pw.BigIntegerField(null=True)
    org_id = pw.BigIntegerField(null=True)
    pricing_scheme = pw.TextField(null=True)
    pricing_scheme_data = pw.JSONField(null=True)
    battery_scheme = pw.TextField(null=True)
    output_annual_kwh = pw.DoubleField(null=True)
    consumption_offset_percentage = pw.DoubleField(null=True)
    commission = pw.DoubleField(null=True)
    commission_override_manually = pw.DoubleField(null=True)
    system_sold = pw.BooleanField(null=True)
    modules = pw.JSONField(null=True)
    inverters = pw.JSONField(null=True)
    batteries = pw.JSONField(null=True)
    others = pw.JSONField(null=True)
    integration_json = pw.JSONField(null=True)


class SystemModule(BaseModel):
    id = pw.AutoField()
    system_id = pw.BigIntegerField()
    module_activation_id = pw.BigIntegerField(null=True)
    code = pw.CharField(max_length=100, null=True)
    manufacturer_name = pw.CharField(max_length=100, null=True)
    quantity = pw.IntegerField(null=True)


class SystemInverter(BaseModel):
    id = pw.AutoField()
    system_id = pw.BigIntegerField()
    inverter_activation_id = pw.BigIntegerField(null=True)
    code = pw.CharField(max_length=100, null=True)
    manufacturer_name = pw.CharField(max_length=100, null=True)
    quantity = pw.IntegerField(null=True)


class SystemBattery(BaseModel):
    id = pw.AutoField()
    system_id = pw.BigIntegerField()
    battery_activation_id = pw.BigIntegerField(null=True)
    code = pw.CharField(max_length=100, null=True)
    manufacturer_name = pw.CharField(max_length=100, null=True)
    quantity = pw.IntegerField(null=True)


class Event(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    org = pw.TextField(null=True)
    project_id = pw.BigIntegerField(null=True)
    duration = pw.IntegerField(null=True)
    event_type_id = pw.IntegerField(null=True)
    action_id = pw.BigIntegerField(null=True)
    start = pw.DateTimeField(null=True)
    end = pw.DateTimeField(null=True)
    created_date = pw.DateTimeField(null=True)
    modified_date = pw.DateTimeField(null=True)
    who_display = pw.CharField(max_length=200, null=True)
    who_email = pw.CharField(max_length=200, null=True)
    who_portrait_image_public_url = pw.TextField(null=True)
    notify_team_members = pw.JSONField(null=True)
    completion_date = pw.DateTimeField(null=True)
    title = pw.TextField(null=True)
    project_name = pw.TextField(null=True)
    is_planned = pw.BooleanField(null=True)
    task_status = pw.IntegerField(null=True)
    is_complete = pw.BooleanField(null=True)
    notes = pw.TextField(null=True)
    is_archived = pw.BooleanField(null=True)
    categories = pw.ArrayField(pw.IntegerField, null=True)
    form_config = pw.IntegerField(null=True)
    team_members = pw.JSONField(null=True)
    event_icon = pw.IntegerField(null=True)


class AvailableCustomerAction(BaseModel):
    id = pw.AutoField()
    project_id = pw.BigIntegerField(null=True)
    system_uuid = pw.UUIDField(null=True)
    actions_available = pw.JSONField(null=True)


class Transaction(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    url = pw.TextField(null=True)
    org = pw.TextField(null=True)
    org_id = pw.BigIntegerField(null=True)
    org_name = pw.CharField(max_length=255, null=True)
    project = pw.TextField(null=True)
    project_name = pw.CharField(max_length=255, null=True)
    system = pw.TextField(null=True)
    payment_option = pw.TextField(null=True)
    is_complete = pw.BooleanField(null=True)
    transaction_datetime = pw.DateTimeField(null=True)
    amount = pw.DoubleField(null=True)
    tax_included = pw.DoubleField(null=True)
    surcharge_amount = pw.DoubleField(null=True)
    funds_confirmed = pw.BooleanField(null=True)
    details = pw.JSONField(null=True)
    contract_details = pw.JSONField(null=True)
    contract_details_hash = pw.CharField(max_length=100, null=True)
    signature_data = pw.TextField(null=True)
    is_commission_payable = pw.BooleanField(null=True)
    external_status_title = pw.CharField(max_length=255, null=True)
    external_status_description = pw.TextField(null=True)
    external_application_id = pw.CharField(max_length=100, null=True)
    external_application_url = pw.TextField(null=True)
    external_finance_amount_approved = pw.DoubleField(null=True)
    external_finance_amount_requested = pw.DoubleField(null=True)
    external_finance_contact_decisions = pw.TextField(null=True)
    transaction_type = pw.CharField(max_length=50, null=True)
    prior_transaction_type = pw.CharField(max_length=50, null=True)
    customer_name = pw.CharField(max_length=255, null=True)
    created_date = pw.DateTimeField(null=True)
    modified_date = pw.DateTimeField(null=True)
    credit_expiration_date = pw.DateField(null=True)


# Add more models as needed for other tables in the schema

# Data ingestion function


def ingest_data(data):
    # 1. Organization
    org_id = int(data["org_id"])
    org, created = Organization.get_or_create(
        id=org_id, defaults={"name": data.get("org_name"), "url": data.get("org")}
    )

    # 2. Project
    project_id = int(data["id"])
    project, created = Project.get_or_create(
        id=project_id,
        defaults={
            "identifier": UUID(data["identifier"]) if data.get("identifier") else None,
            "title": data.get("title"),
            "address": data.get("title"),  # No separate address field in context
            "notes": data.get("notes"),
            "org_id": org_id,
            "org_name": data.get("org_name"),
            "url": data.get("org"),
            "is_residential": data.get("is_residential"),
            "is_pricing_locked": data.get("is_pricing_locked"),
            "installation_date": data.get("installation_date"),
            "language": data.get("language"),
            "created_date": data.get("modified_date"),
            "modified_date": data.get("modified_date"),
            "lat": float(data.get("lat")) if data.get("lat") else None,
            "lon": float(data.get("lon")) if data.get("lon") else None,
            "locality": data.get("locality"),
            "state": data.get("state"),
            "roof_type_name": data.get("roof_type_name"),
            "roof_type": data.get("roof_type"),
            "proposal_template_settings": (
                json.loads(data.get("proposal_template_settings", "{}"))
                if data.get("proposal_template_settings")
                else None
            ),
            "simulate_first_year_only": data.get("simulate_first_year_only"),
            "sold_date": data.get("sold_date"),
            "stage": int(data.get("stage")) if data.get("stage") else None,
            "stage_warning": data.get("stage_warning"),
            "system_sold": data.get("system_sold"),
            "system_installed": data.get("system_installed"),
            "temperature_min_max": (
                [
                    float(data.get("temperature_min_max[0]", 0)),
                    float(data.get("temperature_min_max[1]", 0)),
                ]
                if data.get("temperature_min_max[0]")
                and data.get("temperature_min_max[1]")
                else None
            ),
            "serial_numbers_panels": data.get("serial_numbers_panels"),
            "serial_numbers_inverters": data.get("serial_numbers_inverters"),
            "serial_numbers_batteries": data.get("serial_numbers_batteries"),
            "share_link": data.get("share_link"),
            "timezone_offset": (
                float(data.get("timezone_offset"))
                if data.get("timezone_offset")
                else None
            ),
            "private_files_data": (
                json.dumps(
                    [
                        {
                            "url": data.get("private_files_data[0].url"),
                            "org": data.get("private_files_data[0].org"),
                            "document_template": data.get(
                                "private_files_data[0].document_template"
                            ),
                            "project": data.get("private_files_data[0].project"),
                            "user": data.get("private_files_data[0].user"),
                            "file_tags": [
                                data.get("private_files_data[0].file_tags[0]"),
                                data.get("private_files_data[0].file_tags[1]"),
                            ],
                            "file_tags_data": [
                                {
                                    "url": data.get(
                                        "private_files_data[0].file_tags_data[0].url"
                                    ),
                                    "title": data.get(
                                        "private_files_data[0].file_tags_data[0].title"
                                    ),
                                    "type": data.get(
                                        "private_files_data[0].file_tags_data[0].type"
                                    ),
                                }
                            ],
                        }
                    ]
                )
                if data.get("private_files_data[0].url")
                else None
            ),
        },
    )

    # 3. System(s)
    # Only one system in context: systems[0]
    sys_prefix = "systems[0]."
    system_id = int(data[sys_prefix + "id"])
    system, created = System.get_or_create(
        id=system_id,
        defaults={
            "url": data.get(sys_prefix + "url"),
            "name": data.get(sys_prefix + "name"),
            "uuid": (
                UUID(data[sys_prefix + "uuid"])
                if data.get(sys_prefix + "uuid")
                else None
            ),
            "order": int(data.get(sys_prefix + "order", 0)),
            "system_lifetime": int(data.get(sys_prefix + "system_lifetime", 0)),
            "inverter_range": data.get(sys_prefix + "inverter_range"),
            "dc_optimizer_active": data.get(sys_prefix + "dc_optimizer_active"),
            "dc_optimizer_efficiency": float(
                data.get(sys_prefix + "dc_optimizer_efficiency", 1.0)
            ),
            "show_customer": data.get(sys_prefix + "show_customer"),
            "is_current": data.get(sys_prefix + "is_current"),
            "auto_string": data.get(sys_prefix + "auto_string"),
            "discount": float(data.get(sys_prefix + "discount", 0.0)),
            "adders_per_system": float(data.get(sys_prefix + "adders_per_system", 0.0)),
            "adders_per_panel": float(data.get(sys_prefix + "adders_per_panel", 0.0)),
            "adders_per_watt": float(data.get(sys_prefix + "adders_per_watt", 0.0)),
            "kw_stc": float(data.get(sys_prefix + "kw_stc", 0.0)),
            "battery_total_kwh": float(data.get(sys_prefix + "battery_total_kwh", 0.0)),
            "price_including_tax": float(
                data.get(sys_prefix + "price_including_tax", 0.0)
            ),
            "price_excluding_tax": float(
                data.get(sys_prefix + "price_excluding_tax", 0.0)
            ),
            "net_profit": float(data.get(sys_prefix + "net_profit", 0.0)),
            "module_quantity": int(data.get(sys_prefix + "module_quantity", 0)),
            "co2_tons_lifetime": float(data.get(sys_prefix + "co2_tons_lifetime", 0.0)),
            "project_id": project_id,
            "org_id": org_id,
            "pricing_scheme": data.get(sys_prefix + "pricing_scheme"),
            "pricing_scheme_data": (
                json.loads(
                    data.get(
                        sys_prefix + "pricing_scheme_data.configuration_json", "{}"
                    )
                )
                if data.get(sys_prefix + "pricing_scheme_data.configuration_json")
                else None
            ),
            "battery_scheme": data.get(sys_prefix + "battery_scheme"),
            "output_annual_kwh": float(data.get(sys_prefix + "output_annual_kwh", 0.0)),
            "consumption_offset_percentage": float(
                data.get(sys_prefix + "consumption_offset_percentage", 0.0)
            ),
            "commission": (
                float(data.get(sys_prefix + "commission", 0.0))
                if data.get(sys_prefix + "commission")
                else None
            ),
            "commission_override_manually": float(
                data.get(sys_prefix + "commission_override_manually", 0.0)
            ),
            "system_sold": data.get(sys_prefix + "system_sold"),
            "modules": None,  # We'll store modules in SystemModule
            "inverters": None,  # We'll store in SystemInverter
            "batteries": None,  # We'll store in SystemBattery
            "others": None,
            "integration_json": None,
        },
    )

    # 4. System Modules
    for i in range(2):  # Only 2 modules in context
        mod_prefix = f"systems[0].modules[{i}]."
        if data.get(mod_prefix + "module_activation_id"):
            SystemModule.create(
                system_id=system_id,
                module_activation_id=int(data.get(mod_prefix + "module_activation_id")),
                code=data.get(mod_prefix + "code"),
                manufacturer_name=data.get(mod_prefix + "manufacturer_name"),
                quantity=int(data.get(mod_prefix + "quantity", 0)),
            )

    # 5. System Inverters
    for i in range(1):  # Only 1 inverter in context
        inv_prefix = f"systems[0].inverters[{i}]."
        if data.get(inv_prefix + "inverter_activation_id"):
            SystemInverter.create(
                system_id=system_id,
                inverter_activation_id=int(
                    data.get(inv_prefix + "inverter_activation_id")
                ),
                code=data.get(inv_prefix + "code"),
                manufacturer_name=data.get(inv_prefix + "manufacturer_name"),
                quantity=int(data.get(inv_prefix + "quantity", 0)),
            )

    # 6. System Batteries
    for i in range(1):  # Only 1 battery in context
        bat_prefix = f"systems[0].batteries[{i}]."
        if data.get(bat_prefix + "battery_activation_id"):
            SystemBattery.create(
                system_id=system_id,
                battery_activation_id=int(
                    data.get(bat_prefix + "battery_activation_id")
                ),
                code=data.get(bat_prefix + "code"),
                manufacturer_name=data.get(bat_prefix + "manufacturer_name"),
                quantity=int(data.get(bat_prefix + "quantity", 0)),
            )

    # 7. Events
    # There are 4 events in the context (events_data[25] to events_data[28])
    for idx in range(25, 29):
        ev_prefix = f"events_data[{idx}]."
        if data.get(ev_prefix + "id"):
            Event.create(
                id=(
                    int(data.get(ev_prefix + "id"))
                    if data.get(ev_prefix + "id")
                    else None
                ),
                org=data.get(ev_prefix + "org"),
                project_id=project_id,
                duration=(
                    int(data.get(ev_prefix + "duration", 0))
                    if data.get(ev_prefix + "duration")
                    else None
                ),
                event_type_id=(
                    int(data.get(ev_prefix + "event_type_id", 0))
                    if data.get(ev_prefix + "event_type_id")
                    else None
                ),
                action_id=(
                    int(data.get(ev_prefix + "action_id", 0))
                    if data.get(ev_prefix + "action_id")
                    else None
                ),
                start=(
                    datetime.fromisoformat(
                        data.get(ev_prefix + "start").replace("Z", "+00:00")
                    )
                    if data.get(ev_prefix + "start")
                    else None
                ),
                end=(
                    datetime.fromisoformat(
                        data.get(ev_prefix + "end").replace("Z", "+00:00")
                    )
                    if data.get(ev_prefix + "end")
                    else None
                ),
                created_date=(
                    datetime.fromisoformat(
                        data.get(ev_prefix + "created_date").replace("Z", "+00:00")
                    )
                    if data.get(ev_prefix + "created_date")
                    else None
                ),
                modified_date=(
                    datetime.fromisoformat(
                        data.get(ev_prefix + "modified_date").replace("Z", "+00:00")
                    )
                    if data.get(ev_prefix + "modified_date")
                    else None
                ),
                who_display=data.get(ev_prefix + "who.display"),
                who_email=data.get(ev_prefix + "who.email"),
                who_portrait_image_public_url=data.get(
                    ev_prefix + "who.portrait_image_public_url"
                ),
                completion_date=(
                    datetime.fromisoformat(
                        data.get(ev_prefix + "completion_date").replace("Z", "+00:00")
                    )
                    if data.get(ev_prefix + "completion_date")
                    else None
                ),
                title=data.get(ev_prefix + "title"),
                project_name=data.get(ev_prefix + "project_name"),
                is_planned=data.get(ev_prefix + "is_planned"),
                task_status=(
                    int(data.get(ev_prefix + "task_status", 0))
                    if data.get(ev_prefix + "task_status")
                    else None
                ),
                is_complete=data.get(ev_prefix + "is_complete"),
                notes=data.get(ev_prefix + "notes"),
                is_archived=data.get(ev_prefix + "is_archived"),
                categories=(
                    [
                        int(data.get(ev_prefix + f"categories[{i}]"))
                        for i in range(2)
                        if data.get(ev_prefix + f"categories[{i}]")
                    ]
                    if data.get(ev_prefix + "categories[0]")
                    else None
                ),
                form_config=(
                    int(data.get(ev_prefix + "form_config", 0))
                    if data.get(ev_prefix + "form_config")
                    else None
                ),
                event_icon=(
                    int(data.get(ev_prefix + "event_icon", 0))
                    if data.get(ev_prefix + "event_icon")
                    else None
                ),
            )

    # 8. Available Customer Actions
    for i in range(1):  # Only 1 available_customer_actions[0] in context
        aca_prefix = f"available_customer_actions[{i}]."
        if data.get(aca_prefix + "system_uuid"):
            actions_available = []
            for j in range(1):  # Only 1 actions_available[0] in context
                aa_prefix = aca_prefix + f"actions_available[{j}]."
                aa_dict = {
                    k[len(aa_prefix) :]: data[k]
                    for k in data
                    if k.startswith(aa_prefix)
                }
                if aa_dict:
                    actions_available.append(aa_dict)
            AvailableCustomerAction.create(
                project_id=project_id,
                system_uuid=UUID(data.get(aca_prefix + "system_uuid")),
                actions_available=actions_available,
            )

    # 9. Transactions
    for i in range(1):  # Only 1 transactions_data[0] in context
        t_prefix = f"transactions_data[{i}]."
        if data.get(t_prefix + "url"):
            Transaction.create(
                id=int(data.get(t_prefix + "url").split("/")[-2]),
                url=data.get(t_prefix + "url"),
                org=data.get(t_prefix + "org"),
                org_id=org_id,
                org_name=data.get(t_prefix + "org_name"),
                project=data.get(t_prefix + "project"),
                project_name=data.get(t_prefix + "project_name"),
            )


if __name__ == "__main__":
    # Example: Load data from a flat key-value dict (as in your context)
    # You would typically parse your document into a dict like this:
    # data = { 'org_id': ..., 'systems[0].id': ..., ... }
    # For demonstration, you can load from a JSON file or dict
    import sys
    import yaml

    # Example: python ingest.py data.yaml
    if len(sys.argv) < 2:
        print("Usage: python ingest.py <data.yaml>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        data = yaml.safe_load(f)
    ingest_data(data)
    print("Data ingestion complete.")
