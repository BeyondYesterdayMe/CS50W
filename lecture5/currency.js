document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('form').onsubmit = function () {
        fetch('https://open.er-api.com/v6/latest/USD')
        .then(response => response.json())
        .then(data => {
                console.log(data);
                const currency = document.querySelector('#currency').value.toUpperCase(); 
                const rates = data.rates[currency];
                console.log(currency);
                console.log(rates);

                if (rates === undefined){
                    document.querySelector('#result').innerHTML = `Invalid Currency`;    
                }else {
                    document.querySelector('#result').innerHTML = `1 USD is equal to ${rates.toFixed(3)} ${currency}`
                }  
        })
        .catch(error => {
            console.log('Error:', error);
        });

        return false;
    };               
});