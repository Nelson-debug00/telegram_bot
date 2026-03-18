document.addEventListener('DOMContentLoaded', () => {
    const amountInput = document.getElementById('amount');
    const resultValue = document.getElementById('result-value');
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const currentRateText = document.getElementById('current-rate-text');
    const currentDateText = document.getElementById('current-date-text');

    const initialRates = window.INITIAL_RATES || {};
    const rates = {
        dolar: Number(initialRates.dolar) || 0,
        euro: Number(initialRates.euro) || 0,
        usdt: Number(initialRates.usdt) || 0,
    };

    const dates = {
        dolar: initialRates.fecha_bcv || '',
        euro: initialRates.fecha_bcv || '',
        usdt: initialRates.fecha_usdt || '',
    };

    let currentCurrency = 'dolar';
    const currencySymbols = {
        dolar: 'USD',
        euro: 'EUR',
        usdt: 'USDT',
    };

    function formatAmount(value) {
        return value.toLocaleString('es-VE', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    }

    function formatInput(value) {
        // Remove everything except digits
        let digits = value.replace(/\D/g, '');
        if (digits === '') return '';
        
        // Convert to number (assume cents if we wanted decimals, but here we just follow "every 3 zeros")
        // The user specifically asked for "every 3 zeros a decimal" (meaning dots for thousands)
        let num = parseInt(digits, 10);
        return num.toLocaleString('es-VE');
    }

    function setCurrentRateText() {
        const symbol = currencySymbols[currentCurrency] || currentCurrency.toUpperCase();
        const rate = rates[currentCurrency] || 0;
        currentRateText.textContent = `Tasa actual: ${symbol} ${formatAmount(rate)}`;
        if (currentDateText) {
            currentDateText.textContent = dates[currentCurrency] || '';
        }
    }

    function calculate() {
        // Remove dots (thousand separators) to parse correctly
        const rawValue = amountInput.value.replace(/\./g, '').replace(/,/g, '.');
        const amount = parseFloat(rawValue) || 0;
        const rate = rates[currentCurrency] || 0;
        const result = amount * rate;
        resultValue.textContent = `Bs.S ${formatAmount(result)}`;
    }

    amountInput.addEventListener('input', (e) => {
        const cursorPosition = e.target.selectionStart;
        const prevLength = e.target.value.length;
        
        const formatted = formatInput(e.target.value);
        e.target.value = formatted;
        
        // Adjust cursor position
        const newLength = formatted.length;
        const selectionPos = cursorPosition + (newLength - prevLength);
        e.target.setSelectionRange(selectionPos, selectionPos);
        
        calculate();
    });

    toggleButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            toggleButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentCurrency = btn.dataset.currency;
            setCurrentRateText();
            calculate();
        });
    });

    // Initial formatting for the default value
    amountInput.value = formatInput(amountInput.value);
    setCurrentRateText();
    calculate();
});
