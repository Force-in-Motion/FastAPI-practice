fetch('http://localhost:8000/exchange-rates')
    .then(response => response.json())
    .then(data => viewCurrencies(data))
    .catch(err => console.log(err))


const createCurrency = (code, rate_to_usd) => {
    const mainContainer = document.getElementById('currency');

    const currencyContainer = document.createElement('div')
    const currencyCode = document.createElement('p')
    const currencyRate = document.createElement('p')

    currencyCode.innerHTML = code
    currencyRate.innerHTML = rate_to_usd

    currencyContainer.append(currencyCode, currencyRate)
    mainContainer.appendChild(currencyContainer)
}

const viewCurrencies = (data) => {
    for (const currency of data.currencies) {
        createCurrency(currency.code, currency.rate_to_usd)
    }
}