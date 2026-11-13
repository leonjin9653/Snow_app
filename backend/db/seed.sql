
INSERT INTO resorts (slug, name, latitude, longitude, website_url, report_url, adapter_name, pricing_url)
VALUES (
    'moonstone',
    'Mount St. Louis Moonstone',
    44.6249198,   
    -79.6725548,   
    'https://www.mountstlouis.com/',
    'https://www.mountstlouis.com/status/',
    'moonstone',
    'https://shop.mountstlouis.com/lift-tickets/'
)
ON CONFLICT (slug) DO NOTHING;