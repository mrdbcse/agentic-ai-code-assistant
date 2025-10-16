# peewee_orm_ingest.py
"""
Data ingestion script for Solar Energy Project Management DB using Peewee ORM (PostgreSQL).
Covers all tables in the provided schema.
"""

import json
import os
from datetime import date, datetime

from peewee import *
from playhouse.postgres_ext import ArrayField, JSONField, PostgresqlExtDatabase

# Database connection
DB_NAME = os.getenv("DB_NAME", "solar_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", 5432))

db = PostgresqlExtDatabase(
    DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
)


# Peewee Models
class BaseModel(Model):
    class Meta:
        database = db


class Organization(BaseModel):
    id = BigIntegerField(primary_key=True)
    name = TextField()
    country_iso2 = CharField(max_length=2, null=True)
    country_name = TextField(null=True)
    address = TextField(null=True)


class UserRole(BaseModel):
    id = BigIntegerField(primary_key=True)
    email = TextField(null=True)
    is_admin = BooleanField(null=True)
    user_url = TextField(null=True)
    user_email = TextField(null=True)
    org = ForeignKeyField(
        Organization, backref="user_roles", column_name="org_id", null=True
    )
    is_hidden = BooleanField(null=True)
    url = TextField(null=True)
    first_name = TextField(null=True)
    family_name = TextField(null=True)
    job_title = TextField(null=True)
    accreditation = TextField(null=True)
    user_phone = TextField(null=True)
    display = TextField(null=True)
    phone = TextField(null=True)
    allow_email_notifications = BooleanField(null=True)
    portrait_image = TextField(null=True)
    google_calendar_id = TextField(null=True)
    has_logged_in = BooleanField(null=True)
    schedule_meeting_url = TextField(null=True)
    schedule_meeting_label = TextField(null=True)
    api_key_chat = TextField(null=True)
    user_is_staff = BooleanField(null=True)
    org_name = TextField(null=True)
    mosaic_sales_rep_id = TextField(null=True)
    ironridge_email = TextField(null=True)
    ironridge_terms_accepted = BooleanField(null=True)
    integration_json = JSONField(null=True)
    loanpal_channels = TextField(null=True)
    sungage_email = TextField(null=True)
    permissions_role = IntegerField(null=True)
    permissions_role_title = TextField(null=True)
    brighte_agent_id = TextField(null=True)
    dividend_contact_id = TextField(null=True)
    user_data = JSONField(null=True)
    phoenix_user_email = TextField(null=True)
    managed_by = TextField(null=True)
    portrait_image_public_url = TextField(null=True)
    non_admin_editable = BooleanField(null=True)


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
    org = ForeignKeyField(
        Organization, backref="contacts", column_name="org_id", null=True
    )
    identifier = TextField(null=True)
    type = IntegerField(null=True)
    custom_data = JSONField(null=True)


class Project(BaseModel):
    id = BigIntegerField(primary_key=True)
    identifier = UUIDField(null=True)
    title = TextField(null=True)
    address = TextField(null=True)
    locality = TextField(null=True)
    state = TextField(null=True)
    zip = TextField(null=True)
    country_iso2 = CharField(max_length=2, null=True)
    lat = DecimalField(null=True)
    lon = DecimalField(null=True)
    org = ForeignKeyField(
        Organization, backref="projects", column_name="org_id", null=True
    )
    org_name = TextField(null=True)
    created_date = DateTimeField(null=True)
    modified_date = DateTimeField(null=True)
    notes = TextField(null=True)
    contract_date = DateField(null=True)
    installation_date = DateField(null=True)
    sold_date = DateTimeField(null=True)
    is_residential = BooleanField(null=True)
    is_pricing_locked = BooleanField(null=True)
    priority = IntegerField(null=True)
    lead_source = TextField(null=True)
    number_of_phases = IntegerField(null=True)
    number_of_wires = IntegerField(null=True)
    number_of_storeys = IntegerField(null=True)
    payment_option_sold = TextField(null=True)
    payment_option_sold_title = TextField(null=True)
    project_installed = IntegerField(null=True)
    project_sold = IntegerField(null=True)
    project_stage = IntegerField(null=True)
    stage_warning = TextField(null=True)
    stage = IntegerField(null=True)
    roof_type_name = TextField(null=True)
    roof_type = TextField(null=True)
    simulate_first_year_only = BooleanField(null=True)
    usage_annual_or_guess = DecimalField(null=True)
    usage = DecimalField(null=True)
    timezone_offset = DecimalField(null=True)
    valid_until_date = DateField(null=True)
    years_to_simulate = IntegerField(null=True)
    wind_region = TextField(null=True)
    has_cellular_coverage = BooleanField(null=True)
    allow_email_notifications = BooleanField(null=True)
    brighte_role_connection_status = TextField(null=True)
    auto_apply_max_simulate_years = BooleanField(null=True)
    is_lite = BooleanField(null=True)
    custom_data = JSONField(null=True)
    shared_with = JSONField(null=True)
    workflow_id = BigIntegerField(null=True)
    active_stage_id = BigIntegerField(null=True)
    active_stage_title = TextField(null=True)


class System(BaseModel):
    id = BigIntegerField(primary_key=True)
    uuid = UUIDField(null=True)
    project = ForeignKeyField(
        Project, backref="systems", column_name="project_id", null=True
    )
    org = ForeignKeyField(
        Organization, backref="systems", column_name="org_id", null=True
    )
    name = TextField(null=True)
    order_num = IntegerField(null=True)
    system_lifetime = IntegerField(null=True)
    inverter_range = TextField(null=True)
    dc_optimizer_active = BooleanField(null=True)
    dc_optimizer_efficiency = DecimalField(null=True)
    show_customer = BooleanField(null=True)
    is_current = BooleanField(null=True)
    auto_string = BooleanField(null=True)
    discount = DecimalField(null=True)
    adders_per_system = DecimalField(null=True)
    adders_per_panel = DecimalField(null=True)
    adders_per_watt = DecimalField(null=True)
    kw_stc = DecimalField(null=True)
    battery_total_kwh = DecimalField(null=True)
    price_including_tax = DecimalField(null=True)
    price_excluding_tax = DecimalField(null=True)
    net_profit = DecimalField(null=True)
    module_quantity = IntegerField(null=True)
    co2_tons_lifetime = DecimalField(null=True)
    pricing_scheme = TextField(null=True)
    output_annual_kwh = DecimalField(null=True)
    consumption_offset_percentage = DecimalField(null=True)
    commission = DecimalField(null=True)
    commission_override_manually = DecimalField(null=True)
    system_sold = BooleanField(null=True)
    pricing_scheme_id = BigIntegerField(null=True)


class SystemModule(BaseModel):
    id = AutoField()
    system = ForeignKeyField(System, backref="modules", column_name="system_id")
    module_activation_id = BigIntegerField(null=True)
    code = TextField(null=True)
    manufacturer_name = TextField(null=True)
    quantity = IntegerField(null=True)


class SystemInverter(BaseModel):
    id = AutoField()
    system = ForeignKeyField(System, backref="inverters", column_name="system_id")
    inverter_activation_id = BigIntegerField(null=True)
    code = TextField(null=True)
    manufacturer_name = TextField(null=True)
    quantity = IntegerField(null=True)


class SystemBattery(BaseModel):
    id = AutoField()
    system = ForeignKeyField(System, backref="batteries", column_name="system_id")
    battery_activation_id = BigIntegerField(null=True)
    code = TextField(null=True)
    manufacturer_name = TextField(null=True)
    quantity = IntegerField(null=True)


class Action(BaseModel):
    id = BigIntegerField(primary_key=True)
    url = TextField(null=True)
    org = TextField(null=True)
    stage = IntegerField(null=True)
    title = TextField(null=True)
    order_num = IntegerField(null=True)
    created_date = DateTimeField(null=True)
    modified_date = DateTimeField(null=True)
    share_with_orgs = JSONField(null=True)
    org_shared_time = JSONField(null=True)


class ActionWorkflow(BaseModel):
    id = AutoField()
    action = ForeignKeyField(Action, backref="workflows", column_name="action_id")
    workflow = TextField(null=True)
    stage = TextField(null=True)


class Event(BaseModel):
    id = BigIntegerField(primary_key=True)
    org = TextField(null=True)
    project = ForeignKeyField(
        Project, backref="events", column_name="project_id", null=True
    )
    duration = IntegerField(null=True)
    event_type_id = IntegerField(null=True)
    action = ForeignKeyField(
        Action, backref="events", column_name="action_id", null=True
    )
    start = DateTimeField(null=True)
    end_time = DateTimeField(null=True)
    created_date = DateTimeField(null=True)
    modified_date = DateTimeField(null=True)
    who_display = TextField(null=True)
    who_email = TextField(null=True)
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


class EventTeamMember(BaseModel):
    event = ForeignKeyField(Event, backref="team_members", column_name="event_id")
    team_member_url = TextField(null=True)

    class Meta:
        primary_key = CompositeKey("event", "team_member_url")


class FileTag(BaseModel):
    id = BigIntegerField(primary_key=True)
    url = TextField(null=True)
    title = TextField(null=True)
    type = TextField(null=True)


class PrivateFile(BaseModel):
    id = BigIntegerField(primary_key=True)
    url = TextField(null=True)
    org = TextField(null=True)
    document_template = TextField(null=True)
    project = TextField(null=True)
    user = TextField(null=True)
    title = TextField(null=True)
    system_uuid = UUIDField(null=True)
    input_data = JSONField(null=True)
    input_data_hash = TextField(null=True)
    file_hash = TextField(null=True)
    status = TextField(null=True)
    status_message = TextField(null=True)
    filesize = BigIntegerField(null=True)
    file_contents = TextField(null=True)
    show_customer = BooleanField(null=True)
    created_date = DateTimeField(null=True)
    modified_date = DateTimeField(null=True)
    temporary = BooleanField(null=True)


class PrivateFileTag(BaseModel):
    private_file = ForeignKeyField(
        PrivateFile, backref="tags", column_name="private_file_id"
    )
    file_tag = ForeignKeyField(
        FileTag, backref="private_files", column_name="file_tag_id"
    )

    class Meta:
        primary_key = CompositeKey("private_file", "file_tag")


class Transaction(BaseModel):
    id = BigIntegerField(primary_key=True)
    url = TextField(null=True)
    org = TextField(null=True)
    org_ref = ForeignKeyField(
        Organization, backref="transactions", column_name="org_id", null=True
    )
    org_name = TextField(null=True)
    project = TextField(null=True)
    project_name = TextField(null=True)
    system = TextField(null=True)
    payment_option = TextField(null=True)
    is_complete = BooleanField(null=True)
    transaction_datetime = DateTimeField(null=True)
    amount = DecimalField(null=True)
    tax_included = DecimalField(null=True)
    surcharge_amount = DecimalField(null=True)
    funds_confirmed = BooleanField(null=True)
    details = JSONField(null=True)
    contract_details = JSONField(null=True)
    contract_details_hash = TextField(null=True)
    signature_data = TextField(null=True)
    is_commission_payable = BooleanField(null=True)
    transaction_type = TextField(null=True)
    prior_transaction_type = TextField(null=True)
    customer_name = TextField(null=True)
    created_date = DateTimeField(null=True)
    modified_date = DateTimeField(null=True)
    credit_expiration_date = DateTimeField(null=True)


class UtilityTariff(BaseModel):
    id = BigIntegerField(primary_key=True)
    name = TextField(null=True)
    code = TextField(null=True)
    utility_id = BigIntegerField(null=True)
    utility_name = TextField(null=True)
    utility_aliases = ArrayField(TextField, null=True)
    sector = IntegerField(null=True)
    description = TextField(null=True)
    precision = TextField(null=True)
    data = JSONField(null=True)


class PricingScheme(BaseModel):
    id = BigIntegerField(primary_key=True)
    url = TextField(null=True)
    org = TextField(null=True)
    is_archived = BooleanField(null=True)
    pricing_formula = TextField(null=True)
    title = TextField(null=True)
    priority = IntegerField(null=True)
    configuration_json = JSONField(null=True)
    created_date = DateTimeField(null=True)
    modified_date = DateTimeField(null=True)
    auto_apply_enabled = BooleanField(null=True)


class SystemOther(BaseModel):
    id = AutoField()
    system = ForeignKeyField(System, backref="others", column_name="system_id")
    other_json = JSONField(null=True)


class SystemAction(BaseModel):
    system = ForeignKeyField(System, backref="actions", column_name="system_id")
    action = ForeignKeyField(Action, backref="systems", column_name="action_id")

    class Meta:
        primary_key = CompositeKey("system", "action")


class SystemEvent(BaseModel):
    system = ForeignKeyField(System, backref="events", column_name="system_id")
    event = ForeignKeyField(Event, backref="systems", column_name="event_id")

    class Meta:
        primary_key = CompositeKey("system", "event")


# Add more models as needed for extensibility


# --- Data Ingestion Functions ---
def create_tables():
    db.connect()
    db.create_tables(
        [
            Organization,
            UserRole,
            Contact,
            Project,
            System,
            SystemModule,
            SystemInverter,
            SystemBattery,
            Action,
            ActionWorkflow,
            Event,
            EventTeamMember,
            FileTag,
            PrivateFile,
            PrivateFileTag,
            Transaction,
            UtilityTariff,
            PricingScheme,
            SystemOther,
            SystemAction,
            SystemEvent,
        ]
    )
    db.close()


def ingest_organization(data):
    org, created = Organization.get_or_create(
        id=data["id"],
        defaults={
            "name": data.get("name"),
            "country_iso2": data.get("country_iso2"),
            "country_name": data.get("country_name"),
            "address": data.get("address"),
        },
    )
    return org


# Add similar ingest functions for each model as needed
# Example for Action:
def ingest_action(data):
    action, created = Action.get_or_create(
        id=data["id"],
        defaults={
            "url": data.get("url"),
            "org": data.get("org"),
            "stage": data.get("stage"),
            "title": data.get("title"),
            "order_num": data.get("order"),
            "created_date": data.get("created_date"),
            "modified_date": data.get("modified_date"),
            "share_with_orgs": data.get("share_with_orgs"),
            "org_shared_time": data.get("org_shared_time"),
        },
    )
    return action


# Example for Event:
def ingest_event(data, project=None, action=None):
    event, created = Event.get_or_create(
        id=data["id"],
        defaults={
            "org": data.get("org"),
            "project": project,
            "duration": data.get("duration"),
            "event_type_id": data.get("event_type_id"),
            "action": action,
            "start": data.get("start"),
            "end_time": data.get("end_time"),
            "created_date": data.get("created_date"),
            "modified_date": data.get("modified_date"),
            "who_display": data.get("who_display"),
            "who_email": data.get("who_email"),
            "completion_date": data.get("completion_date"),
            "title": data.get("title"),
            "project_name": data.get("project_name"),
            "is_planned": data.get("is_planned"),
            "task_status": data.get("task_status"),
            "is_complete": data.get("is_complete"),
            "notes": data.get("notes"),
            "is_archived": data.get("is_archived"),
            "categories": data.get("categories"),
            "form_config": data.get("form_config"),
            "event_icon": data.get("event_icon"),
        },
    )
    return event


# Add more ingest functions as needed for other models


def main():
    # Example: create tables
    create_tables()

    # Example: ingest organization
    org_data = {
        "id": 1,
        "name": "OpenSolar",
        "country_iso2": "US",
        "country_name": "United States",
        "address": "123 Solar St, Sunnyvale, CA",
    }
    org = ingest_organization(org_data)

    # Example: ingest action
    action_data = {
        "id": 1001,
        "url": "https://api.opensolar.com/api/orgs/1/actions/1001/",
        "org": "https://api.opensolar.com/api/orgs/1/",
        "stage": 0,
        "title": "Design Systems",
        "order": 0,
        "created_date": datetime.now(),
        "modified_date": datetime.now(),
        "share_with_orgs": [],
        "org_shared_time": None,
    }
    action = ingest_action(action_data)

    # Example: ingest event
    event_data = {
        "id": 2001,
        "org": "https://api.opensolar.com/api/orgs/1/",
        "project_id": None,
        "duration": 60,
        "event_type_id": 1,
        "action_id": 1001,
        "start": datetime.now(),
        "end_time": datetime.now(),
        "created_date": datetime.now(),
        "modified_date": datetime.now(),
        "who_display": "John Doe",
        "who_email": "john@opensolar.com",
        "completion_date": None,
        "title": "System Design Review",
        "project_name": "Project X",
        "is_planned": False,
        "task_status": 0,
        "is_complete": True,
        "notes": None,
        "is_archived": False,
        "categories": [0, 7],
        "form_config": 4,
        "event_icon": 3,
    }
    event = ingest_event(event_data, project=None, action=action)

    print(f"Organization: {org.name}, Action: {action.title}, Event: {event.title}")


if __name__ == "__main__":
    main()
