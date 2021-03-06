from util import remove_special
from util import format_ja_codes
from util import format_class_codes
from util import format_naics_code
from util import format_fair_codes
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select


def select_posted_date(driver, date):
    xpath = "//select[@id='dnf_class_values_procurement_notice__custom_posted_date_']"
    date_options = Select(driver.find_element_by_xpath(xpath))
    date_options.select_by_value(str(date))


def select_performance_state(driver, states):
    xpath = "//select[@id='dnf_class_values_procurement_notice__zipstate___']"
    state_options = Select(driver.find_element_by_xpath(xpath))

    if isinstance(states, str):
        state_options.select_by_value(states.upper())
    else:
        for state in states:
            state_options.select_by_value(str(state).upper())


def select_document_scope(driver, document):
    scope = document.lower()

    if scope == 'active':
        xpath = "//input[@alt='Documents To Search Active Documents']"
        driver.find_element_by_xpath(xpath).click()

    elif scope == 'archived':
        xpath = "//input[@alt='Documents To Search Archived Documents']"
        driver.find_element_by_xpath(xpath).click()

    elif scope == 'both':
        xpath = "//input[@alt='Documents To Search Both']"
        driver.find_element_by_xpath(xpath).click()


def enter_zipcodes(driver, zipcodes):
    xpath = "//input[@id='dnf_class_values_procurement_notice__zipcode_']"
    zip_options = driver.find_element_by_xpath(xpath)

    if isinstance(zipcodes, (str, int)):
        zipcode_list = str(zipcodes)
    else:
        zipcode_list = [f'{zipcode},' for zipcode in zipcodes]
    for zipcode in zipcode_list:
        zip_options.send_keys(zipcode)


def get_codes(driver, code_type):
    """Creates a dictionary to be used by select_codes to select
    codes using their human readable id as an argument (e.g 111110
    from the below label)

    <label>111 -- Crop Production: 111110 -- Soybean Farming</label>

    input values and names for code elements are used to ensure
    correct corresponding code is selected.

     """
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    if code_type.lower() == 'set_aside':
        label_edit = soup.find(
            'div',
            {'id': 'dnf_class_values_procurement_notice__set_aside____widget'}
        ).table
        editor = remove_special

    elif code_type.lower() == 'procurement_type':
        label_edit = soup.find(
            'div',
            {'id': 'dnf_class_values_procurement_notice__procurement_type____widget'}
        ).table
        editor = remove_special

    elif code_type.lower() == 'naics_codes':
        label_edit = soup.find(
            'div',
            {'id': 'scrollable_checkbox_dnf_class_values_procurement_notice__naics_code___'}
        )
        editor = format_naics_code

    elif code_type.lower() == 'class_codes':
        label_edit = soup.find(
            'div',
            {'id': 'scrollable_checkbox_dnf_class_values_procurement_notice__classification_code___'}
        )
        editor = format_class_codes

    elif code_type.lower() == 'ja':
        label_edit = soup.find(
            'div',
            {'id': 'dnf_class_values_procurement_notice__ja_statutory____widget'}
        ).table
        editor = format_ja_codes

    elif code_type.lower() == 'fair_opportunity':
        label_edit = soup.find(
            'div',
            {'id': 'dnf_class_values_procurement_notice__fair_opp_ja____widget'}
        ).table
        editor = format_fair_codes

    page_labels = label_edit.find_all('label')
    labels = [editor(label.text) for label in page_labels]
    inputs = [( element['name'], element['value']) for element in label_edit.find_all('input')]

    return dict(zip(labels, inputs))


def select_codes(driver, codes, code_type=None):
    page_codes = get_codes(driver, code_type)

    if isinstance(codes, str):
        xpath = f"//input[@name='{page_codes[codes][0]}'][@value='{page_codes[codes][1]}']"
        driver.find_element_by_xpath(xpath).click()
    else:
        for code in codes:
            if code in page_codes:
                xpath = f"//input[@name='{page_codes[code][0]}'][@value='{page_codes[code][1]}']"
                driver.find_element_by_xpath(xpath).click()


def change_hidden_date_value(driver, dates, xpaths):
    for count, date in enumerate(dates):
        datefield = driver.find_element_by_xpath(xpaths[count])
        driver.execute_script(
            "arguments[0].setAttribute(arguments[1], arguments[2])",
            datefield, "value", str(date)
        )


def enter_date_ranges(driver, start_date, end_date, date_type):
    dates = (start_date, end_date)

    if date_type.lower() == 'post_range':
        xpaths = (
            "//input[@id='dnf_class_values_procurement_notice__posted_date___start__real']",
            "//input[@id='dnf_class_values_procurement_notice__posted_date___end__real']"
        )
        change_hidden_date_value(driver, dates, xpaths)

    elif date_type.lower() == 'response_date':
        xpaths = (
            "//input[@id='dnf_class_values_procurement_notice__response_deadline___start__real']",
            "//input[@id='dnf_class_values_procurement_notice__response_deadline___end__real']"
        )
        change_hidden_date_value(driver, dates, xpaths)

    elif date_type.lower() == 'last_modified':
        xpaths = (
            "//input[@id='dnf_class_values_procurement_notice__modified___start__real']",
            "//input[@id='dnf_class_values_procurement_notice__modified___end__real']"
        )
        change_hidden_date_value(driver, dates, xpaths)

    elif date_type.lower() == 'award_date':
        xpaths = (
        "//input[@id='dnf_class_values_procurement_notice__contract_award_date___start__real']",
        "//input[@id='dnf_class_values_procurement_notice__contract_award_date___end__real']"
    )
        change_hidden_date_value(driver, dates, xpaths)


def submit_form(driver):
    xpath = "//input[@name='dnf_opt_submit']"
    driver.find_element_by_xpath(xpath).click()


def toggle_recovery_reinvestment_act(driver):
    xpath = "//input[@alt='Recovery and Reinvestment Act Action Yes']"
    driver.find_element_by_xpath(xpath).click()
