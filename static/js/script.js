document.addEventListener('DOMContentLoaded', () => {
    const amountInput = document.getElementById('amount');
    const resultValue = document.getElementById('result-value');
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const currentRateText = document.getElementById('current-rate-text');
    const currentDateText = document.getElementById('current-date-text');

    // New elements for switch
    const switchBtn = document.getElementById('switch-btn');
    const inputLabel = document.getElementById('input-label');
    const outputLabel = document.getElementById('output-label');
    const inputIcon = document.getElementById('input-icon');
    const outputIcon = document.getElementById('output-icon');
    const toggleRateBtn = document.getElementById('toggle-rate-btn');

    const initialRates = window.INITIAL_RATES || {};
    const rates = {
        dolar: Number(initialRates.dolar) || 0,
        euro: Number(initialRates.euro) || 0,
        usdt: Number(initialRates.usdt) || 0,
    };

    const ratesPrev = {
        dolar: Number(initialRates.dolar_ant) || 0,
        euro: Number(initialRates.euro_ant) || 0,
        usdt: Number(initialRates.usdt_ant) || 0,
    };

    const dates = {
        dolar: initialRates.fecha_bcv || '',
        euro: initialRates.fecha_bcv || '',
        usdt: initialRates.fecha_usdt || '',
    };

    const datesPrev = {
        dolar: initialRates.fecha_bcv_ant || '',
        euro: initialRates.fecha_bcv_ant || '',
        usdt: initialRates.fecha_usdt_ant || '',
    };

    let currentCurrency = 'dolar';
    let isReverse = false; // false: FX -> Bs, true: Bs -> FX
    let isPreviousRate = false;

    const currencySymbols = {
        dolar: 'USD',
        euro: 'EUR',
        usdt: 'USDT',
    };

    function formatAmount(value, decimals = 2) {
        return value.toLocaleString('es-VE', {
            minimumFractionDigits: decimals,
            maximumFractionDigits: decimals
        });
    }

    function formatInput(value) {
        // Remove everything except digits and the decimal separator (comma)
        let clean = value.replace(/[^\d,]/g, '');

        // Ensure only one comma exists
        const parts = clean.split(',');
        if (parts.length > 2) {
            clean = parts[0] + ',' + parts.slice(1).join('');
        }

        if (clean === '') return '';

        // Add thousand separators for the integer part
        let [integer, decimal] = clean.split(',');
        let num = parseInt(integer || '0', 10);
        let formatted = num.toLocaleString('es-VE');

        // If there was a comma, re-attach it plus the decimal part
        if (clean.includes(',')) {
            return formatted + ',' + (decimal || '');
        }
        return formatted;
    }

    function updateLabels() {
        const symbol = currencySymbols[currentCurrency] || currentCurrency.toUpperCase();
        if (isReverse) {
            inputLabel.textContent = 'Monto en Bs';
            outputLabel.textContent = `Total en ${symbol}`;
            inputIcon.textContent = '🔢';
            outputIcon.textContent = '💰';
        } else {
            inputLabel.textContent = `Monto en ${symbol}`;
            outputLabel.textContent = 'Total en Bs';
            inputIcon.textContent = '💰';
            outputIcon.textContent = '🔢';
        }
    }

    function setCurrentRateText() {
        const symbol = currencySymbols[currentCurrency] || currentCurrency.toUpperCase();
        const activeRates = isPreviousRate ? ratesPrev : rates;
        const activeDates = isPreviousRate ? datesPrev : dates;
        const rate = activeRates[currentCurrency] || 0;

        const labelText = isPreviousRate ? 'Tasa anterior' : 'Tasa actual';
        currentRateText.textContent = `${labelText}: ${symbol} ${formatAmount(rate)}`;

        if (currentDateText) {
            currentDateText.textContent = activeDates[currentCurrency] || '';
        }
        updateLabels();
    }

    function calculate() {
        // Remove dots (thousand separators) and replace comma with dot for parseFloat
        const rawValue = amountInput.value.replace(/\./g, '').replace(/,/g, '.');
        const amount = parseFloat(rawValue) || 0;

        const activeRates = isPreviousRate ? ratesPrev : rates;
        const rate = activeRates[currentCurrency] || 0;

        const symbol = currencySymbols[currentCurrency] || currentCurrency.toUpperCase();

        if (rate === 0) {
            resultValue.textContent = isReverse ? `${symbol} 0,00` : 'Bs.S 0,00';
            return;
        }

        let result;
        let prefix = '';

        if (isReverse) {
            result = amount / rate;
            prefix = `${symbol} `;
        } else {
            result = amount * rate;
            prefix = 'Bs.S ';
        }

        // Use 2 decimals by default, but more for reverse if value is small
        let decimals = 2;
        if (isReverse && result < 0.01 && result > 0) {
            decimals = 4;
        }

        resultValue.textContent = `${prefix}${formatAmount(result, decimals)}`;
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

    switchBtn.addEventListener('click', () => {
        // Capture current result before switching to put it in input
        const rawResult = resultValue.textContent.replace(/[^\d,]/g, '');

        isReverse = !isReverse;

        // Add animation
        switchBtn.style.transform = isReverse ? 'scale(1.1) rotate(180deg)' : 'scale(1.1) rotate(0deg)';
        setTimeout(() => {
            if (!switchBtn.matches(':hover')) {
                switchBtn.style.transform = isReverse ? 'rotate(180deg)' : 'rotate(0deg)';
            }
        }, 300);

        // Put result in input for a seamless direction swap
        amountInput.value = formatInput(rawResult);

        updateLabels();
        calculate();
    });

    if (toggleRateBtn) {
        toggleRateBtn.addEventListener('click', () => {
            isPreviousRate = !isPreviousRate;
            toggleRateBtn.classList.toggle('active', isPreviousRate);

            // Re-calculate and update text
            setCurrentRateText();
            calculate();
        });
    }

    // Initial formatting for the default value
    amountInput.value = formatInput(amountInput.value);
    setCurrentRateText();
    calculate();
});
