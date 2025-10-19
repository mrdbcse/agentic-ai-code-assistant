"""
Python script for data ingestion using Peewee ORM (PostgreSQL) for Solar Energy Project JSON
This script assumes the DB schema provided is already created in the PostgreSQL database.
The script parses the provided context (as a dict or JSON) and ingests the data into the normalized tables.

Assumptions:
- The context is parsed into a Python dict (from JSON or other source).
- Only the tables present in the provided DB schema are used.
- The script is idempotent for the provided data (uses get_or_create or upsert where appropriate).
- The script focuses on the main entities present in the context: organization, project, roles, systems, modules, inverters, batteries, pricing_scheme, costing, configuration, customer_action, transaction, etc.
- The script is written for clarity and maintainability, not for maximum performance.
"""

import peewee as pw
import uuid
from datetime import datetime
import json

# Database connection
pg_db = pw.PostgresqlDatabase(
    "solar_db",  # Change to your DB name
    user="postgres",
    password="password",
    host="localhost",
    port=5432,
)


# Peewee Models (only those used in this script)
class BaseModel(pw.Model):
    class Meta:
        database = pg_db


class Organization(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    name = pw.TextField(null=True)
    url = pw.TextField(null=True)


class Project(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    identifier = pw.UUIDField(null=True)
    org_id = pw.BigIntegerField(null=True)
    org_name = pw.TextField(null=True)
    url = pw.TextField(null=True)
    title = pw.TextField(null=True)
    address = pw.TextField(null=True)
    state = pw.TextField(null=True)
    sold_date = pw.DateTimeField(null=True)
    stage = pw.IntegerField(null=True)
    stage_warning = pw.TextField(null=True)
    site_notes = pw.TextField(null=True)
    roof_type_name = pw.TextField(null=True)
    roof_type = pw.TextField(null=True)
    simulate_first_year_only = pw.BooleanField(null=True)
    share_link = pw.TextField(null=True)
    system_sold = pw.TextField(null=True)


class Role(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    email = pw.TextField(null=True)
    is_admin = pw.BooleanField(null=True)
    user = pw.TextField(null=True)
    user_email = pw.TextField(null=True)
    org = pw.TextField(null=True)
    is_hidden = pw.BooleanField(null=True)
    url = pw.TextField(null=True)
    first_name = pw.TextField(null=True)
    family_name = pw.TextField(null=True)
    job_title = pw.TextField(null=True)
    accreditation = pw.TextField(null=True)
    user_phone = pw.TextField(null=True)
    display = pw.TextField(null=True)
    phone = pw.TextField(null=True)
    allow_email_notifications = pw.BooleanField(null=True)
    portrait_image = pw.TextField(null=True)
    google_calendar_id = pw.TextField(null=True)
    has_logged_in = pw.BooleanField(null=True)
    schedule_meeting_url = pw.TextField(null=True)
    schedule_meeting_label = pw.TextField(null=True)
    api_key_chat = pw.TextField(null=True)
    user_is_staff = pw.BooleanField(null=True)
    org_name = pw.TextField(null=True)
    mosaic_sales_rep_id = pw.TextField(null=True)
    ironridge_email = pw.TextField(null=True)
    ironridge_terms_accepted = pw.TextField(null=True)
    integration_json = pw.TextField(null=True)
    loanpal_channels = pw.TextField(null=True)
    sungage_email = pw.TextField(null=True)
    permissions_role = pw.IntegerField(null=True)
    permissions_role_title = pw.TextField(null=True)
    brighte_agent_id = pw.TextField(null=True)
    dividend_contact_id = pw.TextField(null=True)
    user_data = pw.TextField(null=True)
    phoenix_user_email = pw.TextField(null=True)
    managed_by = pw.TextField(null=True)
    portrait_image_public_url = pw.TextField(null=True)
    non_admin_editable = pw.BooleanField(null=True)


class ProjectRoleAssignment(BaseModel):
    project_id = pw.BigIntegerField()
    role_id = pw.BigIntegerField()
    role_type = pw.TextField()

    class Meta:
        primary_key = pw.CompositeKey("project_id", "role_id", "role_type")


class System(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    url = pw.TextField(null=True)
    name = pw.TextField(null=True)
    uuid = pw.UUIDField(null=True)
    order = pw.IntegerField(null=True)
    system_lifetime = pw.IntegerField(null=True)
    inverter_range = pw.TextField(null=True)
    dc_optimizer_active = pw.BooleanField(null=True)
    dc_optimizer_efficiency = pw.FloatField(null=True)
    show_customer = pw.BooleanField(null=True)
    is_current = pw.BooleanField(null=True)
    auto_string = pw.BooleanField(null=True)
    discount = pw.FloatField(null=True)
    adders_per_system = pw.FloatField(null=True)
    adders_per_panel = pw.FloatField(null=True)
    adders_per_watt = pw.FloatField(null=True)
    kw_stc = pw.FloatField(null=True)
    battery_total_kwh = pw.FloatField(null=True)
    price_including_tax = pw.FloatField(null=True)
    price_excluding_tax = pw.FloatField(null=True)
    net_profit = pw.FloatField(null=True)
    module_quantity = pw.IntegerField(null=True)
    co2_tons_lifetime = pw.FloatField(null=True)
    project_id = pw.BigIntegerField(null=True)
    org = pw.TextField(null=True)
    pricing_scheme = pw.TextField(null=True)
    battery_scheme = pw.TextField(null=True)
    output_annual_kwh = pw.FloatField(null=True)
    consumption_offset_percentage = pw.FloatField(null=True)
    integration_json = pw.TextField(null=True)
    commission = pw.FloatField(null=True)
    commission_override_manually = pw.FloatField(null=True)
    system_sold = pw.BooleanField(null=True)


class SystemModule(BaseModel):
    system_id = pw.BigIntegerField()
    module_activation_id = pw.BigIntegerField()
    code = pw.TextField(null=True)
    manufacturer_name = pw.TextField(null=True)
    quantity = pw.IntegerField(null=True)

    class Meta:
        primary_key = pw.CompositeKey("system_id", "module_activation_id")


class SystemInverter(BaseModel):
    system_id = pw.BigIntegerField()
    inverter_activation_id = pw.BigIntegerField()
    code = pw.TextField(null=True)
    manufacturer_name = pw.TextField(null=True)
    quantity = pw.IntegerField(null=True)

    class Meta:
        primary_key = pw.CompositeKey("system_id", "inverter_activation_id")


class SystemBattery(BaseModel):
    system_id = pw.BigIntegerField()
    battery_activation_id = pw.BigIntegerField()
    code = pw.TextField(null=True)
    manufacturer_name = pw.TextField(null=True)
    quantity = pw.IntegerField(null=True)

    class Meta:
        primary_key = pw.CompositeKey("system_id", "battery_activation_id")


class PricingScheme(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    url = pw.TextField(null=True)
    org = pw.TextField(null=True)
    is_archived = pw.BooleanField(null=True)
    pricing_formula = pw.TextField(null=True)
    title = pw.TextField(null=True)
    priority = pw.IntegerField(null=True)
    configuration_json = pw.TextField(null=True)
    created_date = pw.DateTimeField(null=True)
    modified_date = pw.DateTimeField(null=True)
    auto_apply_enabled = pw.BooleanField(null=True)
    auto_apply_only_specified_states = pw.TextField(null=True)
    auto_apply_only_specified_zips = pw.TextField(null=True)
    auto_apply_component_codes = pw.TextField(null=True)
    auto_apply_min_system_size = pw.FloatField(null=True)
    auto_apply_max_system_size = pw.FloatField(null=True)
    auto_apply_min_battery_kwh = pw.FloatField(null=True)
    auto_apply_max_battery_kwh = pw.FloatField(null=True)
    auto_apply_battery_capacity_type = pw.IntegerField(null=True)
    auto_apply_sector = pw.IntegerField(null=True)


class Costing(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    is_archived = pw.FloatField(null=True)
    # ... (other fields omitted for brevity)


class Configuration(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    url = pw.TextField(null=True)
    org = pw.TextField(null=True)
    title = pw.TextField(null=True)
    description = pw.TextField(null=True)
    priority = pw.BooleanField(null=True)
    created_date = pw.DateTimeField(null=True)
    modified_date = pw.DateTimeField(null=True)
    performance_calculator = pw.IntegerField(null=True)
    weather_dataset = pw.IntegerField(null=True)
    horizon_shading_provider = pw.IntegerField(null=True)
    inverter_modelling_automation = pw.IntegerField(null=True)
    setbacks_default = pw.FloatField(null=True)
    setbacks_gutter = pw.FloatField(null=True)
    setbacks_ridge = pw.FloatField(null=True)
    setbacks_valley = pw.FloatField(null=True)
    setbacks_hip = pw.FloatField(null=True)
    setbacks_rake = pw.FloatField(null=True)
    setbacks_shared = pw.FloatField(null=True)
    setbacks_flat_gutter = pw.FloatField(null=True)
    setbacks_skylight = pw.FloatField(null=True)
    setbacks_dormer = pw.FloatField(null=True)
    setbacks_objects = pw.FloatField(null=True)
    setbacks_arrays = pw.FloatField(null=True)
    module_spacing_horizontal = pw.FloatField(null=True)
    module_spacing_vertical = pw.FloatField(null=True)
    tilt_rack_default_tilt = pw.FloatField(null=True)
    tilt_rack_default_orientation = pw.TextField(null=True)
    apply_tilt_racks_below_slope = pw.FloatField(null=True)
    years_to_simulate = pw.IntegerField(null=True)
    performance_adjustment = pw.FloatField(null=True)
    discount_rate = pw.FloatField(null=True)
    utility_inflation_annual = pw.FloatField(null=True)
    utility_inflation_annual_upper_bound = pw.FloatField(null=True)
    utility_inflation_annual_lower_bound = pw.FloatField(null=True)
    feed_in_tariff_inflation_annual = pw.FloatField(null=True)
    lower_bound_scaling_factors = pw.TextField(null=True)
    upper_bound_scaling_factors = pw.TextField(null=True)
    scaling_factors_label = pw.TextField(null=True)
    proposed_usage_adjustment = pw.FloatField(null=True)
    sam_string_soiling = pw.FloatField(null=True)
    sam_string_dc_wiring = pw.FloatField(null=True)
    sam_string_mismatch = pw.FloatField(null=True)
    sam_micro_soiling = pw.FloatField(null=True)
    sam_micro_dc_wiring = pw.FloatField(null=True)
    sam_micro_mismatch = pw.FloatField(null=True)
    sam_optimizer_soiling = pw.FloatField(null=True)
    sam_optimizer_dc_wiring = pw.FloatField(null=True)
    sam_optimizer_mismatch = pw.FloatField(null=True)
    sam_ac_wiring = pw.FloatField(null=True)
    sam_nameplate = pw.FloatField(null=True)
    sam_diodes_and_connections = pw.FloatField(null=True)
    sam_dc_system_availability = pw.FloatField(null=True)
    sam_ac_system_availability = pw.FloatField(null=True)
    show_tax_effects_of_solar = pw.BooleanField(null=True)
    auto_apply_max_simulate_years = pw.BooleanField(null=True)
    auto_apply_only_specified_states = pw.TextField(null=True)
    auto_apply_only_specified_zips = pw.TextField(null=True)
    auto_apply_only_specified_countries = pw.TextField(null=True)
    auto_apply_sector = pw.IntegerField(null=True)
    auto_apply_priority = pw.IntegerField(null=True)


class CustomerAction(BaseModel):
    id = pw.BigAutoField(primary_key=True)
    system_uuid = pw.UUIDField(null=True)
    org_id = pw.BigIntegerField(null=True)
    project_id = pw.BigIntegerField(null=True)
    system_id = pw.BigIntegerField(null=True)
    payment_option_id = pw.BigIntegerField(null=True)
    selected_system_title = pw.TextField(null=True)
    selected_system_summary = pw.TextField(null=True)
    loan_amount = pw.FloatField(null=True)
    total_price_payable = pw.FloatField(null=True)
    paid_to_date = pw.FloatField(null=True)
    paid_to_date_tax_included = pw.FloatField(null=True)
    paid_to_date_surcharge_amount = pw.FloatField(null=True)
    balance_outstanding = pw.FloatField(null=True)
    payment_amount = pw.FloatField(null=True)
    payment_amount_tax_included = pw.FloatField(null=True)
    collect_signature = pw.BooleanField(null=True)
    payment_option_type = pw.TextField(null=True)
    payment_method = pw.TextField(null=True)
    payment_title = pw.TextField(null=True)
    payment_stripe_key = pw.TextField(null=True)
    surcharge_amount = pw.FloatField(null=True)
    payment_content = pw.TextField(null=True)
    payment_terminology = pw.TextField(null=True)
    quote_acceptance_heading = pw.TextField(null=True)
    quote_acceptance_content = pw.TextField(null=True)
    additional_details = pw.TextField(null=True)
    status_code = pw.TextField(null=True)
    status_title = pw.TextField(null=True)
    status_title_secondary = pw.TextField(null=True)
    status_description = pw.TextField(null=True)
    is_pro_facing = pw.BooleanField(null=True)
    is_customer_facing = pw.BooleanField(null=True)
    has_api_side_effect = pw.BooleanField(null=True)
    requires_docusign_signature = pw.BooleanField(null=True)
    docusign_contract_complete = pw.BooleanField(null=True)
    total_price_payable_tax_included = pw.FloatField(null=True)
    action_title = pw.TextField(null=True)
    review_action_title = pw.TextField(null=True)
    enable_cta_payment_on_proposal = pw.BooleanField(null=True)


class Transaction(BaseModel):
    id = pw.BigIntegerField(primary_key=True)
    url = pw.TextField(null=True)
    org = pw.TextField(null=True)
    org_id = pw.BigIntegerField(null=True)
    org_name = pw.TextField(null=True)
    project = pw.TextField(null=True)
    project_name = pw.TextField(null=True)


# Add more models as needed for other tables


def parse_and_ingest(context: dict):
    """
    Ingests the provided context dict into the normalized PostgreSQL tables using Peewee ORM.
    """
    with pg_db.atomic():
        # 1. Organization
        org_id = 178878
        org_name = "AOPL Energy Private Limited"
        org_url = f"https://api.opensolar.com/api/orgs/{org_id}/"
        org, _ = Organization.get_or_create(
            id=org_id, defaults={"name": org_name, "url": org_url}
        )

        # 2. Project
        project_id = 7954997
        project_url = (
            f"https://api.opensolar.com/api/orgs/{org_id}/projects/{project_id}/"
        )
        project_title = context.get("title", None)
        project_state = context.get("state", None)
        project_sold_date = context.get("sold_date", None)
        if project_sold_date:
            project_sold_date = datetime.fromisoformat(
                project_sold_date.replace("Z", "+00:00")
            )
        project_stage = int(context.get("stage", 0))
        project_stage_warning = context.get("stage_warning", None)
        project_site_notes = context.get("site_notes", None)
        project_roof_type_name = context.get("roof_type_name", None)
        project_roof_type = context.get("roof_type", None)
        project_simulate_first_year_only = context.get(
            "simulate_first_year_only", False
        )
        project_share_link = context.get("share_link", None)
        project_system_sold = context.get("system_sold", None)
        project, _ = Project.get_or_create(
            id=project_id,
            defaults={
                "identifier": uuid.uuid4(),
                "org_id": org_id,
                "org_name": org_name,
                "url": project_url,
                "title": project_title,
                "state": project_state,
                "sold_date": project_sold_date,
                "stage": project_stage,
                "stage_warning": project_stage_warning,
                "site_notes": project_site_notes,
                "roof_type_name": project_roof_type_name,
                "roof_type": project_roof_type,
                "simulate_first_year_only": project_simulate_first_year_only,
                "share_link": project_share_link,
                "system_sold": project_system_sold,
            },
        )

        # 3. Roles (Designer, Salesperson)
        # Designer
        designer_role_id = int(context.get("assigned_designer_role_id", 0))
        if designer_role_id:
            designer_role, _ = Role.get_or_create(
                id=designer_role_id,
                defaults={
                    "email": context.get("assigned_designer_role_email"),
                    "is_admin": False,
                    "user": context.get("assigned_designer_role_data.user"),
                    "user_email": context.get("assigned_designer_role_data.user_email"),
                    "org": org_url,
                    "is_hidden": False,
                    "url": context.get("assigned_designer_role"),
                    "first_name": context.get("assigned_designer_role_data.display"),
                    "family_name": None,
                    "job_title": context.get(
                        "assigned_designer_role_data.permissions_role_title"
                    ),
                    "accreditation": context.get(
                        "assigned_designer_role_data.accreditation"
                    ),
                    "user_phone": context.get("assigned_designer_role_data.user_phone"),
                    "display": context.get("assigned_designer_role_data.display"),
                    "phone": context.get("assigned_designer_role_data.phone"),
                    "allow_email_notifications": context.get(
                        "assigned_designer_role_data.allow_email_notifications"
                    ),
                    "portrait_image": context.get(
                        "assigned_designer_role_data.portrait_image"
                    ),
                    "google_calendar_id": context.get(
                        "assigned_designer_role_data.google_calendar_id"
                    ),
                    "has_logged_in": context.get(
                        "assigned_designer_role_data.has_logged_in"
                    ),
                    "schedule_meeting_url": context.get(
                        "assigned_designer_role_data.schedule_meeting_url"
                    ),
                    "schedule_meeting_label": context.get(
                        "assigned_designer_role_data.schedule_meeting_label"
                    ),
                    "api_key_chat": context.get(
                        "assigned_designer_role_data.api_key_chat"
                    ),
                    "user_is_staff": context.get(
                        "assigned_designer_role_data.user_is_staff"
                    ),
                    "org_name": context.get("assigned_designer_role_data.org_name"),
                    "mosaic_sales_rep_id": context.get(
                        "assigned_designer_role_data.mosaic_sales_rep_id"
                    ),
                    "ironridge_email": context.get(
                        "assigned_designer_role_data.ironridge_email"
                    ),
                    "ironridge_terms_accepted": context.get(
                        "assigned_designer_role_data.ironridge_terms_accepted"
                    ),
                    "integration_json": context.get(
                        "assigned_designer_role_data.integration_json"
                    ),
                    "loanpal_channels": context.get(
                        "assigned_designer_role_data.loanpal_channels"
                    ),
                    "sungage_email": context.get(
                        "assigned_designer_role_data.sungage_email"
                    ),
                    "permissions_role": context.get(
                        "assigned_designer_role_data.permissions_role"
                    ),
                    "permissions_role_title": context.get(
                        "assigned_designer_role_data.permissions_role_title"
                    ),
                    "brighte_agent_id": context.get(
                        "assigned_designer_role_data.brighte_agent_id"
                    ),
                    "dividend_contact_id": context.get(
                        "assigned_designer_role_data.dividend_contact_id"
                    ),
                    "user_data": context.get("assigned_designer_role_data.user_data"),
                    "phoenix_user_email": context.get(
                        "assigned_designer_role_data.phoenix_user_email"
                    ),
                    "managed_by": context.get("assigned_designer_role_data.managed_by"),
                    "portrait_image_public_url": context.get(
                        "assigned_designer_role_data.portrait_image_public_url"
                    ),
                    "non_admin_editable": context.get(
                        "assigned_designer_role_data.non_admin_editable"
                    ),
                },
            )
            ProjectRoleAssignment.get_or_create(
                project_id=project_id, role_id=designer_role_id, role_type="designer"
            )
        # Salesperson
        salesperson_role_id = int(context.get("assigned_salesperson_role_id", 0))
        if salesperson_role_id:
            salesperson_role, _ = Role.get_or_create(
                id=salesperson_role_id,
                defaults={
                    "email": context.get("assigned_salesperson_role_email"),
                    "is_admin": context.get("assigned_salesperson_role_data.is_admin"),
                    "user": context.get("assigned_salesperson_role_data.user"),
                    "user_email": context.get(
                        "assigned_salesperson_role_data.user_email"
                    ),
                    "org": context.get("assigned_salesperson_role_data.org"),
                    "is_hidden": context.get(
                        "assigned_salesperson_role_data.is_hidden"
                    ),
                    "url": context.get("assigned_salesperson_role"),
                    "first_name": context.get(
                        "assigned_salesperson_role_data.first_name"
                    ),
                    "family_name": context.get(
                        "assigned_salesperson_role_data.family_name"
                    ),
                    "job_title": context.get(
                        "assigned_salesperson_role_data.job_title"
                    ),
                    "accreditation": context.get(
                        "assigned_salesperson_role_data.accreditation"
                    ),
                    "user_phone": context.get(
                        "assigned_salesperson_role_data.user_phone"
                    ),
                    "display": context.get("assigned_salesperson_role_data.display"),
                    "phone": context.get("assigned_salesperson_role_data.phone"),
                    "allow_email_notifications": context.get(
                        "assigned_salesperson_role_data.allow_email_notifications"
                    ),
                    "portrait_image": context.get(
                        "assigned_salesperson_role_data.portrait_image"
                    ),
                    "google_calendar_id": context.get(
                        "assigned_salesperson_role_data.google_calendar_id"
                    ),
                    "has_logged_in": context.get(
                        "assigned_salesperson_role_data.has_logged_in"
                    ),
                    "schedule_meeting_url": context.get(
                        "assigned_salesperson_role_data.schedule_meeting_url"
                    ),
                    "schedule_meeting_label": context.get(
                        "assigned_salesperson_role_data.schedule_meeting_label"
                    ),
                    "api_key_chat": context.get(
                        "assigned_salesperson_role_data.api_key_chat"
                    ),
                    "user_is_staff": context.get(
                        "assigned_salesperson_role_data.user_is_staff"
                    ),
                    "org_name": context.get("assigned_salesperson_role_data.org_name"),
                    "mosaic_sales_rep_id": context.get(
                        "assigned_salesperson_role_data.mosaic_sales_rep_id"
                    ),
                    "ironridge_email": context.get(
                        "assigned_salesperson_role_data.ironridge_email"
                    ),
                    "ironridge_terms_accepted": context.get(
                        "assigned_salesperson_role_data.ironridge_terms_accepted"
                    ),
                    "integration_json": context.get(
                        "assigned_salesperson_role_data.integration_json"
                    ),
                    "loanpal_channels": context.get(
                        "assigned_salesperson_role_data.loanpal_channels"
                    ),
                    "sungage_email": context.get(
                        "assigned_salesperson_role_data.sungage_email"
                    ),
                    "permissions_role": context.get(
                        "assigned_salesperson_role_data.permissions_role"
                    ),
                    "permissions_role_title": context.get(
                        "assigned_salesperson_role_data.permissions_role_title"
                    ),
                    "brighte_agent_id": context.get(
                        "assigned_salesperson_role_data.brighte_agent_id"
                    ),
                    "dividend_contact_id": context.get(
                        "assigned_salesperson_role_data.dividend_contact_id"
                    ),
                    "user_data": (
                        json.dumps(
                            context.get("assigned_salesperson_role_data.user_data")
                        )
                        if context.get("assigned_salesperson_role_data.user_data")
                        else None
                    ),
                    "phoenix_user_email": context.get(
                        "assigned_salesperson_role_data.phoenix_user_email"
                    ),
                    "managed_by": context.get(
                        "assigned_salesperson_role_data.managed_by"
                    ),
                    "portrait_image_public_url": context.get(
                        "assigned_salesperson_role_data.portrait_image_public_url"
                    ),
                    "non_admin_editable": context.get(
                        "assigned_salesperson_role_data.non_admin_editable"
                    ),
                },
            )
            ProjectRoleAssignment.get_or_create(
                project_id=project_id,
                role_id=salesperson_role_id,
                role_type="salesperson",
            )

        # 4. System
        system_id = 9354996
        system_uuid = uuid.UUID("4D8FDCE5-FD00-49A7-895F-44E74563A1E3")
        system_url = f"https://api.opensolar.com/api/orgs/{org_id}/systems/{system_id}/"
        system, _ = System.get_or_create(
            id=system_id,
            defaults={
                "url": system_url,
                "uuid": system_uuid,
                "project_id": project_id,
                "org": org_url,
                "price_including_tax": 5985.0,
                "price_excluding_tax": 5985.0,
                "net_profit": 107479.77,
                "module_quantity": 4,
                "co2_tons_lifetime": 17.16,
                "output_annual_kwh": 1271,
                "consumption_offset_percentage": 118,
                "system_sold": True,
            },
        )
        # System Modules
        SystemModule.get_or_create(
            system_id=system_id,
            module_activation_id=1094449,
            defaults={
                "code": "SPR-P3-335-BLK",
                "manufacturer_name": "SunPower",
                "quantity": 2,
            },
        )
        SystemModule.get_or_create(
            system_id=system_id,
            module_activation_id=1094448,
            defaults={
                "code": "JKM310M-72B",
                "manufacturer_name": "Jinko Solar Co., Ltd.",
                "quantity": 2,
            },
        )
        # System Inverter
        SystemInverter.get_or_create(
            system_id=system_id,
            inverter_activation_id=1159736,
            defaults={
                "code": "Primo 5.0-1",
                "manufacturer_name": "Fronius",
                "quantity": 1,
            },
        )
        # System Battery
        SystemBattery.get_or_create(
            system_id=system_id,
            battery_activation_id=689751,
            defaults={
                "code": "LG Energy Solution RESU10 HV-Type R",
                "manufacturer_name": "LG Energy Solution",
                "quantity": 1,
            },
        )

        # 5. Pricing Scheme
        pricing_scheme_id = 340674
        pricing_scheme_url = f"https://api.opensolar.com/api/orgs/{org_id}/pricing_schemes/{pricing_scheme_id}/"
        pricing_scheme_data = {
            "price_per_watt_0_1": 3.5,
            "price_per_watt_10_12": 3.0,
            "price_per_watt_50_60": 2.5,
            "price_per_watt_100_plus": 2.2,
            "battery_price_per_kwh_0_5": 150.0,
            "tax_percentage_included": 0.0,
            "auto_apply_only_specified_states": None,
            "auto_apply_only_specified_zips": None,
        }
        PricingScheme.get_or_create(
            id=pricing_scheme_id,
            defaults={
                "url": pricing_scheme_url,
                "org": org_url,
                "is_archived": False,
                "pricing_formula": "Price Per Watt By Size",
                "title": "Price Per Watt By Size (default)",
                "priority": 1,
                "configuration_json": json.dumps(pricing_scheme_data),
                "created_date": datetime.fromisoformat(
                    "2025-06-09T06:56:11.849432+00:00"
                ),
                "modified_date": datetime.fromisoformat(
                    "2025-06-09T06:56:11.849455+00:00"
                ),
                "auto_apply_enabled": True,
                "auto_apply_only_specified_states": None,
                "auto_apply_only_specified_zips": None,
                "auto_apply_component_codes": None,
                "auto_apply_min_system_size": None,
                "auto_apply_max_system_size": None,
                "auto_apply_min_battery_kwh": None,
                "auto_apply_max_battery_kwh": None,
                "auto_apply_battery_capacity_type": 1,
                "auto_apply_sector": 0,
            },
        )

        # 6. Configuration
        configuration_id = 147028
        configuration_url = f"https://api.opensolar.com/api/orgs/{org_id}/project_configurations/{configuration_id}/"
        Configuration.get_or_create(
            id=configuration_id,
            defaults={
                "url": configuration_url,
                "org": org_url,
                "title": "Default Project Preset",
                "priority": False,
                "created_date": datetime.fromisoformat(
                    "2025-06-09T06:56:12.128755+00:00"
                ),
                "modified_date": datetime.fromisoformat(
                    "2025-06-09T06:56:12.128777+00:00"
                ),
                "performance_calculator": 2,
                "weather_dataset": 0,
                "horizon_shading_provider": 0,
                "inverter_modelling_automation": 0,
                "setbacks_default": 0.3,
                "setbacks_gutter": 0.3,
                "setbacks_ridge": 0.3,
                "setbacks_valley": 0.3,
                "setbacks_hip": 0.3,
                "setbacks_rake": 0.3,
                "setbacks_shared": 0.3,
                "setbacks_flat_gutter": 0.3,
                "setbacks_skylight": 0.3,
                "setbacks_dormer": 0.3,
                "setbacks_objects": 0.3,
                "setbacks_arrays": 0.0,
                "module_spacing_horizontal": 0.0,
                "module_spacing_vertical": 0.0,
                "tilt_rack_default_tilt": 13.0,
                "tilt_rack_default_orientation": "landscape",
                "apply_tilt_racks_below_slope": 10.0,
                "years_to_simulate": 0,
                "performance_adjustment": 100.0,
                "discount_rate": 6.75,
                "utility_inflation_annual": 4.2,
                "utility_inflation_annual_upper_bound": None,
                "utility_inflation_annual_lower_bound": None,
                "feed_in_tariff_inflation_annual": 0.0,
                "lower_bound_scaling_factors": None,
                "upper_bound_scaling_factors": None,
                "scaling_factors_label": None,
                "proposed_usage_adjustment": 0.0,
                "sam_string_soiling": 5.0,
                "sam_string_dc_wiring": 2.0,
                "sam_string_mismatch": 2.0,
                "sam_micro_soiling": 5.0,
                "sam_micro_dc_wiring": 0.1,
                "sam_micro_mismatch": 0.0,
                "sam_optimizer_soiling": 5.0,
                "sam_optimizer_dc_wiring": 1.0,
                "sam_optimizer_mismatch": 0.0,
                "sam_ac_wiring": 1.0,
                "sam_nameplate": 0.0,
                "sam_diodes_and_connections": 0.5,
                "sam_dc_system_availability": 0.0,
                "sam_ac_system_availability": 0.0,
                "show_tax_effects_of_solar": False,
                "auto_apply_max_simulate_years": False,
            },
        )

        # 7. Customer Action
        CustomerAction.get_or_create(
            system_uuid=system_uuid,
            org_id=org_id,
            project_id=project_id,
            system_id=system_id,
            payment_option_id=907396,
            defaults={
                "selected_system_title": "4 Solar Panels & Battery Storage",
                "selected_system_summary": "2 x SunPower 335 Watt Panels (SPR-P3-335-BLK)\n2 x Jinko Solar Co., Ltd. 310 Watt Panels (JKM310M-72B)\n1 x Primo 5.0-1 (Fronius)\n1 x LG Energy Solution RESU10 HV-Type R (LG Energy Solution)\nTilt Racks (4 panels)",
                "loan_amount": 0,
                "total_price_payable": 5985,
                "paid_to_date": 0.0,
                "paid_to_date_tax_included": 0.0,
                "paid_to_date_surcharge_amount": 0,
                "balance_outstanding": 5985.0,
                "payment_amount": 0,
                "payment_amount_tax_included": 0.0,
                "collect_signature": False,
                "payment_option_type": "cash",
                "payment_method": "none",
                "payment_title": None,
                "payment_stripe_key": None,
                "surcharge_amount": 0,
                "payment_content": None,
                "payment_terminology": None,
                "quote_acceptance_heading": "Quote Acceptance",
                "quote_acceptance_content": "I have read & accept the terms and conditions.",
                "additional_details": None,
                "status_code": "complete",
                "status_title": None,
                "status_title_secondary": None,
                "status_description": None,
                "is_pro_facing": True,
                "is_customer_facing": True,
                "has_api_side_effect": False,
                "requires_docusign_signature": False,
                "docusign_contract_complete": False,
                "total_price_payable_tax_included": 0,
                "action_title": "Accepted",
                "review_action_title": "Review Proposal",
                "enable_cta_payment_on_proposal": False,
            },
        )

        # 8. Transaction
        Transaction.get_or_create(
            id=654822,
            defaults={
                "url": "https://api.opensolar.com/api/orgs/178878/transactions/654822/",
                "org": org_url,
                "org_id": org_id,
                "org_name": org_name,
                "project": project_url,
                "project_name": "my test address line 1.0 my test address line 2.0",
            },
        )


if __name__ == "__main__":
    # Example: context = ... (parse from JSON or other source)
    # parse_and_ingest(context)
    pass
