-- PostgreSQL schema for Solar Energy Project Management
-- This schema is normalized and covers all major entities and relationships from the provided JSON

-- ORGANIZATION
CREATE TABLE organization (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    country_iso2 CHAR(2),
    country_name TEXT,
    address TEXT
);

-- USER ROLES (for assigned_role_data, assigned_designer_role_data, assigned_salesperson_role_data)
CREATE TABLE user_role (
    id BIGINT PRIMARY KEY,
    email TEXT,
    is_admin BOOLEAN,
    user_url TEXT,
    user_email TEXT,
    org_id BIGINT REFERENCES organization(id),
    is_hidden BOOLEAN,
    url TEXT,
    first_name TEXT,
    family_name TEXT,
    job_title TEXT,
    accreditation TEXT,
    user_phone TEXT,
    display TEXT,
    phone TEXT,
    allow_email_notifications BOOLEAN,
    portrait_image TEXT,
    google_calendar_id TEXT,
    has_logged_in BOOLEAN,
    schedule_meeting_url TEXT,
    schedule_meeting_label TEXT,
    api_key_chat TEXT,
    user_is_staff BOOLEAN,
    org_name TEXT,
    mosaic_sales_rep_id TEXT,
    ironridge_email TEXT,
    ironridge_terms_accepted BOOLEAN,
    integration_json JSONB,
    loanpal_channels TEXT,
    sungage_email TEXT,
    permissions_role INT,
    permissions_role_title TEXT,
    brighte_agent_id TEXT,
    dividend_contact_id TEXT,
    user_data JSONB,
    phoenix_user_email TEXT,
    managed_by TEXT,
    portrait_image_public_url TEXT,
    non_admin_editable BOOLEAN
);

-- CONTACTS
CREATE TABLE contact (
    id BIGINT PRIMARY KEY,
    email TEXT,
    phone TEXT,
    url TEXT,
    first_name TEXT,
    family_name TEXT,
    display TEXT,
    passport_number TEXT,
    licence_number TEXT,
    custom_contact_info_1 TEXT,
    custom_contact_info_2 TEXT,
    middle_name TEXT,
    gender INT,
    date_of_birth DATE,
    user_id BIGINT,
    org_id BIGINT REFERENCES organization(id),
    identifier TEXT,
    type INT,
    custom_data JSONB
);

-- PROJECT
CREATE TABLE project (
    id BIGINT PRIMARY KEY,
    identifier UUID,
    title TEXT,
    address TEXT,
    locality TEXT,
    state TEXT,
    zip TEXT,
    country_iso2 CHAR(2),
    lat NUMERIC,
    lon NUMERIC,
    org_id BIGINT REFERENCES organization(id),
    org_name TEXT,
    created_date TIMESTAMP WITH TIME ZONE,
    modified_date TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    contract_date DATE,
    installation_date DATE,
    sold_date TIMESTAMP WITH TIME ZONE,
    is_residential BOOLEAN,
    is_pricing_locked BOOLEAN,
    priority INT,
    lead_source TEXT,
    number_of_phases INT,
    number_of_wires INT,
    number_of_storeys INT,
    payment_option_sold TEXT,
    payment_option_sold_title TEXT,
    project_installed INT,
    project_sold INT,
    project_stage INT,
    stage_warning TEXT,
    stage INT,
    roof_type_name TEXT,
    roof_type TEXT,
    simulate_first_year_only BOOLEAN,
    usage_annual_or_guess NUMERIC,
    usage NUMERIC,
    timezone_offset NUMERIC,
    valid_until_date DATE,
    years_to_simulate INT,
    wind_region TEXT,
    has_cellular_coverage BOOLEAN,
    allow_email_notifications BOOLEAN,
    brighte_role_connection_status TEXT,
    auto_apply_max_simulate_years BOOLEAN,
    is_lite BOOLEAN,
    custom_data JSONB,
    shared_with JSONB,
    workflow_id BIGINT,
    active_stage_id BIGINT,
    active_stage_title TEXT
);

-- SYSTEMS
CREATE TABLE system (
    id BIGINT PRIMARY KEY,
    uuid UUID,
    project_id BIGINT REFERENCES project(id),
    org_id BIGINT REFERENCES organization(id),
    name TEXT,
    order_num INT,
    system_lifetime INT,
    inverter_range TEXT,
    dc_optimizer_active BOOLEAN,
    dc_optimizer_efficiency NUMERIC,
    show_customer BOOLEAN,
    is_current BOOLEAN,
    auto_string BOOLEAN,
    discount NUMERIC,
    adders_per_system NUMERIC,
    adders_per_panel NUMERIC,
    adders_per_watt NUMERIC,
    kw_stc NUMERIC,
    battery_total_kwh NUMERIC,
    price_including_tax NUMERIC,
    price_excluding_tax NUMERIC,
    net_profit NUMERIC,
    module_quantity INT,
    co2_tons_lifetime NUMERIC,
    pricing_scheme TEXT,
    output_annual_kwh NUMERIC,
    consumption_offset_percentage NUMERIC,
    commission NUMERIC,
    commission_override_manually NUMERIC,
    system_sold BOOLEAN
);

-- SYSTEM MODULES
CREATE TABLE system_module (
    id SERIAL PRIMARY KEY,
    system_id BIGINT REFERENCES system(id),
    module_activation_id BIGINT,
    code TEXT,
    manufacturer_name TEXT,
    quantity INT
);

-- SYSTEM INVERTERS
CREATE TABLE system_inverter (
    id SERIAL PRIMARY KEY,
    system_id BIGINT REFERENCES system(id),
    inverter_activation_id BIGINT,
    code TEXT,
    manufacturer_name TEXT,
    quantity INT
);

-- SYSTEM BATTERIES
CREATE TABLE system_battery (
    id SERIAL PRIMARY KEY,
    system_id BIGINT REFERENCES system(id),
    battery_activation_id BIGINT,
    code TEXT,
    manufacturer_name TEXT,
    quantity INT
);

-- ACTIONS
CREATE TABLE action (
    id BIGINT PRIMARY KEY,
    url TEXT,
    org TEXT,
    stage INT,
    title TEXT,
    order_num INT,
    created_date TIMESTAMP WITH TIME ZONE,
    modified_date TIMESTAMP WITH TIME ZONE,
    share_with_orgs JSONB,
    org_shared_time JSONB
);

-- ACTION WORKFLOWS
CREATE TABLE action_workflow (
    id SERIAL PRIMARY KEY,
    action_id BIGINT REFERENCES action(id),
    workflow TEXT,
    stage TEXT
);

-- EVENTS
CREATE TABLE event (
    id BIGINT PRIMARY KEY,
    org TEXT,
    project_id BIGINT REFERENCES project(id),
    duration INT,
    event_type_id INT,
    action_id BIGINT REFERENCES action(id),
    start TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    created_date TIMESTAMP WITH TIME ZONE,
    modified_date TIMESTAMP WITH TIME ZONE,
    who_display TEXT,
    who_email TEXT,
    completion_date TIMESTAMP WITH TIME ZONE,
    title TEXT,
    project_name TEXT,
    is_planned BOOLEAN,
    task_status INT,
    is_complete BOOLEAN,
    notes TEXT,
    is_archived BOOLEAN,
    categories INT[],
    form_config INT,
    event_icon INT
);

-- EVENT TEAM MEMBERS (if needed)
CREATE TABLE event_team_member (
    event_id BIGINT REFERENCES event(id),
    team_member_url TEXT
);

-- FILE TAGS
CREATE TABLE file_tag (
    id BIGINT PRIMARY KEY,
    url TEXT,
    title TEXT,
    type TEXT
);

-- PRIVATE FILES
CREATE TABLE private_file (
    id BIGINT PRIMARY KEY,
    url TEXT,
    org TEXT,
    document_template TEXT,
    project TEXT,
    user TEXT,
    title TEXT,
    system_uuid UUID,
    input_data JSONB,
    input_data_hash TEXT,
    file_hash TEXT,
    status TEXT,
    status_message TEXT,
    filesize BIGINT,
    file_contents TEXT,
    show_customer BOOLEAN,
    created_date TIMESTAMP WITH TIME ZONE,
    modified_date TIMESTAMP WITH TIME ZONE,
    temporary BOOLEAN
);

-- PRIVATE FILE TAGS (many-to-many)
CREATE TABLE private_file_tag (
    private_file_id BIGINT REFERENCES private_file(id),
    file_tag_id BIGINT REFERENCES file_tag(id),
    PRIMARY KEY (private_file_id, file_tag_id)
);

-- TRANSACTIONS
CREATE TABLE transaction (
    id BIGINT PRIMARY KEY,
    url TEXT,
    org TEXT,
    org_id BIGINT REFERENCES organization(id),
    org_name TEXT,
    project TEXT,
    project_name TEXT,
    system TEXT,
    payment_option TEXT,
    is_complete BOOLEAN,
    transaction_datetime TIMESTAMP WITH TIME ZONE,
    amount NUMERIC,
    tax_included NUMERIC,
    surcharge_amount NUMERIC,
    funds_confirmed BOOLEAN,
    details JSONB,
    contract_details JSONB,
    contract_details_hash TEXT,
    signature_data TEXT,
    is_commission_payable BOOLEAN,
    transaction_type TEXT,
    prior_transaction_type TEXT,
    customer_name TEXT,
    created_date TIMESTAMP WITH TIME ZONE,
    modified_date TIMESTAMP WITH TIME ZONE,
    credit_expiration_date TIMESTAMP WITH TIME ZONE
);

-- UTILITY TARIFFS
CREATE TABLE utility_tariff (
    id BIGINT PRIMARY KEY,
    name TEXT,
    code TEXT,
    utility_id BIGINT,
    utility_name TEXT,
    utility_aliases TEXT[],
    sector INT,
    description TEXT,
    precision TEXT,
    data JSONB
);

-- PRICING SCHEME
CREATE TABLE pricing_scheme (
    id BIGINT PRIMARY KEY,
    url TEXT,
    org TEXT,
    is_archived BOOLEAN,
    pricing_formula TEXT,
    title TEXT,
    priority INT,
    configuration_json JSONB,
    created_date TIMESTAMP WITH TIME ZONE,
    modified_date TIMESTAMP WITH TIME ZONE,
    auto_apply_enabled BOOLEAN
);

-- SYSTEM <-> PRICING SCHEME (if needed)
ALTER TABLE system ADD COLUMN pricing_scheme_id BIGINT REFERENCES pricing_scheme(id);

-- SYSTEM OTHERS (for extensibility)
CREATE TABLE system_other (
    id SERIAL PRIMARY KEY,
    system_id BIGINT REFERENCES system(id),
    other_json JSONB
);

-- SYSTEMS <-> ACTIONS (if needed, for many-to-many)
CREATE TABLE system_action (
    system_id BIGINT REFERENCES system(id),
    action_id BIGINT REFERENCES action(id),
    PRIMARY KEY (system_id, action_id)
);

-- SYSTEMS <-> EVENTS (if needed, for many-to-many)
CREATE TABLE system_event (
    system_id BIGINT REFERENCES system(id),
    event_id BIGINT REFERENCES event(id),
    PRIMARY KEY (system_id, event_id)
);

-- Add more tables as needed for configuration, costing, workflows, testimonials, tags, etc.
-- This schema is extensible and can be further normalized as per business needs.