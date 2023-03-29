import os
import sys
import ast

# The default website to use if the country link is not found
DEFAULT_WEBSITE = 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations.html'
COUNTRY_LINKS = {
    'l10n_ar': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/argentina.html',
    'l10n_au': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/australia.html',
    'l10n_be': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/belgium.html',
    'l10n_cl': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/chile.html',
    'l10n_co': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/colombia.html',
    'l10n_ec': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/ecuador.html',
    'l10n_eg': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/egypt.html',
    'l10n_fr': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/france.html',
    'l10n_de': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/germany.html',
    'l10n_in': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/india.html',
    'l10n_id': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/indonesia.html',
    'l10n_it': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/italy.html',
    'l10n_ke': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/kenya.html',
    'l10n_lu': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/luxembourg.html',
    'l10n_mx': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/mexico.html',
    'l10n_nl': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/netherlands.html',
    'l10n_pe': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/peru.html',
    'l10n_es': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/spain.html',
    'l10n_ch': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/switzerland.html',
    'l10n_uk': 'https://www.odoo.com/documentation/master/applications/finance/fiscal_localizations/united_kingdom.html'
}

def update_manifest(manifest_path, country_links):
    """
    Update the website in the manifest file at the given path.

    If the website key is present and matches the corresponding country link, don't do anything.
    Otherwise, replace the website with the corresponding country link.
    If the website key is not present, add it with the corresponding country link.
    """
    with open(manifest_path, 'r') as f:
        lines = f.readlines()

    try:
        manifest = ast.literal_eval(''.join(lines))
    except:
        print(f'Error parsing {manifest_path}. Skipping...')
        return

    # Get the country code from the manifest path
    country_code = os.path.basename(os.path.dirname(manifest_path))

    if country_code not in country_links:
        # Use the default website
        country_links[country_code] = DEFAULT_WEBSITE

    # Check if 'website' key is present and replace it
    for i, line in enumerate(lines):
        if 'website' in line:
            lines[i] = f"    'website': '{country_links[country_code]}',\n"
            break
    else:
        # Find the line number of the 'name' key
        name_line = next(i for i, line in enumerate(lines) if 'name' in line)

        # Add the website line after the 'name' line
        lines.insert(name_line + 1, f"    'website': '{country_links[country_code]}',\n")

    # Write the updated manifest file
    with open(manifest_path, 'w') as f:
        f.writelines(lines)


if __name__ == '__main__':
    # Get the directory path from the command line argument
    directory = sys.argv[1]

    # Iterate over all subfolders that start with "l10n_" followed by 2 letters
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            if d.startswith('l10n_') and len(d) == 7:
                print(f'Updating {d}...')
                manifest_path = os.path.join(root, d, '__manifest__.py')
                if os.path.isfile(manifest_path):
                    # Update the manifest file
                    update_manifest(manifest_path, COUNTRY_LINKS)