-- PostgreSQL schema for Solar Energy Project JSON

-- ORGANIZATION
CREATE TABLE organization (
    id BIGINT PRIMARY KEY,
    name TEXT,
    url TEXT
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
    notes TEXT,
    is_residential BOOLEAN,
    is_pricing_locked BOOLEAN,
    installation_date DATE,
    language TEXT,
    lat NUMERIC,
    lon NUMERIC,
    locality TEXT,
    state TEXT,
    zip TEXT,
    country_iso2 TEXT,
    country_name TEXT,
    org_id BIGINT REFERENCES organization(id),
    created_date TIMESTAMP,
    modified_date TIMESTAMP,
    contract_date DATE,
    contract TEXT,
    design TEXT,
    number_of_phases INT,
    number_of_wires INT,
    number_of_storeys INT,
    payment_option_sold TEXT,
    payment_option_sold_title TEXT,
    priority INT,
    project_installed INT,
    project_sold INT,
    roof_type_name TEXT,
    roof_type TEXT,
    simulate_first_year_only BOOLEAN,
    site_notes TEXT,
    sold_date TIMESTAMP,
    stage INT,
    usage_annual_or_guess NUMERIC,
    usage NUMERIC,
    allow_email_notifications BOOLEAN,
    is_lite BOOLEAN,
    custom_data JSONB
);

-- SYSTEMS
CREATE TABLE system (
    id BIGINT PRIMARY KEY,
    url TEXT,
    name TEXT,
    uuid UUID,
    "order" INT,
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
    project_id BIGINT REFERENCES project(id),
    org_id BIGINT REFERENCES organization(id),
    pricing_scheme TEXT,
    battery_scheme TEXT,
    output_annual_kwh NUMERIC,
    consumption_offset_percentage NUMERIC,
    integration_json JSONB,
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

-- EVENTS
CREATE TABLE event (
    id BIGINT PRIMARY KEY,
    org TEXT,
    project_id BIGINT REFERENCES project(id),
    duration INT,
    event_type_id INT,
    action_id BIGINT,
    start TIMESTAMP,
    "end" TIMESTAMP,
    created_date TIMESTAMP,
    modified_date TIMESTAMP,
    who_display TEXT,
    who_email TEXT,
    who_portrait_image_public_url TEXT,
    completion_date TIMESTAMP,
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

-- ACTIONS
CREATE TABLE action (
    id BIGINT PRIMARY KEY,
    url TEXT,
    org TEXT,
    stage INT,
    title TEXT,
    "order" INT,
    created_date TIMESTAMP,
    modified_date TIMESTAMP,
    share_with_orgs TEXT[],
    org_shared_time TEXT[],
    project_id BIGINT REFERENCES project(id)
);

-- ACTION WORKFLOWS
CREATE TABLE action_workflow (
    id SERIAL PRIMARY KEY,
    action_id BIGINT REFERENCES action(id),
    workflow TEXT,
    stage TEXT
);

-- ACTION EVENTS
CREATE TABLE action_event (
    id SERIAL PRIMARY KEY,
    action_id BIGINT REFERENCES action(id),
    event_id BIGINT REFERENCES event(id)
);

-- PROJECT CONTACTS (many-to-many)
CREATE TABLE project_contact (
    project_id BIGINT REFERENCES project(id),
    contact_id BIGINT REFERENCES contact(id),
    PRIMARY KEY (project_id, contact_id)
);

-- PROJECT FILES
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
    created_date TIMESTAMP,
    modified_date TIMESTAMP,
    temporary BOOLEAN
);

-- FILE TAGS
CREATE TABLE file_tag (
    id BIGINT PRIMARY KEY,
    url TEXT,
    title TEXT,
    type TEXT
);

-- FILE <-> TAGS (many-to-many)
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
    transaction_datetime TIMESTAMP,
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
    created_date TIMESTAMP,
    modified_date TIMESTAMP,
    credit_expiration_date TIMESTAMP
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
    data JSONB,
    org_id BIGINT,
    ui_message_key TEXT,
    eia_id TEXT
);

-- PREMIUM IMAGERY ACTIVATIONS
CREATE TABLE premium_imagery_activation (
    id BIGINT PRIMARY KEY,
    org BIGINT REFERENCES organization(id),
    product_id BIGINT,
    lon NUMERIC,
    lat NUMERIC,
    is_cancelled BOOLEAN,
    project_id BIGINT REFERENCES project(id),
    period TEXT,
    dates JSONB,
    bounds JSONB
);

-- SYSTEM PRICING SCHEME
CREATE TABLE pricing_scheme (
    id BIGINT PRIMARY KEY,
    url TEXT,
    org TEXT,
    is_archived BOOLEAN,
    pricing_formula TEXT,
    title TEXT,
    priority INT,
    configuration_json JSONB,
    created_date TIMESTAMP,
    modified_date TIMESTAMP,
    auto_apply_enabled BOOLEAN,
    auto_apply_only_specified_states TEXT[],
    auto_apply_only_specified_zips TEXT[],
    auto_apply_component_codes TEXT[],
    auto_apply_min_system_size NUMERIC,
    auto_apply_max_system_size NUMERIC,
    auto_apply_min_battery_kwh NUMERIC,
    auto_apply_max_battery_kwh NUMERIC,
    auto_apply_battery_capacity_type INT,
    auto_apply_sector INT,
    share_with_orgs TEXT[],
    org_shared_time TEXT[]
);

-- SYSTEM <-> PRICING SCHEME (many-to-one)
ALTER TABLE system ADD COLUMN pricing_scheme_id BIGINT REFERENCES pricing_scheme(id);

-- PROJECT <-> SYSTEMS (one-to-many)
ALTER TABLE system ADD COLUMN project_id BIGINT REFERENCES project(id);

-- PROJECT <-> EVENTS (one-to-many)
ALTER TABLE event ADD COLUMN project_id BIGINT REFERENCES project(id);

-- PROJECT <-> ACTIONS (one-to-many)
ALTER TABLE action ADD COLUMN project_id BIGINT REFERENCES project(id);

-- PROJECT <-> TRANSACTIONS (one-to-many)
ALTER TABLE transaction ADD COLUMN project_id BIGINT REFERENCES project(id);

-- PROJECT <-> PRIVATE FILES (one-to-many)
ALTER TABLE private_file ADD COLUMN project_id BIGINT REFERENCES project(id);

-- PROJECT <-> PREMIUM IMAGERY ACTIVATIONS (one-to-many)
ALTER TABLE premium_imagery_activation ADD COLUMN project_id BIGINT REFERENCES project(id);

-- SYSTEM <-> MODULES/INVERTERS/BATTERIES (one-to-many)
ALTER TABLE system_module ADD COLUMN system_id BIGINT REFERENCES system(id);
ALTER TABLE system_inverter ADD COLUMN system_id BIGINT REFERENCES system(id);
ALTER TABLE system_battery ADD COLUMN system_id BIGINT REFERENCES system(id);

-- Add more tables as needed for nested/complex objects (e.g., costing, configuration, available_customer_actions, etc.)
-- For JSONB fields, store the full nested object for flexibility.
