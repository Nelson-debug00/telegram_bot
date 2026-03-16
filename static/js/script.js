document - addEventListener('DOMContentLoaded', () => {
    const amountInput = document.getElementById('amount');
    const resultValue = document.getElementById('result-value');
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const currentRateText = document.getElementById('current-rate-text');

    // Tasas de ejemplo (se pueden conectar al backend luego)
    let rates = {
        'dolar': 446.80,
        'euro': 468.20
    };

    let currentCurrency = 'dolar';

    function calculate() {
        const amount = parseFloat(amountInput.value) || 0;
        const rate = rates[currentCurrency];
        const result = amount * rate;

        resultValue.textContent = `Bs.S ${result.toLocaleString('es-VE', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
    }

    amountInput.addEventListener('input', calculate);

    toggleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            // UI Update
            toggleButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Logic Update
            currentCurrency = btn.dataset.currency;
            const symbol = currentCurrency === 'dolar' ? 'USD' : 'EUR';
            currentRateText.textContent = `Tasa actual: ${symbol} ${rates[currentCurrency].toLocaleString('es-VE', { minimumFractionDigits: 2 })}`;

            calculate();
        });
    });

    // Iniciar con cálculo base
    calculate();
});
