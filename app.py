from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

history = []

API_URL = "https://open.er-api.com/v6/latest/"


CURRENCIES = {
    "AED": "United Arab Emirates - UAE Dirham",
    "AFN": "Afghanistan - Afghani",
    "ALL": "Albania - Lek",
    "AMD": "Armenia - Armenian Dram",
    "ANG": "Netherlands Antilles - Netherlands Antillean Guilder",
    "AOA": "Angola - Kwanza",
    "ARS": "Argentina - Argentine Peso",
    "AUD": "Australia - Australian Dollar",
    "AWG": "Aruba - Aruban Florin",
    "AZN": "Azerbaijan - Azerbaijani Manat",

    "BAM": "Bosnia and Herzegovina - Convertible Mark",
    "BBD": "Barbados - Barbados Dollar",
    "BDT": "Bangladesh - Taka",
    "BGN": "Bulgaria - Bulgarian Lev",
    "BHD": "Bahrain - Bahraini Dinar",
    "BIF": "Burundi - Burundi Franc",
    "BMD": "Bermuda - Bermudian Dollar",
    "BND": "Brunei - Brunei Dollar",
    "BOB": "Bolivia - Boliviano",
    "BRL": "Brazil - Brazilian Real",
    "BSD": "Bahamas - Bahamian Dollar",
    "BTN": "Bhutan - Ngultrum",
    "BWP": "Botswana - Pula",
    "BYN": "Belarus - Belarusian Ruble",
    "BZD": "Belize - Belize Dollar",

    "CAD": "Canada - Canadian Dollar",
    "CDF": "Democratic Republic of the Congo - Congolese Franc",
    "CHF": "Switzerland - Swiss Franc",
    "CLP": "Chile - Chilean Peso",
    "CNY": "China - Chinese Yuan",
    "COP": "Colombia - Colombian Peso",
    "CRC": "Costa Rica - Costa Rican Colón",
    "CUP": "Cuba - Cuban Peso",
    "CVE": "Cape Verde - Cape Verdean Escudo",
    "CZK": "Czech Republic - Czech Koruna",

    "DJF": "Djibouti - Djiboutian Franc",
    "DKK": "Denmark - Danish Krone",
    "DOP": "Dominican Republic - Dominican Peso",
    "DZD": "Algeria - Algerian Dinar",
    "EGP": "Egypt - Egyptian Pound",
    "ERN": "Eritrea - Eritrean Nakfa",
    "ETB": "Ethiopia - Ethiopian Birr",
    "EUR": "Eurozone - Euro",

    "FJD": "Fiji - Fijian Dollar",
    "FKP": "Falkland Islands - Falkland Islands Pound",

    "GEL": "Georgia - Georgian Lari",
    "GHS": "Ghana - Ghanaian Cedi",
    "GIP": "Gibraltar - Gibraltar Pound",
    "GMD": "Gambia - Gambian Dalasi",
    "GNF": "Guinea - Guinean Franc",
    "GTQ": "Guatemala - Guatemalan Quetzal",
    "GYD": "Guyana - Guyanese Dollar",

    "HKD": "Hong Kong - Hong Kong Dollar",
    "HNL": "Honduras - Honduran Lempira",
    "HRK": "Croatia - Croatian Kuna",
    "HTG": "Haiti - Haitian Gourde",
    "HUF": "Hungary - Hungarian Forint",

    "IDR": "Indonesia - Indonesian Rupiah",
    "ILS": "Israel - Israeli New Shekel",
    "INR": "India - Indian Rupee",
    "IQD": "Iraq - Iraqi Dinar",
    "IRR": "Iran - Iranian Rial",
    "ISK": "Iceland - Icelandic Króna",

    "JMD": "Jamaica - Jamaican Dollar",
    "JOD": "Jordan - Jordanian Dinar",
    "JPY": "Japan - Japanese Yen",

    "KES": "Kenya - Kenyan Shilling",
    "KGS": "Kyrgyzstan - Kyrgyzstani Som",
    "KHR": "Cambodia - Cambodian Riel",
    "KMF": "Comoros - Comorian Franc",
    "KPW": "North Korea - North Korean Won",
    "KRW": "South Korea - South Korean Won",
    "KWD": "Kuwait - Kuwaiti Dinar",
    "KYD": "Cayman Islands - Cayman Islands Dollar",
    "KZT": "Kazakhstan - Kazakhstani Tenge",
    "LAK": "Laos - Lao Kip",
    "LBP": "Lebanon - Lebanese Pound",
    "LKR": "Sri Lanka - Sri Lankan Rupee",
    "LRD": "Liberia - Liberian Dollar",
    "LSL": "Lesotho - Lesotho Loti",
    "LYD": "Libya - Libyan Dinar",

    "MAD": "Morocco - Moroccan Dirham",
    "MDL": "Moldova - Moldovan Leu",
    "MGA": "Madagascar - Malagasy Ariary",
    "MKD": "North Macedonia - Macedonian Denar",
    "MMK": "Myanmar - Myanmar Kyat",
    "MNT": "Mongolia - Mongolian Tögrög",
    "MOP": "Macau - Macanese Pataca",
    "MRU": "Mauritania - Ouguiya",
    "MUR": "Mauritius - Mauritian Rupee",
    "MVR": "Maldives - Maldivian Rufiyaa",
    "MWK": "Malawi - Malawian Kwacha",
    "MXN": "Mexico - Mexican Peso",
    "MYR": "Malaysia - Malaysian Ringgit",
    "MZN": "Mozambique - Mozambican Metical",

    "NAD": "Namibia - Namibian Dollar",
    "NGN": "Nigeria - Nigerian Naira",
    "NIO": "Nicaragua - Nicaraguan Córdoba",
    "NOK": "Norway - Norwegian Krone",
    "NPR": "Nepal - Nepalese Rupee",
    "NZD": "New Zealand - New Zealand Dollar",

    "OMR": "Oman - Omani Rial",

    "PAB": "Panama - Panamanian Balboa",
    "PEN": "Peru - Peruvian Sol",
    "PGK": "Papua New Guinea - Papua New Guinean Kina",
    "PHP": "Philippines - Philippine Peso",
    "PKR": "Pakistan - Pakistani Rupee",
    "PLN": "Poland - Polish Złoty",
    "PYG": "Paraguay - Paraguayan Guaraní",
    "LAK": "Laos - Lao Kip",
    "LBP": "Lebanon - Lebanese Pound",
    "LKR": "Sri Lanka - Sri Lankan Rupee",
    "LRD": "Liberia - Liberian Dollar",
    "LSL": "Lesotho - Lesotho Loti",
    "LYD": "Libya - Libyan Dinar",

    "MAD": "Morocco - Moroccan Dirham",
    "MDL": "Moldova - Moldovan Leu",
    "MGA": "Madagascar - Malagasy Ariary",
    "MKD": "North Macedonia - Macedonian Denar",
    "MMK": "Myanmar - Myanmar Kyat",
    "MNT": "Mongolia - Mongolian Tögrög",
    "MOP": "Macau - Macanese Pataca",
    "MRU": "Mauritania - Ouguiya",
    "MUR": "Mauritius - Mauritian Rupee",
    "MVR": "Maldives - Maldivian Rufiyaa",
    "MWK": "Malawi - Malawian Kwacha",
    "MXN": "Mexico - Mexican Peso",
    "MYR": "Malaysia - Malaysian Ringgit",
    "MZN": "Mozambique - Mozambican Metical",

    "NAD": "Namibia - Namibian Dollar",
    "NGN": "Nigeria - Nigerian Naira",
    "NIO": "Nicaragua - Nicaraguan Córdoba",
    "NOK": "Norway - Norwegian Krone",
    "NPR": "Nepal - Nepalese Rupee",
    "NZD": "New Zealand - New Zealand Dollar",

    "OMR": "Oman - Omani Rial",

    "PAB": "Panama - Panamanian Balboa",
    "PEN": "Peru - Peruvian Sol",
    "PGK": "Papua New Guinea - Papua New Guinean Kina",
    "PHP": "Philippines - Philippine Peso",
    "PKR": "Pakistan - Pakistani Rupee",
    "PLN": "Poland - Polish Złoty",
    "PYG": "Paraguay - Paraguayan Guaraní",
    "QAR": "Qatar - Qatari Riyal",

    "RON": "Romania - Romanian Leu",
    "RSD": "Serbia - Serbian Dinar",
    "RUB": "Russia - Russian Ruble",
    "RWF": "Rwanda - Rwandan Franc",

    "SAR": "Saudi Arabia - Saudi Riyal",
    "SBD": "Solomon Islands - Solomon Islands Dollar",
    "SCR": "Seychelles - Seychellois Rupee",
    "SDG": "Sudan - Sudanese Pound",
    "SEK": "Sweden - Swedish Krona",
    "SGD": "Singapore - Singapore Dollar",
    "SLE": "Sierra Leone - Leone",
    "SOS": "Somalia - Somali Shilling",
    "SRD": "Suriname - Surinamese Dollar",
    "SSP": "South Sudan - South Sudanese Pound",
    "STN": "São Tomé and Príncipe - Dobra",
    "SYP": "Syria - Syrian Pound",
    "SZL": "Eswatini - Lilangeni",

    "THB": "Thailand - Thai Baht",
    "TJS": "Tajikistan - Tajikistani Somoni",
    "TMT": "Turkmenistan - Turkmenistan Manat",
    "TND": "Tunisia - Tunisian Dinar",
    "TOP": "Tonga - Tongan Paʻanga",
    "TRY": "Türkiye - Turkish Lira",
    "TTD": "Trinidad and Tobago - Trinidad and Tobago Dollar",
    "TWD": "Taiwan - New Taiwan Dollar",
    "TZS": "Tanzania - Tanzanian Shilling",
    
    "UAH": "Ukraine - Ukrainian Hryvnia",
    "UGX": "Uganda - Ugandan Shilling",
    "USD": "United States - US Dollar",
    "UYU": "Uruguay - Uruguayan Peso",
    "UZS": "Uzbekistan - Uzbekistani Som",

    "VES": "Venezuela - Venezuelan Bolívar",
    "VND": "Vietnam - Vietnamese Đồng",
    "VUV": "Vanuatu - Vanuatu Vatu",

    "WST": "Samoa - Samoan Tala",

    "XAF": "Central African CFA Zone - CFA Franc BEAC",
    "XCD": "Eastern Caribbean - East Caribbean Dollar",
    "XDR": "International Monetary Fund - Special Drawing Rights",
    "XOF": "West African CFA Zone - CFA Franc BCEAO",
    "XPF": "French Pacific Territories - CFP Franc",

    "YER": "Yemen - Yemeni Rial",

    "ZAR": "South Africa - South African Rand",
    "ZMW": "Zambia - Zambian Kwacha",
    "ZWG": "Zimbabwe - Zimbabwe Gold"
}




class CurrencyConverter:
    def fetch_rates(self, base):
        try:
            response = requests.get(API_URL + base, timeout=10)

            if response.status_code == 200:
                data = response.json()

                if data.get("result") == "success":
                    return data.get("rates")

            return None

        except requests.exceptions.RequestException:
            return None

    def convert(self, amount, base, target):
        rates = self.fetch_rates(base)

        if not rates:
            return None

        if target not in rates:
            return None

        rate = rates[target]
        converted = amount * rate

        return {
            "amount": amount,
            "base": base,
            "target": target,
            "rate": rate,
            "result": converted
        }


converter = CurrencyConverter()


@app.route("/", methods=["GET", "POST"])
def index():

    data = None

    if request.method == "POST":

        try:
            amount = float(request.form["amount"])
            base = request.form["base"]
            target = request.form["target"]

            data = converter.convert(
                amount,
                base,
                target
            )

        except Exception:
            data = None

    return render_template(
        "index.html",
        currencies=CURRENCIES,
        data=data
    )

    conversion = {
    "amount": amount,
    "base": base,
    "target": target,
    "result": result,
    "rate": rate
    }


@app.route("/save_history", methods=["POST"])
def save_history():

    data = request.get_json()

    history.append(data["result"])

    return jsonify({"message": "History saved successfully!"})


@app.route("/history")
def show_history():

    return render_template(
        "history.html",
        history=history
    )

@app.route("/delete_history", methods=["POST"])
def delete_history():

    history.clear()

    return jsonify({"message": "History deleted successfully!"})


if __name__ == "__main__":
    app.run(debug=True)
